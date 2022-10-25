package autocomplete;

import java.util.ArrayList;
import java.util.List;

public class SampleExample {
    public static void main(String[] args) {
        List<CharSequence> terms = new ArrayList<>();
        terms.add("alpha");
        terms.add("delta");
        terms.add("do");
        terms.add("cats");
        terms.add("dog");
        terms.add("dodgy");
        terms.add("pilot");
        terms.add("dog");
        terms.add("dodgy");

// Choose your Autocomplete implementation.
        Autocomplete autocomplete = new TreeSetAutocomplete();
        autocomplete.addAll(terms);

        Autocomplete autocompleteSS = new SequentialSearchAutocomplete();
        autocompleteSS.addAll(terms);

        Autocomplete autocompleteBS = new BinarySearchAutocomplete();
        autocompleteBS.addAll(terms);

        Autocomplete autocompleteTS = new TernarySearchTreeAutocomplete();
        autocompleteTS.addAll(terms);


// Choose your prefix string.
        CharSequence prefix = "do";
        List<CharSequence> matches = autocomplete.allMatches(prefix);
        for (CharSequence match : matches) {
            System.out.println(match);
        }
        System.out.println();

        List<CharSequence> matchesSS = autocompleteSS.allMatches(prefix);
        for (CharSequence matchSS : matchesSS) {
            System.out.println(matchSS);
        }
        System.out.println();

        List<CharSequence> matchesBS = autocompleteBS.allMatches(prefix);
        for (CharSequence matchBS : matchesBS) {
            System.out.println(matchBS);
        }
        System.out.println();

        List<CharSequence> matchesTS = autocompleteTS.allMatches(prefix);
        for (CharSequence matchTS : matchesTS) {
            System.out.println(matchTS);
        }
    }
}
