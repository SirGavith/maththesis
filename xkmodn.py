# x k mod n ; k is the multiplier
import networkx as nx
import matplotlib.pyplot as plt
import netgraph
# from itertools import permutations
# import math

from mathy import units

Ks = [2,3,4,5,6,7,8,9]
# Ns = [1,4,8,9,10,12,16,18,20] #nonsquarefree nums
# Ns = [1,2,3,5,7,11,13,17] #primes
Ns = [3,5,15] #n

Ks = [1,2,3,4,5]
Ns = [3,5,6,15] #n

def createGraph(k: int | list[int], n: int) -> nx.MultiDiGraph:
    G = nx.MultiDiGraph()
    G.add_nodes_from(range(0,n))

    if isinstance(k, int): k = [k]

    for k_i in k:
        def alpha_k_i(x):
            return x * k_i % n
        for x in range(0,n):
            G.add_edge(x, alpha_k_i(x), k_value=k_i)
    G.graph['k_values'] = k
    G.graph['n'] = n
    G.graph['N'] = n
    return G

def get_graph_nodes_units_colors(G: nx.MultiDiGraph):
    u = units(G.graph['n'])
    return ['red' if x in u else 'blue' for x in range(G.graph['n'])]

def get_graph_nodes_units_colormap(G: nx.MultiDiGraph):
    u = units(G.graph['n'])
    nodes_colormap = {}
    for n in G.nodes():
        nodes_colormap[n] = 'gray' if n in u else 'white'
    return nodes_colormap

def get_graph_edges_colormap(G: nx.MultiDiGraph):
    color_map = {}
    colors = ['blue', 'orange', 'green', 'red', 'white']
    for i,k in enumerate(G.graph['k_values']):
        color_map[k] = colors[i % len(colors)] 

    edges_colormap = {}
    for u,v,k in G.edges.data('k_value'):
        edges_colormap[(u,v)] = color_map[k]
    return edges_colormap

def singlePlot(G: nx.MultiDiGraph):
    plt.plot()
    colors = get_graph_nodes_units_colors(G)
    nx.draw(G, with_labels=True, font_color='white', node_color=colors)
    plt.show()

def singlePlotInteractive(G: nx.MultiDiGraph):
    plt.plot()
    nodes_color_map = get_graph_nodes_units_colormap(G)
    edges_color_map = get_graph_edges_colormap(G)

    interactivegraph = netgraph.InteractiveGraph(createGraph([3,8],11), node_labels=True, arrows=True,
                                                 node_color=nodes_color_map, edge_color=edges_color_map)

    plt.show()

def multiPlot(Ks: list[int | list[int]], Ns: list[int]):
    rows = len(Ns)
    cols = len(Ks)

    if rows == 1 and cols == 1:
        G = createGraph(Ks[0], Ns[0])
        singlePlot(G)
        return

    fig, axs = plt.subplots(rows, cols, constrained_layout=True)
    for row, n in enumerate(Ns):
        for col, k in enumerate(Ks):
            if rows != 1:
                axs[row,col].set_xticklabels([])
                axs[row,col].set_yticklabels([])
                plt.subplot2grid((rows, cols), (row, col))
            else:
                axs[col].set_xticklabels([])
                axs[col].set_yticklabels([])
                plt.subplot2grid((rows, cols), (row, col))

            # first_k = k if isinstance(k, int) else k[0]
            # color = ['green','blue','orange','purple', 'red'][(n+first_k)%5]
            G = createGraph(k, n)
            color_map = get_graph_nodes_units_colors(G)
            nx.draw(G, with_labels=True, font_color='white', node_color=color_map)
            # axs[row,col].set_axis_off()

            # iscoprime = math.gcd(n,k) == 1
            # numComponents = len([*nx.weakly_connected_components(G)])
            # dividesn1 = (n-1) % (numComponents-1) if numComponents != 1 else '-'
            # axs[row,col].set_title(f'{math.gcd(n,k)} {numComponents} {dividesn1}')

    fig.canvas.draw()
    # Row labels
    if rows != 1:
        for row in range(rows):
            ax = axs[row, 0]  # leftmost column
            pos = ax.get_position()
            fig.text(
                x=pos.x0 + 0.01,
                y=(pos.y0+pos.y1)/2,
                s=f'n= {Ns[row]}',
                ha='right',
                va='center',
                fontsize=12,
            )
    # Column labels
        for col in range(cols):
            ax = axs[0, col]  # top row
            pos = ax.get_position()
            fig.text(
                x=(pos.x0+pos.x1)/2,
                y=pos.y1-0.01,
                s=f'k = {Ks[col]}',
                fontsize=12
            )
    if rows == 1:
        for i, ax in enumerate(axs):
            ax.set_title(f'G({Ks[i]}, {Ns[0]})')



