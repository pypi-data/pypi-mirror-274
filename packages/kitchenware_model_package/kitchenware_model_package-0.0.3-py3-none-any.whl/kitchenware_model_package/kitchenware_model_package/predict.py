import os,sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from kitchenware_model_package.config.core import *
from kitchenware_model_package.data_processing import data_manager as dm
from kitchenware_model_package.data_processing import preprocessor as pp
import numpy as np
from loguru import logger
from kitchenware_model_package import __version__

# load the model
cnn_model = dm.load_model()

def make_single_img_prediction(folder: str, file: str):
    """ make a prediction on a single image file"""
    data = dm.load_single_img(data_folder = folder, filename= file)

    updated_data = data.drop(['label'], axis=1)
    
    logger.log(_Logger__message = updated_data, _Logger__level = 20)

    # preprocess the data
    preprocessed_data = pp.image_resizing_and_dataset_creation(
        data= updated_data,
        c_mode= None, 
        shufle= False,
        ylabelname= None
    )
    logger.info('Loaded data being preprocessed')

    # make prediction
    prediction = cnn_model.predict(preprocessed_data)
    # obtain the class with the highest probability
    predicted_class = np.argmax(prediction, axis=1)
    logger.info('Generating prediction on the data')


    result = {value:key for key, value in config.modelConfig.class_names.items()}
    
    result_class =  [result[f'{i}'] for i in predicted_class]
    logger.log(_Logger__message = dict(image_class = result_class, version = __version__),  _Logger__level = 20)
    return dict(
        image_class = result_class,
        version = __version__
        )


def make_bulk_prediction(*, images_data: Path) -> dict:
    """" use this method to retrieve batch of predictions"""
    # Load the image files 
    loaded_images = dm.load_multiple_img_via_path(folder=images_data)

    updated_data = loaded_images.drop(['label'], axis=1)

    # convert images data to a dataset 
    dataset_of_images  = pp.image_resizing_and_dataset_creation(
        data= updated_data,
        c_mode= None,
        shufle= False,
        ylabelname= None)
    logger.info('Loaded data being preprocessed')

    # call the cnn model predict method
    pred = cnn_model.predict(dataset_of_images)
    logger.info('Generating prediction on the data')
    
    predicted_class = np.argmax(pred, axis=1)
    # this will be used to map the class names to the predicted class
    result = {value:key for key, value in config.modelConfig.class_names.items()}
    result_classes =  [result[f'{i}'] for i in list(predicted_class)]
     
    logger.log(_Logger__message = dict(image_classes = result_classes, version = __version__),  _Logger__level = 20)

    return dict(
        image_classes = result_classes,
        version = __version__
    )

    