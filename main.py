from mathy import *
from xkmodn import *


def print_information(N: int):
    print(f'N={N}')
    print(f'Units: {units(N)}')
    print(f'Primitive roots: {primitiveRoots(N)}')
    print(f'Inverses: {inverses(N)}')
    print(f'Orders: {orders(N)}')

def investigate_fixing_of_nonprime_n(N):
    print(f'N={N}')
    print('   '+' '.join([str(k) for k in range(1,N)]))
    for k_1 in range(1,N):
        for k_2 in range(1,N):
            if k_2 <= k_1: continue
            o_1 = order(k_1, N)
            o_2 = order(k_2, N)

            G = createGraph([k_1,k_2], N)
            G_1 = createGraph(k_1, N)
            G_2 = createGraph(k_2, N)

            # singlePlot(G)
            fix_num = fixing_number(G)
            # print(k_1, k_2)
            
            print(f'{k_1}, {k_2}: {fixing_number(G_1)}, {fixing_number(G_2)}; {fix_num}')

# Investigating n=p^t
def investiate_primepower_n():
    print(primitiveRoots(3))
    print(primitiveRoots(9))
    print(orders(27))
    print(primitiveRoots(27))
    multiPlot([1,2,3,4,5,6,7,8],[3,9,27])
    multiPlot([1,2,3,4,5,6,7,8],[3,9,27])

def investigating_power2_n(N):
    print(inverses(N))
    multiPlot([[2, 3], [2, 4], [2, 5], [2, 6]], [N])
    multiPlot([[3, 4],[3, 5],[3, 6]], [N])

    G = createGraph([6,10], N)
    print(fixing_number_set(G))
    singlePlot(G)

    multiPlot([1,2,3,4,5,6,7,8],[2,4,8,16])

#Investigating k_1+k_2=n
def investigating_antidiagonal():
    #N = 7
    # multiPlot([3,4,[3,4],2,5,[2,5],1,6,[1,6]],[7])

    # N = 11
    print_information(N)
    multiPlot([3,8,[3,8],2,9,[2,9]],[11])
    multiPlot([4,7,[4,7],5,6,[5,6]],[11])

    # N = 8
    multiPlot([1,7,[1,7],2,6,[2,6],3,5,[3,5]],[8])

    # N = 24
    # print(units(N))
    # print('5,19',fixing_number(createGraph([5,19],N)))
    # print('7,17',fixing_number(createGraph([7,17],N)))
    # print('11,13',fixing_number(createGraph([11,13],N)))

def compare_circulant_fixing(N):
    inv = inverses(N)
    print(f'N={N}')
    print('fix(G), simple circulant fix(G)')
    print('We now know that there exist some automorphism groups more complicated than Z_d and D_d for individual circulants.')
    print('   '+' '.join([f' {k} ' for k in range(1,N)]))
    for k_1 in range(1,N):
        fix_nums = [f'{k_1}:']
        for k_2 in range(1,N):
            if k_2 <= k_1:
                fix_nums.append(' - ')
            elif k_1 == 1 and N > 13 and k_2 == N//2:
                fix_nums.append('X')
            elif k_1 == 1 and N > 13 and k_2 == N - 1:
                fix_nums.append('X')
            else:
                G = createGraph([k_1,k_2], N)
                fix_num = fixing_number_set(G)[0]

                oK_1 = order(k_1,N)
                oK_2 = order(k_2,N)
                assert oK_1 is not None and oK_2 is not None

                circ_fix_num = None

                if divides(oK_1, oK_2):
                    circ_fix_num = (N-1) // oK_2
                elif divides(oK_2, oK_1):
                    circ_fix_num = (N-1) // oK_1

                if inv[k_1] == k_2:
                    circ_fix_num = 2 * (N-1) // oK_1

                fix_nums.append(f'{fix_num},{circ_fix_num if circ_fix_num is not None else 'N'}')

        print(' '.join(fix_nums))   


N=11
print_information(N)

# multiPlot([3,5,[3,5], 4,5,[4,5], 9],[N])
# multiPlot([[2,2**8], [2,2**9], [2, 1]],[N])


# print(automorphisms(createGraph([3,8],11)))
# print(len(automorphisms(createGraph([3,8],11))))
# print(fixing_number_set(createGraph([3,8],11)))
singlePlotInteractive(createGraph([3,8],11))