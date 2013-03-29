#!/usr/bin/env python
#################################################################
############  TODO: Add null token to foreign sentence ##########
#################################################################
import optparse
import sys
from collections import defaultdict
from itertools import izip, count
from pprint import pprint

optparser = optparse.OptionParser()
optparser.add_option("-d", "--data", dest="train", default="data/hansards", help="Data filename prefix (default=data)")
optparser.add_option("-e", "--english", dest="english", default="e", help="Suffix of English filename (default=e)")
optparser.add_option("-f", "--french", dest="french", default="f", help="Suffix of French filename (default=f)")
optparser.add_option("-t", "--threshold", dest="threshold", default=0.5, type="float", help="Threshold for aligning with Dice's coefficient (default=0.5)")
optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxint, type="int", help="Number of sentences to use for training and alignment")
(opts, _) = optparser.parse_args()
f_data = "%s.%s" % (opts.train, opts.french)
e_data = "%s.%s" % (opts.train, opts.english)

sys.stderr.write("Training with IBM Model 1...\n")
bitext = [[sentence.strip().split() for sentence in pair] for pair in zip(open(f_data), open(e_data))[:opts.num_sents]]
f_count = defaultdict(float)
e_count = defaultdict(int)
fe_count = defaultdict(int)
fe_prob = defaultdict(float)
#trans = defaultdict(float)
s_total = defaultdict(float)
t = defaultdict(float)

## This is one way to initialize t(e|f)
"""
for (f_s, e_s) in bitext:
  num_e = 0
  for e_w in set(e_s):
    num_e += 1
  for e_w in set(e_s):
    for f_w in set(f_s):
      t[(e_w,f_w)] = 1.0/(num_e)
   
# Max likelihood probs per sentence 
#for k in sorted(t.keys()):
#  print "P(%s|%s) " % k, "%.3f" % t[k]
"""
all_e = []  
for (f,e) in bitext:
  for e_w in set(e):
    all_e += [e_w]
#print len(set(all_e))
for (f,e) in bitext:
  for e_w in e:
    for f_w in f:
      t[(e_w,f_w)] = 1.0/len(set(all_e))
    
for k in sorted(t.keys()):
  print k, t[k]

for N in range(1,5):
  sys.stderr.write("Beginning iteration: %i\n" % N)
  # zero out counts
  for it in fe_count.values():
    it = 0
  for it in f_count.values():
    it = 0
  for (n, (f,e)) in izip(count(),bitext):
    # compute normalization ?!
    for e_i in set(e):
      s_total[e_i] = 0 
      for f_i in set(f):
        s_total[e_i] += t[(e_i,f_i)]
    for e_i in set(e):
      for f_i in set(f):
        fe_count[(e_i,f_i)] += t[(e_i,f_i)] / s_total[e_i]
        f_count[f_i] += t[(e_i,f_i)] / s_total[e_i]

  # do some pretty printing of ttables
  # h = max(s_total.keys())
  #print "               ",
  #for e_i in sorted(s_total.keys()):
    #print  e_i.center(6),
  #print
  for f_i in sorted(f_count.keys()):
    #print f_i.rjust(15),
    for e_i in sorted(s_total.keys()):
      t[(e_i,f_i)] = fe_count[(e_i,f_i)] / f_count[f_i]
      #print "%.4f" % t[(e_i,f_i)] ,
    #print 


  N += 1

#print t.keys()[0]
#for k in sorted(t.keys()):
#  print k, t[k]

## Check marginal probabilities...
#for f_i in sorted(f_count.keys()):
#  r_sum = 0
#  for e_i in sorted(s_total.keys()):
#    r_sum += t[(e_i,f_i)]
#  #print "P(*|%s) = %f" %(f_i,r_sum )
#print ""
#for e_i in sorted(s_total.keys()):
#  c_sum = 0
#  for f_i in sorted(f_count.keys()):
#    c_sum += t[(e_i,f_i)]
#  #print "P(%s|*) = %f" %(e_i,c_sum )

for (f,e) in bitext:
  ii =0
  for(i,f_i) in enumerate(f):
    jj = 0
    p_max = 0
    for(j,e_j) in enumerate(e):
      if  t[(e_j,f_i)] > p_max:
        p_max = t[(e_j,f_i)]
        ii = i
        jj = j 
    print  "%i-%i" %(ii,jj),
  print
      
"""
initialize t(f|e) uniformly 
 -- need to count unique english words to set t[(f_i,e_i)] = 1/length(e_count.keyset()*1.0)
do
  set count(f|e) to 0 for all f,e
  set total(e) to 0 for all e
  for all sentence pairs (f_s,e_s)
    for all unique words f in f_s
      n_f = count of f in f_s
      total_s = 0
      for all unique words e in e_s
        total_s += t(f|e) * n_f
      for all unique words e in e_s
        n_e = count of e in e_s
        count(f|e) += t(f|e) * n_f * n_e / total_s
        total(e) += t(f|e) * n_f * n_e / total_s
  for all e in domain( total(.) )
    for all f in domain( count(.|e) )
      t(f|e) = count(f|e) / total(e)
until convergence
"""
