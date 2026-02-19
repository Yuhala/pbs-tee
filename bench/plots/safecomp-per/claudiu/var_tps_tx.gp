# 
# Author: Peterson Yuhala
#

#set term postscript size 5in,2.3in linewidth 1 color eps enhanced 22
set term postscript size 5in,4in linewidth 1 color eps enhanced 22
set encoding utf8


set output "var_tps_tx.eps"
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
          

#mp_startx=0.08
#mp_starty=0.15

#mp_height=0.65
#mp_rowgap=0.19
#mp_colgap=0.1
#mp_width=0.9

#eval mpSetup(2, 1)

mp_startx=0.08
mp_starty=0.08
mp_height=0.80
mp_rowgap=0.15
mp_colgap=0.1
mp_width=0.90

eval mpSetup(2, 2)
#

font_size = 14
label_size = 18

set ytics nomirror
set grid y
set ytics font ",12"


eval mpNext
# --- GRAPH a (top left)


set title "Time to inclusion (30 TPS)" font "Helvetica-bold,14" #offset 0,-0.2

set ylabel "Num. of Txs" font ",16"  offset 4,0
set xlabel "Time buckets" font ",16"
set xtics font ",14"


#set xtics("1-2s" 0, "2-3s" 1, "3-4s" 2, "4-5s" 3, "5+s" 4) font ",14"
set xtics("[1,2[s" 0, "[2,3[s" 1, "[3,4[s" 2, "[4,5[s" 3, "5+s" 4) font ",14"


#set xtics rotate by 60

set style fill solid border -1
set boxwidth 0.15
set xtics offset 0.4,0.4,0
set ytics offset 0.5,0,0
set xlabel offset 0,1,0

dx=0.08
#set offset 25, -0.5, 0, 0 #left,right,top,bottom

set yrange [0:6000]

#set key samplen 1 font ",14" at graph 0.5,0.95
#set key maxrows 1 samplen 0.5 width -2 invert center at graph 1.1,1.125 font ",12"
#set key samplen 1 font ",14" at graph 0.5,0.95

set key samplen 0.75 maxrows 2 at graph 0.5, 0.98 center font ",14"



plot 'data/no_pbs_no_tee/no-pbs_no-tee_30_tx_tti.csv' u ($1-dx):3 t "noPBS-noTEE" with boxes ls 1 lc rgb C2 fillstyle pattern 4, \
    'data/no_pbs_tee/no-pbs_tee_30_tx_tti.csv' u ($1+dx):3 t "noPBS-TEE"  with boxes ls 1 lc rgb C3 fillstyle pattern 2, \
    'data/pbs_no_tee/pbs_rbuilder_no-tee_30_tx_tti.csv' u ($1+3*dx):3 t "PBS-noTEE"  with boxes ls 1 lc rgb C1 fillstyle pattern 3, \
    'data/pbs_tee/pbs_rbuilder_tee_30_tx_tti.csv' u ($1+5*dx):3 t "PBS-TEE"  with boxes ls 1 lc rgb C5 fillstyle pattern 9
    

unset ytics

unset xtics

eval mpNext
# --- GRAPH b (top right)
set xrange[0:350]

set ytics autofreq
set ytics  font ",14"
set yrange [0:200]


set title "Pending Txs (270 TPS)" font "Helvetica-bold,14" #offset 0,-0.2

set ylabel "Num. of pending Txs" font ",16"  offset 3,0
set xlabel "Timestamp" font ",16" 
set xtics offset 0,0.4,0 font ",12"


#set key samplen 1 maxrows 1 center top outside at graph 0.5, 1.0 font ",14"

plot 'data/no_pbs_no_tee/no-pbs_no-tee_30_tx_pending_tx_smoothed.csv' u 1:4 every 2  w l ls 2006 notitle, \
     '' u 1:4 every 20 t "noPBS-noTEE" w lp ls 2006, \
     'data/no_pbs_tee/no-pbs_tee_30_tx_pending_tx_smoothed.csv' u 1:4 every 2  w l ls 2007 notitle, \
     '' u 1:4 every 20 t "noPBS-TEE" w lp ls 2007, \
     'data/pbs_no_tee/pbs_rbuilder_no-tee_30_tx_pending_tx_smoothed.csv' u 1:4 every 2 w l ls 22004 notitle, \
     '' u 1:4 every 20 t "PBS-noTEE" w lp ls 22004, \
     'data/pbs_tee/pbs_rbuilder_tee_30_tx_pending_tx_smoothed.csv' u 1:4 every 2 w l ls 22001 notitle, \
        '' u 1:4 every 20 t "PBS-TEE" w lp ls 22001
     


