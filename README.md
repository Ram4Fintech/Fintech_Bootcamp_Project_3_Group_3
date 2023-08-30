<h1> SIR: A Decentralised Artwork Minting Platform </h1>

*Group 3: Shayan, Isabel, Ram*

*The machine learning portion of this project was developed in Google Colab to leverage its powerful GPU capabilities. The remainder of the code was written in VS Code using Python, and Remix was utilised for the Solidity components.*

---
## Overview
Our project revolves around creating a fintech solution that combines the power of Generative Adversarial Networks (GANs) with the Ethereum blockchain to generate and mint unique art pieces as non-fungible tokens (NFTs). Using TensorFlow for training a Wasserstein GAN (WGAN) on the CelebA dataset, our project then proceeds to mint the generated images as NFTs using Solidity smart contracts. Our project also integrates with IPFS for decentralised storage and Streamlit for a user-friendly minting platform.<br>

## Prerequisites
- Python 3.x<br>
- MetaMask Browser Extension<br>
- Ganache Local Ethereum Blockchain<br>

<br>

## Installation
- Environment Setup:
  - Ensure Python 3.x is installed. If not, download it from the official Python website.
- Install Dependencies: 
  - <i>pip install tensorflow tensorflow_datasets streamlit web3</i> 
- MetaMask Setup: 
  - Install MetaMask
  - Create an account and safeguard the mnemonic phrase.
  - Ensure Ganache instance is connected to MetaMask as a test network.
- Pinata IPFS Setup:
  - Ensure Pinata account is setup and have keys available for pasting into ".env" file


## Libraries and Dependencies
**Remix:**
- Solidity version 0.5.0 or above
- Compiler version 0.5.17
- ERC721Full Standards: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol

**Python:**
- imports: os, json, requests, streamlit, Web3 from web3, Path from pathlib, load_dotenv from dotenv

<br>

## Usage
- Training the WGAN Model  <br>
  - Use Google Colab or a local machine with sufficient computational resources.
  - Load the CelebA dataset and preprocess the images.
  - Train the model using the provided code.
  - Adjust the batch size and epochs based on your computational capabilities. 
  
- Image Generation and Minting:<br>
  - Use the trained model to generate desired images.<br>
  - Ensure the image format and resolution adhere to OpenSea's requirements
  - For decentralised storage, upload the image to Pinata and obtain the IPFS hash.
  - Ensure Ganache and MetaMask are connected with the correspending Ganache address loaded into MetaMask's Ganache test network.
  - Deploy the Solidity smart contract using Remix. Ensure 'Dev - Ganache Provider' is selected as the environment to integrate Remix with Ganache.
  - Mint the NFT using the mint function.<br>

- Streamlit User Interface: <br>
  - Execute the Streamlit script: <i>streamlit run your_script_name.py</i>

*Please review the Smart Contract Video Demonstration in the evidence folder for more information*
  
<br>

## Project Structure:
- WGAN Model: Trains on CelebA, producing unique art.
- Solidity Contract: Facilitates the minting process on a Ganache based Ethereum Blockchain for testing
- Streamlit UI: Interactive platform for minting.

<br>

---
## Resources and References
- Slide deck template from: https://slidesgo.com/theme/futuristic-background#search-blockchain&position-4&results-97&rs=search
- https://ethereum.org/en/nft/
- https://ethereum.org/en/developers/docs/standards/tokens/erc-721/
- https://linda.mirror.xyz/df649d61efb92c910464a4e74ae213c4cab150b9cbcc4b7fb6090fc77881a95d
- https://opensea.io/blog/guides/non-fungible-tokens/
- https://www.investopedia.com/how-to-create-an-nft-6362495
- https://nftnewstoday.com/2022/12/10/nft-tokenomics-ideas-and-examples/#
- https://brightnode.io/nft-tokenomics-getting-started-for-a-successful-nft-business/
- https://ebutemetaverse.com/nft-image-size/#:~:text=The%20ideal%20NFT%20image%20size,50MB%20to%20100MB%20is%20recommended.
- https://pypi.org/project/opensea-api/
- https://docs.opensea.io/reference/api-overview
- @inproceedings{liu2015faceattributes, title = {Deep Learning Face Attributes in the Wild},  author = {Liu, Ziwei and Luo, Ping and Wang, Xiaogang and Tang, Xiaoou}, booktitle = {Proceedings of International Conference on Computer Vision (ICCV)},  month = {December}, year = {20
- Learning Multiple Layers of Features from Tiny Images: https://www.cs.toronto.edu/~kriz/learning-features-2009-TR.pdf, Alex Krizhevsky, 2009
- MNIST is made available under the terms of the Creative Commons Attribution-Share Alike 3.0 license. In another source, it says mnist is available for non commercial use, but I would be careful in usi

