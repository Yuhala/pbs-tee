# 
# Author: Peterson Yuhala
#

#set term postscript size 3.3in,2.8in linewidth 1 color eps enhanced 22
set term postscript size 5in,4in linewidth 1 color eps enhanced 22
#call "common.gnuplot" "3.4in, 3.9in"
set encoding utf8

set output "erc20.eps"
set datafile separator comma

load "styles.inc"
load "common.gnuplot" 
load "linetypes.gnuplot"

## Variables
COEFF = 1000  # how much we multiply values; in this case we are changin seconds to milli seconds


mp_startx=0.12
mp_starty=0.08
mp_height=0.80
mp_rowgap=0.17
mp_colgap=0.08
mp_width=0.80      


font_size = 14
label_size = 18

eval mpSetup(2,2)

set ytics nomirror
set grid y
set ytics font ",12"


eval mpNext
# --- GRAPH a (top left)


set title "Time to inclusion (TTI)" font "Helvetica-bold,14" #offset 0,-0.2

set ylabel "Num. of Txs" font ",16"  offset 2.5,0
set xlabel "Time buckets" font ",16"
set xtics font ",14"


set xtics("1-2s" 0, "2-3s" 1, "3-4s" 2, "4-5s" 3, "5+s" 4) font ",14"
#set xtics rotate by 60

set style fill solid border -1
set boxwidth 0.15
set xtics offset 0.4,0.4,0
set ytics offset 0.5,0,0
set xlabel offset 0,1,0

dx=0.08
#set offset 25, -0.5, 0, 0 #left,right,top,bottom

#set xrange[0:400]
set yrange [0:800]

#set key samplen 1 font ",14" at graph 0.5,0.95
#set key maxrows 1 samplen 0.5 width -2 invert center at graph 1.1,1.125 font ",12"
#set key samplen 1 font ",14" at graph 0.5,0.95

set key samplen 0.75 maxrows 2 at graph 0.5, 0.98 center font ",14"



plot 'data/erc20/nopbs_notee_erc20_tti.csv' u ($1-dx):3 t "noPBS-noTEE" with boxes ls 1 lc rgb C2 fillstyle pattern 4, \
    'data/erc20/nopbs_tee_erc20_tti.csv' u ($1+dx):3 t "noPBS-TEE"  with boxes ls 1 lc rgb C3 fillstyle pattern 2, \
    'data/erc20/pbs_notee_op-rbuilder-erc20_tti.csv' u ($1+3*dx):3 t "PBS-noTEE"  with boxes ls 1 lc rgb C1 fillstyle pattern 3, \
    'data/erc20/pbs_tee_op-rbuilder_erc20_tti.csv' u ($1+5*dx):3 t "PBS-TEE"  with boxes ls 1 lc rgb C5 fillstyle pattern 9
     
unset xtics
eval mpNext
# --- GRAPH b (top right)
set xrange[0:220]


set yrange [0:20]
set title "Pending Txs" font "Helvetica-bold,14" #offset 0,-0.2

set ylabel "Num. of pending Txs" font ",16"  offset 2.5,0
set xlabel "Timestamp" font ",16" 
set xtics offset 0,0.4,0 font ",12"


#set key samplen 1 maxrows 1 center top outside at graph 0.5, 1.0 font ",14"

plot 'data/erc20/nopbs_notee_erc20_pending_tx.csv' u 1:3 every 2  w l ls 2006 notitle, \
      '' u 1:3 every 10 t "noPBS-noTEE" w lp ls 2006, \
     'data/erc20/nopbs_tee_erc20_pending_tx.csv' u 1:3 every 2  w l ls 2007 notitle, \
     '' u 1:3 every 10 t "noPBS-TEE" w lp ls 2007, \
     'data/erc20/pbs_notee_op-rbuilder-erc20_pending_tx.csv' u 1:3 every 2 w l ls 22004 notitle, \
     '' u 1:3 every 10 t "PBS-noTEE" w lp ls 22004, \
     'data/erc20/pbs_tee_op-rbuilder_erc20_pending_tx.csv' u 1:3 every 2 w l ls 22001 notitle, \
        '' u 1:3 every 10 t "PBS-TEE" w lp ls 22001

