from matplotlib import pyplot as plt

accs = {"mcts": [], "uepso": [], "nrpa_true": [], "nrpa_false": [], "nepa_true": [], "nepa_false": [], "graphvine": []}
rtcs = {"mcts": [], "uepso": [], "nrpa_true": [], "nrpa_false": [], "nepa_true": [], "nepa_false": [], "graphvine": []}

mark = ['--o', '--v', '-.+', '-.s', '-p', '-*', ':h']

label = {"mcts": "MaVEN-S", "uepso": "UEPSO", "nrpa_true": "NRPA-D", "nrpa_false": "NRPA", "nepa_true": "NEPA-D", "nepa_false": "NEPA", "graphvine": "GraphVine"}

lambds = [0.02, 0.03, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075, 0.08]

for i in lambds:
    dir = "Imv_lambda:{}/".format(i)
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
            accs[alg].append(acc)
            rtcs[alg].append(rtc)

print(accs)
k = 0
for alg, acc in accs.items():
    plt.plot(lambds, acc, mark[k], label=label[alg])
    k += 1

plt.legend()
plt.xlabel("Arrival rate $\lambda$")
plt.ylabel("Acceptance ratio")
plt.savefig("acc_lambda.png")

plt.clf()
k = 0
for alg, rtc in rtcs.items():
    plt.plot(lambds, rtc, mark[k], label=label[alg])
    k += 1

plt.legend()
plt.xlabel("Arrival rate $\lambda$")
plt.ylabel("Revenue-to-cost ratio")
plt.savefig("rtc_lambda.png")

plt.clf()


accs = {"mcts": [], "uepso": [], "nrpa_true": [], "nrpa_false": [], "nepa_true": [], "nepa_false": [], "graphvine": []}
rtcs = {"mcts": [], "uepso": [], "nrpa_true": [], "nrpa_false": [], "nepa_true": [], "nepa_false": [], "graphvine": []}

tailles = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

for i in tailles:
    dir = "Imv_taille:{}/".format(i)
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
            accs[alg].append(acc)
            rtcs[alg].append(rtc)

k = 0
for i in range(len(tailles)):
    tailles[i] = (7 + 13) / 2 + i
for alg, acc in accs.items():
    plt.plot(tailles, acc, mark[k], label=label[alg])
    k += 1

plt.legend()
plt.xlabel("Mean number of nodes")
plt.ylabel("Acceptance ratio")
plt.savefig("acc_taille.png")

plt.clf()

k = 0
for alg, rtc in rtcs.items():
    plt.plot(tailles, rtc, mark[k], label=label[alg])
    k += 1

plt.legend()
plt.xlabel("Mean number of nodes")
plt.ylabel("Revenue-to-cost ratio")
plt.savefig("rtc_taille.png")

plt.clf()


accs = {"mcts": [], "uepso": [], "nrpa_true": [], "nrpa_false": [], "nepa_true": [], "nepa_false": [], "graphvine": []}
rtcs = {"mcts": [], "uepso": [], "nrpa_true": [], "nrpa_false": [], "nepa_true": [], "nepa_false": [], "graphvine": []}

res = [-5, -10, -15, -17, -20, -22, -25, -27, -30]

for i in res:
    dir = "Imv_ressources:{}/".format(i)
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
            accs[alg].append(acc)
            rtcs[alg].append(rtc)

ressources = []
for i in res:
    ressources.append(75+i)

print(ressources)
print(accs["mcts"])
k = 0
for alg, acc in accs.items():
    plt.plot(ressources, acc, mark[k], label=label[alg])
    k += 1

plt.legend()
plt.xlabel("Mean number of resources")
plt.ylabel("Acceptance ratio")
plt.savefig("acc_resources.png")

plt.clf()
k = 0
for alg, rtc in rtcs.items():
    plt.plot(ressources, rtc, mark[k], label=label[alg])
    k += 1

plt.legend()
plt.xlabel("Mean number of resources")
plt.ylabel("Revenue-to-cost ratio")
plt.savefig("rtc_resources.png")

plt.clf()