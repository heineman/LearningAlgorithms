"""
Determine if there are any hash() clashes on the words in the English language.

Because Python uses 64-bit hashcodes the likelihood is tremendously small.
Also remember that Python now salts hash code values, so they are not the
same from one run to the next.

The Python code below finds no clashes on hash() values.

The following Java code finds 11 clashes::

    import java.book.*;
    public class EnglishClash {
        public static void main(String[] args) throws Exception {
            java.io.File f = new java.io.File("words.english.txt");
            Scanner sc = new Scanner(f);
            Hashtable<Integer,String> ht = new Hashtable<>();
            while (sc.hasNextLine()) {
                String s = sc.nextLine();
                int i = s.hashCode();
                if (ht.containsKey(i)) {
                    System.out.println("clash on " + s + " and " + ht.get(i));
                } else {
                    ht.put(i, s);
                }
            }
            sc.close();
        }
    }

The above code finds 11 clashes

    clash on hazardless and agarwal
    clash on hierarch and crinolines
    clash on isohel and epistolaries
    clash on kindergartener and acouasm
    clash on misused and horsemints
    clash on poised and dentinalgia
    clash on proselytized and nonguard
    clash on righto and buzzards
    clash on unapprehending and fineable
    clash on unheavenly and hypoplankton
    clash on variants and gelato
"""

from resources.english import english_words

def search_duplicate_hash(words):
    """Print out words in the English dictionary with same hash value."""
    hash_values = {}
    for w in words:
        hc = hash(w)
        if hc in hash_values:
            print('clash on', w, 'and', hash_values[hc])
        hash_values[hc] = w
    print('DONE', len(hash_values))

if __name__ == '__main__':
    search_duplicate_hash(english_words())
