"""
Phrase Extraction algorithm based on Philipp Koehn's book in chapter 5
new updates
"""
#word_alignment = [(1,1), (2,2), (2,3), (2,4), (3,6), (4,7), (5,10), (6,10), (7,8), (8,8), (9,9)]
word_alignment = [(0,0), (1,1), (1,2), (1,3), (2,5), (3,6), (4,9), (5,9), (6,7), (7,7), (8,8)]
english = "michael assumes that he will stay in the house"
foreign = "michael geht davon aus , dass er im haus bleibt"

list_e = []
list_f = []

for x,y in word_alignment:
    if x not in list_e:
        list_e.append(x)

    if y not in list_f:
        list_f.append(y)



words_e = english.split(" ")
words_f = foreign.split(" ")
print list_f



def extract(f_start, f_end, e_start, e_end):
#    print "awalnya ", e_start, e_end, f_start, f_end
    if f_end == -1:
        return
       
    for e,f in word_alignment:
#        print e,f
        if e_start <= e <= e_end and f_start <= f <= f_end:
#            print "masuk case 1"
            continue
        elif (e > e_end or e < e_start) and (f > f_end or f < f_start) :
#            print "masuk case 2"
            continue
        elif e_start <= e <= e_end  and (f > f_end or f < f_start):
#            print "masuk case 3"
            return
        elif (e > e_end or e < e_start) and f_start <= f <= f_end :
#            print "masuk case 4"
            return

    E =[]
    fs = f_start
    while True:
        fe = f_end

        while True:
           # print "out ", e_start,e_end, fs,fe
            print words_e[e_start:e_end+1], " - ", words_f[fs:fe+1]
            fe += 1       
            if fe in list_f or fe > (len(words_f)-1):
                break

        fs -= 1
        if fs in list_f or fs < 0:
            break
    return
#extract(1, 4, 1, 2)

for e_start in range(0, len(words_e)):
    for e_end in range(e_start, len(words_e)):
        (f_start, f_end) = (len(words_f)-1, 0)

        for (e,f) in word_alignment:
            if e_start <= e <= e_end:
                f_start = min(f, f_start)
                f_end = max(f, f_end)
        extract(f_start, f_end, e_start, e_end)
