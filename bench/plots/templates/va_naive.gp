set term postscript size 5in,2in linewidth 1 color eps enhanced 22
set encoding utf8

set output "va_naive.eps"
set datafile separator ","

load "styles.inc"

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
          

mp_startx=0.1
mp_starty=0.15

mp_height=0.65
mp_rowgap=0.19
mp_colgap=0.1
mp_width=0.85


eval mpSetup(2,1)

set ytics nomirror
set grid ytics


set ytics font ",12"


eval mpNext
# --- GRAPH a (top left)

set title " (a) Vector addition: DPU vs CPU" font "Helvetica-bold,14" #offset 0,-0.2
set xlabel "Vector size (MiB)" font ",16"
set xtics("64" 1, "128" 2, "256" 3, "512" 4) font ",12"
set style fill solid border -1

set boxwidth 0.36
set xtics offset 0,0.4,0
set ytics offset 0.5,0,0
set xlabel offset 0,1,0

dx=0.19
set offset 0.3, 0.3, 0, 0 #left,right,top,bottom

#set label 2 "xx: " at screen 0.2,0.53 font "Arial,11"
#set key  reverse Left maxrows 1 spacing 1.75 samplen 1 width 1.75 invert center at graph 1,1.07 font ",12"
#set key inside top left samplen 1 font ",12" 
set key samplen 1 font ",14" at graph 0.4,0.95

set label "System configuration:" at graph 0.1,0.7 font "Helvetica-bold,12"
set label "256 DPUs (16 tasklets/DPU)" at graph 0.1,0.6 font "Helvetica-bold,12"
set label "64 CPU threads" at graph 0.1,0.5 font "Helvetica-bold,12"

set ylabel "Time (ms)" font ",16"  offset 2,0


plot 'data/dpu/va_naive_dpu.csv' using ($1-dx):($4*COEFF) title "DPU " with boxes ls 1 lc rgb C3 fillstyle pattern 2, \
     'data/host/va_naive_cpu.csv' u ($1+dx):($3*COEFF) t "CPU " with boxes ls 1 lc rgb C2 fillstyle pattern 4, \
   

eval mpNext
# --- GRAPH b (top right)
unset label

set title " (b) Host-to-DPU data transfer" font "Helvetica-bold,14" #offset 0,-0.2

set ylabel "Time(s)" font ",16"  offset 4,0
set key samplen 1 font ",14" at graph 0.75,0.95
set yrange[0:2]
plot 'data/dpu/va_naive_dpu.csv' using ($1):($3) title "host-to-DPU copy " with boxes ls 1 lc rgb C1 fillstyle pattern 1, \
     #'data/vary_n/dpu_poly_multi_naive.csv' u ($1-dx):($5*COEFF + $6*COEFF) t "host-dpu " ls 2 with boxes, \
     


unset multiplot
### End multiplot

     
!epstopdf "va_naive.eps"
!rm "va_naive.eps"
quit