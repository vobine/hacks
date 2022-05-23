#! /usr/bin/env python3

with open('bal.dot', 'wt') as balf:
    # Preamble
    print('digraph {', file=balf)
    print('    overlap=false;', file=balf)
    print('    splines=true;', file=balf)

    # First few nodes that don't quite fit the pattern
    print('    1 [style=filled, fillcolor=magenta, fontcolor=white];', file=balf);
    print('    2 -> 1;', file=balf)
    print('    3 [style=filled, fillcolor=cyan, fontcolor=black];', file=balf);
    print('    3 -> 1;', file=balf)
    print('    4 -> 2;', file=balf)

    # The rest of the nodes, that *do* fit the pattern
    for i in range(5, 100):
        bmod = i % 3
        athird = i // 3
        if 0 == bmod:
            print('    {0:d} [style=filled, fillcolor=cyan, fontcolor=black];'.format(i), file=balf);
        print('    {0:d} -> {1:d};'.format(i, athird), file=balf)
        if 0 != bmod:
            print('    {0:d} -> {1:d};'.format(i, athird+1), file=balf)

    # Appendix
    print('}', file=balf)
