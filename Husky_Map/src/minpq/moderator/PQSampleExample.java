package minpq.moderator;

import minpq.*;

public class PQSampleExample {
    public static void main(String[] args) {
        //ExtrinsicMinPQ<String> pq = new DoubleMapMinPQ<>();
        //ExtrinsicMinPQ<String> pq = new UnsortedArrayMinPQ<>();
        //ExtrinsicMinPQ<String> pq = new HeapMinPQ<>();
        ExtrinsicMinPQ<String> pq = new OptimizedHeapMinPQ<>();


        pq.add("4", 4.0);
        pq.add("2", 2.0);
        pq.add("3", 3.0);
        pq.add("1", 1.0);
        pq.add("5", 5.0);
        pq.add("6", 6.0);

// Call methods to evaluate behavior.
        //pq.changePriority("1", 11.0);
        //pq.changePriority("2", 12.0);
        //pq.changePriority("1", 7.0);
        //pq.changePriority("4", 8.0);
        pq.changePriority("3", 99.0);
        pq.changePriority("3", 70.0);
        pq.changePriority("6", 19.0);

        //System.out.println(pq.size())
        while (!pq.isEmpty()) {
            System.out.println(pq.removeMin());
        }
    }
}
