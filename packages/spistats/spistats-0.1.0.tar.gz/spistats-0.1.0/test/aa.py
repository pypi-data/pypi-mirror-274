import numpy as np
import spistats.desynchronization as dsync

def proba_desync_once(p,m,N):
    packet_count = dsync.NumberOfPacketBeforeDsync(p,m)
    packet_count.eigenvalues()
    return packet_count.cdf_multin(N)


import data2 as data

tbl = {}
for key,val in data.data.items():
    i = key.split("-")
    p = 0.5*(int(i[0]) + int(i[1]))/100
    tbl[key] = {}
    for m in [5,10,15,30]:
        tbl[key][m] = proba_desync_once(p,m,np.array(val))


col = len(data.data.keys())
tbl_conf = "{c|"
for i in range(col):
    tbl_conf += "c"
tbl_conf+= "}"
tex = """
\\documentclass{article}
\\begin{document}
\\begin{tabular}"""
tex += tbl_conf
tex += "\n"
tex += "pregen&"
for key in tbl.keys():
    tex += f"{key}&"
tex = tex[:-1]
tex += "\\\\\n"
tex += "\\hline\n"

for m in tbl[list(tbl.keys())[0]].keys():
    tex += f"{m}&"
    for p in tbl.keys():
        tex += f"{round(tbl[p][m],3)}&"
    tex = tex[:-1]
    tex += "\\\\\n"
tex += """
\\end{tabular}
\\end{document}
"""

with open("main.tex", "w") as f:
    f.write(tex)

import os
os.system("pdflatex main.tex")


