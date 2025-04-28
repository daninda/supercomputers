import subprocess, re, csv


def run_seq(N):
    p = subprocess.run(
        ["python", "sequential.py", str(N)], stdout=subprocess.PIPE, text=True
    )
    m = re.search(r"time=(\d+\.\d+)", p.stdout)
    return float(m.group(1))


def run_par(N):
    p = subprocess.run(
        ["mpirun", "-np", "16", "python", "parallel.py", str(N)],
        stdout=subprocess.PIPE,
        text=True,
    )
    times = [float(x) for x in re.findall(r"time=(\d+\.\d+)", p.stdout)]
    return max(times)


small = [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
large = [50_000_000, 100_000_000, 150_000_000, 200_000_000, 250_000_000, 300_000_000, 350_000_000, 400_000_000]

with open("times_small.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(("N", "time_seq", "time_par"))
    for N in small:
        t_seq = run_seq(N)
        t_par = run_par(N)
        print(f"N={N}: seq={t_seq:.4f}s, par={t_par:.4f}s")
        w.writerow((N, t_seq, t_par))

with open("times_large.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(("N", "time_seq", "time_par"))
    for N in large:
        t_seq = run_seq(N)
        t_par = run_par(N)
        print(f"N={N}: seq={t_seq:.4f}s, par={t_par:.4f}s")
        w.writerow((N, t_seq, t_par))
