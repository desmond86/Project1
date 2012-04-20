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
english = "" #english sentence
foreign = "" #foreign sentence
words_e = [] #list of word from english sentence
words_f = [] #list of word from foreign sentence

"""
This function will extract the position of word alignment(WA) into two list.
list_e will contain all of the position of 'e' that is used in WA
list_f will contain all of the position of 'f' that is used in WA
"""
def extract_word_alignment(word_alignment):
    global list_e, list_f

    #extract e and f from word alignment
    for e,f in word_alignment:
        if e not in list_e:
            list_e.append(e)

        if f not in list_f:
            list_f.append(f)

"""
This function will find all of possibility of phrase
"""
def find_phrase(e, f, wa):
    global english, foreign, word_alignment, words_e, words_f

    #updates to global variable
    english = e
    foreign = f
    word_alignment = wa

    #extract a sentence into a list of words
    words_e = english.split(" ")
    words_f = foreign.split(" ")

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
            extract(f_start, f_end, e_start, e_end)

"""
This function will extract each possible 
"""
def extract(f_start, f_end, e_start, e_end):
#    print f_start, f_end, e_start, e_end

    #if the position of f_end is -1
    if f_end == -1:
        return

    #check the consistency   
    for e,f in word_alignment:
        #each of word alignment is inside the phrase range
        if e_start <= e <= e_end and f_start <= f <= f_end:
            continue
        #each of word alignment is outside the phrase range
        elif (e > e_end or e < e_start) and (f > f_end or f < f_start) :
            continue
        #f position outside the phrase range
        elif e_start <= e <= e_end  and (f > f_end or f < f_start):
            return
        #e position outside the phrase range
        elif (e > e_end or e < e_start) and f_start <= f <= f_end :
            return

    E =[]
    fs = f_start

    #check the possible phrase pair for unaligned words
    #do until position of fs inside of word alignment
    while True:
        fe = f_end

        #do until position of fe inside of word alignment
        while True:
            print words_e[e_start:e_end+1], " - ", words_f[fs:fe+1]
            fe += 1
            
            #check into f position in word alignment and
            #have a value > length of foreign sentence
            if fe in list_f or fe > (len(words_f)-1):
                break

        fs -= 1

        #check into f position in word alignment or have a value < 0
        if fs in list_f or fs < 0:
            break
    return


#--------------
# Run the program
#--------------
find_phrase("michael assumes that he will stay in the house", "michael geht davon aus , dass er im haus bleibt", [(0,0), (1,1), (1,2), (1,3), (2,5), (3,6), (4,9), (5,9), (6,7), (7,7), (8,8)])

# run doctests
if __name__ == "__main__":
    import doctest
    doctest.testmod()
