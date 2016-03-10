# encoding: utf8
"""
Spanish spelling checker.
The dictionary of words has been obtained from:
    ftp://ftp.gnu.org/gnu/aspell/dict/es/
The training texts have been downloaded from:
    estanquera.txt: http://www.hhgroups.com/letras/los-chikos-del-maiz/la-estanquera-de-saigon-37868/la-estanquera-de-saigon-9206/
"""

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
        print elem
        global_text += file('training/' + elem).read().decode('utf8')
    return training(get_words(global_text))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

NWORDS = do_train()

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

if __name__ == '__main__':
    while True:
        corrected = u''
        for word in get_words(raw_input()):
            corrected += ' %s' %correct(word)
        print corrected
