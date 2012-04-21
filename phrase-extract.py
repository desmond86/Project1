"""
Phrase Extraction algorithm based on Philipp Koehn's book in chapter 5

Author: Desmond Putra (555802)

This program is based on phrase extraction pseudo code that is provided in the 
book. However, there are some updates to cover lack of information in the 
pseudo codes. 

Input for this program:
1. A sentence in English language. 
   Example : "michael assumes that he will stay in the house"
2. A sentence in Foreign language. 
   Example: "michael geht davon aus , dass er im haus bleibt"
   Make sure that every punctuation is separated by space because, every 
   punctuation is considered as standalone word.
3. List of word alignment from English and foreign sentences above. This 
   alignment consists of tuple (e,f) where 'e' refers to English word and 'f' 
   refers to Foreign word. First word in a setence is considered as position 0
   (starting index)
"""

#global variable
list_e = [] #list of word e position (unique)
list_f = [] #list of word f position (unique)
word_alignment = [] #list of word alignments


def extract_word_alignment(word_alignment):
    """
    This function will extract the position of word alignment(WA) into two list.
    list_e will contain all of the position of 'e' that is used in WA
    list_f will contain all of the position of 'f' that is used in WA
    
    input:
    word alignment
    """
    global list_e, list_f

    #extract e and f from word alignment
    for e,f in word_alignment:
        if e not in list_e:
            list_e.append(e)

        if f not in list_f:
            list_f.append(f)


def find_phrase(e, f, wa):
    """
    This function will find all possible of english phrase and foreign phrase 
    given these 3 inputs:
    e: english sentence
    f: foreign sentenvce
    wa: list of word alignment based on e and f

    After get all of the possibility of english and foreign phrase, it will
    call extract function to check its consistency. In the end, it will call
    print_phrase_apir function to generate the pair or english and foreign 
    phrase

    output: 
    list of english and foreign pair
    """
    global word_alignment

    #updates to global variable
    word_alignment = wa

    phrase_pair_position_list =[]

    #extract a sentence into a list of words
    words_e = e.split(" ") #list of word from english sentence
    words_f = f.split(" ") #list of word from foreign sentence

    #extract the position
    extract_word_alignment(word_alignment)

    #loop
    for e_start in range(0, len(words_e)):
        for e_end in range(e_start, len(words_e)):
            (f_start, f_end) = (len(words_f)-1, 0)

            for (e,f) in word_alignment:
                if e_start <= e <= e_end:
                    f_start = min(f, f_start)
                    f_end = max(f, f_end)

            #find the minimal foreign phrase
            phrase_pair_position = extract(f_start, f_end, e_start, e_end, len(words_f))

            #add into phrase_pair list
            if phrase_pair_position:
                for i in phrase_pair_position:
                    if i not in phrase_pair_position_list: 
                        phrase_pair_position_list.append(i)
            
    #generate phrase pair from 
    output = print_phrase_pair(words_e, words_f, phrase_pair_position_list)
    return output


def extract(f_start, f_end, e_start, e_end, len_f):
    """
    This function will find the minimal foreign phrase that matches and 
    consistent with the word alignment. The consistency is checked by 
    examining each word alignment in the possible pair of english and
    foreign phrase.

    input:
    f_start = start position of foreign word
    f_end = end position of foreign word
    e_start = start position of english word
    e_end = end position of english word
    len_f = length of sentence f

    output:
    phrase_pair_position = list of phrase pair position (start to end)

    """
    phrase_pair_position = []

    #if the position of f_end is -1
    if f_end == -1:
        return ""

    #check the consistency   
    for e,f in word_alignment:
        #each of word alignment is inside the phrase range
        if e_start <= e <= e_end and f_start <= f <= f_end:
            continue
        #each of word alignment is outside the phrase range
        elif (e > e_end or e < e_start) and (f > f_end or f < f_start):
            continue
        #'f' position outside the phrase range
        elif (e_start <= e <= e_end)  and (f > f_end or f < f_start):
            return []
        #'e' position outside the phrase range
        elif (e > e_end or e < e_start) and (f_start <= f <= f_end):
            return []

    fs = f_start

    #check the possible phrase pair for unaligned words
    #do until position of fs inside of word alignment
    while True:
        fe = f_end

        #do until position of fe inside of word alignment
        while True:
            phrase_pair_position.append([(e_start, e_end),(fs, fe)])
            fe += 1
            
            #check fe position in word alignment or
            #its position index > length of foreign sentence - 1
            if fe in list_f or fe > (len_f-1):
                break

        fs -= 1

        #check fs position in word alignment or its position index < 0
        if fs in list_f or fs < 0:
            break

    return phrase_pair_position


def print_phrase_pair(words_e, words_f, phrase_pair_position_list):
    """
    This function will generate a phrase pair from a list of phrase position
    Each pair of english and foreign phrase are separated by '-' 

    input: 
    words_e = list of english words
    words_f = list of foreign words
    phrase_pair_position_list: list of phrase position from start to end

    output: 
    list of phrase pair such as

    >>> phrase_pair_position_list = [[(0, 0), (0, 0)], [(0, 1), (0, 3)]]
    >>> words_e = ['michael', 'assumes', 'that', 'he', 'will', 'stay', 'in', 'the', 'house']
    >>> words_f = ['michael', 'geht', 'davon', 'aus', ',', 'dass', 'er', 'im', 'haus', 'bleibt']
    >>> print_phrase_pair(words_e, words_f, phrase_pair_position_list)
    ['michael - michael', 'michael assumes - michael geht davon aus']
    """
    output = []

    for pair in phrase_pair_position_list:
        phrase_e =""
        phrase_f =""

        #english range 
        (start,end) = pair[0]
        for i in range(start, end+1):
            phrase_e = phrase_e + " " + words_e[i]

        #foreign range
        (start,end) = pair[1]
        for i in range(start, end+1):
            phrase_f = phrase_f + " " + words_f[i]

        output.append(phrase_e.strip() +" - "+ phrase_f.strip())
    
    return output

#--------------
# Run the program
#--------------

e_sentence = "michael assumes that he will stay in the house"
f_sentence = "michael geht davon aus , dass er im haus bleibt"
w_alignment = [(0,0), (1,1), (1,2), (1,3), (2,5), (3,6), (4,9), (5,9), (6,7), (7,7), (8,8)]

phrase_pair = find_phrase(e_sentence, f_sentence, w_alignment)

#print the result
for pair in phrase_pair:
    print pair

# run doctests
if __name__ == "__main__":
    import doctest
    doctest.testmod()