eval mpNext
# --- GRAPH a (bottom left)
unset xrange

set title "Time to inclusion (270 TPS)" font "Helvetica-bold,14" #offset 0,-0.2

set ylabel "Num. of Txs" font ",16"  offset 2,0
set xlabel "Time buckets" font ",16"

set xtics("[1,2[s" 0, "[2,3[s" 1, "[3,4[s" 2, "[4,5[s" 3, "5+s" 4) font ",14"
set ytics("10k" 10000, "20k" 20000, "30k" 30000, "40k" 40000, "50k" 50000) font ",14"

#set xtics rotate by 60

set style fill solid border -1
set boxwidth 0.15
set xtics offset 0.4,0.4,0
set ytics offset 0.5,0,0
set xlabel offset 0,1,0

dx=0.08
#set offset 25, -0.5, 0, 0 #left,right,top,bottom

#set xrange[0:400]
set yrange [0:50000]

set key samplen 0.75 maxrows 2 at graph 0.5, 0.98 center font ",14"



plot 'data/no_pbs_no_tee/no-pbs_no-tee_270_tx_tti.csv' u ($1-dx):3 t "noPBS-noTEE" with boxes ls 1 lc rgb C2 fillstyle pattern 4, \
    'data/no_pbs_tee/no-pbs_tee_270_tx_tti.csv' u ($1+dx):3 t "noPBS-TEE"  with boxes ls 1 lc rgb C3 fillstyle pattern 2, \
    'data/pbs_no_tee/pbs_rbuilder_no-tee_270_tx_tti.csv' u ($1+3*dx):3 t "PBS-noTEE"  with boxes ls 1 lc rgb C1 fillstyle pattern 3, \
    'data/pbs_tee/pbs_rbuilder_tee_270_tx_tti.csv' u ($1+5*dx):3 t "PBS-TEE"  with boxes ls 1 lc rgb C5 fillstyle pattern 9
    

unset ytics
unset xtics

eval mpNext
# --- GRAPH b (bottom right)
set xrange[0:350]

set ytics autofreq
set ytics  font ",14"
set yrange [0:1200]


set title "Pending Txs (270 TPS)" font "Helvetica-bold,14" #offset 0,-0.2

set ylabel "Num. of pending Txs" font ",16"  offset 3.5,0
set xlabel "Timestamp" font ",16" 
set xtics offset 0,0.4,0 font ",12"


#set key samplen 1 maxrows 1 center top outside at graph 0.5, 1.0 font ",14"

plot 'data/no_pbs_no_tee/no-pbs_no-tee_270_tx_pending_tx_smoothed.csv' u 1:4 every 2  w l ls 2006 notitle, \
     '' u 1:4 every 20 t "noPBS-noTEE" w lp ls 2006, \
     'data/no_pbs_tee/no-pbs_tee_270_tx_pending_tx_smoothed.csv' u 1:4 every 2  w l ls 2007 notitle, \
     '' u 1:4 every 20 t "noPBS-TEE" w lp ls 2007, \
     'data/pbs_no_tee/pbs_rbuilder_no-tee_270_tx_pending_tx_smoothed.csv' u 1:4 every 2 w l ls 22004 notitle, \
     '' u 1:4 every 20 t "PBS-noTEE" w lp ls 22004, \
     'data/pbs_tee/pbs_rbuilder_tee_270_tx_pending_tx_smoothed.csv' u 1:4 every 2 w l ls 22001 notitle, \
        '' u 1:4 every 20 t "PBS-TEE" w lp ls 22001
     


     
!epstopdf "var_tps_tx.eps"
!rm "var_tps_tx.eps"
quit
