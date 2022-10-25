package autocomplete;

import java.util.*;

/*import java.util.ArrayList;
import java.util.Collection;
import java.util.List;*/
/**
 * Binary search implementation of the {@link Autocomplete} interface.
 *
 * @see Autocomplete
 */
public class BinarySearchAutocomplete implements Autocomplete {
    /**
     * {@link List} of added autocompletion terms.
     */
    private final List<CharSequence> terms;

    /**
     * Constructs an empty instance.
     */
    public BinarySearchAutocomplete() {
        this.terms = new ArrayList<>();
    }

    @Override
    public void addAll(Collection<? extends CharSequence> terms) {
        // TODO: Replace with your code
        this.terms.addAll(terms);
        Collections.sort(this.terms, CharSequence::compare);
    }

    @Override
    public List<CharSequence> allMatches(CharSequence prefix) {
        // TODO: Replace with your code
        List<CharSequence> result = new ArrayList<>();
        if (prefix == null || prefix.length() == 0) {
            return result;
        }

        int i = Collections.binarySearch(terms, prefix, CharSequence::compare);
        int start;
        if (i >= 0) {
            start = i;
        } else {
            start = -(i+1);
        }
        for (int k = start; k < terms.size(); k++ ) {
            CharSequence word = terms.get(k).subSequence(0, prefix.length());
            if (CharSequence.compare(prefix, word) == 0) {
                if (!result.contains(terms.get(k))) {
                    result.add(terms.get(k));
                }
            } else {
                break;
            }
        }
        return result;
    }
}