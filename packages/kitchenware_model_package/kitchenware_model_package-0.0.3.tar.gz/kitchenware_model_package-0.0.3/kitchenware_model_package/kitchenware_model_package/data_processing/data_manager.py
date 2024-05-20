import pandas as pd
from glob import glob
import re
import os,sys
from pathlib import Path
from typing import Union
from loguru import logger
from sklearn.model_selection import train_test_split


from kitchenware_model_package.config.core import KITCHENWARE_DATA_DIR, config, TRAINED_MODEL_DIR, IMAGES
import tensorflow as tf


def load_single_img(data_folder: str, filename: str) -> pd.DataFrame:
    """ loads a single image and convert it to a dataframe"""
    image_list = []

    for image in glob(os.path.join(data_folder, f'{filename}')):
        # Create a DataFrame for each image and its target
        tmp = pd.DataFrame([[image, 'unknown']], columns=['image', 'label'])
        image_list.append(tmp)

    # Combine the list of DataFrames by concatenating them to form a new DataFrame
    final_df = pd.concat(image_list, ignore_index=True)
    
    return final_df

def load_multiple_img_via_path(folder: Path) -> Union[pd.DataFrame, pd.Series]:
    """ loads  multiple images and converts them to a dataframe"""
    image_names = []

    # Iterate through files in the folder
    for filename in os.listdir(folder):
        # Check if the file is an image
        if filename.endswith(".jpeg") or filename.endswith(".png") or filename.endswith(".jpg"):
            # Read the image file
            image_path = os.path.join(folder, filename)
            
            # Append image name to lists
            image_names.append(image_path)
    # Create DataFrame from image data
    df = pd.DataFrame({"image": image_names, "label": 'unknown'})
    return df


def load_image_csv_data(*, filename: str) -> pd.DataFrame:
    try:
        train_data = pd.read_csv(Path(f"{KITCHENWARE_DATA_DIR}/{filename}"), dtype={'Id': str})
        logger.info(f'Loaded data from {filename} successfully')
    except:
        logger.error(f'Error loading data from {filename}')

    # create new column with image path
    try:
        train_data['image'] =  f"{IMAGES}/" + train_data['Id'] + ".jpg"
        
        logger.info(f'Created image column from {IMAGES}')
        logger.log(_Logger__message = train_data.head(), _Logger__level = 20 )
    except:
        logger.error(f'Could not create image column from {IMAGES}. Check if path exists')

    # return train_data
    return train_data

def split_data_to_train_and_test(*, data: pd.DataFrame):
    """" split dataframe into train and test"""
    x_train, x_val, y_train, y_val = train_test_split(
        data, 
        data['label'], 
        test_size = config.modelConfig.test_size, 
        random_state = config.modelConfig.random_state)
    logger.info(f'Spliting data into train and test')
    logger.log(_Logger__message = (x_train.shape, x_val.shape ,y_train.shape,y_val.shape ), _Logger__level = 20)

    # reset the index
    x_train.reset_index(drop=True, inplace=True)
    x_val.reset_index(drop=True, inplace=True)
    y_train.reset_index(drop=True, inplace=True)
    y_val.reset_index(drop=True, inplace=True)

    # drop the Id column
    x_train.drop(columns=['Id'], inplace=True)
    x_val.drop(columns=['Id'], inplace=True)

    return x_train, x_val, y_train, y_val


def retain_best_model(path: Path) -> None:
    """" retains only best saved model after training"""
    # Define the folder path
    folder_path = path

    # List all files in the given directory
    files = os.listdir(path=folder_path)

    # Filter only the .keras files related to kitchenware_xception_model
    keras_files = [file for file in files if file.startswith('kitchenware_xception_model_val-acc_') and file.endswith('.keras')]

    if not keras_files:
        logger.info("No valid model files found in the directory.")

    # Extract the accuracy from filenames and identify the highest one
    max_accuracy = -1.0
    best_file = ""

    for file in keras_files:
        try:
            accuracy_str = file.split('_')[-1].replace('.keras', '')
            accuracy = float(accuracy_str)
            if accuracy > max_accuracy:
                max_accuracy = accuracy
                best_file = file
        except:
            logger.error(f"Error processing file: {file}")
            continue

    # Retain the file with the highest accuracy and remove the others
    for file in keras_files:
        if file != best_file:
            try:
                os.remove(os.path.join(folder_path, file))
                logger.info(f"Removed file: {file}")
            except:
                logger.error(f"Error removing file: {file}, {e}")

    logger.info(f"Retained file: {best_file}")


# load the trained model
def load_model():
    """ load model from disk"""
    logger.info(f'Loading model from {TRAINED_MODEL_DIR}')
    for file in os.listdir(TRAINED_MODEL_DIR):
        if file.endswith(".keras"):
            model_path = os.path.join(TRAINED_MODEL_DIR, file)
    model = tf.keras.models.load_model(model_path)
    return model
