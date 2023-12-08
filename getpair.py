from web3 import Web3
import time
from decimal import Decimal
class UniswapHelper:
    def __init__(self, rpc_url,contract_address):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.contract_address = contract_address
        self.last_block = self.w3.eth.block_number
        self.bought=0
        self.amount0In = 0.0
        self.amount1In = 0.0
        self.amount0Out =0.0
        self.amount1Out=0.0
        self.swap_event_abi = {
            "anonymous": False,
            "inputs": [
                {"indexed": True, "internalType": "address", "name": "sender", "type": "address"},
                {"indexed": False, "internalType": "uint256", "name": "amount0In", "type": "uint256"},
                {"indexed": False, "internalType": "uint256", "name": "amount1In", "type": "uint256"},
                {"indexed": False, "internalType": "uint256", "name": "amount0Out", "type": "uint256"},
                {"indexed": False, "internalType": "uint256", "name": "amount1Out", "type": "uint256"},
                {"indexed": True, "internalType": "address", "name": "to", "type": "address"}
            ],
            "name": "Swap",
            "type": "event"
        }
        self.contract_abi = [self.swap_event_abi]
        self.event_signature = self.w3.keccak(
            text="Swap(address,uint256,uint256,uint256,uint256,address)"
        ).hex()

        # Uniswap V2 Factory Contract Address and ABI
        self.factory_address = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
        self.factory_address = self.w3.to_checksum_address(self.factory_address)

        self.factory_abi = [
            {
                "constant": True,
                "inputs": [{"name": "tokenA", "type": "address"}, {"name": "tokenB", "type": "address"}],
                "name": "getPair",
                "outputs": [{"name": "", "type": "address"}],
                "type": "function"
            }
        ]

        # Initialize Factory Contract
        self.factory_contract = self.w3.eth.contract(address=self.factory_address, abi=self.factory_abi)

        # Uniswap V2 Router Contract Address and ABI
        self.router_address = "0x7a250d5630B4cF539739df2C5DACb4C659F2488D"
        self.router_address = self.w3.to_checksum_address(self.router_address)

        self.router_abi = [
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
        self.router_contract = self.w3.eth.contract(address=self.router_address, abi=self.router_abi)

    def get_uniswap_pair_address(self, token_address, weth_address):
        try:
            pair_address = self.factory_contract.functions.getPair(token_address, weth_address).call()
            return pair_address
        except Exception as e:
            print(f"An error occurred while getting the pair address: {e}")
            return None

    def get_token_details(self, token_address):
        abi = [
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

        instance = self.w3.eth.contract(address=token_address, abi=abi)
        token_supply = instance.functions.totalSupply().call()
        self.decimal = instance.functions.decimals().call()
        self.token_supply = token_supply / (10 ** self.decimal)
        name = instance.functions.name().call()
        symbol = instance.functions.symbol().call()

        return name,symbol,token_address,self.decimal


    def get_amount_in_weth(self, token_address, amount_in=1):
        path = [token_address,'0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2']
        #  path = ["0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", "0xdAC17F958D2ee523a2206206994597C13D831ec7"]

        try:
            amounts_out = self.router_contract.functions.getAmountsOut(amount_in * 10**self.decimal, path).call()
            self.price=amounts_out[1] / 10**18
            print(f"Amount in WETH for {amount_in} Token: {amounts_out[1] / 10**18} WETH")
        except Exception as e:
            print(f"An error occurred: {e}")
    def get_amount_in_usd(self,token_address,amount_in=1):
        self.get_token_details(token_address)
        # path = [token_address, weth_address]
        path = ["0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", "0xdAC17F958D2ee523a2206206994597C13D831ec7"]
        try:
            amounts_out = self.router_contract.functions.getAmountsOut(amount_in * 10**self.decimal, path).call()
            # print(f"Amount in USD for {amount_in} Token: {amounts_out[-1]/10**6} USD")
            path = [token_address,"0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", "0xdAC17F958D2ee523a2206206994597C13D831ec7"]
            amounts_out = self.router_contract.functions.getAmountsOut(amount_in * 10**self.decimal, path).call()
            self.value_in_usd=amounts_out[-1]/10**6
            scientific_notation_number = '6e-06'  # or any other scientific notation
            decimal_number = Decimal(self.value_in_usd)
            formatted_number = float(decimal_number) 
            print(f"this: {self.value_in_usd}")
            print(formatted_number)
            return self.value_in_usd
            # print(self.price*inusd)
        except Exception as e:
            print(f"An error occurred: {e}")
    def get_market_cap(self,contract_address):
        in_usd=self.get_amount_in_usd(contract_address)
        try:
            market_cap=float(self.value_in_usd)*float(self.token_supply)
            # print(market_cap)

            # if market_cap >= 1e6:
            #     return f"{market_cap / 1e6:.1f}M",in_usd
            # elif market_cap >= 1e3:
            #     return f"{market_cap / 1e3:.1f}K",in_usd
            # else:
            #     return f"{market_cap:.1f}",in_usd
            return market_cap,in_usd
        except Exception as e:
            print(e)
        
    def get_positions(self):
        position=self.router_contract.functions.getReserves().call()
        print(position)
    def query_swap_events(self,pair_address,contract_address):
        token_amount=0
        final_usd=0
        transaction_hash=''
        buyers_address=''

        mkt,value_in_usd=self.get_market_cap(contract_address)
        # print(f"this is mKT: {mkt}")
        print('pullimg')
        current_block = self.w3.eth.block_number
        if current_block > self.last_block:
            filter_params = {
                "fromBlock": self.last_block + 1,
                "toBlock": current_block,
                "topics": [self.event_signature],
                "address": pair_address
            }
            new_entries = self.w3.eth.get_logs(filter_params)                                                                                                                                                                                                                                                                                                                                                                                            
            for entry in new_entries:
                event_data = self.w3.eth.contract(
                    abi=self.contract_abi, address=pair_address
                ).events.Swap().process_log(entry)
                self.amount0In = event_data['args']['amount0In']
                self.amount1In = event_data['args']['amount1In']
                self.amount0Out = event_data['args']['amount0Out']
                self.amount1Out = event_data['args']['amount1Out']
                if self.amount0In > 0 and self.amount1Out > 0:
                    print(f"sell: {self.amount0In} token0 for {self.amount1Out} token1")
                if self.amount1In > 0 and self.amount0Out > 0:
                    self.bought=1
                    desired_value = entry['topics'][2]
                    desired_value_hex_string = desired_value.hex()
                    buyers_address=desired_value_hex_string.lstrip('0x')
                    print(f"0x{buyers_address}")
                    print(f"buy: {self.amount1In/10**18} token1 for {self.amount0Out/10**self.decimal} token0")
                    token_amount=int(self.amount0Out/10**self.decimal)
                    path = ["0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", "0xdAC17F958D2ee523a2206206994597C13D831ec7"]

                    try:
                        amounts_out = self.router_contract.functions.getAmountsOut(1 * 10**self.decimal, path).call()
                        print(f"Amount in USD for {1} Token: {amounts_out[-1]/10**6} USD")
                        
                        path = [self.contract_address,"0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", "0xdAC17F958D2ee523a2206206994597C13D831ec7"]

                        amounts_out = self.router_contract.functions.getAmountsOut(1 * 10**self.decimal, path).call()
                        self.value_in_usd=amounts_out[-1]/10**6
                        print(f"this is value: {self.value_in_usd}")

                        final_usd= value_in_usd*token_amount
                        transaction_hash = entry['transactionHash'].hex()  # This will give you the transaction hash
                       
                    except Exception as e:
                        print(f"An error occurred: {e}")                    
            self.last_block = current_block
        return mkt,token_amount,final_usd,transaction_hash,buyers_address
    def start_listening(self,pair_address,contract_address,query_interval=2):
        while True:
            self.query_swap_events(pair_address,contract_address)
            
            time.sleep(query_interval)
# # # # # Example Usage
# rpc_url = "https://mainnet.infura.io/v3/7c2a5e84734b44e6a9af8b545ffbbdb3"

# contract_address = '0xc0200B1c6598a996a339196259fFdC30C1f44339'
# weth_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
# uniswap_helper = UniswapHelper(rpc_url,contract_address)

# pair_address = uniswap_helper.get_uniswap_pair_address(contract_address, weth_address)
# if pair_address:
#     print(f"Pair Address for Token-WETH: {pair_address}")

# name,symbol,token_supply,decimal=uniswap_helper.get_token_details(contract_address)
# uniswap_helper.get_amount_in_weth(contract_address)
# uniswap_helper.get_amount_in_usd(contract_address)
# print(name)
# print(f"decimal {decimal}")
# uniswap_helper.get_market_cap(contract_address)
# # uniswap_helper.get_positions
# uniswap_helper.start_listening(pair_address,contract_address)

# # print(work.amount1In)