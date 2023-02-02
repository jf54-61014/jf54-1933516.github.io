package minpq;

import java.util.*;

/**
 * {@link PriorityQueue} implementation of the {@link ExtrinsicMinPQ} interface.
 *
 * @param <T> the type of elements in this priority queue.
 * @see ExtrinsicMinPQ
 */
public class HeapMinPQ<T> implements ExtrinsicMinPQ<T> {
    /**
     * {@link PriorityQueue} storing {@link PriorityNode} objects representing each item-priority pair.
     */
    private final PriorityQueue<PriorityNode<T>> pq;

    /**
     * Constructs an empty instance.
     */
    public HeapMinPQ() {
        pq = new PriorityQueue<>(Comparator.comparingDouble(PriorityNode::priority));
    }

    @Override
    public void add(T item, double priority) {
        if (contains(item)) {
            throw new IllegalArgumentException("Already contains " + item);
        }
        // TODO: Replace with your code
        pq.add(new PriorityNode<>(item, priority));
    }

    @Override
    public boolean contains(T item) {
        // TODO: Replace with your code
        return pq.contains(new PriorityNode<>(item, 0));
    }

    @Override
    public T peekMin() {
        if (isEmpty()) {
            throw new NoSuchElementException("PQ is empty");
        }
        // TODO: Replace with your code
        PriorityNode<T> pair = pq.remove();
        pq.add(pair);
        return pair.item();
    }

    @Override
    public T removeMin() {
        if (isEmpty()) {
            throw new NoSuchElementException("PQ is empty");
        }
        // TODO: Replace with your code
        PriorityNode<T> pair = pq.remove();
        return pair.item();
    }

    @Override
    public void changePriority(T item, double priority) {
        if (!contains(item)) {
            throw new NoSuchElementException("PQ does not contain " + item);
        }
        // TODO: Replace with your code
        pq.remove(new PriorityNode<>(item, 0));
        pq.add(new PriorityNode<>(item, priority));
        /* PriorityNode<T> Node = new PriorityNode<>(item, priority);
        List<PriorityNode<T>> list = new ArrayList<>();
        int s = pq.size();
        for (int i = 0; i < s; i++){
            PriorityNode<T> pair = pq.remove();
            if (pair.equals(Node)) {
                list.add(Node);
            } else {
                list.add(pair);
            }
        }
        for (int i = 0; i < list.size(); i++) {
            pq.add(list.get(i));
        } */
    }

    @Override
    public int size() {
        // TODO: Replace with your code
        return pq.size();
    }
}
