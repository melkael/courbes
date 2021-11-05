import pprint
from statistics import mean
import matplotlib.ticker as mtick
from matplotlib import pyplot as plt
pp = pprint.PrettyPrinter()

mark = ['--o', '--v', '-.+', '-.s', '-p', '-*', ':h']
label = {"mcts": "MaVEN-S", "uepso": "UEPSO", "nrpa_true": "NRPA-D", "nrpa_false": "NRPA", "nepa_true": "NEPA-D", "nepa_false": "NEPA", "graphvine": "GraphVine"}

accs = {"mcts": {50: [], 60: [], 70: [], 80: [], 90: [], 100: []},
       "uepso": {50: [], 60: [], 70: [], 80: [], 90: [], 100: []},
       "nrpa_true": {50: [], 60: [], 70: [], 80: [], 90: [], 100: []},
       "nrpa_false": {50: [], 60: [], 70: [], 80: [], 90: [], 100: []},
       "nepa_true": {50: [], 60: [], 70: [], 80: [], 90: [], 100: []},
       "nepa_false": {50: [], 60: [], 70: [], 80: [], 90: [], 100: []}
}
#       "graphvine": {}}
rtcs = {"mcts": {50: [], 60: [], 70: [], 80: [], 90: [], 100: []},
       "uepso": {50: [], 60: [], 70: [], 80: [], 90: [], 100: []},
       "nrpa_true": {50: [], 60: [], 70: [], 80: [], 90: [], 100: []},
       "nrpa_false": {50: [], 60: [], 70: [], 80: [], 90: [], 100: []},
       "nepa_true": {50: [], 60: [], 70: [], 80: [], 90: [], 100: []},
       "nepa_false": {50: [], 60: [], 70: [], 80: [], 90: [], 100: []}
}


idx = list(range(10))
sizes = [50, 60, 70, 80, 90, 100]

for s in sizes:
    for i in idx:
        dir = f"var_sn:{s}_{i}/"
        for alg in accs.keys():
            acc = 0
            rtc = 0
            le = 0
            with open(dir + alg + ".txt") as f:
                for l in f.readlines():
                    le += 1
                    acc += float(l.split(",")[0])
                    rtc += float(l.split(",")[1])
            
                acc /= le
                acc /= 500
                rtc /= le

                accs[alg][s].append(acc)
                rtcs[alg][s].append(rtc)


accs_improvements = {"mcts": [], "uepso": [], "nrpa_true": [], "nrpa_false": [], "nepa_true": [], "nepa_false": []}

for size in sizes:
    for alg, res in accs.items():
        if alg != "mcts":
            for i in range(10):
                accs[alg][size][i] = accs[alg][size][i]# - accs["mcts"][size][i]) / accs["mcts"][size][i] 

#for size in sizes:
#    for i in range(10):
#        accs["mcts"][size][i] = 0

for i in accs_improvements:
    for s in sizes:
        accs_improvements[i].append(mean(accs[i][s]))

rtcs_improvements = {"mcts": [], "uepso": [], "nrpa_true": [], "nrpa_false": [], "nepa_true": [], "nepa_false": []}

for size in sizes:
    for alg, res in rtcs.items():
        if alg != "mcts":
            for i in range(10):
                rtcs[alg][size][i] = rtcs[alg][size][i]# - rtcs["mcts"][size][i]) / rtcs["mcts"][size][i] 

#for size in sizes:
#    for i in range(10):
#        rtcs["mcts"][size][i] = 0

for i in rtcs_improvements:
    for s in sizes:
        rtcs_improvements[i].append(mean(rtcs[i][s]))


k = 0

fig = plt.figure()
ax = fig.add_subplot(111)

for alg, acc in accs_improvements.items():
    ax.plot(sizes, acc, mark[k], label=label[alg])
    k += 1

ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.legend()
ax.set_xlabel("Size of physical network $|V|$")
ax.set_ylabel("Mean acceptance ratio")
plt.savefig("acc_var_sn.png")

plt.clf()

fig = plt.figure()
ax = fig.add_subplot(111)

k = 0
for alg, rtc in rtcs_improvements.items():
    ax.plot(sizes, rtc, mark[k], label=alg)
    k += 1

#ax.legend()
#ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.set_xlabel("Size of physical network $|V|$")
ax.set_ylabel("Mean revenue-to-cost ratio")
plt.savefig("rtc_var_sn.png")

plt.clf()