import optparse
import sys
import pickle
from collections import defaultdict
from itertools import izip, count
from pprint import pprint

optparser = optparse.OptionParser()
optparser.add_option("-d", "--data", dest="train", default="data/hansards", help="Data filename prefix (default=data)")
optparser.add_option("-e", "--english", dest="english", default="e", help="Suffix of English filename (default=e)")
optparser.add_option("-f", "--french", dest="french", default="f", help="Suffix of French filename (default=f)")
optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxint, type="int", help="Number of sentences to use for training and alignment")
optparser.add_option("-t", "--translation_table",dest="p_t_t",help="Use pickled translation table output by Model 1")
(opts, _) = optparser.parse_args()
f_data = "%s.%s" % (opts.train, opts.french)
e_data = "%s.%s" % (opts.train, opts.english)

sys.stderr.write("Training with IBM Model 2...\n")
sys.exit('Program aparently still under construction. Exiting now...')
bitext = [[sentence.strip().split() for sentence in pair] for pair in zip(open(f_data), open(e_data))[:opts.num_sents]]
f_count = defaultdict(float)
e_count = defaultdict(int)
fe_count = defaultdict(int)
fe_prob = defaultdict(float)
s_total = defaultdict(float)
t = pickle.load(open('my_first_pickle.pi','r'))
a_count = defaultdict(float)
a_total = defaultdict(float)
a = defaultdict(float)


## This is one way to initialize t(e|f)
"""
"""
all_e = []  
for (f,e) in bitext:
  for e_w in set(e):
    all_e += [e_w]
    #all_e += None

# Carry over t(.|.) from model 1.
### Remember t(.|.) is map of tuples to floats.
### In particular (e,f) -> p(e|f)

# Initialize a(i|j,len(e),len(j)) = 1/(len(f)+1) for all i, j, len(e), len(f)
# i := position of i-th foreign word in sentnse
# j := positio of j-th foreign word in sentence

for (f,e) in bitext:
  for i in range(1,len(e)):
    for j in range(1,len(f)):
      print i,j,len(e),len(f)
      a[(i,j,len(e),len(f))]  = 1/(len(f)+1) # (j,l_e,l_f) -> i   [P(i,j,l_e,l_f)] 
  print "i,j,len(e),len(f)"

for N in range(1,5):
  sys.stderr.write("Beginning iteration: %i\n" % N)
  # zero out counts
  ## Zero out count(e|f)
  for it in fe_count.values():
    it = 0
  ## Zero out total(f)
  for it in f_count.values():
    it = 0
  ##  Zero out a_count
  for v in a_count.values():
    v = 0  
  # Zero out a_total
  for v in a_total.values():
    v = 0
    
  for (n, (f,e)) in izip(count(),bitext):
    l_e = len(e)
    l_f = len(f)
    print "le %s, lf %s" % (l_e,l_f)

    # compute normalization ?!
    for j in range(1,l_e):
      s_total[e[j]] = 0
      for i in range(1,l_f):
       #print "t: ", t[(e[j],f[j])] 
       #print "a: ",  a[(i,j,l_e,l_f)]
       s_total[e[j]] += t[(e[j],f[j])] * a[(i,j,l_e,l_f)]

    for j in range(1,l_e):
      for i in range(1,l_f):
        print s_total
        print "##################################################"
        print t
        print "##################################################"
        c = t[(e[j],f[j])] * a[(i,j,l_e,l_f)] / s_total[e[j]]
        count[(e[j],f[i])] += c
        fe_count[(e[j],f[i])]
        f_count[f[i]] += c
        a_count[(i,j,l_e,l_f)] += c
        a_total[(j,l_e,l_f)] += c
  for (f,e) in bitext:
    for (i,f_w) in enumerate(f):
      for (j,e_w) in enumerate(e):
        t[(e_w,f_w)] = 0
        a[(i,j,len(e),len(f))] = 0

  for (f,e) in bitext:
    for f_w in f:
      for e_w in e:
        t[(e_w,f_w)] = fe_count[(e_w,f_w)] / f_count[f_w]

  for (n,(f,e)) in izip(count(), bitext):
    for i in f:
      for j in e:
        a[(i,j,len(e),len(f))] = a_count[(i,j,len(e),len(j))]/a[(j,len(e),len(f))]
  N += 1


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
