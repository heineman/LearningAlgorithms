"""
Create a Hashtable of size 1023 and insert 512 randomly-selected words into this hashtable.

Represent the open addressing as an image of 2046 x 2 pixels using a filled rectangle to
represent an entry and an empty 2x2 space as an unused entry.

Now do the same for a linked list, this time representing.

Depends upon the 'png' module which can be installed here

  https://github.com/drj11/pypng

6423300 (1.0252860679090188, 4) (1.026213939875142, 5)
--     --                        --
642330 (1.2516152133638472, 7) (1.2516152133638472, 7) (1.4942163685333085, 38)
610213 (1.2631451123254402, 6) (1.2631451123254402, 6) (1.5548051624554358, 37)
579702 (1.276633506141703, 6) (1.276633506141703, 6) (1.615973097940311, 41)
550716 (1.2913300017125153, 7) (1.2913300017125153, 7) (1.6931203586941292, 44)
523180 (1.3049180327868852, 7) (1.3049180327868852, 7) (1.7968458580480438, 56)
497021 (1.323721451590304, 7) (1.323721451590304, 7) (1.9183161303379883, 70)
472169 (1.339573116622297, 8) (1.339573116622297, 8) (2.0616443261252004, 102)
448560 (1.3591051328756247, 7) (1.3591051328756247, 7) (2.25799822521134, 135)
426132 (1.1884701010384071, 6) (1.3757445549795277, 8) (2.52925443307957, 153)
404825 (1.1983902355487055, 5) (1.397714570392166, 8) (2.9141811841265395, 301)
384583 (1.2089642395653324, 6) (1.4186819858951008, 7) (3.509871872713403, 512)
365353 (1.2214873974436815, 7) (1.439406535581399, 8) (4.631924400230411, 458)
347085 (1.2310774835365, 7) (1.4643687824015692, 8) (7.1925988199212245, 1620)
329730 (1.244014758768857, 7) (1.4853922438621892, 8) (22.829909859418056, 10275)
313243 (1.2558435695047716, 8) (1.5146513474382326, 9) ('-', '-')
297580 (1.2704217458315819, 7) (1.5398564600750393, 8) ('-', '-')
282701 (1.2851524917098687, 7) (1.5664845173041895, 9) ('-', '-')
268565 (1.2984322700169695, 8) (1.598256347983124, 9) ('-', '-')
255136 (1.3157971759064655, 7) (1.6283903912319213, 8) ('-', '-')
242379 (1.3309046751669702, 7) (1.6623884918966887, 9) ('-', '-')
230260 (1.3477028941509817, 7) (1.6980492893061199, 10) ('-', '-')
218747 (1.3687450375974965, 7) (1.7327355097846902, 9) ('-', '-')
207809 (1.1934426229508197, 7) (1.7728830974732614, 10) ('-', '-')
197418 (1.2033191661606961, 6) (1.8138744881914282, 10) ('-', '-')
187547 (1.2141547179798546, 6) (1.8545171485062195, 10) ('-', '-')
178169 (1.2257873678638707, 6) (1.899606121464045, 10) ('-', '-')
169260 (1.238469322622328, 6) (1.9468746594429656, 11) ('-', '-')
160797 (1.248940575716532, 6) (1.997549546183426, 10) ('-', '-')
152757 (1.2623449005962668, 8) (2.052966543676926, 10) ('-', '-')
145119 (1.2766895520993882, 7) (2.104756122242461, 11) ('-', '-')
137863 (1.291087135895879, 6) (2.1612846978967197, 12) ('-', '-')
130969 (1.305403764420158, 7) (2.225700185263027, 12) ('-', '-')
124420 (1.3222019834041692, 7) (2.287764856070867, 12) ('-', '-')
118199 (1.3397101178521944, 7) (2.359366680678156, 13) ('-', '-')
112289 (1.3569691591549515, 7) (2.4289166005013, 13) ('-', '-')
106674 (1.1867575856646895, 7) (2.5023741690408356, 12) ('-', '-')
101340 (1.1990285367334548, 5) (2.5858110317126712, 12) ('-', '-')
96273 (1.208120436535737, 7) (2.666034592810549, 13) ('-', '-')
91459 (1.2188189871249981, 6) (2.7558949449659833, 15) ('-', '-')
86886 (1.2303800227297494, 6) (2.848121682001463, 14) ('-', '-')
82541 (1.2434636401849517, 6) (2.950256098889979, 17) ('-', '-')
78413 (1.2568088054426851, 7) (3.0436348917223235, 15) ('-', '-')
74492 (1.2707050892843244, 7) (3.155300235081656, 17) ('-', '-')
70767 (1.2835520682515218, 6) (3.2669998287484625, 15) ('-', '-')
67228 (1.298939797300453, 7) (3.386415082589946, 16) ('-', '-')
63866 (1.3132252891815734, 7) (3.510285990067411, 17) ('-', '-')
60672 (1.3300951224448492, 8) (3.6492176918406427, 17) ('-', '-')
57638 (1.3469525010508616, 7) (3.788121370635032, 18) ('-', '-')
54756 (1.3668363613718806, 7) (3.934550776080831, 20) ('-', '-')
52018 (1.1924493640340634, 6) (4.084037799884794, 18) ('-', '-')
49417 (1.2026341600112092, 6) (4.249077576946429, 21) ('-', '-')
46946 (1.2155714352435665, 6) (4.418884374075631, 20) ('-', '-')
44598 (1.2250774523998569, 7) (4.597431226939424, 20) ('-', '-')
42368 (1.23602198247007, 6) (4.787392773185123, 20) ('-', '-')
40249 (1.249376488720751, 6) (4.993068983232917, 23) ('-', '-')
38236 (1.2615010975666714, 7) (5.207214360219825, 24) ('-', '-')
36324 (1.276857689972444, 6) (5.4176856133140285, 23) ('-', '-')
34507 (1.2909906123020878, 7) (5.656503666339732, 23) ('-', '-')
32781 (1.3062818177572275, 7) (5.897918515404855, 25) ('-', '-')
31141 (1.3233758348512448, 7) (6.154011178054894, 25) ('-', '-')
29583 (1.3395886849438763, 7) (6.430224339513957, 26) ('-', '-')
28103 (1.355835785343982, 7) (6.7077576946429405, 26) ('-', '-')
26697 (1.1883735774446158, 5) (7.016919651892329, 29) ('-', '-')
25362 (1.1981068920959632, 6) (7.3417993866081295, 31) ('-', '-')
24093 (1.2085750315258512, 6) (7.674179938660813, 32) ('-', '-')
22888 (1.218903056061526, 6) (8.021079507418305, 33) ('-', '-')
21743 (1.2305543879314371, 7) (8.384979683340338, 32) ('-', '-')
20655 (1.2424143353105102, 7) (8.783382373546308, 38) ('-', '-')
"""

