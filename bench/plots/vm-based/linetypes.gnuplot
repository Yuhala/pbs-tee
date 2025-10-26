set linetype 1 lw 0.1 lc rgb '#00dd00'
set linetype 2 lw 1 lc rgb '#0000ff'
set linetype 3 lw 1 lc rgb '#ff0000'
set linetype 10 lw 1 lc rgb 'black'

# https://bit.ly/3wrgciA
set style line 1 lt rgb "#E69F00" lw 5 pt 1 #orange
set style line 2 lt rgb "#56B4E9" lw 5 pt 2 #skyblue
set style line 3 lt rgb "#009E73" lw 1 pt 5 #green
set style line 4 lt rgb "#F0E442" lw 1 pt 7 #yellow
set style line 5 lt rgb "#0072B2" lw 1 pt 13 #blue
set style line 6 lt rgb "#D55E00" lw 1 pt 9 #vermilion
set style line 7 lt rgb "#CC79A7" lw 1 pt 3 #pink

C1 = "#E69F00"
C2 = "#56B4E9"
C3 = "#009E73"
C4 = "#F0E442"
C5 = "#0072B2"
C6 = "#D55E00"
C7 = "#CC79A7"

set style line 10 lc rgb 'black' lt 1 lw 1.5

hist_pattern_0=7
hist_pattern_1=1
hist_pattern_2=2
hist_pattern_3=7

# line style
ls1 = 1
ls2 = 2
ls3 = 3
ls4 = 5
ls4 = 6
ls5 = 7


# color
cdpu = C1
ccpu = C2
ccpu_dpu = C3
cdpu_cpu= C5


# pattern
pstock = 6
pconcord = 10
plockstat = 17
pvictim= 10

set ytics nomirror
set xtics nomirror
set grid back lt 0 lt rgb '#999999'
set border 3 back

set style line 1 dt 1 lc rgb C1 lw 4
set style line 2 dt (2,2) lc rgb C2 lw 1
set style line 3 dt (1,1) lc rgb C3 lw 4
set style line 4 dt 3 lc rgb C4 lw 4
set style line 5 dt 4 lc rgb C5 lw 4
set style line 6 dt 5 lc rgb C6 lw 4
set style line 7 dt 6 lc rgb C7 lw 4

