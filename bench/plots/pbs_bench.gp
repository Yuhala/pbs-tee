# 
# Author: Peterson Yuhala
#

set term postscript size 5in,4in linewidth 1 color eps enhanced 22
#call "common.gnuplot" "3.4in, 3.9in"
set encoding utf8

set output "pbs_bench.eps"
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


set title "Time to inclusion" font "Helvetica-bold,14" #offset 0,-0.2

set ylabel "Num. of TXs" font ",16"  offset 1.25,0
set xlabel "Time buckets" font ",16"
set xtics font ",14"


set xtics("2-3s" 1, "3-4s" 2, "4-5s" 3, "5-6s" 4, "6-7s" 5, "7-8s" 6, "8-9s" 7, "9-10s" 8, "10-11s" 9, "11-12s" 10) font ",10"
#set xtics rotate by 60

set style fill solid border -1
set boxwidth 0.2
set xtics offset 0.4,0.4,0
set ytics offset 0.5,0,0
set xlabel offset 0,1,0

dx=0.14
#set offset 25, -0.5, 0, 0 #left,right,top,bottom

#set xrange[0:400]
set yrange [0:15]

#set key samplen 1 font ",14" at graph 0.5,0.95
#set key maxrows 1 samplen 0.5 width -2 invert center at graph 1.1,1.125 font ",12"
#set key samplen 1 font ",14" at graph 0.5,0.95

set key samplen 0.1 maxrows 2 at graph 0.5, 0.95 center font ",14"


plot 'data/nopbs-native/tti.csv' u ($1-dx):3 t "no-pbs-native" with boxes ls 1 lc rgb C2 fillstyle pattern 4, \
    'data/nopbs-tee/tti.csv' u ($1+dx):3 t "no-pbs-TEE"  with boxes ls 1 lc rgb C3 fillstyle pattern 2, \
    'data/pbs-native/tti.csv' u ($1+3*dx):3 t "pbs-native"  with boxes ls 1 lc rgb C1 fillstyle pattern 3
     
unset xtics
eval mpNext
# --- GRAPH b (top right)
#set xrange[0:400]


set yrange [0:15]
set title "Pending TXs" font "Helvetica-bold,12" #offset 0,-0.2

set ylabel "Num. of pending TXs" font ",16"  offset 2.5,0
set xlabel "Timestamp" font ",16" 
set xtics offset 0,0.4,0 font ",12"


#set key samplen 1 maxrows 1 center top outside at graph 0.5, 1.0 font ",14"

plot 'data/nopbs-native/pending_tx.csv' u 1:3 t "no-pbs-native" w lp ls 2006, \
     'data/nopbs-tee/pending_tx.csv' u 1:3 t "no-pbs-TEE" w lp ls 2007, \
     'data/pbs-native/pending_tx.csv' u 1:3 t "pbs-native" w lp ls 22004   


eval mpNext
# --- GRAPH bottom left

set title "Gas per block" font "Helvetica-bold,12" 
set xlabel "Block number" font ",16"
set xtics font ",14"



set style fill solid border -1
#set boxwidth 20
set xtics offset 0,0.4,0
set ytics offset 0.5,0,0
set xlabel offset 0,1,0

#set xrange[1:20]
set yrange [0:70000000]

#unset key 
set ylabel "Gas used (wei)" font ",16"  offset 2.5,0
#set key samplen 1 maxrows 1 center top outside at graph 0.5, 1.0 font ",14"

plot 'data/nopbs-native/gas_per_block.csv' u 1:3 t "no-pbs-native" w lp ls 2006, \
     'data/nopbs-tee/gas_per_block.csv' u 1:3 t "no-pbs-TEE" w lp ls 2007, \
     'data/pbs-native/gas_per_block.csv' u 1:3 t "pbs-native" w lp ls 22004   
     

eval mpNext
# --- GRAPH: bottom right
set yrange [0:40]
unset xtics

set style fill solid border -1
set boxwidth 0.25

set xtics("44k-48k" 1, "56k-60k" 2, "5.2M-5.2M" 3, "6.0M-6.0M" 4) offset 0,0.3,0 font ",12"
#set xtics rotate by 45

set title "TX gas used" font "Helvetica-bold,12" #offset 0,-0.2

set ylabel "Num. of TXs" font ",16"  offset 2.5,0
set xlabel "Gas used" font ",16"
dx=0.15

#set label "min = 1μs" at graph 0.6,0.9 font ",16"
#set label "avg = 2^{48}μs" at graph 0.6,0.78 font ",16"
#set label "max = 2^{64}-1μs" at graph 0.6,0.65 font ",16"

#set key samplen 1 maxrows 1 center top outside at graph 0.5, 1.0 font ",14"

plot 'data/nopbs-native/gas_used.csv' u ($1-dx):3 t "no-pbs-native" with boxes ls 1 lc rgb C2 fillstyle pattern 4, \
     'data/nopbs-tee/gas_used.csv' u ($1+dx):3 t "no-pbs-TEE" with boxes ls 1 lc rgb C3 fillstyle pattern 2, \
     'data/pbs-native/gas_used.csv' u ($1+3*dx):3 t "pbs-native"  with boxes ls 1 lc rgb C1 fillstyle pattern 3  

     
!epstopdf "pbs_bench.eps"
!rm "pbs_bench.eps"
quit
