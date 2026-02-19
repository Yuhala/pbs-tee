# 
# Author: Peterson Yuhala
#

#set term postscript size 5in,2.3in linewidth 1 color eps enhanced 22
set term postscript size 5in,4in linewidth 1 color eps enhanced 22
set encoding utf8


set output "l2_cpu_logscale.eps"
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

set style fill solid border -1
set boxwidth 0.15
set xtics offset 0.4,0.4,0
set ytics offset 0.5,0,0
set xlabel offset 0,1,0


set ytics nomirror
set grid y
set ytics font ",12"

eval mpNext
# --- GRAPH a (top left: noPBS-noTEE)

set title "noPBS-noTEE" font "Helvetica-bold,14" #offset 0,-0.2

set ylabel "CPU (millicores)" font ",16"  offset 5,0
set xlabel "Timestamp" font ",16"
set xtics font ",14"

set xrange[0:100]

#set yrange [0:5000]
#set yrange [0:5000]
set logscale y

set key samplen 0.75 maxrows 2 at graph 0.5, 0.98 center font ",14"


plot 'data/no_pbs_no_tee/no-pbs_no-tee_270_sys_op-batcher_cpu_ram.csv' u 1:4 every 5  w l ls 2006 notitle, \
     '' u 1:4 every 5 t "op-batcher" w lp ls 2006, \
     'data/no_pbs_no_tee/no-pbs_no-tee_270_sys_op-geth_cpu_ram.csv' u 1:4 every 5  w l ls 2007 notitle, \
     '' u 1:4 every 5 t "op-geth" w lp ls 2007, \
     'data/no_pbs_no_tee/no-pbs_no-tee_270_sys_op-node_cpu_ram.csv' u 1:4 every 5 w l ls 22004 notitle, \
     '' u 1:4 every 5 t "op-node" w lp ls 22004

eval mpNext
# --- GRAPH a (top left: noPBS-noTEE)

set title "noPBS-TEE" font "Helvetica-bold,14" #offset 0,-0.2

set ylabel "CPU (millicores)" font ",16"  offset 5,0
set xlabel "Timestamp" font ",16"
set xtics font ",14"

set xrange[0:100]

#set yrange [0:5000]
#set yrange [0:500]

set key samplen 0.75 maxrows 2 at graph 0.5, 0.98 center font ",14"


plot 'data/no_pbs_tee/no-pbs_tee_270_sys_op-batcher_cpu_ram.csv' u 1:4 every 5  w l ls 2006 notitle, \
     '' u 1:4 every 5 t "op-batcher" w lp ls 2006, \
     'data/no_pbs_tee/no-pbs_tee_270_sys_op-geth_cpu_ram.csv' u 1:4 every 5  w l ls 2007 notitle, \
     '' u 1:4 every 5 t "op-geth" w lp ls 2007, \
     'data/no_pbs_tee/no-pbs_tee_270_sys_op-node_cpu_ram.csv' u 1:4 every 5 w l ls 22004 notitle, \
     '' u 1:4 every 5 t "op-node" w lp ls 22004


eval mpNext
# --- GRAPH a (top left: noPBS-noTEE)

set title "PBS-noTEE" font "Helvetica-bold,14" #offset 0,-0.2

set ylabel "CPU (millicores)" font ",16"  offset 4,0
set xlabel "Timestamp" font ",16"
set xtics font ",14"

set xrange[0:60]

#set yrange [0:400]

set key samplen 0.75 maxrows 2 at graph 0.5, 0.98 center font ",14"


plot 'data/pbs_no_tee/pbs_rbuilder_no-tee_270_sys_op-batcher_cpu_ram.csv' u 1:4 every 5  w l ls 2006 notitle, \
     '' u 1:4 every 5 t "op-batcher" w lp ls 2006, \
     'data/pbs_no_tee/pbs_rbuilder_no-tee_270_sys_op-geth_cpu_ram.csv' u 1:4 every 5  w l ls 2007 notitle, \
     '' u 1:4 every 5 t "op-geth" w lp ls 2007, \
     'data/pbs_no_tee/pbs_rbuilder_no-tee_270_sys_op-node_cpu_ram.csv' u 1:4 every 5 w l ls 22004 notitle, \
     '' u 1:4 every 5 t "op-node" w lp ls 22004, \
     'data/pbs_no_tee/pbs_rbuilder_no-tee_270_sys_op-rbuilder_cpu_ram.csv' u 1:4 every 5 w l ls 22001 notitle, \
        '' u 1:4 every 5 t "op-rbuilder" w lp ls 22001


eval mpNext
# --- GRAPH a (top left: noPBS-noTEE)

set title "PBS-TEE" font "Helvetica-bold,14" #offset 0,-0.2

set ylabel "CPU (millicores)" font ",16"  offset 4,0
set xlabel "Timestamp" font ",16"
set xtics font ",14"

#set yrange [0:5000]
#set yrange [0:500]

set key samplen 0.75 maxrows 2 at graph 0.5, 0.98 center font ",14"


plot 'data/pbs_tee/pbs_rbuilder_tee_270_sys_op-batcher_cpu_ram.csv' u 1:4 every 5  w l ls 2006 notitle, \
     '' u 1:4 every 5 t "op-batcher" w lp ls 2006, \
     'data/pbs_tee/pbs_rbuilder_tee_270_sys_op-geth_cpu_ram.csv' u 1:4 every 5  w l ls 2007 notitle, \
     '' u 1:4 every 5 t "op-geth" w lp ls 2007, \
     'data/pbs_tee/pbs_rbuilder_tee_270_sys_op-node_cpu_ram.csv' u 1:4 every 5 w l ls 22004 notitle, \
     '' u 1:4 every 5 t "op-node" w lp ls 22004, \
     'data/pbs_tee/pbs_rbuilder_tee_270_sys_op-rbuilder_cpu_ram.csv' u 1:4 every 5 w l ls 22001 notitle, \
     '' u 1:4 every 5 t "op-rbuilder" w lp ls 22001


     
!epstopdf "l2_cpu_logscale.eps"
!rm "l2_cpu_logscale.eps"
quit
