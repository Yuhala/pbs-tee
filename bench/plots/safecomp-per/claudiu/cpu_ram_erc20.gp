# 
# Author: Peterson Yuhala
#

set term postscript size 5in,2.3in linewidth 1 color eps enhanced 22
set encoding utf8


set output "cpu_ram_erc20.eps"
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


set title "CPU usage (op-geth)" font "Helvetica-bold,14" #offset 0,-0.2

set ylabel "CPU (millicores)" font ",16"  offset 3.5,0
set xlabel "Timestamp" font ",16"
set xtics font ",14"


#set xtics("1-2s" 0, "2-3s" 1, "3-4s" 2, "4-5s" 3, "5+s" 4) font ",14"
#set xtics rotate by 60

set style fill solid border -1
set boxwidth 0.15
set xtics offset 0.4,0.4,0
set ytics offset 0.5,0,0
set xlabel offset 0,1,0

dx=0.08
#set offset 25, -0.5, 0, 0 #left,right,top,bottom

#set xrange[0:100]
set xrange[0:60]

#set yrange [0:5000]
set yrange [0:500]

#set key samplen 1 font ",14" at graph 0.5,0.95
#set key maxrows 1 samplen 0.5 width -2 invert center at graph 1.1,1.125 font ",12"
#set key samplen 1 font ",14" at graph 0.5,0.95

set key samplen 0.75 maxrows 2 at graph 0.5, 0.98 center font ",14"


plot 'data/no_pbs_no_tee/no-pbs_no-tee_270_sys_cpu_ram.csv' u 1:3 every 1  w l ls 2006 notitle, \
     '' u 1:3 every 5 t "noPBS-noTEE" w lp ls 2006, \
     'data/no_pbs_tee/no-pbs_tee_270_sys_cpu_ram.csv' u 1:3 every 1  w l ls 2007 notitle, \
     '' u 1:3 every 5 t "noPBS-TEE" w lp ls 2007, \
     'data/pbs_no_tee/pbs_rbuilder_no-tee_270_sys_cpu_ram.csv' u 1:3 every 1 w l ls 22004 notitle, \
     '' u 1:3 every 5 t "PBS-noTEE" w lp ls 22004, \
     'data/pbs_tee/pbs_rbuilder_tee_270_sys_cpu_ram.csv' u 1:3 every 1 w l ls 22001 notitle, \
        '' u 1:3 every 5 t "PBS-TEE" w lp ls 22001


unset xtics
eval mpNext
# --- GRAPH b (top right)
#set xrange[0:100]
set xrange[0:60]


set yrange [0:1000]
set title "RAM usage (op-geth)" font "Helvetica-bold,14" #offset 0,-0.2

set ylabel "RAM usage (MB)" font ",16"  offset 3.5,0
set xlabel "Timestamp" font ",16" 
set xtics offset 0,0.4,0 font ",12"


#set key samplen 1 maxrows 1 center top outside at graph 0.5, 1.0 font ",14"

plot 'data/no_pbs_no_tee/no-pbs_no-tee_270_sys_cpu_ram.csv' u 1:4 every 2  w l ls 2006 notitle, \
     '' u 1:4 every 5 t "noPBS-noTEE" w lp ls 2006, \
     'data/no_pbs_tee/no-pbs_tee_270_sys_cpu_ram.csv' u 1:4 every 2  w l ls 2007 notitle, \
     '' u 1:4 every 5 t "noPBS-TEE" w lp ls 2007, \
     'data/pbs_no_tee/pbs_rbuilder_no-tee_270_sys_cpu_ram.csv' u 1:4 every 2 w l ls 22004 notitle, \
     '' u 1:4 every 5 t "PBS-noTEE" w lp ls 22004, \
     'data/pbs_tee/pbs_rbuilder_tee_270_sys_cpu_ram.csv' u 1:4 every 2 w l ls 22001 notitle, \
        '' u 1:4 every 5 t "PBS-TEE" w lp ls 22001


## Gas plots removed
     
!epstopdf "cpu_ram_erc20.eps"
!rm "cpu_ram_erc20.eps"
quit
