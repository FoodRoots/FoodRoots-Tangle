# Import datetime library
from datetime import datetime

# Import the PyOTA library
import iota
from iota import Transaction
from iota import Address

# Import json
import json

# Import from PrettyTable
from prettytable import PrettyTable

# Define IOTA address where all transactions (supply chain records) are stored, replace with your own address.
# IOTA addresses can be created with the IOTA Wallet
FoodLogAddr = b"QSTNPAGBBFUSQPTINAKSGEIHVWKDZGU9QX9KNYMHYHIMKVB9ZSAWSMIOORDDHXEXFEKQENPYJVHCTZW9CRM9TP9AT9"
address = [Address(b'QSTNPAGBBFUSQPTINAKSGEIHVWKDZGU9QX9KNYMHYHIMKVB9ZSAWSMIOORDDHXEXFEKQENPYJVHCTZW9CRM9TP9AT9')]

# Create IOTA object, specify full node to be used when sending transactions.
# Notice that not all nodes in the field.deviota.com cluster has enabled attaching transactions to the tangle
# In this case you will get an error, you can try again later or change to a different full node.
api = iota.Iota("https://nodes.thetangle.org:443")

# Show welcome message
print("\nWelcome to the FoodRoots log system")
print("\nType 'newinput()' in the console in order to register a new data transaction")
print("\nor type 'retrieve()' in the console in order to retrieve all data transactions")
def newinput():
    # Get the ID of the sender
    senderid = input("\nPlease type your username and press Enter: ")
  
    # Get the ID of the receiver
    receiverid = input("\nPlease type the username of the receiver and press Enter: ")
   
    # Get the ID of the product
    productid = input("\nPlease type the identification code of the product and press Enter: ")

    # Get the ID of the product
    susimp = input("\nPlease type the sustainability impact and press Enter: ")

    # Create json data to be uploaded to the tangle
    data = {'Sender': senderid, 'Receiver': receiverid, 'Product ID': productid}

    # Define new IOTA transaction
    pt = iota.ProposedTransaction(address = iota.Address(FoodLogAddr),
                                  message = iota.TryteString.from_unicode(json.dumps(data)),
                                  tag     = iota.Tag(b'HOTELIOTA'),
                                  value   = 0)

    # Print waiting message
    print("\nSending transaction...Please wait...")

    # Send transaction to the tangle
    api.send_transfer(depth=3, transfers=[pt], min_weight_magnitude=14)['bundle']

    # Print confirmation message 
    print("\nTransaction sucessfully completed!")
    print("\nType 'newinput()' in the console in order to register a new data transaction")
    print("\nor type 'retrieve()' in the console in order to retrieve all data transactions")

def retrieve(): 
    x = PrettyTable()
    
    # Specify column headers for the table
    x.field_names = ["Sender", "Receiver", "Product ID", "Date and Time"]

    # Find all transacions for selected IOTA address
    result = api.find_transactions(addresses=address)
    
    # Create a list of transaction hashes
    myhashes = result['hashes']

    # Print wait message
    print("Please wait while retrieving FoodRoots data from the tangle...")

    # Loop trough all transaction hashes
    for txn_hash in myhashes:
    
        # Convert to bytes
        txn_hash_as_bytes = bytes(txn_hash)

        # Get the raw transaction data (trytes) of transaction
        gt_result = api.get_trytes([txn_hash_as_bytes])
    
        # Convert to string
        trytes = str(gt_result['trytes'][0])
    
        # Get transaction object
        txn = Transaction.from_tryte_string(trytes)
    
        # Get transaction timestamp
        timestamp = txn.timestamp
    
        # Convert timestamp to datetime
        dateandtime = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        # Get transaction message as string
        txn_data = str(txn.signature_message_fragment.decode())
    
        # Convert to json
        json_data = json.loads(txn_data)
    
        # Check if json data has the expected json tag's
        if all(key in json.dumps(json_data) for key in ["Sender", "Receiver", "Product ID"]):
            # Add table row with json values
            x.add_row([json_data['Sender'], json_data['Receiver'], json_data['Product ID'], dateandtime])

    # Sort table by cleaned datetime
    x.sortby = "Date and Time"
    
    # Print table to terminal
    print(x)
    
    # Print continuation message 
    print("\nType 'newinput()' in the console in order to register a new data transaction")
    print("\nor type 'retrieve()' in the console in order to retrieve all data transactions")