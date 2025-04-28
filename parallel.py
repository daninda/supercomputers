from mpi4py import MPI
import numpy as np
import sys


def psrs_sort(local):
    local.sort()
    p = size

    samples = [local[(i + 1) * len(local) // (p + 1)] for i in range(p)]
    return np.array(samples, dtype="int")


def partition_and_exchange(local, pivots):
    indices = np.searchsorted(local, pivots)

    splits = np.concatenate(([0], indices, [len(local)]))
    chunks = [local[splits[i] : splits[i + 1]] for i in range(len(splits) - 1)]

    sendcounts = [len(chunk) for chunk in chunks]

    recvcounts = comm.alltoall(sendcounts)

    sendbuf = np.concatenate(chunks) if chunks else np.empty(0, dtype="int")

    recvbuf = np.empty(sum(recvcounts), dtype="int")

    comm.Alltoallv(
        [sendbuf, sendcounts, None, MPI.INT], [recvbuf, recvcounts, None, MPI.INT]
    )
    return recvbuf


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

N = int(sys.argv[1])

n_local = N // size + (1 if rank < N % size else 0)

np.random.seed(42 + rank)
local = np.random.randint(0, 10**9, size=n_local, dtype="int")

comm.Barrier()
t0 = MPI.Wtime()

local.sort()
samples = psrs_sort(local)

all_samples = None
if rank == 0:
    all_samples = np.empty(size * size, dtype="int")
comm.Gather(samples, all_samples, root=0)

if rank == 0:
    all_samples.sort()
    pivots = [all_samples[(i + 1) * size] for i in range(size - 1)]
    pivots = np.array(pivots, dtype="int")
else:
    pivots = np.empty(size - 1, dtype="int")

comm.Bcast(pivots, root=0)

recvbuf = partition_and_exchange(local, pivots)

recvbuf.sort()

comm.Barrier()
t1 = MPI.Wtime()

print(f"time={t1-t0:.6f}s")
