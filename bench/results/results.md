## No PBS monolythic baseline (host)

1. time to inclusion: // a histogram showing number of txs in buckets of time to inclusion
const buckets = ["3 - 4 s", "4 - 5 s", "5 - 6 s", "6 - 7 s", "8 - 9 s"];
      const counts = [36, 6, 4, 2, 2];

2. pending txs: a line chart showing pending transactions over time
const timestamps = [1760965027, 1760965028, 1760965029, 1760965030, 1760965031, 1760965032, 1760965033, 1760965034, 1760965035, 1760965036, 1760965037, 1760965038, 1760965039, 1760965040, 1760965041];
      const pendingTxs = [0, 8, 10, 18, 12, 20, 13, 21, 14, 22, 15, 15, 6, 6, 0];


## No PBS monolythic baseline (VM)
1. time to inclusion:
 const buckets = ["3 - 4 s", "4 - 5 s", "5 - 6 s", "6 - 7 s"];
      const counts = [15, 15, 4, 1];

2. pending txs:
const timestamps = [1761039528, 1761039529, 1761039530, 1761039531, 1761039532, 1761039533, 1761039534, 1761039535, 1761039536, 1761039537, 1761039538, 1761039539, 1761039540];
      const pendingTxs = [0, 5, 10, 15, 15, 20, 16, 20, 12, 12, 3, 3, 0];


3. Gas per block:
const blocks = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23];
      const gasValues = [52242, 5210541, 43854, 30043824, 54043800, 54052188, 54043800, 18043836, 43854, 43854, 43854];

4. Gas used: 
  const buckets = ["44k - 48k", "56k - 60k", "5.2M - 5.2M", "6.0M - 6.0M"];
      const gasUsed = [9, 2, 1, 35];


## No PBS TDX/TEE baseline 
1. time to inclusion (bar chart):
const buckets = ["2 - 3 s", "3 - 4 s", "4 - 5 s", "5 - 6 s", "6 - 7 s", "7 - 8 s", "8 - 9 s"];
      const counts = [3, 22, 19, 2, 2, 1, 1];

2. pending txs (line plot):
  const timestamps = [1761037835, 1761037836, 1761037837, 1761037838, 1761037839, 1761037840, 1761037841, 1761037842, 1761037843, 1761037844, 1761037845, 1761037846, 1761037847, 1761037848, 1761037849];
      const pendingTxs = [0, 6, 10, 15, 14, 19, 15, 20, 16, 20, 17, 17, 8, 8, 0];


3. Gas per block (line plot):
const blocks = [713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724];
      const gasValues = [43818, 5210505, 52206, 36043782, 54043764, 54043764, 54043764, 54052152, 48043770, 43818, 43818, 43818];

4. Gas used (bar chart):
    const buckets = ["44k - 48k", "56k - 60k", "5.2M - 5.2M", "6.0M - 6.0M"];
      const gasUsed = [10, 2, 1, 50];

RPC Response Latency
Method	p50 (ms)	p90 (ms)	p99 (ms)
eth_blockNumber	10	50	50
eth_chainId	6	10	10
eth_estimateGas	0	0	0
eth_gasPrice	6	10	10
eth_getBlockByNumber	21	46	50
eth_getBlockReceipts	30	50	50
eth_getTransactionCount	7	32	50
eth_sendBundle	0	0	0
eth_sendRawTransaction	6	9	50
