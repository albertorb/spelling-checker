# encoding: utf8
"""
Spanish spelling checker.
The dictionary of words has been obtained from:
    - ftp://ftp.gnu.org/gnu/aspell/dict/es/
The training texts have been downloaded from:
    - http://www.hhgroups.com/letras/
    - GNU project.
"""
__autor__='Alberto Rincón Borreguero'

import re, collections, os

def get_words(text):
    """
    Get list of individual words from text argument.
    """
    return re.findall('\w+', text.lower(), re.UNICODE)

MODEL = collections.defaultdict(lambda: 1)
def training(features):
    """
    Count word appearances on file
    """
    global MODEL
    for f in features:
        MODEL[f] += 1
    return MODEL

def do_train():
    """
    Train algorithm with files on training directory.
    """
    global_text = u''
    training_files = os.listdir('./training')
    for elem in training_files:
        global_text += open('training/' + elem).read()
    return training(get_words(global_text))

alphabet = 'abcdefghijklmnopqrstuvwxyzóéúüíáç'
qwerty = {
    'q':'aws',
    'w':'qase',
    'e':'wsdr',
    'r':'edft',
    't':'rfgy',
    'y':'tghu',
    'u':'yhji',
    'i':'ujko',
    'o':'iklp',
    'a':'qzws',
    's':'azxwde',
    'd':'esxcfr',
    'f':'rdcvgt',
    'g':'tfvbhy',
    'h':'gbnjuy',
    'j':'uhnmki',
    'k':'ijmlo',
    'l':'opk',
    'z':'asx',
    'x':'zsdc',
    'c':'xdfv',
    'v':'cfgb',
    'b':'vghn',
    'n':'bhjm',
    'm':'njk'
}

def edits1_qwerty(word):
    """
    Return those possibilities of letter's neighbours on a qwerty keyboard.
    """
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    replaces = []
    for a,b in splits:
        if b:
            for c in qwerty[b[0]]:
                replaces.append(a + c + b[1:])
    return set(replaces)

def edits1(word):
    """
    Return possibilities of one operation.

    splits: It divides the word in two parts, being the first of length i and the
            second one of length len(word) - i with i<=len(word).
    deletes: Drops a letter from the word for every pair of splits obtained before.
    tranposes: It swaps two consecutive letters on the word for every pair of splits.
    replaces: It replace a letter of the word with one from the alphabet for every
                pair of splits.
    replaces: It adds a new letter from the alphabet in the word for every
                pair of splits.
    :return: set of all possibilities.
    """
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts    = [a + c + b     for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

NWORDS = do_train()

def known_edits2(word):
    """
    Return possibilities for two operations.

    It applies edits1 again on the word, obtaining new possibilities as result
    of applying two operations for each.
    """
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    """
    Return the word proposed as correction
    """
    candidates = known([word]) or known(edits1_qwerty(word)) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

if __name__ == '__main__':
    while True:
        corrected = u''
        for word in get_words(input()):
            corrected += u' %s' %correct(word)
        print(corrected)
