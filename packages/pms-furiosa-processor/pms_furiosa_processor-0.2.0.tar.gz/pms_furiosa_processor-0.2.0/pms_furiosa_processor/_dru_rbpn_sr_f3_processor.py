from ._const import *


@register
class DRURBPNSRF3Processor(IEngineProcessor[EngineIOData, EngineIOData]):

    @staticmethod
    def preprocess(
        image: np.ndarray,
    ) -> Iterator[Tuple[List[np.ndarray], int, int]]:
        image = image.transpose(2, 0, 1)
        image = np.expand_dims(image, 0)
        _, _, row, col = image.shape

        upscale_ratio = DRURBPNSRF3Config.UPSCALE_RATIO
        pad_size = DRURBPNSRF3Config.PAD_SIZE
        row_size = DRURBPNSRF3Config.ROW_SIZE
        col_size = DRURBPNSRF3Config.COL_SIZE
        i_row_size = row_size + 2 * pad_size
        i_col_size = col_size + 2 * pad_size
        input = np.pad(
            image,
            (
                (0, 0),
                (0, 0),
                (pad_size, pad_size),
                (pad_size, pad_size),
            ),
            mode="edge",
        )
        # c = [
        #     (index_row, index_col)
        #     for index_row in [
        #         *range(0, row - row_size, row_size),
        #         row - row_size,
        #     ]
        #     for index_col in [
        #         *range(0, col - col_size, col_size),
        #         col - col_size,
        #     ]
        # ]
        return (
            (
                [
                    input[
                        :,
                        3:6,
                        index_row : index_row + i_row_size,
                        index_col : index_col + i_col_size,
                    ],
                    input[
                        :,
                        0:3,
                        index_row : index_row + i_row_size,
                        index_col : index_col + i_col_size,
                    ],
                    input[
                        :,
                        6:9,
                        index_row : index_row + i_row_size,
                        index_col : index_col + i_col_size,
                    ],
                ],
                index_row,
                index_col,
            )
            for index_row in [
                *range(0, row - row_size, row_size),
                row - row_size,
            ]
            for index_col in [
                *range(0, col - col_size, col_size),
                col - col_size,
            ]
        )

    @staticmethod
    def postprocess(
        data: Iterable[Tuple[np.ndarray, int, int]],
        width: int,
        height: int,
    ) -> np.ndarray:

        upscale_ratio = DRURBPNSRF3Config.UPSCALE_RATIO
        pad_size = DRURBPNSRF3Config.PAD_SIZE
        row_size = DRURBPNSRF3Config.ROW_SIZE
        col_size = DRURBPNSRF3Config.COL_SIZE
        i_row_size = row_size + upscale_ratio * pad_size
        i_col_size = col_size + upscale_ratio * pad_size

        prediction = np.empty(
            (
                1,
                3,
                height * upscale_ratio,
                width * upscale_ratio,
            ),
            np.uint8,
        )

        for output, index_row, index_col in data:
            cut_output = output[0]
            prediction[
                :,
                :,
                index_row * upscale_ratio : (index_row + row_size) * upscale_ratio,
                index_col * upscale_ratio : (index_col + col_size) * upscale_ratio,
            ] = cut_output[
                :,
                :,
                pad_size * upscale_ratio : (pad_size + row_size) * upscale_ratio,
                pad_size * upscale_ratio : (pad_size + col_size) * upscale_ratio,
            ]
        img = np.squeeze(prediction, axis=0)  # Remove batch dimension
        img = np.transpose(img, (1, 2, 0))

        return img

    @staticmethod
    async def predict(
        session: frs.Session,  # type : NuxModel, TypeHint 적용 시 컴파일 오류가 발생하여 주석으로 대체.
        tensor: List[np.ndarray],
        row: int,
        col: int,
    ) -> Tuple[np.ndarray, int, int]:

        result = await asyncio.to_thread(session.run, tensor)  # type: ignore
        return (result.numpy(), row, col)

    def __init__(self, index: int, concurrency: int, path: str) -> None:
        logger.info(f"{self.__class__}[{index}]>> Init Start")
        super().__init__(index, concurrency)
        assert os.path.exists(path)
        self.path = path
        self.device = NPU_DEVICES[index]
        self.session = frs.create(
            model=path,
            device=self.device,
            batch_size=1,
            worker_num=2,
        )
        logger.info(self.session.print_summary())
        logger.info(f"{self.__class__}[{index}]>> Init END")

    def _bind_io(self, input_data: EngineIOData) -> bool:
        return True

    def _get_concurrency(self) -> int:
        return self._concurrency

    def _get_live(self) -> bool:
        return True

    def _ready_processor(self) -> bool:
        return True

    async def _run(self, input_data: EngineIOData) -> EngineIOData:
        assert input_data.frame.shape[2] == 9
        output_image = np.expand_dims(
            np.zeros(
                (
                    input_data.frame.shape[0] * DRURBPNSRF3Config.UPSCALE_RATIO,
                    input_data.frame.shape[1] * DRURBPNSRF3Config.UPSCALE_RATIO,
                    3,
                ),
                np.uint8,
            ),
            0,
        )
        h, w, c = input_data.frame.shape
        data = self.preprocess(input_data.frame)
        preds = await asyncio.gather(
            *(self.predict(self.session, *data) for data in data)
        )
        output_image = self.postprocess(preds, w, h)
        output_data = EngineIOData(input_data.frame_id, output_image)
        return output_data