import random
import statistics

from resources.english import english_words
from ch03.hashtable_linked import stats_linked_lists
from ch03.hashtable_open import stats_open_addressing
from ch03.hashtable_linked import Hashtable as HL
from ch03.hashtable_open import Hashtable as OHL


def random_words(all_words, n):
    """Select small list of random n from file of large list."""
    random_list = []

    low_bar = len(all_words) / 2
    if n > low_bar:
        raise RuntimeError('n must be smaller than {}'.format(low_bar))

    while len(random_list) < n:
        s = all_words[random.randint(0, len(all_words))]
        if not s in random_list:
            random_list.append(s)

    return random_list

# a sample random list, generated by the following command.
#print(random_words(english_words(), 511))
random_word_list = ['tooroo', 'syrinxes', 'unpurposing', 'lucile',
                    'unsociableness', 'close', 'nidification', 'nonphysicians',
                    'nondelegates', 'midlatitude', 'emydosauria', 'lowbell',
                    'populism', 'teutolatry', 'antinegro', 'turrical',
                    'isagoge', 'neurofibrils', 'underemployed', 'becomma',
                    'guatambu', 'forgat', 'choreatic', 'misperceived',
                    'maliciousness', 'clinkerer', 'erythraea',
                    'conceptualization', 'bain', 'gazogenes', 'plater',
                    'supratemporal', 'nestiatria', 'psephitic', 'unoffended',
                    'material', 'dishtowel', 'waterdrop', 'perinatally',
                    'alphanumerics', 'congestible', 'encarditis', 'fruition',
                    'culicinae', 'futhorks', 'terricolous', 'tolerancy',
                    'introductoriness', 'angild', 'pteropaedes', 'synethnic',
                    'swerd', 'dullard', 'unconstancy', 'dongolas',
                    'bioengineers', 'thoracobronchotomy', 'datableness',
                    'lodens', 'balbutiate', 'upturned', 'overpass',
                    'syphilogenesis', 'necrogenous', 'inlands', 'deglycerine',
                    'underfringe', 'unrebukable', 'flamboyants',
                    'internalness', 'diopsidae', 'revalues', 'stalwarts',
                    'cycloserine', 'peronial', 'gallicolae', 'pitheciinae',
                    'tuberculoma', 'reindeers', 'coinhere', 'glandlike',
                    'emigration', 'bumpering', 'campanulaceous', 'travale',
                    'maneless', 'persecutions', 'fresnels', 'twattle',
                    'fonding', 'liebfraumilch', 'nigglingly', 'illuminisms',
                    'pyrometrically', 'uningeniousness', 'masseuse',
                    'cozeningly', 'sorehawk', 'noselite', 'categorical',
                    'unsubjection', 'noninformative', 'hermitages',
                    'saddletrees', 'lateropulsion', 'unaccordant', 'chicanos',
                    'lactonize', 'importraiture', 'protodynastic', 'smugglery',
                    'revalidates', 'overrestrain', 'electrodeposit',
                    'cragginess', 'redividing', 'nonemission', 'eloiner',
                    'wretchedness', 'champaks', 'pachydermia', 'swacking',
                    'idola', 'apothecial', 'peloponnesian', 'brass',
                    'diapason', 'resoak', 'diodon', 'furanes', 'embanking',
                    'dihexagonal', 'maceman', 'dungy', 'nematocide',
                    'duckmeat', 'indagating', 'banner', 'exterioration',
                    'immingles', 'corrugate', 'unlightened', 'amritsar',
                    'pneumathaemia', 'voodooisms', 'manipulation', 'rebuffing',
                    'narrowy', 'belchers', 'grovelled', 'ceilings',
                    'copiapite', 'yao', 'bookholder', 'cystonectae',
                    'unpursed', 'nontuned', 'subprimates', 'dentatoangulate',
                    'premodifying', 'superprofit', 'churled',
                    'enlightenedness', 'smouldering', 'sicilica',
                    'quarrelingly', 'missends', 'weevillike', 'caroling',
                    'dioxy', 'parse', 'hematothorax', 'pyrolyzed', 'spodium',
                    'ethologies', 'alkalize', 'vermoulu', 'thinning', 'fat',
                    'solaceproof', 'gruffish', 'dragomanate', 'bedazzlements',
                    'descanting', 'toniest', 'misprofess', 'retroviral',
                    'jynx', 'holophotal', 'whanging', 'cannulate', 'ler',
                    'uncouthness', 'shrining', 'permutableness', 'albedoes',
                    'matronage', 'materialise', 'liquidamber',
                    'isopilocarpine', 'dogmatisms', 'ringhals', 'fratricidal',
                    'overhastiness', 'switzeress', 'bartholinitis', 'hosted',
                    'inconceivable', 'beautifulest', 'socketing', 'chitra',
                    'folliculous', 'astrocytoma', 'disbenefit', 'habilitate',
                    'amimide', 'anatherum', 'outcavils', 'lungee',
                    'footballer', 'backvelder', 'squamosoparietal',
                    'fluoroscoped', 'encephaloma', 'stupendly', 'lorica',
                    'innest', 'pinguin', 'musicalises', 'gestalts',
                    'dezymotize', 'landlordry', 'tubework', 'dandriffs',
                    'bannered', 'twanking', 'contemplatingly', 'vacoa',
                    'nonpopery', 'respiratored', 'nargiles', 'changelessly',
                    'blistering', 'lithofractor', 'chanceful', 'orchardists',
                    'pronate', 'bipartisan', 'muscose', 'alighted', 'agamian',
                    'misdirections', 'appressed', 'quahaug', 'yowler',
                    'narrows', 'rabbinica', 'abashed', 'attidae', 'browache',
                    'piquancy', 'monophonous', 'calcisponge',
                    'agelacrinitidae', 'silicification', 'protogyny',
                    'dumbfounds', 'cardiodysesthesia', 'dunked',
                    'acetonitrile', 'percuss', 'underbuilding', 'stannite',
                    'striper', 'paramitome', 'fyke', 'fraulein', 'coroado',
                    'irretrievability', 'agrochemicals', 'casualty', 'arcate',
                    'scurfier', 'berylloid', 'debus', 'stipendiary',
                    'pleasurer', 'hydromagnetic', 'amba', 'banjorine',
                    'cynophilist', 'quaffs', 'autosomes', 'gentianales',
                    'taxology', 'samara', 'trainability', 'perpetuities',
                    'preassigned', 'hazzan', 'caliburn', 'prodigalish',
                    'florence', 'iconographer', 'untedious', 'physicochemic',
                    'desmidiologist', 'stableboy', 'spectropolariscope',
                    'doggereler', 'musciform', 'allioniaceae', 'trellised',
                    'sugary', 'jettying', 'cothish', 'kermises', 'coins',
                    'unmeddling', 'gnathophorous', 'autolesion',
                    'neurodendrite', 'cottages', 'angiodermatitis', 'varletry',
                    'password', 'rubrisher', 'coactor', 'taunt', 'latinist',
                    'cassinette', 'gasifying', 'albertina', 'stadium',
                    'nitrogenize', 'nunchakus', 'stockless', 'ascalabota',
                    'cyanoguanidine', 'chironomic', 'unflinching', 'endymal',
                    'flattie', 'defibrillates', 'jowlop', 'dolous', 'natured',
                    'greyiaceae', 'dare', 'animalia', 'celiocyesis', 'trilby',
                    'absentment', 'centralises', 'guepard', 'myoneme',
                    'anatripsis', 'gearwheel', 'prelibation', 'dipt',
                    'meliorist', 'methylenimine', 'oversecurely',
                    'prosopopoeial', 'geogenesis', 'sparse', 'logicaster',
                    'saponifier', 'yobi', 'crystallophyllian', 'trinerve',
                    'porphyrogeniture', 'sowlth', 'teston', 'semisavagedom',
                    'tendentious', 'psilophyte', 'benzotriazole', 'unoverdone',
                    'morbidnesses', 'tugriks', 'paleohistology', 'voiding',
                    'anticholinergic', 'wingedness', 'tilletiaceae', 'lophine',
                    'lachrymal', 'erupted', 'nonconcurs', 'burnings',
                    'disciplinarily', 'chrysomonadine', 'inattentiveness',
                    'hermetic', 'footsy', 'antilocapridae', 'recommencer',
                    'outwatch', 'antilopinae', 'reascend', 'neurotoxin',
                    'protonated', 'peronosporaceous', 'isonymy', 'indows',
                    'coelelminth', 'thalline', 'unstoppably', 'reconvalescent',
                    'overbooking', 'limonitization', 'epidemiology',
                    'primiparas', 'unthinkingness', 'cogitates', 'mellow',
                    'reformations', 'protravel', 'telautomatic', 'upshut',
                    'sobrieties', 'fluorimetry', 'acataposis', 'reciprocators',
                    'besoothed', 'stably', 'readably', 'acidometer',
                    'unproduceableness', 'philosophicohistorical', 'becross',
                    'salacities', 'judgeship', 'megatherian', 'overarm',
                    'applyingly', 'existibility', 'ehatisaht', 'overservile',
                    'barytones', 'chimneys', 'sinnen', 'glagol', 'tennisdom',
                    'unifactorial', 'carcajou', 'gavials', 'stakerope',
                    'predigestions', 'monopetalae', 'flaskets', 'urinals',
                    'splanchnapophysis', 'unblackened', 'gondang',
                    'inconfutable', 'sleaves', 'anagrammatically', 'eugubium',
                    'interdicts', 'nearctica', 'unvatted', 'proavis',
                    'cephaloclasia', 'ungreeted', 'displanted', 'ultrafilter',
                    'colliding', 'unscraped', 'sniper', 'extravaganzas',
                    'centralised', 'wintle', 'motherhouse', 'discomfiter',
                    'dipentene', 'vignetters', 'unrepentingly', 'trappy',
                    'mynheers', 'undiocesed', 'trunk', 'yagnob', 'mosatenan',
                    'cloakmaker', 'roughriders', 'policeman', 'pimpleback',
                    'overtruthfully', 'pacation', 'hogback', 'fleay',
                    'subdeducible', 'stumpiest', 'hypidiomorphic',
                    'castanopsis', 'sufflate', 'inviolacies', 'updrafts',
                    'fidgetingly', 'futurition', 'contribution', 'boneshaw',
                    'ensculpture', 'papillulate', 'recirculate', 'beseen',
                    'vertebroiliac', 'warstles', 'cymenes']

