import numpy as np
import sys
import time


def psrs_seq(arr):
    arr.sort()
    return arr


if __name__ == "__main__":
    N = int(sys.argv[1])

    np.random.seed(42)

    arr = np.random.randint(0, 10**9, size=N, dtype="int")

    t0 = time.time()
    sorted_arr = psrs_seq(arr)
    t1 = time.time()

    print(f"time={t1-t0:.6f}s")