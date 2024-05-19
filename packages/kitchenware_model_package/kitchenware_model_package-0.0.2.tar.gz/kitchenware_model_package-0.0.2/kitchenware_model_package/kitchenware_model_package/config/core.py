import os
from pathlib import Path
from pydantic import BaseModel
from strictyaml import YAML, load

PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE_PATH = Path(os.path.join(PACKAGE_ROOT, 'config.yml'))
DATASET_DIR = Path(os.path.join(PACKAGE_ROOT, 'datasets'))
KITCHENWARE_DATA_DIR= Path(os.path.join(DATASET_DIR, 'kitchenware-data'))
IMAGES = Path(os.path.join(KITCHENWARE_DATA_DIR, 'images'))
TRAINED_MODEL_DIR = Path(os.path.join(PACKAGE_ROOT, 'trained_models'))

class AppConfig(BaseModel):
    """ application level  config"""
    package_name: str
    train_data_file: str # TODO
    test_data_file: str
    # pipeline_save_file: str

class ModelConfig(BaseModel):
    modelname: str
    img_size: int
    batch_size: int
    epoch: int
    class_names: dict
    image_set: str
    learning_rate: float
    random_state: int
    test_size: float
    drop_rate: float
    dense_layer_first_inner_size: int
    sample_test_image: str

class Config(BaseModel):
    """ master config object"""
    appConfig: AppConfig
    modelConfig: ModelConfig

def find_config_file() -> Path:
    """ locate the configuration file"""
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f'Config not found at {CONFIG_FILE_PATH!r}')

def fetch_config_from_yaml(cfg_path: Path = None) -> YAML:
    """ parse the yaml containing the package configuration"""
    if not cfg_path:
        cfg_path =  find_config_file()

    if cfg_path:
        with open(cfg_path, "r") as conf_file:
            parsed_config = load(conf_file.read())
            return parsed_config
    raise OSError(f'did not find config file at path: {cfg_path}')

def create_and_validate_config(parsed_config: YAML = None) -> Config:
    """ run validation on config"""
    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

        # specify the data attribute from the strictyaml YAML type
    _config = Config(
        appConfig = AppConfig(**parsed_config.data),
        modelConfig= ModelConfig(**parsed_config.data)
    )
    return _config

config =  create_and_validate_config()
