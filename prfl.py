#!/usr/bin/env python

import profile, pstats, subprocess
#python -m cProfile myscript.py
subprocess.call(["python","-m","cProfile","-o","stats","game.py"])
file = 'stats'
p = pstats.Stats(file)
p.sort_stats('cumulative').print_stats(20)