from web3 import Web3
from web3.contract import Contract

class TokenTransactionListener:
    def init(self, rpc_url, token_address):
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        self.token_address = Web3.toChecksumAddress(token_address)
        self.token_abi = [...]  # ERC-20 Token ABI

    def listen_for_buyers(self):
        token_contract = self.web3.eth.contract(address=self.token_address, abi=self.token_abi)
        
        # Filter for Transfer events
        transfer_filter = token_contract.events.Transfer.createFilter(fromBlock='latest')
        
        while True:
            for event in transfer_filter.get_new_entries():
                # Extract buyer's address (the 'to' field in the event)
                buyer_address = event['args']['to']
                print(f"New buyer detected: {buyer_address}")

# Example usage
rpc_url = 'https://mainnet.infura.io/v3/yourProjectId'  # Replace with your Ethereum RPC URL
token_address = '0xTokenContractAddress'  # Replace with the token contract address
listener = TokenTransactionListener(rpc_url, token_address)
listener.listen_for_buyers()






















from web3 import Web3

# Connect to an Ethereum node
w3 = Web3(Web3.HTTPProvider('YOUR_ETHEREUM_NODE_URL'))

# Uniswap V2 contract address (for example, the Router contract)
uniswap_v2_router_address = '0xUniswapV2RouterAddress'

# ABI for the Uniswap V2 Router (simplified for example)
uniswap_v2_router_abi = [...]  # Replace with actual ABI

# Create a contract instance
uniswap_v2_contract = w3.eth.contract(address=uniswap_v2_router_address, abi=uniswap_v2_router_abi)

# Define the token you're interested in
token_address = '0xTokenAddress'

# Define the block number to start tracking from
start_block = 'YOUR_START_BLOCK'

# Event filter for Swap events involving your token
swap_filter = uniswap_v2_contract.events.Swap.createFilter(fromBlock=start_block, argument_filters={'token': token_address})

# Poll for new entries (or use event listener in a more advanced implementation)
while True:
    for event in swap_filter.get_new_entries():
        buyer_address = event.args.buyer  # Or appropriate field based on the event
        print(f"New Token Purchase by {buyer_address}")