# 
# Author: Peterson Yuhala
#

set term postscript size 5in,2.3in linewidth 1 color eps enhanced 22
set encoding utf8


set output "uniswap.eps"
set datafile separator comma

load "styles.inc"
load "common.gnuplot" 
load "linetypes.gnuplot"

## Multiplot settings

## mp_startx # Left edge of col 0 plot area
## mp_starty          # Top of row 0 plot area
## mp_width            # Total width of plot area
## mp_height         # Total height of plot area
## mp_rowgap         # Gap between plot rows
## mp_colgap          # Gap between plot columns
          

mp_startx=0.08
mp_starty=0.15

mp_height=0.65
mp_rowgap=0.19
mp_colgap=0.1
mp_width=0.9

eval mpSetup(2, 1)


font_size = 14
label_size = 18



set ytics nomirror
set grid y
set ytics font ",12"


eval mpNext
# --- GRAPH a (top left)


set title "Time to inclusion (TTI)" font "Helvetica-bold,14" #offset 0,-0.2

set ylabel "Num. of Txs" font ",16"  offset 4,0
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
set yrange [0:5000]

#set key samplen 1 font ",14" at graph 0.5,0.95
#set key maxrows 1 samplen 0.5 width -2 invert center at graph 1.1,1.125 font ",12"
#set key samplen 1 font ",14" at graph 0.5,0.95

set key samplen 0.75 maxrows 2 at graph 0.5, 0.98 center font ",14"



plot 'data/no_pbs_no_tee/uniswap/uniswap-30_tti.csv' u ($1-dx):3 t "noPBS-noTEE" with boxes ls 1 lc rgb C2 fillstyle pattern 4, \
     'data/pbs_tee_op-rbuilder/uniswap/uniswap-30_tti.csv' u ($1+5*dx):3 t "PBS-TEE"  with boxes ls 1 lc rgb C5 fillstyle pattern 9
     
    #'data/uniswap/nopbs_tee_uniswap_tti.csv' u ($1+dx):3 t "noPBS-TEE"  with boxes ls 1 lc rgb C3 fillstyle pattern 2, \
    #'data/uniswap/pbs_notee_op-rbuilder-uniswap_tti.csv' u ($1+3*dx):3 t "PBS-noTEE"  with boxes ls 1 lc rgb C1 fillstyle pattern 3, \
    



unset xtics
eval mpNext
# --- GRAPH b (top right)
set xrange[0:350]


set yrange [0:160]
set title "Pending Txs" font "Helvetica-bold,14" #offset 0,-0.2

set ylabel "Num. of pending Txs" font ",16"  offset 3,0
set xlabel "Timestamp" font ",16" 
set xtics offset 0,0.4,0 font ",12"


#set key samplen 1 maxrows 1 center top outside at graph 0.5, 1.0 font ",14"

plot 'data/no_pbs_no_tee/uniswap/uniswap-30_pending_tx.csv' u 1:3 every 2  w l ls 2006 notitle, \
      '' u 1:3 every 10 t "noPBS-noTEE" w lp ls 2006, \
      'data/pbs_tee_op-rbuilder/uniswap/uniswap-30_pending_tx.csv' u 1:3 every 2 w l ls 22001 notitle, \
        '' u 1:3 every 10 t "PBS-TEE" w lp ls 22001
     #'data/uniswap/nopbs_tee_uniswap_pending_tx.csv' u 1:3 every 2  w l ls 2007 notitle, \
     #'' u 1:3 every 10 t "noPBS-TEE" w lp ls 2007, \
     #'data/uniswap/pbs_notee_op-rbuilder-uniswap_pending_tx.csv' u 1:3 every 2 w l ls 22004 notitle, \
     #'' u 1:3 every 10 t "PBS-noTEE" w lp ls 22004, \
     


## Gas plots removed
     
!epstopdf "uniswap.eps"
!rm "uniswap.eps"
quit
