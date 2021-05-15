"""Timing results for chapter 3.

Average search Times with separate chaining hashtables (time in ns)
       N       8,192      16,384      32,768      65,536     131,072     262,144     524,288    1,048,576    
      32       0.481       0.369       0.289       0.264       0.344       0.324       0.315       0.334    
      64       0.722       0.479       0.350       0.321       0.371       0.365       0.348       0.334    
     128       1.223       0.744       0.480       0.364       0.407       0.379       0.357       0.349    
     256       2.228       1.242       0.733       0.490       0.444       0.384       0.357       0.351    
     512       4.149       2.407       1.233       0.743       0.568       0.473       0.387       0.371    
   1,024       8.477       4.450       2.306       1.278       0.852       0.595       0.441       0.406    
   2,048      16.966       8.596       4.367       2.301       1.389       0.906       0.576       0.485    
   4,096      34.964      17.214       8.635       4.443       2.505       1.438       0.916       0.638    
   8,192      71.714      36.167      17.442       9.053       4.664       2.555       1.423       0.882    
  16,384     153.146      71.819      34.965      17.323       8.890       4.687       2.526       1.444    

Count how many times hashcode is computed (i.e., when % is invoked) on PUT.
Out of 900 attempts there were 126 failures

Statistics from the perfect hash on just a few words
G has 667596 entries.
a 0
aa 1
aah 2
aahed 3
aahing 4
aahs 5
aal 6
aalii 7
aaliis 8
aals 9

Compare performance of perfect hash with regular hashtable
       N      Linked     Perfect    
 321,129      0.3386      1.4224    


"""
import timeit
import random

from resources.english import english_words
from algs.table import DataTable, comma, SKIP
from ch03.perfect.generated_dictionary import perfect_hash, G

def time_results_linked(output=True, decimals=3):
    """Average time to find a key in growing hashtable_open."""

    sizes = [8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576]
    tbl = DataTable([8] + [8]*len(sizes), ['N'] + [comma(sz) for sz in sizes],
                    output=output, decimals=decimals)
    # Now start with M words to be added into a table of size N.
    # Start at 1000 and work up to 2000
    words = english_words()
    for num_to_add in [32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]:
        all_words = words[:num_to_add]

        line = [num_to_add]
        for size in sizes:
            time1 = min(timeit.repeat(stmt='''
table = Hashtable({})
for word in words:
    table.put(word, 99)'''.format(size), setup='''
from ch03.hashtable_linked import Hashtable
words={}'''.format(all_words), repeat=1, number=100))
            line.append(1000000*time1/size)
        tbl.row(line)
    return tbl

def probability_of_failure():
    """Produce report of failures resulting from collisions."""
    from ch03.months import key_array
    from ch03.hashtable import Hashtable

    failures = 0
    low = 100
    high = 1000
    for N in range(low, high):
        table = Hashtable(N)
        try:
            for day in key_array:
                table.put(day, 'ignore')
        except RuntimeError:
            failures += 1

    print('Out of', (high - low), 'attempts there were', failures, 'failures')

def run_access_trials(max_trials=100000, output=True, decimals=5):
    """Generate performance table for up to max_trials number of runs."""
    tbl = DataTable([10,10,10], ['Dict', 'Raw', 'BAS'], output=output, decimals=decimals)
    tbl.format('Dict', 'f')

    m1 = min(timeit.repeat(stmt='days_in_month[s_data[2]]',
           setup='from ch03.months import s_data, days_in_month', repeat=10, number=max_trials))

    m2 = min(timeit.repeat(stmt='days_mixed(s_data[2])',
            setup='from ch03.months import s_data, days_mixed', repeat=10, number=max_trials))

    m3 = min(timeit.repeat(stmt='days_bas(s_data[2])',
            setup='from ch03.months import s_data, days_bas', repeat=10, number=max_trials))
    tbl.row([m1,m2,m3])
    return tbl

def time_results_open(words, output=True, decimals=4):
    """Average time to find a key in growing hashtable_open."""
    sizes = [8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576]
    widths = [8] + [10] * len(sizes)
    headers = ['N'] + sizes
    tbl = DataTable(widths, headers, output=output, decimals=decimals)

    # Now start with N words to be added into a table of size M.
    # Start at 1000 and work up to 2000
    for num_to_add in [32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]:
        all_words = words[:num_to_add]

        arow = [num_to_add]
        for size in sizes:
            if num_to_add < size:
                m1 = min(timeit.repeat(stmt='''
table = Hashtable({})
for word in words:
    table.put(word, 99)'''.format(size), setup='''
from ch03.hashtable_open import Hashtable
words={}'''.format(all_words), repeat=1, number=100))
                arow.append((100000.0 * m1) / size)
            else:
                arow.append(SKIP)
        tbl.row(arow)
    return tbl

def simple_stats(words):
    """Generate stats on specific words from perfect hash structures."""
    print('G has',len(G),'entries. Here are the results on a few words:')
    for i in words:
        print(i, perfect_hash(i))

def compare_time(words, output=True, decimals=4):
    """Generate table of performance differences with linked hashtable and perfect hashing."""
    tbl = DataTable([8,8,8],['N', 'Linked', 'Perfect'], output=output, decimals=decimals)

    t_perfect = min(timeit.repeat(stmt='''
ht = HL()
for w in words:
    ht.put(w,w)''', setup='''
from ch03.hashtable_open_perfect import Hashtable as HL
words={}'''.format(words),
                repeat=3, number=5))/5

    t_linked = min(timeit.repeat(stmt='''
ht = HL(len(words))
for w in words:
    ht.put(w,w)''', setup='''
from ch03.hashtable_linked import Hashtable as HL
words={}'''.format(words),
                repeat=3, number=5))/5

    tbl.row([len(words), t_linked, t_perfect])
    return tbl

def check_for_duplicates():
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
    hash_values = {}
    for w in english_words():
        hc = hash(w)
        if hc in hash_values:
            print('clash on', w, 'and', hash_values[hc])
        hash_values[hc] = w
    print('Number of duplicate hashcodes found for dictionary:', len(hash_values))

#######################################################################
if __name__ == '__main__':
    print('Average search Times with separate chaining hashtables (time in ns)')
    time_results_linked()
    print()

    print('Count how many times hashcode is computed (i.e., when % is invoked) on PUT.')
    probability_of_failure()
    print()

    print('Statistics from the perfect hash on just a few words')
    ewords = english_words()
    simple_stats(ewords[:10])
    print()

    print('Compare performance of perfect hash with regular hashtable')
    random.shuffle(ewords)
    compare_time(ewords)
    print()

    print('Trying to find two words in the dictionary with the same hash value.')
    check_for_duplicates()
    print()
