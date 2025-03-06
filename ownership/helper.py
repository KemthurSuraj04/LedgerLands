from web3 import Web3
import json
# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"  # Update if Ganache is running elsewhere
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Verify connection
if not web3.is_connected:
    raise Exception("Unable to connect to the blockchain network.")


# Path to the contract's ABI
contract_path = "land-smartcontract/build/contracts/Land.json"

with open(contract_path) as file:
    contract_data = json.load(file)

contract_abi = contract_data["abi"]
contract_address = "0x61Bb5c3E6806fc669AF61D68247525f124050190"  # Replace with the deployed contract address

# Instantiate the contract
land_contract = web3.eth.contract(address=contract_address, abi=contract_abi)


def registerUser(userDetails):
    # buyerDetails is a dictionary with the buyer's details
    #
    
    
    
    checksum_address = Web3.to_checksum_address(userDetails["id"]) #blockchain address have to be in specific format
    txn = land_contract.functions.registerUser(
        userDetails['name'],
        userDetails['age'],
        userDetails['city'],
        userDetails['aadharNumber'],
        userDetails['panNumber'],
        userDetails['document'],
        userDetails['email']
    ).transact({
        'from': checksum_address,
        'gas': 2000000,  # Gas limit for the function call (adjust as needed)
        'gasPrice': web3.to_wei('20', 'gwei'),  # Gas price (adjust as needed)
        'nonce': web3.eth.get_transaction_count(checksum_address),
    })
    
    receipt = web3.eth.wait_for_transaction_receipt(txn)
    
    
    print("Buyer Receipt Transaction Hash",receipt.transactionHash.hex())
    return(receipt.status)
    
    #print(gas_estimate)
    
    
    