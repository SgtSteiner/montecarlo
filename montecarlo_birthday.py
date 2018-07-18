import random
import collections
import matplotlib.pyplot as plt

CYCLES = 5000
MAX_STUDENTS = 50
hist = {}


def draw_hist(data):
    plt.plot(data.values())
    plt.xlabel('Students')
    plt.ylabel('Probability')
    plt.axis([2, 50, 0, 1])
    plt.show()


for students in range(2, MAX_STUDENTS+1):
    res = 0
    for _ in range(CYCLES):
        classroom = collections.Counter([random.randint(1, 365) for _ in range(students)])
        if max(classroom.values()) > 1:
            res += 1
    hist[students] = res/CYCLES
    print("Students: {0} - Prob: {1:.2%}".format(students, res/CYCLES))

draw_hist(hist)
