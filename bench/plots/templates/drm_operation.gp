set term postscript size 5.5in,1.7in linewidth 1 color eps enhanced 22
set encoding utf8

set output "drm_operation.eps"
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
          

mp_startx=0.08
mp_starty=0.15

mp_height=0.65
mp_rowgap=0.19
mp_colgap=0.08
mp_width=0.9

DATA_SIZE=0.5 # 512MB of data was hashed

eval mpSetup(3,1)

set ytics nomirror
set grid ytics


set ytics font ",12"

set style fill solid border -1

set boxwidth 0.18
set xtics offset 0,0.4,0
set ytics offset 0.5,0,0
set xlabel offset 0,1,0


dx=0.12
set offset 0.3, 0.3, 0, 0 #left,right,top,bottom

set key samplen 1 font ",12" at graph 0.6,0.95


set ylabel "Time (s)" font ",14"  offset 4,0
set yrange[0:0.25]



eval mpNext

# --- GRAPH b (top right)
unset label

set title " (a) Varying data size" font "Helvetica-bold,14" #offset 0,-0.2
set xlabel "Data size (GiB)" font ",14"

set xtics("0.25" 0, "0.5" 1, "1" 2, "2" 3) font ",12"


set yrange[0:0.15]

#
# Num of DPUs: 256
# Num of DRM threads: 32
# Data size: varies
#
#data_file='data/drm/vary-data/vary_data.csv'
data_file='data/drm/new-data/vary_data.csv'

plot data_file using ($1-2*dx):($3) t "R=0      " with boxes ls 1 lc rgb C1 fillstyle pattern 5, \
     '' u ($1-0.5*dx):($6) t "R=0.25 " with boxes ls 1 lc rgb C6 fillstyle pattern 1, \
     '' u ($1+dx):($6) title "R=0.75 " with boxes ls 1 lc rgb C2 fillstyle pattern 4, \
     '' u ($1+2.4*dx):($4) title "R=1      " with boxes ls 1 lc rgb C3 fillstyle pattern 2, \



eval mpNext
# --- GRAPH a (top left)

set title " (b) Varying num. of DRM threads" font "Helvetica-bold,14" #offset 0,-0.2
set xlabel "Num. of DRM threads" font ",14"
set xtics("4" 0, "8" 1, "16" 2, "32" 3, "64" 4) font ",12"

set yrange[0:0.25]

#
# Num of DPUs: 256
# Num of DRM threads: vareies
# Data size: 1GB
#

data='data/drm/vary-threads/vary_threads.csv'
#data='data/drm/new-data/vary_threads.csv'

#
# Beware when changing the data source above as 
# the column orders change, to be fixed.
#

plot data using ($1-2*dx):($3) t "R=0      " with boxes ls 1 lc rgb C1 fillstyle pattern 5, \
     '' u ($1-0.5*dx):($4) t "R=0.25 " with boxes ls 1 lc rgb C6 fillstyle pattern 1, \
     '' u ($1+dx):($5) title "R=0.75 " with boxes ls 1 lc rgb C2 fillstyle pattern 4, \
     '' u ($1+2.4*dx):($6) title "R=1      " with boxes ls 1 lc rgb C3 fillstyle pattern 2, \
         

eval mpNext
# --- GRAPH b (top right)
unset label
set title " (c) Varying num. of DPUs" font "Helvetica-bold,14" #offset 0,-0.2
set xlabel "Num. of DPUs" font ",14"
set xtics("32" 0, "64" 1, "128" 2, "256" 3) font ",12"


set yrange[0:0.25]
#
# Num of DPUs: varies
# Num of DRM threads: 32
# Data size: 1GB
#

dpu_data = 'data/drm/vary-dpus/vary_dpus.csv'
#dpu_data='data/drm/new-data/vary_dpus.csv'

plot dpu_data using ($1-2*dx):($3) t "R=0      " with boxes ls 1 lc rgb C1 fillstyle pattern 5, \
     '' u ($1-0.5*dx):($4) t "R=0.25 " with boxes ls 1 lc rgb C6 fillstyle pattern 1, \
     '' u ($1+dx):($5) title "R=0.75 " with boxes ls 1 lc rgb C2 fillstyle pattern 4, \
     '' u ($1+2.4*dx):($6) title "R=1      " with boxes ls 1 lc rgb C3 fillstyle pattern 2, \

    


unset multiplot
### End multiplot

     
!epstopdf "drm_operation.eps"
!rm "drm_operation.eps"
quit