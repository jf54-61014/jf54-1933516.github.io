package graphs.shortestpaths;

import graphs.Edge;
import graphs.Graph;

import java.util.*;

/**
 * Topological sorting implementation of the {@link ShortestPathSolver} interface for <b>directed acyclic graphs</b>.
 *
 * @param <V> the type of vertices.
 * @see ShortestPathSolver
 */
public class ToposortDAGSolver<V> implements ShortestPathSolver<V> {
    private final Map<V, Edge<V>> edgeTo;
    private final Map<V, Double> distTo;

    /**
     * Constructs a new instance by executing the toposort-DAG-shortest-paths algorithm on the graph from the start.
     *
     * @param graph the input graph.
     * @param start the start vertex.
     */
    public ToposortDAGSolver(Graph<V> graph, V start) {
        this.edgeTo = new HashMap<>();
        this.distTo = new HashMap<>();
        Set<V> visited = new HashSet<>();
        List<V> result = new ArrayList<>();
        // There may be more than 1 connected component...
        // So run the algorithm from every possible start.
        dfsPostOrder(graph, start, visited, result);
        // Reverse the DFS postorder.
        Collections.reverse(result);
        edgeTo.put(start, null);
        distTo.put(start, 0.0);
        for (V from : result) {
            for (Edge<V> e : graph.neighbors(from)) {
                V to = e.to;
                double oldDist = distTo.getOrDefault(to, Double.POSITIVE_INFINITY);
                double newDist = distTo.get(from) + e.weight;
                if (newDist < oldDist) {
                    edgeTo.put(to, e);
                    distTo.put(to, newDist);
                }
            }
        }
    }

    /**
     * Recursively adds nodes from the graph to the result in DFS postorder from the start vertex.
     *
     * @param graph   the input graph.
     * @param start   the start vertex.
     * @param visited the set of visited vertices.
     * @param result  the destination for adding nodes.
     */
    private void dfsPostOrder(Graph<V> graph, V start, Set<V> visited, List<V> result) {
        visited.add(start);
        for (Edge<V> neighbor : graph.neighbors(start)) {
            if (!visited.contains(neighbor.to)) {
                dfsPostOrder(graph, neighbor.to, visited, result);
            }
        }
        // Postorder: Add start after visiting all the neighbors.
        result.add(start);
    }

    @Override
    public List<V> solution(V goal) {
        List<V> path = new ArrayList<>();
        V curr = goal;
        path.add(curr);
        while (edgeTo.get(curr) != null) {
            curr = edgeTo.get(curr).from;
            path.add(curr);
        }
        Collections.reverse(path);
        return path;
    }
}
