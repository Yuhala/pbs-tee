# 
# Author: Peterson Yuhala
#
set term postscript size 3.5in,3in linewidth 1 color eps enhanced 22
#call "common.gnuplot" "3.4in, 3.9in"
set encoding utf8

set output "load_tps.eps"
set datafile separator comma

load "styles.inc"
load "common.gnuplot" 
load "linetypes.gnuplot"

## Variables
COEFF = 1000  # how much we multiply values; in this case we are changin seconds to milli seconds

set size 1,1

mp_startx=0.12
mp_starty=0.08
mp_height=0.80
mp_rowgap=0.17
mp_colgap=0.08
mp_width=0.80        

font_size = 14
label_size = 18

eval mpSetup(1,1)

set ytics nomirror
set grid y
set ytics font ",12"


eval mpNext
# --- GRAPH a (top left)


set title "Mined/executed transactions per second for varying loads" font "Helvetica-bold,14" #offset 0,-0.2

set ylabel "Mined TPS (Tx/s)" font ",16"  offset 3,0
set xlabel "Client load (Tx/s)" font ",16"
set xtics font ",14"


set xtics("5" 0, "10" 1, "20" 2, "25" 3, "50" 4, "100" 5, "200" 6, "400" 7, "800" 8, "1000" 9, "1600" 10, "2000" 11) font ",10"
#set xtics rotate by 60

set style fill solid border -1
set boxwidth 0.2
set xtics offset 0.4,0.4,0
set ytics offset 0.5,0,0
set xlabel offset 0,1,0

dx=0.12
#set offset 25, -0.5, 0, 0 #left,right,top,bottom

#set xrange[0:400]
set yrange [0:100]

#set key samplen 1 font ",14" at graph 0.5,0.95
#set key maxrows 1 samplen 0.5 width -2 invert center at graph 1.1,1.125 font ",12"
#set key samplen 1 font ",14" at graph 0.5,0.95

set key samplen 0.1 maxrows 2 at graph 0.5, 0.95 center font ",14"

#set key samplen 1 maxrows 1 center top outside at graph 0.5, 1.0 font ",14"

plot 'data/tps/nopbs-native.csv' u 1:3 t "no-pbs-native" w lp ls 2006, \
     'data/tps/nopbs-tdx.csv' u 1:3 t "no-pbs-TEE" w lp ls 2007, \
     'data/tps/pbs-native.csv' u 1:3 t "pbs-native" w lp ls 22004   

     
!epstopdf "load_tps.eps"
!rm "load_tps.eps"
quit