unset xrange
eval mpNext
# --- GRAPH bottom left

set title "Gas per block" font "Helvetica-bold,14" 
set xlabel "Block number" font ",16"
set xtics font ",14"

set style fill solid border -1



#unset key 
set ylabel "Gas used (wei)" font ",16"  offset 2.5,0
#set key samplen 1 maxrows 1 center top outside at graph 0.5, 1.0 font ",14"
set yrange [0:1000000]
set xrange [0:120]
set ytics("200k" 200000, "400k" 400000, "600k" 600000, "800k" 800000, "1M" 1000000) font ",12"


plot 'data/erc20/nopbs_notee_erc20_gas_per_block.csv' u 1:3 every 2  w l ls 2006 notitle, \
      '' u 1:3 every 10 t "noPBS-noTEE" w lp ls 2006, \
     'data/erc20/nopbs_tee_erc20_gas_per_block.csv' u 1:3 every 2  w l ls 2007 notitle, \
     '' u 1:3 every 10 t "noPBS-TEE" w lp ls 2007, \
     'data/erc20/pbs_notee_op-rbuilder-erc20_gas_per_block.csv' u 1:3 every 2 w l ls 22004 notitle, \
     '' u 1:3 every 10 t "PBS-noTEE" w lp ls 22004, \
     'data/erc20/pbs_tee_op-rbuilder_erc20_gas_per_block.csv' u 1:3 every 2 w l ls 22001 notitle, \
        '' u 1:3 every 10 t "PBS-TEE" w lp ls 22001
     

eval mpNext
# --- GRAPH: bottom right
set yrange [0:1000]
unset xrange

set style fill solid border -1
set boxwidth 0.15
set xtics offset 0.4,0.4,0
set ytics offset 0.5,0,0
set xlabel offset 0,1,0


#set xtics("0-500k" 0, "500k-650k" 1, "650k-850k" 2, "850k-1M" 3, "1M-1.3M" 4, "1.3M+" 5) offset 0,0.3,0 font ",10"
set xtics("0-5" 0, "5-6.5" 1) font ",10"
#set xtics rotate by 45
#set xrange [-0.7:10]



set ytics("200" 200, "400" 400, "600" 600, "800" 800, "1000" 1000) font ",12"

set title "Tx gas used" font "Helvetica-bold,14" #offset 0,-0.2

set ylabel "Num. of Txs" font ",16"  offset 3.5,0
set xlabel "Gas used (x100000 wei)" font ",16"
dx=0.08

#set label "min = 1μs" at graph 0.6,0.9 font ",16"
#set label "avg = 2^{48}μs" at graph 0.6,0.78 font ",16"
#set label "max = 2^{64}-1μs" at graph 0.6,0.65 font ",16"

#set key samplen 1 maxrows 1 center top outside at graph 0.5, 1.0 font ",14"

plot 'data/erc20/nopbs_notee_erc20_tx_gas_used.csv' u ($1-dx):3 t "noPBS-noTEE" with boxes ls 1 lc rgb C2 fillstyle pattern 4, \
     'data/erc20/nopbs_tee_erc20_tx_gas_used.csv' u ($1+dx):3 t "noPBS-TEE" with boxes ls 1 lc rgb C3 fillstyle pattern 2, \
     'data/erc20/pbs_notee_op-rbuilder-erc20_tx_gas_used.csv' u ($1+3*dx):3 t "PBS-noTEE"  with boxes ls 1 lc rgb C1 fillstyle pattern 3, \
     'data/erc20/pbs_tee_op-rbuilder_erc20_tx_gas_used.csv' u ($1+5*dx):3 t "PBS-TEE"  with boxes ls 1 lc rgb C5 fillstyle pattern 9

     
!epstopdf "erc20.eps"
!rm "erc20.eps"
quit
