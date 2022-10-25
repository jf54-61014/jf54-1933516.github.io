package minpq;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.NoSuchElementException;

/**
 * Unsorted array (or {@link ArrayList}) implementation of the {@link ExtrinsicMinPQ} interface.
 *
 * @param <T> the type of elements in this priority queue.
 * @see ExtrinsicMinPQ
 */
public class UnsortedArrayMinPQ<T> implements ExtrinsicMinPQ<T> {
    /**
     * {@link List} of {@link PriorityNode} objects representing the item-priority pairs in no specific order.
     */
    private final List<PriorityNode<T>> items;

    /**
     * Constructs an empty instance.
     */
    public UnsortedArrayMinPQ() {
        items = new ArrayList<>();
    }

    private ArrayList<Double> pri = new ArrayList<Double>();
    @Override
    public void add(T item, double priority) {
        if (contains(item)) {
            throw new IllegalArgumentException("Already contains " + item);
        }
        // TODO: Replace with your code
        items.add(new PriorityNode<>(item, priority));
    }

    @Override
    public boolean contains(T item) {
        // TODO: Replace with your code
        return items.contains(new PriorityNode<>(item, 1));
    }

    @Override
    public T peekMin() {
        if (isEmpty()) {
            throw new NoSuchElementException("PQ is empty");
        }
        // TODO: Replace with your code
        double min = items.get(0).priority();
        int index = 0;
        for (int i = 1; i < items.size(); i++) {
           if (items.get(i).priority() < min) {
               min = items.get(i).priority();
               index = i;
           }
        }
        return items.get(index).item();
    }
    @Override
    public T removeMin() {
        if (isEmpty()) {
            throw new NoSuchElementException("PQ is empty");
        }
        // TODO: Replace with your code
        T MinItem = peekMin();
        items.remove(new PriorityNode<>(MinItem, 0));
        return MinItem;
    }

    @Override
    public void changePriority(T item, double priority) {
        if (!contains(item)) {
            throw new NoSuchElementException("PQ does not contain " + item);
        }
        // TODO: Replace with your code
        items.set(items.indexOf(new PriorityNode<>(item, 0)), new PriorityNode<>(item, priority));
    }

    @Override
    public int size() {
        // TODO: Replace with your code
        return items.size();
    }
}