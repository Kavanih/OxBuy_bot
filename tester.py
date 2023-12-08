
from web3 import Web3

# Initialize a Web3 instance connected to an Ethereum node
rpc_url = "https://mainnet.infura.io/v3/7c2a5e84734b44e6a9af8b545ffbbdb3"

w3 = Web3(Web3.HTTPProvider(rpc_url))

abi=abi = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [
            {"name": "", "type": "string"}
        ],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {"name": "", "type": "string"}
        ],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {"name": "", "type": "uint256"}
        ],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [
            {"name": "balance", "type": "uint256"}
        ],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {"name": "", "type": "uint8"}
        ],
        "type": "function",
    },
]

# Check connection
if not w3.is_connected():
    print("Failed to connect to Ethereum node.")
    exit()
# individual token
contract_address='0x4507cEf57C46789eF8d1a19EA45f4216bae2B528'

# Uniswap V2 Router Contract Address and ABI
router_address = "0x7a250d5630B4cF539739df2C5DACb4C659F2488D"
router_address=w3.to_checksum_address(router_address)

router_abi = [
    {
        "constant": False,
        "inputs": [
            {"name": "amountOutMin", "type": "uint256"},
            {"name": "path", "type": "address[]"},
            {"name": "to", "type": "address"},
            {"name": "deadline", "type": "uint256"}
        ],
        "name": "swapExactTokensForTokens",
        "outputs": [
            {"name": "amounts", "type": "uint256[]"}
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {"name": "amountIn", "type": "uint256"},
            {"name": "path", "type": "address[]"}
        ],
        "name": "getAmountsOut",
        "outputs": [
            {"name": "amounts", "type": "uint256[]"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# Initialize Router Contract
router_contract = w3.eth.contract(address=router_address, abi=router_abi)

#token information
instance=w3.eth.contract(address=contract_address,abi=abi)
token_supply=instance.functions.totalSupply().call()
decimal = instance.functions.decimals().call()
token_supply=token_supply / (10 ** decimal)
name=instance.functions.name().call()
symbol=instance.functions.symbol().call()

# Token Information
token_address = "0x2D9D7c64F6c00e16C28595ec4EbE4065ef3A250b"
weth_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
token_address=contract_address
# Define the path (Token -> WETH)
path = [token_address, weth_address]

# Define the amount (e.g., 1 Token)
amount_in = 1 * 10**18  # Adjust the decimals as per your token's decimal count

# Call getAmountsOut
try:
    amounts_out = router_contract.functions.getAmountsOut(amount_in, path).call()
    print(f"Amount in WETH for 1 Token: {amounts_out[1] / 10**18} WETH")
except Exception as e:
    print(f"An error occurred: {e}")


factory_address = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
factory_address = w3.to_checksum_address(factory_address)

factory_abi = [
    {
        "constant": True,
        "inputs": [{"name": "tokenA", "type": "address"}, {"name": "tokenB", "type": "address"}],
        "name": "getPair",
        "outputs": [{"name": "", "type": "address"}],
        "type": "function"
    }
]

# Initialize Factory Contract
factory_contract = w3.eth.contract(address=factory_address, abi=factory_abi)

# Get Pair Address
try:
    pair_address = factory_contract.functions.getPair(token_address, weth_address).call()
    print(f"Pair Address for {name}-{symbol}: {pair_address}")
except Exception as e:
    print(f"An error occurred while getting the pair address: {e}")


print(f'name {name}')
print(f'symbol {symbol}')
print(f'token_supply {token_supply}')


