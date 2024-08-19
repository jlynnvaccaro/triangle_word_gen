import csv

def reduce_pair(word, pair = "ab", n = 3):
    ''' Reduces the word using the relation (ab)^n = 1. 
    e.g. reduce_pair("abab", "ab", 3) returns "ba" '''
    if n == 0: # Ideal angle
        return word
    max_ = pair*n
    min_ = ""
    _max = pair[::-1]*n
    _min = ""
    while len(max_) > len(min_):
        word = word.replace(max_, min_)
        word = word.replace(_max, _min)
        max_, min_ = max_[:-1], max_[-1] + min_
        _max, _min = _max[:-1], _max[-1] + _min
    return word

def reduce_layer_pqr(word, p, q, r):
    ''' Checks for any reduction in the word directly from T(p,q,r) presentation'''
    word = reduce_pair(word, "ab", p)
    word = reduce_pair(word, "ac", q)
    word = reduce_pair(word, "bc", r)
    word = word.replace("aa","")
    word = word.replace("bb","")
    word = word.replace("cc","")
    return word

def is_reduced(word, reduce_layer=reduce_layer_344, p=None, q=None, r=None):
    if len(word) <= 1:
        return True
    new_word = reduce_layer(word, p=p, q=q, r=r)
    if new_word == word:
        return True
    return False

def reduce(word, reduce_layer=reduce_layer_344,p=None, q=None, r=None):
    if len(word) <= 1:
        return word
    done = False
    old_word = word
    while not done:
        word = reduce_layer(word,p=p,q=q,r=q)
        if old_word == word:
            done = True
        else:
            old_word = word
    return word

def is_inforder(word, reduce_layer=reduce_layer_344, max_order=24, p=None, q=None, r=None):
    return reduce(word*max_order, reduce_layer=reduce_layer, p=p, q=q, r=r) != ""

def compute_max_order(L):
    '''This is a fake lcm but works for this purpose'''
    prod = 2
    for x in L:
        if x == 0 or prod % x == 0:
            continue
        else:
            prod = prod*x
    return prod


def gen_words_pqr(p,q,r,max_length = 5, L=None, filter_during=False):
    ''' Generates a nested list of words up to a designated max_length. Removes reducible words throughout. 
    Optionally removes conjugates and finite-order elements throughout.
    Returns L = [ [words len 0], ... , [words len max_length] ]
    
    e.g. gen_words_pqr(5,5,5, max_length=2,L=None, filter_during=False) returns
    [[""], ["a","b","c"], ["ab", "ac", "ba", "bc", "ca", "cb"]]
    
    e.g. gen_words_pqr(5,5,5, max_length=3,L=None, filter_during=True) returns
    [[], [], [], ["abc"]] because all words of length <=2 are finite-order.'''

    alphabet = ["a","b","c"]
    max_order = compute_max_order([p,q,r]) # torsion elements have an order which divides this max_order
    print("Compiling words of T(",p,q,r,") up to length",max_length,"with max order",max_order)
    if L is None:
        L = [[""]]
    start = len(L)-1
    for i in range(start,max_length):
        print("Starting length",i+1)
        new_L = []
        for word in L[i]:
            for x in alphabet:
                new_L += [word + x]
        filter_reduced(new_L, reduce_layer=reduce_layer_pqr, is_Ln=True, p=p, q=q, r=r)
        L += [new_L]
        if filter_during:
            filter_inforder(L[i], reduce_layer=reduce_layer_pqr, max_order=max_order, is_Ln=True, p=p, q=q, r=r)
            filter_conj(L[i], reduce_layer=reduce_layer_pqr, is_Ln=True, p=p, q=q, r=r)
        print("Finished length",i+1)
    if filter_during:
        filter_inforder(L[max_length], reduce_layer=reduce_layer_pqr, max_order=max_order, is_Ln=True,p=p,q=q,r=r)
        filter_conj(L[max_length], reduce_layer=reduce_layer_pqr, is_Ln=True,p=p,q=q,r=r)
        filter_pow(L)
    return L

def filter_reduced(L, reduce_layer=reduce_layer_344, is_Ln=False, p=None, q=None, r=None):
    if is_Ln:
        for word in L[::-1]:
            if not is_reduced(word, reduce_layer=reduce_layer, p=p, q=q, r=r):
                L.remove(word)
    else:
        for L_n in L:
            filter_reduced(L_n, reduce_layer=reduce_layer, is_Ln=True, p=p, q=q, r=r)
    return L

def filter_inforder(L, reduce_layer=reduce_layer_344, max_order=2, is_Ln=False, p=None, q=None,r=None):
    ''' Iterates through words (backwards) and removes finite-order elements'''
    if is_Ln:
        for word in L[::-1]:
            if not is_inforder(word, reduce_layer=reduce_layer, max_order=max_order, p=p, q=q, r=r):
                L.remove(word)
    else:
        for L_n in L:
            filter_inforder(L_n, reduce_layer=reduce_layer, max_order=max_order, is_Ln=True, p=p, q=q, r=r)
    return L

def rotate_word(word,n,rev=False):
    if rev:
        word = word[::-1]
    return word[n::] + word[0:n]

def filter_conj(L, reduce_layer=reduce_layer_344, is_Ln=False, p=None, q=None, r=None):
    '''Filters out conjugates and their inverses for each word'''
    if is_Ln:
        for word in L[::-1]:
            for n in range(1,len(word)):
                if not is_reduced(rotate_word(word,n), reduce_layer=reduce_layer, p=p, q=q, r=r) or not is_reduced(rotate_word(word,n,rev=True), reduce_layer=reduce_layer, p=p, q=q, r=r):
                    L.remove(word)
                    break
                elif rotate_word(word,n) in L and word != rotate_word(word,n):
                    L.remove(word)
                    break
                elif rotate_word(word,n,rev=True) in L and word != rotate_word(word,n,rev=True):
                    L.remove(word)
                    break
    else:
        for L_n in L:
            filter_conj(L_n, reduce_layer=reduce_layer, is_Ln=True)
    return L

def filter_pow(L):
    '''Filters out w*n powers of previously listed words.'''
    N = len(L)
    for n, L_n in enumerate(L):
        if n==0:
            continue
        for word in L_n:
            for i in range(2*n, N, n):
                if word*(i//n) in L[i]:
                    L[i].remove(word*(i//n))
    return L

def summary(L):
    ''' Prints the number of words for each length in the nested list'''
    for i,L_n in enumerate(L):
        print(i, len(L_n)) 

def write_L(L, fname="WORDS"):
    ''' Writes the word list to a csv file'''
    with open(fname, 'w') as f:
        fwriter = csv.writer(f)
        for Ln in L:
            for word in Ln:
                fwriter.writerow([word])
