from matplotlib import pyplot as plt
import json
import numpy as np
from vne_lib.graph_classes import SN
import networkx as nx
from scipy.stats import pearsonr
from statistics import mean
def file_to_SN(file):
    with open(file) as json_file:
        data = json.load(json_file)

    sn = SN()
    G = nx.Graph()
    for n in data["nodes_cap"]:
        G.add_node(int(n), cpu_max = data["nodes_cap"][n], cpu_used=0)

    for e in data['edges']:
        u = int(e['e'][0])
        v = int(e['e'][1])
        w = int(e['weight'])
        G.add_edge(u, v, BW_max = w, BW_used = 0)
    
    sn.graph = G
    sn.number_of_edges = len(data['edges'])
    sn.number_of_nodes = len(data['nodes_cap'])

    return sn

accs = {"mcts": [], "uepso": [], "nrpa_true": [], "nrpa_false": [], "nepa_true": [], "nepa_false": [], "graphvine": []}
rtcs = {"mcts": [], "uepso": [], "nrpa_true": [], "nrpa_false": [], "nepa_true": [], "nepa_false": [], "graphvine": []}

mark = ['--o', '--v', '-.+', '-.s', '-p', '-*', ':h']


for i in ['Intellifibe', 'Latnet', 'VtlWavenet2011', 'Syrin', 'Globenet', 'Forthnet', 'GtsCe', 'Ulaknet', 'Sinet', 'Internode', 'UsCarrie', 'RedBeste', 'Missouri', 'Interoute', 'Columbus', 'Garr201201', 'Cogentco', 'Deltaco', 'AsnetA', 'Switc', 'Uninett2011', 'Ion', 'Pern', 'Esnet', 'Colt', 'TataNld']:
    dir = "real:{}/".format(i)
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


labels = ['Intellifibe', 'Latnet', 'VtlWavenet2011', 'Syrin', 'Globenet', 'Forthnet', 'GtsCe', 'Ulaknet', 'Sinet', 'Internode', 'UsCarrie', 'RedBeste', 'Missouri', 'Interoute', 'Columbus', 'Garr201201', 'Cogentco', 'Deltaco', 'AsnetA', 'Switc', 'Uninett2011', 'Ion', 'Pern', 'Esnet', 'Colt', 'TataNld']
x = np.arange(len(labels))  # the label locations

#all_dist = []
scores = []
scores2 = []
for graph in labels:
    s = file_to_SN(f"real:{graph}/instance/test_network")
    l = nx.shortest_path_length(s.graph)
    all_dist = []
    while(True):
        try:
            n = next(l)
            n = list(n[1].values())
            n.remove(0)
            all_dist += n
        except:
            break
    
    #scores.append(max(all_dist))
    #bc = list(nx.betweenness_centrality(s.graph, weight="BW_max"))
    #scores.append(sum([max(bc) - b for b in bc]) / len(bc))
    
    #scores.append(np.quantile(all_dist, 0.75))
    #scores.append()
    
    #scores.append(nx.average_clustering(s.graph))
    #l = list(dict(s.graph.degree).values())
    #scores.append(np.std(l))
    scores.append(mean(all_dist))
    scores2.append(max(all_dist))

print("###############")
print(pearsonr(scores, scores2))

sort = np.argsort(scores)


print(np.array(scores)[sort])

for k in labels:
    with open(f"real:{k}/instance/test_network", "r") as f:
        data = json.load(f)
        scores.append (  data["m"] / ((data["n"] * (data["n"] - 1) ) / 2) )

for i in accs:
    accs[i] = np.array(accs[i])[sort]

labels = np.array(labels)[sort]
print(labels)
width = 1/8  # the width of the bars

fig, ax = plt.subplots()
fig.set_size_inches(18.5, 6)

rects1 = ax.bar(x - 2 * width, rtcs["mcts"], width, label='MaVEN-S')
rects2 = ax.bar(x - width, rtcs["uepso"], width, label='UEPSO')
rects3 = ax.bar(x + width, rtcs["nrpa_true"], width, label='NRPA-D')
rects4 = ax.bar(x , rtcs["nrpa_false"], width, label='NRPA')
rects5 = ax.bar(x + 3 * width, rtcs["nepa_true"], width, label='NEPA-D')
rects6 = ax.bar(x + 2 * width, rtcs["nepa_false"], width, label='NEPA')
rects7 = ax.bar(x - 3 * width, rtcs["graphvine"], width, label="GraphVine")

diff = []

for i in range(len(accs["nrpa_true"])):
    dep = accs["nrpa_false"][i]# + accs["mcts"][i] + accs["uepso"][i]
    arr = accs["nepa_true"][i]# + accs["nepa_false"][i]
    diff.append((arr - dep) / arr)

#ax.plot(x, diff, c="black")

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Revenue-to-cost ratio')
ax.set_xticks(x)
ax.set_xticklabels(labels)
#ax.legend()


fig.tight_layout()
plt.xticks(rotation=45)

print(pearsonr(diff, np.array(scores)[sort]))

plt.show()