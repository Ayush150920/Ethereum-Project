import streamlit as st
from web3 import Web3

# Define ABI and contract address
abi = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [],
        "name": "homeowner",
        "outputs": [
            {
                "internalType": "address payable",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "loanAmount",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_loanAmount",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "_monthlyPayment",
                "type": "uint256"
            },
            {
                "internalType": "address payable",
                "name": "_homeowner",
                "type": "address"
            }
        ],
        "name": "submitLoan",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "makePayment",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    }
]

contract_address = "0x7f07c72eC543beaf3635D122a1E7593D24D9B5aD"  # Update with correct contract address

# Streamlit app
st.title("Smart Contract Data Viewer")

# Connect to a local Ethereum node
node_url = "HTTP://127.0.0.1:9545"
web3 = Web3(Web3.HTTPProvider(node_url))

# Check if connected to the Ethereum node
if web3.is_connected():
    st.write("Connected to Ethereum node successfully!")
    contract = web3.eth.contract(address=contract_address, abi=abi)

    try:
        # Display homeowner's address
        homeowner = contract.functions.homeowner().call()
        st.write("Homeowner Address:", homeowner)

        # Display loan amount
        loan_amount = contract.functions.loanAmount().call()
        st.write("Loan Amount:", loan_amount)
    except Exception as e:
        st.error(f"Error fetching contract data: {str(e)}")

    # Submit new loan form
    st.subheader("Submit New Loan")
    loan_amount_input = st.number_input("Loan Amount", min_value=1)
    monthly_payment_input = st.number_input("Monthly Payment", min_value=1)
    homeowner_address_input = st.text_input("Homeowner Address")

    if st.button("Submit Loan"):
        try:
            # Get the first account from the node
            account = web3.eth.accounts[0]

            # Send transaction from the specified account
            tx_hash = contract.functions.submitLoan(loan_amount_input, monthly_payment_input, homeowner_address_input).transact({"from": account})

            st.success(f"Loan submitted. Transaction hash: {tx_hash.hex()}")
        except Exception as e:
            st.error(f"Error submitting loan: {str(e)}")

    # Make payment form
    st.subheader("Make Payment")
    payment_amount_input = st.number_input("Payment Amount", min_value=1)

    if st.button("Make Payment"):
        try:
            # Get the sender address from the connected web3 instance
            sender_address = web3.eth.accounts[0]  # Assuming the sender is the first account

            # Call the makePayment function and specify the sender address and payment amount
            tx_hash = contract.functions.makePayment().transact({"from": sender_address, "value": payment_amount_input})

            st.success(f"Payment made. Transaction hash: {tx_hash.hex()}")
        except Exception as e:
            st.error(f"Error making payment: {str(e)}")
else:
    st.error("Failed to connect to Ethereum node. Please check your connection.")
