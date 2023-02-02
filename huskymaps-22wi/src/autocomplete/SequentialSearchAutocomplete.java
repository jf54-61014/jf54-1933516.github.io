package autocomplete;

import java.util.*;
import java.util.stream.Collectors;

/**
 * Sequential search implementation of the {@link Autocomplete} interface.
 *
 * @see Autocomplete
 */
public class SequentialSearchAutocomplete implements Autocomplete {
    /**
     * {@link List} of added autocompletion terms.
     */
    private final List<CharSequence> terms;

    /**
     * Constructs an empty instance.
     */
    public SequentialSearchAutocomplete() {
        this.terms = new ArrayList<>();
    }

    @Override
    public void addAll(Collection<? extends CharSequence> terms) {
        // TODO: Replace with your code
        this.terms.addAll(terms);
    }

    @Override
    public List<CharSequence> allMatches(CharSequence prefix) {
        // TODO: Replace with your code
        List<CharSequence> result = new ArrayList<>();
        if (prefix == null || prefix.length() == 0) {
            return result;
        }
        for (CharSequence term : this.terms) {
            if (Autocomplete.isPrefixOf(prefix, term)) {
                if (!result.contains(term)) {
                    result.add(term);
                }
            }
        }
        return result;
    }
}
