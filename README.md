<h1> SIR: A Decentralised Artwork Minting Platform </h1>

## Overview
Our project revolves around creating a fintech solution that combines the power of Generative Adversarial Networks (GANs) with the Ethereum blockchain to generate and mint unique art pieces as non-fungible tokens (NFTs). Using TensorFlow for training a Wasserstein GAN (WGAN) on the CelebA dataset, our project then proceeds to mint the generated images as NFTs using Solidity smart contracts. Our project also integrates with IPFS for decentralised storage and Streamlit for a user-friendly minting platform.<br>

## Prerequisites
- Python 3.x<br>
- MetaMask browser extension<br>
- Access to Rinkeby Testnet Ethereum (optional for testing)<br>

<br>

## Installation
- Environment Setup:<br>
  - Ensure Python 3.x is installed. If not, download it from the official Python website.<br>
- Install Dependencies: <br>
  - <i>pip install tensorflow tensorflow_datasets streamlit web3</i> <br>
- MetaMask Setup:  <br>
  - Install MetaMask <br>
  - Create an account and safeguard the mnemonic phrase.<br>
  - If testing, fund your MetaMask with Rinkeby Testnet Ethereum from Rinkeby Faucet.<br>
<br>

## Usage
- Training the WGAN Model  <br>
  - Use Google Colab or a local machine with sufficient computational resources.<br>
  - Load the CelebA dataset and preprocess the images.<br>
  - Train the model using the provided code.<br>
  - Adjust the batch size and epochs based on your computational capabilities. <br>
  
- Image Generation and Minting:<br>
  - Use the trained model to generate desired images.<br>
  - Ensure the image format and resolution adhere to OpenSea's requirements<br>
  - For decentralised storage, upload the image to Pinata and obtain the IPFS hash.<br>
  - Deploy the Solidity smart contract using Remix. Ensure 'Injected Web3' is selected to integrate Remix with MetaMask.<br>
  - Mint the NFT using the mint function.<br>

- Streamlit User Interface: <br>
  - Execute the Streamlit script: <i>streamlit run your_script_name.py</i>
  
<br>

## Project Structure:
- WGAN Model: Trains on CelebA, producing unique art.<br>
- Solidity Contract: Facilitates the minting process on Ethereum<br>
- Streamlit UI: Interactive platform for minting.<br>
