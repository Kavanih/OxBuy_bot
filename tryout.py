

from web3 import Web3
import time

class SwapScanner:
    def __init__(self, rpc_url, contract_address):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.contract_address = contract_address
        self.last_block = self.w3.eth.block_number
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

    def query_swap_events(self):
        current_block = self.w3.eth.block_number
        if current_block > self.last_block:
            filter_params = {
                "fromBlock": self.last_block + 1,
                "toBlock": current_block,
                "topics": [self.event_signature],
                "address": self.contract_address
            }
            new_entries = self.w3.eth.get_logs(filter_params)
            for entry in new_entries:
                event_data = self.w3.eth.contract(
                    abi=self.contract_abi, address=self.contract_address
                ).events.Swap().process_log(entry)
                amount0In = event_data['args']['amount0In']
                amount1In = event_data['args']['amount1In']
                amount0Out = event_data['args']['amount0Out']
                amount1Out = event_data['args']['amount1Out']
                if amount0In > 0 and amount1Out > 0:
                    print(f"sell: {amount0In} token0 for {amount1Out} token1")
                if amount1In > 0 and amount0Out > 0:
                    print(f"buy: {amount1In} token1 for {amount0Out} token0")
            self.last_block = current_block

    def start(self, query_interval=10):
        while True:
            self.query_swap_events()
            time.sleep(query_interval)


