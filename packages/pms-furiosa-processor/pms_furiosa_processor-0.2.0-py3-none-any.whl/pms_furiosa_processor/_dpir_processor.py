from ._const import *


@register
class DPIRProcessor(IEngineProcessor[EngineIOData, EngineIOData]):

    @staticmethod
    def preprocess(image: np.ndarray) -> Iterator[Tuple[np.ndarray, int, int]]:
        image = image.transpose(2, 0, 1)
        _, height, width = image.shape
        input_buffer = np.ones((1, 4, height, width), np.uint8)
        input_buffer[0, :3, :, :] = image
        _, _, row, col = input_buffer.shape
        input = np.pad(
            input_buffer,
            (
                (0, 0),
                (0, 0),
                (DPIRConfig.PAD_SIZE, DPIRConfig.PAD_SIZE),
                (DPIRConfig.PAD_SIZE, DPIRConfig.PAD_SIZE),
            ),
            mode="edge",
        )

        return (
            (
                input[
                    :,
                    :,
                    index_row : index_row
                    + DPIRConfig.PAD_SIZE * 2
                    + DPIRConfig.ROW_SIZE,
                    index_col : index_col
                    + DPIRConfig.PAD_SIZE * 2
                    + DPIRConfig.COL_SIZE,
                ],
                index_row,
                index_col,
            )
            for index_row in [
                *range(0, row - DPIRConfig.ROW_SIZE, DPIRConfig.ROW_SIZE),
                row - DPIRConfig.ROW_SIZE,
            ]
            for index_col in [
                *range(0, col - DPIRConfig.COL_SIZE, DPIRConfig.COL_SIZE),
                col - DPIRConfig.COL_SIZE,
            ]
        )

    @staticmethod
    async def predict(
        session: frs.Session,  # type : NuxModel, TypeHint 적용 시 컴파일 오류가 발생하여 주석으로 대체.
        tensor: np.ndarray,
        row: int,
        col: int,
    ) -> Tuple[np.ndarray, int, int]:

        result = await asyncio.to_thread(session.run, tensor)
        return (result.numpy(), row, col)

    @staticmethod
    def postprocess(
        data: Iterable[Tuple[np.ndarray, int, int]], width, height
    ) -> np.ndarray:
        prediction = np.empty((1, 3, height, width), np.uint8)

        for output, index_row, index_col in data:
            cut_output = output[0]
            prediction[
                :,
                :,
                index_row : index_row + DPIRConfig.ROW_SIZE,
                index_col : index_col + DPIRConfig.COL_SIZE,
            ] = cut_output[
                :,
                :,
                DPIRConfig.PAD_SIZE : DPIRConfig.PAD_SIZE + DPIRConfig.ROW_SIZE,
                DPIRConfig.PAD_SIZE : DPIRConfig.PAD_SIZE + DPIRConfig.COL_SIZE,
            ]

            img = np.squeeze(prediction, axis=0)
            img = np.transpose(img, axes=[1, 2, 0])
        return img

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
        h, w, c = input_data.frame.shape
        self.input_buffer = np.ones((1, 4, h, w), np.uint8)
        self.output_buffer = np.ones((1, c, h, w), np.uint8)
        return True

    def _get_concurrency(self) -> int:
        return self._concurrency

    def _get_live(self) -> bool:
        return True

    def _ready_processor(self) -> bool:
        return True

    async def _run(self, input_data: EngineIOData) -> EngineIOData:
        output_image = np.expand_dims(input_data.frame.copy(), 0)
        h, w, c = input_data.frame.shape
        data = self.preprocess(input_data.frame)
        preds = await asyncio.gather(
            *(self.predict(self.session, *data) for data in data)
        )
        output_image = self.postprocess(preds, w, h)
        output_data = EngineIOData(input_data.frame_id, output_image)
        return output_data
