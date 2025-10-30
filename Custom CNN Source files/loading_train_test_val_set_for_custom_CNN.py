import tensorflow as tf

def train_ds_loader(from_dir__):
    return tf.keras.utils.image_dataset_from_directory(
        from_dir__,image_size=(224,224)
        ,batch_size=32,
        color_mode='grayscale'# or 'RGB'
        )
    
def test_ds_loader(from_dir__):
    return tf.keras.utils.image_dataset_from_directory(
        from_dir__,image_size=(224,224)
        ,batch_size=32,
        color_mode='grayscale'# or 'RGB'
        )

def val_ds_loader(from_dir__):
    return tf.keras.utils.image_dataset_from_directory(
        from_dir__,image_size=(224,224)
        ,batch_size=32,
        color_mode='grayscale'# or 'RGB'
        )