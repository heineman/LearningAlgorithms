"""
Timing Results for chapter 7.

Executing Floyd-Warshall on Massachusetts Highway is costly since it is an O(N^3)
algorithm and the graph has 2305 vertices. An alternative is to use a technique
called "Chained Dijkstra's", where multiple invocations of Dijkstra's single-source
shortest path are used, one for each vertex, v, to find the best computed shortest path
from that vertex.

Perform Floyd-Warshall on MA highway data.
This might take awhile
start (42.045357, -70.214707) to end (42.539347, -73.341637) in longest shortest distance 251.43114701935508 in time 1334.837 seconds
start (42.045357, -70.214707) to end (42.539347, -73.341637) in longest shortest distance 251.4311470193551 in time 7.694 seconds

now compute same results with chained Dijkstra
start (42.045357, -70.214707) to end (42.539347, -73.341637) in longest shortest distance 251.4311470193551 in time 73.632 seconds

The first result above takes about twenty minutes. Using the chained approach, the
second result (implemented by networkx as all_pairs_dijkstra_path_length) takes
significantly faster. This is because Floyd-Warshall is O(V^3) while Chained
Dijkstra's is O(V * (V+E) * log V) and since the graph is sparse, E is on the
order of V, leading to an overall classification of O(V^2 * log V) which handily
beats O(V^3).

The third approach is native Python code implementing Chained Dijkstra's, and this
native code outperforms Floyd-Warshall handily, though the networkx implementation
is still better, which is the reason for using Networkx in the first place.

"""
import time

def floyd_warshall_highway():
    """Generate Floyd-Warshall results with MA highway data."""
    from ch07.tmg_load import tmg_load, highway_map
    from ch07.dependencies import plt_error

    if not plt_error:
        (G, positions, _) = tmg_load(highway_map())
        from networkx.algorithms.shortest_paths.dense import floyd_warshall
        print('This might take awhile')
        start_fw_time = time.time()
        dist_to = floyd_warshall(G, weight='weight')
        longest_so_far = 0
        start = -1
        end = -1
        for i in range(G.number_of_nodes()):
            for j in range(i+1,G.number_of_nodes()):
                if dist_to[i][j] > longest_so_far:
                    longest_so_far = dist_to[i][j]
                    start = i
                    end = j
        end_fw_time = time.time()
        print('start {} to end {} in longest shortest distance {} in time {:.3f} seconds'
              .format(positions[start], positions[end], longest_so_far, end_fw_time-start_fw_time))

        # so much faster since graph is sparse
        from networkx.algorithms.shortest_paths.weighted import all_pairs_dijkstra_path_length
        start_time = time.time()
        dist_to = dict(all_pairs_dijkstra_path_length(G))

        longest_so_far = 0
        start = -1
        end = -1
        for i in range(G.number_of_nodes()):
            for j in range(i+1,G.number_of_nodes()):
                if dist_to[i][j] > longest_so_far:
                    longest_so_far = dist_to[i][j]
                    start = i
                    end = j
        end_time = time.time()
        print('start {} to end {} in longest shortest distance {} in time {:.3f} seconds'
              .format(positions[start], positions[end], longest_so_far, end_time-start_time))

def chained_dijkstra():
    """Generate Chained Dijkstra results with MA highway data."""
    from ch07.tmg_load import tmg_load, highway_map
    from ch07.dependencies import plt_error
    from ch07.single_source_sp import dijkstra_sp

    if not plt_error:
        (G, positions, _) = tmg_load(highway_map())

        start_time = time.time()
        longest_so_far = 0
        start = -1
        end = -1
        for i in range(G.number_of_nodes()):
            (dist_to, _) = dijkstra_sp(G, i)
            for j in range(i+1, G.number_of_nodes()):
                if dist_to[j] > longest_so_far:
                    longest_so_far = dist_to[j]
                    start = i
                    end = j

        end_time = time.time()
        print('start {} to end {} in longest shortest distance {} in time {:.3f} seconds'
              .format(positions[start], positions[end], longest_so_far, end_time-start_time))

#######################################################################
if __name__ == '__main__':
    print('Perform Floyd-Warshall on MA highway data.')
    floyd_warshall_highway()
    print()

    print('now compute same results with chained Dijkstra')
    chained_dijkstra()
    print()
