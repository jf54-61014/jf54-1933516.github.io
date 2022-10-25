package autocomplete;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Queue;

/**
 * Ternary search tree (TST) implementation of the {@link Autocomplete} interface.
 *
 * @see Autocomplete
 */
public class TernarySearchTreeAutocomplete implements Autocomplete {
    /**
     * The overall root of the tree: the first character of the first autocompletion term added to this tree.
     */
    private Node overallRoot;

    /**
     * Constructs an empty instance.
     */
    public TernarySearchTreeAutocomplete() {
        overallRoot = null;
    }

    @Override
    public void addAll(Collection<? extends CharSequence> terms) {
        // TODO: Replace with your code
        for (CharSequence term : terms) {
            if (!contains(term)) {
                overallRoot = put(overallRoot, term,0);
            }
        }
    }

    public boolean contains(CharSequence key) {
        if (key == null) {
            throw new NullPointerException("calls get() with null argument");
        } else if (key.length() == 0) {
            throw new IllegalArgumentException("key must have length >= 1");
        }
        Node x = get(overallRoot, key, 0);
        return x != null && x.isTerm;
    }

    // return subtrie corresponding to given key
    private Node get(Node x, CharSequence key, int d) {
        if (x == null) {
            return null;
        }
        char c = key.charAt(d);
        if (c < x.data) {
            return get(x.left, key, d);
        } else if (c > x.data) {
            return get(x.right, key, d);
        } else if (d < key.length() - 1) {
            return get(x.mid, key, d+1);
        } else {
            return x;
        }
    }

    private Node put(Node x, CharSequence key, int d) {
        char c = key.charAt(d);
        if (x == null) {
            x = new Node(c, false);
        }
        if (c < x.data) {
            x.left  = put(x.left, key, d);
        } else if (c > x.data) {
            x.right = put(x.right, key, d);
        } else if (d < key.length() - 1) {
            x.mid = put(x.mid, key, d+1);
        } else {
            x.isTerm= true;
        }
        return x;
    }


    @Override
    public List<CharSequence> allMatches(CharSequence prefix) {
        // TODO: Replace with your code
        if (prefix == null) {
            throw new IllegalArgumentException("calls keysWithPrefix() with null argument");
        } else if (prefix.length() == 0) {
            throw new IllegalArgumentException("prefix must have length >= 1");
        }
        List<CharSequence> result = new ArrayList<>();
        Node x = get(overallRoot, prefix, 0);
        if (x == null) {
            return result;
        }
        if (x.isTerm) {
            result.add(prefix);
        }
        collect(x.mid, new StringBuilder(prefix), result);
        return result;
    }

    // all keys in subtrie rooted at x with given prefix
    private void collect(Node x, StringBuilder prefix, List<CharSequence> result) {
        if (x == null) {
            return;
        }
        collect(x.left,  prefix, result);
        if (x.isTerm) {
            result.add(prefix.toString() + x.data);
        }
        collect(x.mid, prefix.append(x.data), result);
        prefix.deleteCharAt(prefix.length() - 1);
        collect(x.right, prefix, result);
    }


    /**
     * A search tree node representing a single character in an autocompletion term.
     */
    private static class Node {
        private final char data;
        private boolean isTerm;
        private Node left;
        private Node mid;
        private Node right;

        public Node(char data, boolean b) {
            this.data = data;
            this.isTerm = false;
            this.left = null;
            this.mid = null;
            this.right = null;
        }
    }
}
