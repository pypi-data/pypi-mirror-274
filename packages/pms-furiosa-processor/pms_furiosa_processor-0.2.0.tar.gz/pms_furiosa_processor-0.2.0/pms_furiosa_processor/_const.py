from typing import List, Any, Coroutine, Iterator, Tuple, Iterable
import os
import numpy as np
from loguru import logger
import asyncio
import furiosa
import glob
import furiosa.runtime.session as frs
from pms_inference_engine import IEngineProcessor, EngineIOData, register


def __get_env(key: str) -> str:
    val = os.getenv(key)
    if val is None:
        raise ValueError(f"ERROR, The environment variable [{key}] is not setted.")
    return val


NPU_DEVICES = sorted(
    [g.split("/")[-1] for g in glob.glob("/dev/npu*pe?")],
    key=lambda x: int(x[3 : x.index("pe")]),
)
NUMBER_OF_NPU = len(NPU_DEVICES) // 2


class DPIRConfig:
    PAD_SIZE = 16
    ROW_SIZE = 280
    COL_SIZE = 320


class DRURBPNSRF3Config:
    PAD_SIZE = 4
    ROW_SIZE = 120
    COL_SIZE = 248
    UPSCALE_RATIO = 2
