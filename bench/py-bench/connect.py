from web3 import Web3
from requests.adapters import HTTPAdapter
from requests import Session
from urllib3.util.retry import Retry

# Builder RPC endpoint
builder_rpc = "http://127.0.0.1:2222"  # NOT 4444!

# Session with retry and larger pool
session = Session()
adapter = HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=Retry(total=5, backoff_factor=0.2))
session.mount("http://", adapter)
session.mount("https://", adapter)

w3 = Web3(Web3.HTTPProvider(builder_rpc, session=session))

if not w3.is_connected():
    print("Could not connect to builder RPC at", builder_rpc)
else:
    print("Connected to builder RPC")
    print("Latest block:", w3.eth.block_number)
