# 
# Author: Peterson Yuhala
#

set term postscript size 5in,2.3in linewidth 1 color eps enhanced 22
set encoding utf8


set output "cpu_only.eps"
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
mp_starty=0.15

mp_height=0.65
mp_rowgap=0.19
mp_colgap=0.1
mp_width=0.9

eval mpSetup(2, 1)
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

set title "CPU: 30 TPS" font "Helvetica-bold,14" #offset 0,-0.2

set ylabel "CPU (millicores)" font ",16"  offset 4,0
set xlabel "Timestamp (s)" font ",16"
set xtics font ",14"

set xrange[0:700]

set yrange [0:0.25]

#set logscale y

set key samplen 0.75 maxrows 2 at graph 0.5, 0.98 center font ",10"


plot 'data/no_pbs_no_tee/no-pbs_no-tee_30_sys_op-geth.csv' u 1:4 every 4  w l ls 2006 notitle, \
     '' u 1:4 every 4 t "noPBS-noTEE" w lp ls 2006, \
     'data/no_pbs_tee/no-pbs_tee_30_sys_op-geth.csv' u 1:4 every 4  w l ls 2007 notitle, \
     '' u 1:4 every 4 t "noPBS-TEE" w lp ls 2007, \
     'data/pbs_no_tee/pbs_geth_no-tee_30_sys_op-geth-ext.csv' u 1:4 every 4 w l ls 22004 notitle, \
     '' u 1:4 every 4 t "PBS-noTEE" w lp ls 22004,\
     'data/pbs_tee/pbs_geth_tee_30_sys_op-geth-ext.csv' u 1:4 every 4 w l ls 22001 notitle, \
     '' u 1:4 every 4 t "PBS-TEE" w lp ls 22001, \
     'data/pbs_no_tee/pbs_rbuilder_no-tee_30_sys_op-rbuilder.csv' u 1:4 every 4 w l ls 2002 notitle, \
     '' u 1:4 every 4 t "PBS-noTEE-rb" w lp ls 2002, \
     'data/pbs_tee/pbs_rbuilder_tee_30_sys_op-rbuilder.csv' u 1:4 every 4 w l ls 2004 notitle, \
     '' u 1:4 every 4 t "PBS-TEE-rb" w lp ls 2004
    

eval mpNext
# --- GRAPH a (top left: noPBS-noTEE)

set title "CPU: 210 TPS" font "Helvetica-bold,14" #offset 0,-0.2

set ylabel "CPU (millicores)" font ",16"  offset 3,0
set xlabel "Timestamp (s)" font ",16"
set xtics font ",14"



#set yrange [0:5000]
set yrange [0:1]
set xrange[0:700]

set key samplen 0.75 maxrows 2 at graph 0.5, 0.98 center font ",10"

plot 'data/no_pbs_no_tee/no-pbs_no-tee_210_sys_op-geth.csv' u 1:4 every 4  w l ls 2006 notitle, \
     '' u 1:4 every 4 t "noPBS-noTEE" w lp ls 2006, \
     'data/no_pbs_tee/no-pbs_tee_210_sys_op-geth.csv' u 1:4 every 4  w l ls 2007 notitle, \
     '' u 1:4 every 4 t "noPBS-TEE" w lp ls 2007, \
     'data/pbs_no_tee/pbs_geth_no-tee_210_sys_op-geth-ext.csv' u 1:4  every 4 w l ls 22004 notitle, \
     '' u 1:4 every 4 t "PBS-noTEE" w lp ls 22004,\
     'data/pbs_tee/pbs_geth_tee_210_sys_op-geth-ext.csv' u 1:4 every 4 w l ls 22001 notitle, \
     '' u 1:4 every 4 t "PBS-TEE" w lp ls 22001, \
     'data/pbs_no_tee/pbs_rbuilder_no-tee_210_sys_op-rbuilder.csv' u 1:4 every 4 w l ls 2002 notitle, \
     '' u 1:4 every 4 t "PBS-noTEE-rb" w lp ls 2002, \
     'data/pbs_tee/pbs_rbuilder_tee_210_sys_op-rbuilder.csv' u 1:4 every 4 w l ls 2004 notitle, \
     '' u 1:4 every 4 t "PBS-TEE-rb" w lp ls 2004
    


     
!epstopdf "cpu_only.eps"
!rm "cpu_only.eps"
quit
