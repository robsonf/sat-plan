#!/usr/bin/gnuplot
 
 set title "Domínio Blocks-Ground"
 set xlabel "Arquivo"
 set ylabel "Tempo, Numero "
 set ytics "5"
 set xtics "5"

 set key box right outside title "Legenda"

 set border linewidth 1.5
 set pointintervalbox 0.5
 
 set style line 1 lc rgb '#006000' lt 1 lw 3 pt 10 pi -1 ps 0.5
 set style line 2 lc rgb '#0060ad' lt 1 lw 3 pt 12 pi -1 ps 0.5
 set style line 3 lc rgb '#6060ad' lt 1 lw 3 pt 7 pi -1 ps 0.5

# set style line 1 lc rgb '#0060ad' lt 1 lw 3 pt 7 pi -1 ps 0.5
# set style line 2 lc rgb '#000000' lt 1 lw 3 pt 13 pi -1 ps 0.5
# set style line 3 lc rgb '#6060ad' lt 1 lw 3 pt 14 pi -1 ps 0.5
# set style line 4 lc rgb '#006000' lt 1 lw 3 pt 15 pi -1 ps 0.5
# set style line 5 lc rgb '#000000' lt 1 lw 3 pt 16 pi -1 ps 0.5
# set style line 6 lc rgb '#000000' lt 1 lw 3 pt 17 pi -1 ps 0.5


# set style line 1 lc rgb '#0060ad' lt 1 lw 3 pt 7 ps 1.0   # --- blue
# set style line 2 lc rgb '#000000' lt 1 lw 3 pt 13 ps 1.0   # --- black

# set terminal epslatex size 6,4 standalone color colortext 10
 set terminal pdf
 set output 'bateria1.pdf'


 plot "dt1" title "Dummy" with linespoints ls 1, "et1" title "ReduçãoE" with linespoints ls 2, "tt1" title "ReduçãoT" with linespoints ls 3

#, "de1" title "Dummy (e)" with linespoints ls 2
#, "te1" title "ReduçãoE(e)" with linespoints ls 4
#, "te1" title "ReduçãoT(e)" with linespoints ls 6
 pause -1 "Hit any key to continue"
