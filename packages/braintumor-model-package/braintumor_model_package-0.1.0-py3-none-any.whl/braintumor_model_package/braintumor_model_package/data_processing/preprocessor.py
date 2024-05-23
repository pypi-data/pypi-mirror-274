from tensorflow.keras.applications.xception import preprocess_input
from braintumor_model_package.config.core import config
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import pandas as pd
from loguru import logger



def image_resizing_and_dataset_creation(*, data: pd.DataFrame, c_mode: str, shufle: bool, ylabelname:str | None):
    """ creates a dataset suitable for the xception model, kindly pass a class_mode to c_mode"""
    img_gen = ImageDataGenerator(preprocessing_function= preprocess_input)
    ds = None

    try:
        ds = img_gen.flow_from_dataframe(
            data,
            target_size = (config.modelConfig.img_size ,config.modelConfig.img_size),
            batch_size = config.modelConfig.batch_size,
            x_col = 'image',
            y_col = ylabelname,
            class_mode = c_mode,
            shuffle = shufle,
            seed = config.modelConfig.random_state
    )   
    except:
        logger.error('Error in creating dataset')
    
    return ds