# ----------------------
# IMPORTS & INITIALIZATIONS
# ----------------------

import numpy as np
import tensorflow as tf
import os
import matplotlib.pyplot as plt
import tensorflow_datasets as tfds
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from SIR_Pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Reshape, BatchNormalization, Conv2DTranspose, LeakyReLU, Conv2D, Flatten, Input


load_dotenv()

# Retrieve the address from the environment variables
address = os.getenv("YOUR_ENV_VARIABLE_NAME_FOR_ADDRESS")


# Web3 setup
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Dataset setup
celeba_data, info = tfds.load('celeb_a', split='train', with_info=True)


# ----------------------
# FUNCTION & MODEL DEFINITIONS
# ----------------------

# Functions and definitions from the WGAN file

def preprocess_dataset(dataset):
    """
    Preprocesses the dataset images:
    - Resize the images to 256x256.
    - Normalize the images to [-1, 1].
    """
    def _preprocess_img(img):
        # Resise the image
        img = tf.image.resize(img, (256, 256))
        # Normalise to [-1, 1]
        img = (img - 127.5) / 127.5
        return img

    return dataset.map(lambda x: (_preprocess_img(x['image']), x['attributes']), num_parallel_calls=tf.data.experimental.AUTOTUNE)


# Constants
BATCH_SIZE = 8 
EPOCHS = 200  
NOISE_DIM = 200
SAVE_INTERVAL = 25
TRAINING_RATIO = 5

celeba_dataset_processed = preprocess_dataset(celeba_data).batch(BATCH_SIZE).prefetch(tf.data.experimental.AUTOTUNE)

IMG_SHAPE = (512, 512, 3)

# build generator
def build_simplified_generator():
    model = Sequential()

    # Start with 8x8 spatial resolution
    model.add(Dense(128 * 8 * 8, activation="relu", input_shape=(NOISE_DIM,)))
    model.add(Reshape((8, 8, 128)))
    model.add(BatchNormalization())

    # UpSample to 16x16
    model.add(Conv2DTranspose(64, kernel_size=4, strides=2, padding="same"))
    model.add(BatchNormalization())
    model.add(LeakyReLU(0.2))

    # UpSample to 32x32
    model.add(Conv2DTranspose(32, kernel_size=4, strides=2, padding="same"))
    model.add(BatchNormalization())
    model.add(LeakyReLU(0.2))

    # UpSample to 64x64
    model.add(Conv2DTranspose(16, kernel_size=4, strides=2, padding="same"))
    model.add(BatchNormalization())
    model.add(LeakyReLU(0.2))

    # UpSample to 128x128
    model.add(Conv2DTranspose(8, kernel_size=4, strides=2, padding="same"))
    model.add(BatchNormalization())
    model.add(LeakyReLU(0.2))

    # UpSample to 256x256
    model.add(Conv2DTranspose(3, kernel_size=4, strides=2, padding="same", activation="tanh"))

    return model

# build discriminator
def build_simplified_discriminator():
    model = Sequential()

    model.add(Conv2D(16, kernel_size=4, strides=2, padding="same", input_shape=(256, 256, 3)))
    model.add(LeakyReLU(0.2))

    model.add(Conv2D(32, kernel_size=4, strides=2, padding="same"))
    model.add(LeakyReLU(0.2))

    model.add(Conv2D(64, kernel_size=4, strides=2, padding="same"))
    model.add(LeakyReLU(0.2))

    model.add(Conv2D(128, kernel_size=4, strides=2, padding="same"))
    model.add(LeakyReLU(0.2))

    model.add(Flatten())
    model.add(Dense(1))

    return model

# Instantiate the new models
generator_512 = build_simplified_generator()
discriminator_512 = build_simplified_discriminator()

optimizer_gen = tf.keras.optimizers.Adam(0.0001, beta_1=0.5, beta_2=0.9)
optimizer_disc = tf.keras.optimizers.Adam(0.0004, beta_1=0.5, beta_2=0.9)


