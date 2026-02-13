set term postscript size 5.6in,1.7in linewidth 1 color eps enhanced 22
set encoding utf8

set output "copy_synthetic.eps"
set datafile separator ","

#load "styles.inc"

load "common.gnuplot" 
load "linetypes.gnuplot"



## Variables
COEFF = 1000  #how much we multiply values; in this case we are changin seconds to milli seconds

## Set margins
MX=0.0
MY=0.0

## Graph sizes
SX=0.45
SY=0.5


## Common layout (shared by all plots)
set style data histogram
set style histogram clustered gap 0.3

## Multiplot settings

## mp_startx # Left edge of col 0 plot area
## mp_starty          # Top of row 0 plot area
## mp_width            # Total width of plot area
## mp_height         # Total height of plot area
## mp_rowgap         # Gap between plot rows
## mp_colgap          # Gap between plot columns
          

mp_startx=0.06
mp_starty=0.15

mp_height=0.65
mp_rowgap=0.1
mp_colgap=0.05
mp_width=0.9

DATA_SIZE=0.5 # 512MB of data was hashed

eval mpSetup(4,1)

set ytics nomirror
set grid ytics


set ytics font ",12"


eval mpNext
# --- GRAPH a (top left)

set title " (a) R=0" font "Helvetica-bold,12" #offset 0,-0.2
set xlabel "Data size (GiB)" font ",14"
set xtics("0.125" 0, "0.25" 1, "0.5" 2, "1" 3, "2" 4) font ",12"

set style fill solid border -1

set boxwidth 0.18
set xtics offset 0,0.4,0
set ytics offset 0.5,0,0
set xlabel offset 0,1,0

dx=0.19
set offset 0.3, 0.3, 0, 0 #left,right,top,bottom
set key samplen 1 font ",12" at graph 0.6,0.95


set ylabel "Copy time (s)" font ",14"  offset 2,0
set yrange[0:5]

#
# Num of DPUs: 256
# Num of DRM threads: vareies
# Data size: 1GB
#
plot 'data/copy/naive_copy.csv' using ($1):($3) t "naive" with lp ls 6, \
     'data/copy/cac_copy.csv' u ($1):($3) t "CAC" with lp ls 5, \
     

eval mpNext
# --- GRAPH b (top right)
unset label
set title " (b) R=0.25" font "Helvetica-bold,12" #offset 0,-0.2
set xlabel "Data size (GiB)" font ",14"
set xtics("0.125" 0, "0.25" 1, "0.5" 2, "1" 3, "2" 4) font ",12"



#unset key
#set key samplen 1 font ",12" at graph 0.75,0.95
set yrange[0:5]
unset ylabel

#
# Num of DPUs: varies
# Num of DRM threads: 32
# Data size: 1GB
#

plot 'data/copy/naive_copy.csv' using ($1):($4) t "naive" with lp ls 6, \
     'data/copy/cac_copy.csv' u ($1):($4) t "CAC" with lp ls 5, \

eval mpNext
# --- GRAPH b (top right)
unset label

set title " (c) R=0.75" font "Helvetica-bold,12" #offset 0,-0.2
set xlabel "Data size (GiB)" font ",14"
set xtics("0.125" 0, "0.25" 1, "0.5" 2, "1" 3, "2" 4) font ",12"

set yrange[0:4]

#
# Num of DPUs: 256
# Num of DRM threads: 32
# Data size: varies
#
plot 'data/copy/naive_copy.csv' using ($1):($5) t "naive" with lp ls 6, \
     'data/copy/cac_copy.csv' u ($1):($5) t "CAC" with lp ls 5, \
     


eval mpNext
# --- GRAPH b (top right)
unset label
set title " (d) R=1" font "Helvetica-bold,12" #offset 0,-0.2
set xlabel "Data size (GiB)" font ",14"
set xtics("0.125" 0, "0.25" 1, "0.5" 2, "1" 3, "2" 4) font ",12"



#unset key
#set key samplen 1 font ",12" at graph 0.75,0.95
set yrange[0:4]

#
# Num of DPUs: varies
# Num of DRM threads: 32
# Data size: 1GB
#

plot 'data/copy/naive_copy.csv' using ($1):($6) t "naive" with lp ls 6, \
     'data/copy/cac_copy.csv' u ($1):($6) t "CAC" with lp ls 5, \


unset multiplot
### End multiplot

     
!epstopdf "copy_synthetic.eps"
!rm "copy_synthetic.eps"
quit