def stats_just_1024():
    """Pick your M with a threshold of 0.75 and you will see the sizes of avg/max."""
    all_words = english_words()
    # start twice as big as the number of words, and reduce steadily, counting collisions
    M = 8192
    threshold = (M * 3) // 4

    ll_stats_avg = []
    ll_stats_max = []
    oa_stats_avg = []
    oa_stats_max = []
    for _ in range(150):
        words_to_use = []
        for _ in range(threshold):
            words_to_use.append(random.choice(all_words))

        hl = HL(M)
        ohl = OHL(M)
        for w in words_to_use:
            hl.put(w, 1)
            ohl.put(w, 1)
        avg_max_ll = stats_linked_lists(hl)
        avg_max_oa = stats_open_addressing(ohl)

        ll_stats_avg.append(avg_max_ll[0])
        ll_stats_max.append(avg_max_ll[1])
        oa_stats_avg.append(avg_max_oa[0])
        oa_stats_max.append(avg_max_oa[1])

    print('linked list average is', statistics.mean(ll_stats_avg), '+/-',
          statistics.stdev(ll_stats_avg))
    print('linked list max is', statistics.mean(ll_stats_max), '+/-',
          statistics.stdev(ll_stats_max))

    print('open addressing average is', statistics.mean(oa_stats_avg), '+/-',
          statistics.stdev(oa_stats_avg))
    print('open addressing max is', statistics.mean(oa_stats_max), '+/-',
          statistics.stdev(oa_stats_max))

#######################################################################
if __name__ == '__main__':
    ohl1 = OHL(1023)
    for aw1 in random_word_list:
        ohl1.put(aw1, 1)
    print (stats_open_addressing(ohl1))

    hl1 = HL(1023)
    for aw1 in random_word_list:
        hl1.put(aw1, 1)
    print (stats_linked_lists(hl1))

    from ch03.hashtable_linked import DynamicHashtable as DHL
    dl1 = DHL(1023)
    for aw1 in random_word_list:
        dl1.put(aw1, 1)
    print (stats_linked_lists(dl1))
