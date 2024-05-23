import os,sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from braintumor_model_package.data_processing import data_manager, preprocessor
from braintumor_model_package.config.core import config
from braintumor_model_package.data_processing.data_manager import retain_best_model
from braintumor_model_package.config import core
from model import make_model
import tensorflow as tf
import keras
from tensorflow import keras
from loguru import logger


filepath = "braintumor_xception_model_val-acc_{val_accuracy:.3f}.keras"

checkpoint = keras.callbacks.ModelCheckpoint(
    f"{str(core.TRAINED_MODEL_DIR)}/{filepath}",
    save_best_only=True,
    monitor='val_accuracy',
    mode='max'
)

def run_training(save_results: bool =  True) -> None:
    """ train the model"""
    #load the image data
    data = data_manager.load_image_paths(data_folder=core.TRAIN_DATA_DIR)

    # split the data into train and test
    x_train, x_val, y_train, y_val = data_manager.split_data_to_train_and_test(data=data)

    # convert the data to tf dataset processable by the model
    train_ds = preprocessor.image_resizing_and_dataset_creation(
        data= x_train,
        c_mode= 'categorical',
        shufle=True,
        ylabelname= 'label'
    )
    val_ds = preprocessor.image_resizing_and_dataset_creation(
        data= x_val,
        c_mode= 'categorical',
        shufle=False,
        ylabelname= 'label'
    )


    model = make_model(
        input_size= config.modelConfig.img_size,
        learning_rate= config.modelConfig.learning_rate,
        size_inner= config.modelConfig.dense_layer_first_inner_size,
        droprate= config.modelConfig.drop_rate
    )

    model.fit(train_ds, 
              epochs=config.modelConfig.epoch, 
              validation_data=val_ds,
              callbacks=[checkpoint])
    logger.info(f'Saving model to {core.TRAINED_MODEL_DIR}')
    
    # call the method - retain best model
    retain_best_model(core.TRAINED_MODEL_DIR)

if __name__ == '__main__':
    run_training(save_results=True)