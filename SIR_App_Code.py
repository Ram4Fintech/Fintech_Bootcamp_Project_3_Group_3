import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from SIR_Pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

#################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
#################################################################################

# Cache the contract on load
@st.cache(allow_output_mutation=True)
# Define the load_contract function
def load_contract():

    # Load SIR_NFT Gallery ABI
    with open(Path('/Users/shayan/Desktop/USYD_FinTech_Bootcamp_2023_Material/Project_3/Contracts/Compiled/SIR_NFT_abi.json')) as f:
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

#################################################################################
# Register New Artwork with Pre-Existing URI
#################################################################################
# st.title("Register New Artwork")
# accounts = w3.eth.accounts

# # Use a Streamlit component to get the address of the artwork owner from the user
# address = st.selectbox("Select Artwork Owner", options=accounts)

# # Use a Streamlit component to get the artwork's URI
# artwork_uri = st.text_input("The URI of the artwork")

# if st.button("Register Artwork"):

#     # Use the contract to send a transaction to the registerArtwork function
#     tx_hash = contract.functions.registerArtwork(
#         address,
#         artwork_uri
#     ).transact({'from': address, 'gas': 1000000})
#     receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#     st.write("Transaction receipt mined:")
#     st.write(dict(receipt))

# st.markdown("---")

################################################################################
# Helper functions to pin files and json to Pinata
################################################################################


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


st.title("Art Registry Appraisal System")
st.write("Choose an account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
st.markdown("---")

################################################################################
# Register New Artwork using Pinata IPFS
################################################################################
st.markdown("## Register New Artwork")
artwork_name = st.text_input("Enter the name of the artwork")
artist_name = st.text_input("Enter the artist name")
initial_appraisal_value = st.text_input("Enter the initial appraisal amount")

# Use the Streamlit `file_uploader` function create the list of digital image file types(jpg, jpeg, or png) that will be uploaded to Pinata.
file = st.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png"])

#nft_images = ##[Path('/Users/shayan/Desktop/USYD_FinTech_Bootcamp_2023_Material/Project_3/Contracts/Compiled/SIR_NFT_abi.json')]
#file = st.selectbox("Upload Artwork", options=nft_images, type=["jpg", "jpeg", "png"])

if st.button("Register Artwork"):
    # Use the `pin_artwork` helper function to pin the file to IPFS
    artwork_ipfs_hash, token_json = pin_artwork(artwork_name, file)

    artwork_uri = f"ipfs://{artwork_ipfs_hash}"

    tx_hash = contract.functions.registerArtwork(
        address,
        artwork_name,
        artist_name,
        int(initial_appraisal_value),
        artwork_uri,
        token_json['image']
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
    st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    st.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{artwork_ipfs_hash})")
    st.markdown(f"[Artwork IPFS Image Link](https://ipfs.io/ipfs/{token_json['image']})")

st.markdown("---")


################################################################################
# Appraise Art
################################################################################
st.markdown("## Appraise Artwork")
tokens = contract.functions.totalSupply().call()
token_id = st.selectbox("Choose an Art Token ID", list(range(tokens)))
new_appraisal_value = st.text_input("Enter the new appraisal amount")
appraisal_report_content = st.text_area("Enter details for the Appraisal Report")

if st.button("Appraise Artwork"):

    # Make a call to the contract to get the image uri
    image_uri = str(contract.functions.imageUri(token_id).call())
    
    # Use Pinata to pin an appraisal report for the report content
    appraisal_report_ipfs_hash =  pin_appraisal_report(appraisal_report_content+image_uri)

    # Copy and save the URI to this report for later use as the smart contract’s `reportURI` parameter.
    report_uri = f"ipfs://{appraisal_report_ipfs_hash}"

    tx_hash = contract.functions.newAppraisal(
        token_id,
        int(new_appraisal_value),
        report_uri,
        image_uri

    ).transact({"from": w3.eth.accounts[0]})
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    st.write(receipt)
st.markdown("---")

################################################################################
# Get Appraisals
################################################################################
st.markdown("## Get the appraisal report history")
art_token_id = st.number_input("Artwork ID", value=0, step=1)
if st.button("Get Appraisal Reports"):
    appraisal_filter = contract.events.Appraisal.create_filter(
        fromBlock=0, argument_filters={"tokenId": art_token_id}
    )
    reports = appraisal_filter.get_all_entries()
    if reports:
        for report in reports:
            report_dictionary = dict(report)
            st.markdown("### Appraisal Report Event Log")
            st.write(report_dictionary)
            st.markdown("### Pinata IPFS Report URI")
            report_uri = report_dictionary["args"]["reportURI"]
            report_ipfs_hash = report_uri[7:]
            image_uri = report_dictionary["args"]["artJson"]
            st.markdown(
                f"The report is located at the following URI: "
                f"{report_uri}"
            )
            st.write("You can also view the report URI with the following ipfs gateway link")
            st.markdown(f"[IPFS Gateway Link](https://ipfs.io/ipfs/{report_ipfs_hash})")
            st.markdown("### Appraisal Event Details")
            st.write(report_dictionary["args"])
            st.image(f'https://ipfs.io/ipfs/{image_uri}')
    else:
        st.write("This artwork has no new appraisals")