def automorphisms(graph: nx.MultiDiGraph) -> list[dict[int,int]]:
    return list(nx.algorithms.isomorphism.MultiDiGraphMatcher(graph, graph).isomorphisms_iter())

def fixing_number_set(graph: nx.MultiDiGraph, max_fix_number = 15) -> tuple[int | None, set[int] | None]:
    N = graph.number_of_nodes()
    all_auts = automorphisms(graph)
    if len(all_auts) == 1:
        return 0, set()

    # Starting at 1 and up to max_fix_number, 
    # recursively attempts to fix that many nodes.
    # Could probably be optimized to prioritize nodes that
    # make the automorphism number go down more in later steps.

    for trial_fix_num in range(1, max_fix_number):

        def recurse(auts: list[dict[int,int]], trial_fix_num_remaining: int, fixed: set[int]):
            for v in range(N):
                if v in fixed: continue
                newfixed = fixed.union(set([v]))
                # find automorphisms that fix x
                stabX = [a for a in auts if a[v] == v]

                if len(stabX) == 1: return trial_fix_num, newfixed
                elif trial_fix_num_remaining > 1:
                    fixing_n, fixing_s = recurse(stabX, trial_fix_num_remaining - 1, newfixed)
                    if fixing_n is not None:
                                return fixing_n, fixing_s
            # Failed to find fixing set of size trial_fix_num
            return None, None
        fixing_n, fixing_s = recurse(all_auts, trial_fix_num, set())
        if fixing_n is not None:
            return fixing_n, fixing_s
        
    #Fixing number greater than max_fix_number
    return None, None

# Greedy fixing number algorithm: repeatedly chooses to fix the vertex with
#   the smallest stabilizer until only the trivial automorphism remains.
# Returns the greedy fixing number and a fixing set
def greedy_fixing_number_set(graph: nx.MultiDiGraph) -> tuple[int,set[int]]:
    N = graph.number_of_nodes()
    auts = automorphisms(graph)
    fixed = set()
    unfixed = set(range(N))

    while len(auts) > 1:

        stabilizers = ((v, stabV := [a for a in auts if a[v] == v], len(stabV)) for v in unfixed)
        min_stab_v, min_stab, min_stab_l = min(stabilizers, key = lambda v_stabV_l: v_stabV_l[2])

        auts = min_stab
        fixed.add(min_stab_v)
        unfixed.remove(min_stab_v)
    return len(fixed), fixed

# Checks the well-definedness of the greedy fixing algorithm by recursively 
#  ensuring the fixing numbers of all vertices with minimal stabilizer size are equal
#  (implying that it does not matter which minimal stabilizing vertex you pick).
# Returns the greedy fixing number and a list of all found fixing sets
def all_greedy_fixing_numbers(graph: nx.MultiDiGraph) -> tuple[int, list[set[int]]]:

    def recurse(auts, fixed, unfixed) -> tuple[int, list[set[int]]]:
        if len(auts) == 1:
            return len(fixed), [fixed]

        stabilizers = [(v, stabV := [a for a in auts if a[v] == v], len(stabV)) for v in unfixed]

        minimal_stab_size = min(stabilizers, key = lambda v_stabV_l: v_stabV_l[2])[2]

        branches = [recurse(stab, fixed.union(set([v])), unfixed.difference(set([v])))
         for v, stab, l in [s for s in stabilizers if s[2] == minimal_stab_size]]

        for fixing_number_i, fixing_set_i in branches: 
            #Check that the greedy fixing number is well-defined.
            assert fixing_number_i == branches[0][0]

        return branches[0][0], [fixing_set_i for branch in branches for fixing_set_i in branch[1]]

    N = graph.number_of_nodes()
    auts = automorphisms(graph)
    fixed = set()
    unfixed = set(range(N))

    return recurse(auts, fixed, unfixed)

def fixing_number(graph: nx.MultiDiGraph, max_fix_number = 15):
    return fixing_number_set(graph, max_fix_number)[0]

def printFixingNumbersFor2KValuesTable(N):
    print(f'N={N}')
    print('   '+' '.join([str(k) for k in range(1,N)]))
    for k_1 in range(1,N):
        fix_nums = [f'{k_1}:']
        for k_2 in range(1,N):
            if k_2 <= k_1:
                fix_nums.append('-')
            elif k_1 == 1 and N > 13 and k_2 == N//2:
                fix_nums.append('X')
            elif k_1 == 1 and N > 13 and k_2 == N - 1:
                fix_nums.append('X')
            else:
                G = createGraph([k_1,k_2], N)
                # singlePlot(G)
                fix_num = fixing_number_set(G)[0]
                # print(k_1, k_2)
                fix_nums.append(str(fix_num))

        print(' '.join(fix_nums))   

def printFixingNumbersFor2KValuesTables(maxN = 15):
    for N in range(2, maxN):
        printFixingNumbersFor2KValuesTable(N)
        print()
