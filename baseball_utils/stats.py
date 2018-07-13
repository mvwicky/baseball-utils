import random
import time

import numpy as np

from tools import timeit


class RandomWalker(object):
    def __init__(self):
        self.position = 0

    def walk(self, n):
        self.position = 0
        for i in range(n):
            yield self.position
            self.position += 2 * random.randint(0, 1) - 1


def random_walk(n):
    position = 0
    walk = [position]
    for i in range(n):
        position += 2 * random.randint(0, 1) - 1
        walk.append(position)
    return walk


def random_walk_iter(n):
    from itertools import accumulate
    steps = random.choices([-1, 1], k=n)
    return [0] + list(accumulate(steps))


def random_walk_np(n):
    steps = np.random.choice([-1, 1], n)
    return np.cumsum(steps)


if __name__ == '__main__':
    random.seed()

    walker = RandomWalker()
    print('Object Oriented')
    start_time = time.perf_counter()
    timeit('[position for position in walker.walk(n=10000)]', globals())
    print('Elapsed Time: {0:.8f}'.format(time.perf_counter() - start_time))
    print('')
    print('Procedural')
    start_time = time.perf_counter()
    timeit('random_walk(n=10000)', globals())
    print('Elapsed Time: {0:.8f}'.format(time.perf_counter() - start_time))
    print('')
    print('Itertools')
    start_time = time.perf_counter()
    timeit('random_walk_iter(n=10000)', globals())
    print('Elapsed Time: {0:.8f}'.format(time.perf_counter() - start_time))
    print('')
    print('Numpy')
    start_time = time.perf_counter()
    timeit('random_walk_np(n=10000)', globals())
    print('Elapsed Time: {0:.8f}'.format(time.perf_counter() - start_time))
