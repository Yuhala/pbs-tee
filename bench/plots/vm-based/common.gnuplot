TARGET="`echo $TARGET`"
TARGET="pdf"

gplt_ver=`gnuplot --version |awk '{print $2}'`

#
# Inspired from: https://github.com/rs3lab/Odinfs/blob/master/eval/fig/common.gnuplot
#



mp_startx=0.090                 # Left edge of col 0 plot area
mp_starty=0.120                 # Top of row 0 plot area
mp_width=0.825                  # Total width of plot area
mp_height=0.780                 # Total height of plot area
mp_colgap=0.07                  # Gap between columns
mp_rowgap=0.15                  # Gap between rows
# The screen coordinate of the left edge of column col
mp_left(col)=mp_startx + col*((mp_width+mp_colgap)/real(mp_ncols))
# The screen coordinate of the top edge of row row
mp_top(row)=1 - (mp_starty + row*((mp_height+mp_rowgap)/real(mp_nrows)))

# Set up a multiplot with w columns and h rows
mpSetup(w,h) = sprintf('\
    mp_nplot=-1; \
    mp_ncols=%d; \
    mp_nrows=%d; \
    set multiplot', w, h)
# Start the next graph in the multiplot
mpNext = '\
    mp_nplot=mp_nplot+1; \
    set lmargin at screen mp_left(mp_nplot%mp_ncols); \
    set rmargin at screen mp_left(mp_nplot%mp_ncols+1)-mp_colgap; \
    set tmargin at screen mp_top(mp_nplot/mp_ncols); \
    set bmargin at screen mp_top(mp_nplot/mp_ncols+1)+mp_rowgap; \
    unset label 1; \
    unset label'

set ytics nomirror
set xtics nomirror
set grid back lt 0 lt rgb '#999999'
set border 3 back


#
# Multiplot stuff
#


  # Based on
  # http://youinfinitesnake.blogspot.com/2011/02/attractive-scientific-plots-with.html

  # Line style for axes
  #set style line 80 lt 1
  #set style line 80 lt rgb "#808080"

  # Line style for grid
  #set style line 81 lt 3  # Dotted
  #set style line 81 lt rgb "#808080" lw 0.5

  #set grid back linestyle 81
  #set border 3 back linestyle 80