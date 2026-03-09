# 
# Author: Peterson Yuhala
#

set term postscript size 5in,2.3in linewidth 1 color eps enhanced 22
set encoding utf8


set output "cumulative_tti.eps"
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


set title "30 TPS" font "Helvetica-bold,14" #offset 0,-0.2

set ylabel "Included Txs (%)" font ",16"  offset 3.5,0
set xlabel "TTI (ms)" font ",16"
set xtics font ",12"


#set xtics("1-2s" 0, "2-3s" 1, "3-4s" 2, "4-5s" 3, "5+s" 4) font ",14"
#set ytics("10k" 10000, "20k" 20000, "30k" 30000, "40k" 40000, "50k" 50000) font ",14"

#set xtics rotate by 60

set style fill solid border -1
set boxwidth 0.15
set xtics offset 0.4,0.4,0
set ytics offset 0.5,0,0
set xlabel offset 0,1,0

dx=0.08
#set offset 25, -0.5, 0, 0 #left,right,top,bottom

set xrange[0:4500]
set yrange [0:120]

#set key samplen 1 font ",14" at graph 0.5,0.95
#set key maxrows 1 samplen 0.5 width -2 invert center at graph 1.1,1.125 font ",12"
#set key samplen 1 font ",14" at graph 0.5,0.95

set key samplen 0.75 maxrows 2 at graph 0.5, 0.95 center font ",10"

plot 'data/no_pbs_no_tee/no-pbs_no-tee_30_tx_cumu_tti.csv' u 1:2 every 50  w l ls 2006 notitle, \
     '' u 1:2 every 300 t "noPBS-noTEE" w lp ls 2006, \
     'data/no_pbs_tee/no-pbs_tee_30_tx_cumu_tti.csv' u 1:2 every 50  w l ls 2007 notitle, \
     '' u 1:2 every 300 t "noPBS-TEE" w lp ls 2007, \
     'data/pbs_no_tee/pbs_geth_no-tee_30_tx_cumu_tti.csv' u 1:2 every 50 w l ls 22004 notitle, \
     '' u 1:2 every 300 t "PBS-noTEE" w lp ls 22004, \
     'data/pbs_tee/pbs_geth_tee_30_tx_cumu_tti.csv' u 1:2 every 50 w l ls 22001 notitle, \
     '' u 1:2 every 300 t "PBS-TEE" w lp ls 22001, \
     'data/pbs_no_tee/pbs_rbuilder_no-tee_30_tx_cumu_tti.csv' u 1:2 every 50 w l ls 2002 notitle, \
     '' u 1:2 every 300 t "PBS-noTEE-rb" w lp ls 2002, \
     'data/pbs_tee/pbs_rbuilder_tee_30_tx_cumu_tti.csv' u 1:2 every 50 w l ls 2004 notitle, \
     '' u 1:2 every 300 t "PBS-TEE-rb" w lp ls 2004
    


unset ytics

unset xtics

eval mpNext
# --- GRAPH b (top right)
#set xrange[0:400]

set ytics  font ",14"
set yrange [0:120]


set title "210 TPS" font "Helvetica-bold,14" #offset 0,-0.2

set ylabel "Included Txs (%)" font ",16"  offset 3,0
set xlabel "TTI (ms)" font ",16" 
set xtics offset 0,0.4,0 font ",12"


#set key samplen 1 maxrows 1 center top outside at graph 0.5, 1.0 font ",14"

plot 'data/no_pbs_no_tee/no-pbs_no-tee_210_tx_cumu_tti.csv' u 1:2 every 50  w l ls 2006 notitle, \
     '' u 1:2 every 300 t "noPBS-noTEE" w lp ls 2006, \
     'data/no_pbs_tee/no-pbs_tee_210_tx_cumu_tti.csv' u 1:2 every 50  w l ls 2007 notitle, \
     '' u 1:2 every 300 t "noPBS-TEE" w lp ls 2007, \
     'data/pbs_no_tee/pbs_geth_no-tee_210_tx_cumu_tti.csv' u 1:2 every 50 w l ls 22004 notitle, \
     '' u 1:2 every 300 t "PBS-noTEE" w lp ls 22004, \
     'data/pbs_tee/pbs_geth_tee_210_tx_cumu_tti.csv' u 1:2 every 50 w l ls 22001 notitle, \
     '' u 1:2 every 300 t "PBS-TEE" w lp ls 22001, \
     'data/pbs_no_tee/pbs_rbuilder_no-tee_210_tx_cumu_tti.csv' u 1:2 every 50 w l ls 2002 notitle, \
     '' u 1:2 every 300 t "PBS-noTEE-rb" w lp ls 2002, \
     'data/pbs_tee/pbs_rbuilder_tee_210_tx_cumu_tti.csv' u 1:2 every 50 w l ls 2004 notitle, \
     '' u 1:2 every 300 t "PBS-TEE-rb" w lp ls 2004
     
     
     
## Gas plots removed
     
!epstopdf "cumulative_tti.eps"
!rm "cumulative_tti.eps"
quit
