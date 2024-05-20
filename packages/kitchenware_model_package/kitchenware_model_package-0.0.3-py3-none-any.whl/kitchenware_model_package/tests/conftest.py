import pytest
from kitchenware_model_package.config import core
from kitchenware_model_package.config.core  import config
import os

@pytest.fixture
def img_file():
    filename = os.path.join(core.IMAGES, config.modelConfig.sample_test_image)
    return filename