# Loss function (Wasserstein loss)
def wasserstein_loss(y_true, y_pred):
    return -tf.reduce_mean(y_true * y_pred)

generator_512.compile(optimizer=optimizer_gen, loss=wasserstein_loss)
discriminator_512.compile(optimizer=optimizer_disc, loss=wasserstein_loss)

z = Input(shape=(NOISE_DIM,))
img = generator_512(z)
discriminator_512.trainable = False
valid = discriminator_512(img)
combined = Model(z, valid)
combined.compile(loss=wasserstein_loss, optimizer=optimizer_gen)

def train_gan_512(dataset, epochs, batch_size=BATCH_SIZE, save_interval=SAVE_INTERVAL):
    valid = -np.ones((batch_size, 1))
    fake = np.ones((batch_size, 1))

    for epoch in range(epochs):
        for _ in range(TRAINING_RATIO):
            for imgs, _ in dataset.take(1):
                noise = np.random.normal(0, 1, (batch_size, NOISE_DIM))
                gen_imgs = generator_512.predict(noise)

                d_loss_real = discriminator_512.train_on_batch(imgs, valid)
                d_loss_fake = discriminator_512.train_on_batch(gen_imgs, fake)
                d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

                for l in discriminator_512.layers:
                    weights = l.get_weights()
                    weights = [np.clip(w, -0.01, 0.01) for w in weights]
                    l.set_weights(weights)

        g_loss = combined.train_on_batch(noise, valid)

        print(f"Epoch: {epoch+1}/{epochs} | Discriminator Loss: {d_loss:.4f} | Generator Loss: {g_loss:.4f}")

        # Save and mint the generated image only! (at the end of training)
        if epoch == epochs - 1:
            save_imgs(generator_512, epoch, num_samples=1)



# Functions and definitions from the Contract file

@st.cache(allow_output_mutation=True)
def load_contract():

    # Load SIR_NFT Gallery ABI
    with open(Path('/Users/shayan/Desktop/USYD_FinTech_Bootcamp_2023_Material/Project_3/Contracts/Compiled/SIR_NFT_abi.json')) as f:
        certificate_abi = json.load(f)


    # Set the contract address (** address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")


    # Get the contract using web3
    contract = w3.eth.contract(address = contract_address,
                               abi = certificate_abi)


    # Return the contract from the function
    return contract



# Load the contract
contract = load_contract()

def pin_artwork(artwork_name, artwork_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(artwork_file.getvalue())

    # Build a token metadata file for the artwork
    token_json = {
        "name": artwork_name,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash, token_json


def pin_appraisal_report(report_content):
    json_report = convert_data_to_json(report_content)
    report_ipfs_hash = pin_json_to_ipfs(json_report)
    return report_ipfs_hash


# ----------------------
# MODIFIED save_imgs FUNCTION
# ----------------------

def save_imgs(generator, epoch, save_path="gan_images", num_samples=1):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    noise = np.random.normal(0, 1, (num_samples, NOISE_DIM))
    gen_imgs = generator.predict(noise)

    gen_imgs = 0.5 * gen_imgs + 0.5

    img_path = f"{save_path}/image_at_epoch_{epoch}.png"
    plt.imshow(gen_imgs[0])
    plt.axis('off')
    plt.savefig(img_path)
    plt.close()

    with open(img_path, 'rb') as file:
        artwork_ipfs_hash, token_json = pin_artwork(f"Generated Image", file)

        tx_hash = contract.functions.registerArtwork(
            address,
            "Generated Image",
            "WGAN",
            0,
            f"ipfs://{artwork_ipfs_hash}",
            token_json['image']
        ).transact({'from': address, 'gas': 1000000})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


# ----------------------
# TRAINING & MINTING
# ----------------------

# Load the contract (from smart contract code)
contract = load_contract()

# Train the WGAN and mint the images (from WGAN code)
train_gan_512(celeba_dataset_processed, EPOCHS)
