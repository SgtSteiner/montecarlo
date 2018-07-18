import random
import collections

CYCLES = 5000

trials = collections.Counter([random.randint(1, 6) for _ in range(CYCLES)])
for key in sorted(trials):
    print("Nº {0} Prob: {1:.2f}".format(key, trials[key]/CYCLES))
