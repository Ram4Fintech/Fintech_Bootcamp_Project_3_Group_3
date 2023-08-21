import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################

# Cache the contract on load
@st.cache(allow_output_mutation=True)
# Define the load_contract function
def load_contract():

    # Load Art Gallery ABI
    with open(Path('/Users/shayan/Desktop/USYD_FinTech_Bootcamp_2023_Material/22-dApps/3/Activities/02-Evr_Certificate_dApp/Unsolved/contracts/compiled/certificate_abi.json')) as f:
        certificate_abi = json.load(f)


    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")


    # Get the contract using web3
    contract = w3.eth.contract(address = contract_address,
                               abi = certificate_abi)


    # Return the contract from the function
    return contract



# Load the contract
contract = load_contract()

################################################################################
# Register New Artwork
################################################################################
st.title("Register New Artwork")
accounts = w3.eth.accounts

# Use a Streamlit component to get the address of the artwork owner from the user
address = st.selectbox("Select Artwork Owner", options=accounts)

# Use a Streamlit component to get the artwork's URI
artwork_uri = st.text_input("The URI to the artwork")

if st.button("Register Artwork"):

    # Use the contract to send a transaction to the registerArtwork function
    tx_hash = contract.functions.registerArtwork(
        address,
        artwork_uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))

st.markdown("---")


################################################################################
# Display a Token
################################################################################
st.markdown("## Check Balance of an Account")

selected_address = st.selectbox("Select Account", options=accounts)

tokens = contract.functions.balanceOf(selected_address).call()

st.write(f"This address owns {tokens} tokens")

st.markdown("## Check  Ownership and Display Token")

total_token_supply = contract.functions.totalSupply().call()

token_id = st.selectbox("Artwork Tokens", list(range(total_token_supply)))

if st.button("Display"):

    # Get the art token owner
    owner = contract.functions.ownerOf(token_id).call()
    
    st.write(f"The token is registered to {owner}")

    # Get the art token's URI
    token_uri = contract.functions.tokenURI(token_id).call()

    st.write(f"The tokenURI is {token_uri}")
    st.image(token_uri)

################################################################################
# Award Certificate
################################################################################

accounts = w3.eth.accounts
account = accounts[0]
student_account = st.selectbox("Select Account", options=accounts)
certificate_details = st.text_input("Certificate Details", value="FinTech Certificate of Completion")
if st.button("Award Certificate"):
    contract.functions.awardCertificate(student_account, certificate_details).transact({'from': account, 'gas': 1000000})

################################################################################
# Display Certificate
################################################################################
certificate_id = st.number_input("Enter a Certificate Token ID to display", value=0, step=1)
if st.button("Display Certificate"):
    # Get the certificate owner
    certificate_owner = contract.functions.ownerOf(certificate_id).call()
    st.write(f"The certificate was awarded to {certificate_owner}")

    # Get the certificate's metadata
    token_uri = contract.functions.tokenURI(certificate_id).call()
    st.write(f"The certificate's tokenURI metadata is {token_uri}")
