import pathlib
import shutil
from pathlib import Path

import pytest
from _pytest.tmpdir import TempPathFactory
from loguru import logger

from dynrender_skia.Core import DynRender


@pytest.fixture(scope="session")
def shared_cache(tmp_path_factory: TempPathFactory) -> object:
    cache_dir = tmp_path_factory.mktemp("cache", numbered=False)
    logger.info(f"创建共享缓存目录：{cache_dir}")
    yield cache_dir
    shutil.rmtree(cache_dir)
    logger.info(f"删除共享缓存目录：{cache_dir}")


@pytest.fixture(scope="session")
def resource_dir() -> pathlib.Path:
    return Path(__file__).parent / "res"


@pytest.fixture(scope="session")
def dynrender_instance(shared_cache: pathlib.Path) -> DynRender:
    dynrender_instance = DynRender(static_path=str(shared_cache))
    logger.info("DynRender实例创建成功")
    return dynrender_instance


@pytest.fixture(scope="module")
def mock_img_url() -> str:
    return "http://bilibili.com"


@pytest.fixture(scope="module")
def img_path(resource_dir: pathlib.Path) -> pathlib.Path:
    return Path(resource_dir / "bilibili.png")
