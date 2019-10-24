import os

from tensorflow import keras

from model.unet_model import unet_little
from loss.loss_function import dice_coef, dice_2_coef
from dataset.load_dataset import load_dataset

os.environ["CUDA_VISIBLE_DEVICES"] = "2, 3"

# load train dataset
train_ds = load_dataset("dataset")
print(type(train_ds))

# load unet model
model = unet_little()
model.summary()

# todo: change the file path to google drive
callbacks_list = [
    keras.callbacks.ReduceLROnPlateau(
        monitor='loss',
        factor=0.5,
        patience=10
    ),
    keras.callbacks.ModelCheckpoint(
        filepath='save_models/deep_binary_ver0.9_best_loss.h5',
        monitor='loss',
        save_best_only=True
    ),
    keras.callbacks.ModelCheckpoint(
        filepath='save_models/deep_binary_ver0.9_best_dice.h5',
        monitor='dice_coef',
        save_best_only=True
    ),
    keras.callbacks.ModelCheckpoint(
        filepath='save_models/deep_binary_ver0.9_best_dice_2.h5',
        monitor='dice_2_coef',
        save_best_only=True
    )
]

# compile model
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-4),
    loss='binary_crossentropy',
    metrics=['accuracy', dice_coef, dice_2_coef]
)

# train model
history = model.fit(
    train_ds,
    epochs=100,
    callbacks=callbacks_list,
    steps_per_epoch=100,
)

model.save_weights("save_models/test_model.h5")