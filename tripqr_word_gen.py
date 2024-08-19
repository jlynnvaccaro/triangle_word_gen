from words import *

# Use 0 for an ideal angle

p=3
q=5
r=5
max_length=5
fname = "tri_"+str(p)+"_"+str(q)+"_"+str(r)+"_len"+str(max_length)+".csv"

Lpqr = gen_words_pqr(p=p,q=q,r=r, max_length=max_length, filter_during=True)

summary(Lpqr)
write_L(Lpqr, fname)
