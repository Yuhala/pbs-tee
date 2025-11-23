# 
# Author: Peterson Yuhala
#

set term postscript size 3.4in, 5.5in linewidth 1 color eps enhanced 22
#call "common.gnuplot" "3.4in, 3.9in"
set encoding utf8

set output "flood_bench_lat.eps"
set datafile separator comma

load "styles.inc"
load "common.gnuplot" 
load "linetypes.gnuplot"

#
# Benchmark descriptions: all are read-only RPC calls which do not modify state nor consume gas
# 1. eth_call : queries data from smart contracts
# 2. eth_getBalance : returns ETH balance at a specific address and block
# 3. eth_getBlockByNumber: fetches block by number
# 4. eth_getCode: returns smart contract bytecode
# 5. eth_getStorageAt: reads a single storage slot from a contract
# 6. eth_getTransactionByHash: returns Tx object for a given Tx hash
# 7. eth_getTransactionCount: returns num. of Txs sent by an address
# 8. eth_getTransactionReceipt: returns receipt for a mined Tx



## Variables
mp_startx=0.15
mp_starty=0.08
mp_height=0.80
mp_rowgap=0.17
mp_colgap=0.08
mp_width=0.80 

mp_startx=0.15
mp_starty=0.05
mp_height=0.9
mp_rowgap=0.07
mp_colgap=0.08
mp_width=0.8


eval mpSetup(2,4)

set ytics nomirror
set grid y
set ytics font ",12"


eval mpNext
# --- GRAPH a (top left)


set ylabel "Median latency (s)" font ",14"  offset -12,0
set xlabel "Requests per second" font ",10"  offset 1.25,-0.5
set xtics font ",10"
set ytics font ",10"


#set xtics("" 1, "" 2, "" 3, "" 4, "" 5, "" 6, "" 7, "" 8, "" 9, "" 10) font ",10"
set xtics ("0" 0, "200" 200, "400" 400, "600" 600, "800" 800, "1000" 1000)
#set xtics rotate by 60

set style fill solid border -1
set boxwidth 0.2
set xtics offset 0.4,0.4,0
set ytics offset 0.5,0,0
set xlabel offset 0,1,0

dx=0.12
#set offset 25, -0.5, 0, 0 #left,right,top,bottom

#set xrange[0:400]
set yrange [0:0.015]

#set key samplen 1 font ",14" at graph 0.5,0.95
set key maxrows 1 samplen 0.5 width -2 invert center at graph 1.0,1.2 font ",12"
#set key samplen 1 font ",14" at graph 0.5,0.95

#set key samplen 0.1 maxrows 2 at graph 0.5, 0.95 center font ",14"

set title "eth-call" font "Helvetica-bold,10" offset 0,-0.75

plot 'data/flood/nopbs-native/data.csv' u 2:11 t "no-pbs-native" w lp ls 2006, \
     'data/flood/nopbs-tee/data.csv' u 2:11 t "no-pbs-TEE" w lp ls 2007, \
     'data/flood/pbs-native/data.csv' u 2:11 t "pbs-native" w lp ls 22004, \
     'data/flood/pbs-tee/data.csv' u 2:11 t "pbs-native" w lp ls 2009
     

eval mpNext

unset key
set title "eth-getBalance" font "Helvetica-bold,10" #offset 0,-0.2

plot 'data/flood/nopbs-native/data.csv' u 2:11 t "no-pbs-native" w lp ls 2006, \
     'data/flood/nopbs-tee/data.csv' u 2:11 t "no-pbs-TEE" w lp ls 2007, \
     'data/flood/pbs-native/data.csv' u 2:11 t "pbs-native" w lp ls 22004 




eval mpNext

set title "eth-getBlockByNumber" font "Helvetica-bold,10" #offset 0,-0.2

plot 'data/flood/nopbs-native/data.csv' u 2:11 t "no-pbs-native" w lp ls 2006, \
     'data/flood/nopbs-tee/data.csv' u 2:11 t "no-pbs-TEE" w lp ls 2007, \
     'data/flood/pbs-native/data.csv' u 2:11 t "pbs-native" w lp ls 22004 


eval mpNext

set title "eth-getCode" font "Helvetica-bold,10" #offset 0,-0.2

plot 'data/flood/nopbs-native/data.csv' u 2:11 t "no-pbs-native" w lp ls 2006, \
     'data/flood/nopbs-tee/data.csv' u 2:11 t "no-pbs-TEE" w lp ls 2007, \
     'data/flood/pbs-native/data.csv' u 2:11 t "pbs-native" w lp ls 22004 

eval mpNext

set title "eth-getStorageAt" font "Helvetica-bold,10" #offset 0,-0.2

plot 'data/flood/nopbs-native/data.csv' u 2:11 t "no-pbs-native" w lp ls 2006, \
     'data/flood/nopbs-tee/data.csv' u 2:11 t "no-pbs-TEE" w lp ls 2007, \
     'data/flood/pbs-native/data.csv' u 2:11 t "pbs-native" w lp ls 22004 

eval mpNext

set title "eth-getTransactionByHash" font "Helvetica-bold,10" #offset 0,-0.2

plot 'data/flood/nopbs-native/data.csv' u 2:11 t "no-pbs-native" w lp ls 2006, \
     'data/flood/nopbs-tee/data.csv' u 2:11 t "no-pbs-TEE" w lp ls 2007, \
     'data/flood/pbs-native/data.csv' u 2:11 t "pbs-native" w lp ls 22004 

eval mpNext

set title "eth-getTransactionCount" font "Helvetica-bold,10" #offset 0,-0.2

plot 'data/flood/nopbs-native/data.csv' u 2:11 t "no-pbs-native" w lp ls 2006, \
     'data/flood/nopbs-tee/data.csv' u 2:11 t "no-pbs-TEE" w lp ls 2007, \
     'data/flood/pbs-native/data.csv' u 2:11 t "pbs-native" w lp ls 22004 
     

eval mpNext

set title "eth-getTransactionReceipt" font "Helvetica-bold,10" #offset 0,-0.2

plot 'data/flood/nopbs-native/data.csv' u 2:11 t "no-pbs-native" w lp ls 2006, \
     'data/flood/nopbs-tee/data.csv' u 2:11 t "no-pbs-TEE" w lp ls 2007, \
     'data/flood/pbs-native/data.csv' u 2:11 t "pbs-native" w lp ls 22004 


!epstopdf "flood_bench_lat.eps"
!rm "flood_bench_lat.eps"
quit
