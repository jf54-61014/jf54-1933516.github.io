package minpq;

import java.util.*;

/**
 * Optimized binary heap implementation of the {@link ExtrinsicMinPQ} interface.
 *
 * @param <T> the type of elements in this priority queue.
 * @see ExtrinsicMinPQ
 */
public class OptimizedHeapMinPQ<T> implements ExtrinsicMinPQ<T> {
    /**
     * {@link List} of {@link PriorityNode} objects representing the heap of item-priority pairs.
     */
    private final List<PriorityNode<T>> items;
    /**
     * {@link Map} of each item to its associated index in the {@code items} heap.
     */
    private final Map<T, Integer> itemToIndex;

    /**
     * Constructs an empty instance.
     */

    public OptimizedHeapMinPQ() {
        items = new ArrayList<>();
        items.add(null);
        itemToIndex = new HashMap<>();
    }

    @Override
    public void add(T item, double priority) {
        if (contains(item)) {
            throw new IllegalArgumentException("Already contains " + item);
        }
        // TODO: Replace with your code
        items.add(new PriorityNode<>(item, priority));
        //itemToIndex.put(item, item.hashCode());
        itemToIndex.put(item,items.indexOf(new PriorityNode<>(item, priority)));
        swim(size());
    }

    @Override
    public boolean contains(T item) {
        // TODO: Replace with your code
        return itemToIndex.containsKey(item);
    }

    @Override
    public T peekMin() {
        if (isEmpty()) {
            throw new NoSuchElementException("PQ is empty");
        }
        // TODO: Replace with your code
        return items.get(1).item();
    }

    @Override
    public T removeMin() {
        if (isEmpty()) {
            throw new NoSuchElementException("PQ is empty");
        }
        // TODO: Replace with your code
        T min = peekMin();
        swap(1, size());
        items.remove(size());
        sink(1);
        itemToIndex.remove(min);
        return min;
    }

    @Override
    public void changePriority(T item, double priority) {
        if (!contains(item)) {
            throw new NoSuchElementException("PQ does not contain " + item);
        }
        // TODO: Replace with your code
        int oldPri = itemToIndex.get(item);
        items.set(items.indexOf(new PriorityNode<>(item, 0)), new PriorityNode<>(item, priority));
        int index = items.indexOf(new PriorityNode<>(item, priority));
        if (priority > oldPri) {
            sink(index);
        } else {
            swim(index);
        }
        int newindex = items.indexOf(new PriorityNode<>(item, priority));
        itemToIndex.replace(item, oldPri, newindex);
        items.remove(new PriorityNode<>(item, 0));
        itemToIndex.remove(item);
        add(item, priority);
    }

    @Override
    public int size() {
        // TODO: Replace with your code
        return items.size()-1;
    }

    private static int parent(int index) {
        return index / 2;
    }

    private static int left(int index) {
        return index * 2;
    }

    private static int right(int index) {
        return left(index) + 1;
    }

    private boolean accessible(int index) {
        return 1 <= index && index <= size()-1;
    }

    private int min(int index1, int index2) {
        if (!accessible(index1) && !accessible(index2)) {
            return 0;
        } else if (accessible(index1) && (!accessible(index2)
                || items.get(index1).priority() - items.get(index2).priority() < 0)) {
            return index1;
        } else {
            return index2;
        }
    }

    private void swap(int index1, int index2) {
        PriorityNode<T> temp = items.get(index1);
        items.set(index1, items.get(index2));
        items.set(index2, temp);
    }

    private void swim(int index) {
        int parent = parent(index);
        while (accessible(parent) && items.get(index).priority()-items.get(parent).priority() < 0) {
            swap(index, parent);
            index = parent;
            parent = parent(index);
        }
    }

    private void sink(int index) {
        int child = min(left(index), right(index));
        while (accessible(child) && items.get(index).priority() - items.get(child).priority() > 0) {
            swap(index, child);
            index = child;
            child = min(left(index), right(index));
        }
    }
    /*
    public OptimizedHeapMinPQ() {
        items = new ArrayList<>();
        items.add(null);
        itemToIndex = new HashMap<>();
    }

    @Override
    public void add(T item, double priority) {
        if (contains(item)) {
            throw new IllegalArgumentException("Already contains " + item);
        }
        // TODO: Replace with your code
        items.add(new PriorityNode<>(item, priority));
        itemToIndex.put(item, items.indexOf(new PriorityNode<>(item, priority)));
        swim(items.size()-1);
    }

    @Override
    public boolean contains(T item) {
        // TODO: Replace with your code
        return itemToIndex.containsKey(item);
    }

    @Override
    public T peekMin() {
        if (isEmpty()) {
            throw new NoSuchElementException("PQ is empty");
        }
        // TODO: Replace with your code
        return items.get(1).item();
    }

    @Override
    public T removeMin() {
        if (isEmpty()) {
            throw new NoSuchElementException("PQ is empty");
        }
        // TODO: Replace with your code
        T min = peekMin();
        System.out.println("min:  " +min);
        swap(1, size());
        System.out.println(items);
        items.remove(size());

        sink(1);
        System.out.println(items);
        itemToIndex.remove(min);
        System.out.println("-----------");
        return min;
    }

    @Override
    public void changePriority(T item, double priority) {
        if (!contains(item)) {
            throw new NoSuchElementException("PQ does not contain " + item);
        }
        // TODO: Replace with your code
        int oldIndex = itemToIndex.get(item);
        System.out.println("Change P:    ");
        System.out.println(oldIndex);
        double oldPri = items.get(oldIndex).priority();
        System.out.println(oldPri);

        //items.set(items.indexOf(new PriorityNode<>(item, 0)), new PriorityNode<>(item, priority));
        //int index = items.indexOf(new PriorityNode<>(item, priority));
        //swim(items.indexOf(new PriorityNode<>(item, priority)));
        //sink(items.indexOf(new PriorityNode<>(item, priority)));
        /*if (priority > oldPri) {
            sink(items.indexOf(new PriorityNode<>(item, 0)));
        } else {
            swim(items.indexOf(new PriorityNode<>(item, 0)));
        }
        itemToIndex.remove(new PriorityNode<>(item, oldIndex));
        itemToIndex.put(item, items.indexOf(new PriorityNode<>(item, priority)));
        items.remove(new PriorityNode<>(item, oldPri));
        itemToIndex.remove(item);
    add(item, priority);
}

    @Override
    public int size() {
        // TODO: Replace with your code
        return items.size()-1;
    }
     */
}
