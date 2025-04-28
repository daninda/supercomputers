import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("times_small.csv")

sizes = df["N"].astype(int).tolist()

plt.figure(figsize=(10, 6))
plt.plot(sizes, df["time_seq"], marker="o", label="Sequential")
plt.plot(sizes, df["time_par"], marker="s", label="Parallel")

plt.xscale("log")

plt.xticks(sizes, [str(n) for n in sizes], rotation=45)

plt.xlabel("Size N")
plt.ylabel("Time, s")
plt.legend()
plt.grid(which="both", ls="--", lw=0.5)
plt.tight_layout()

plt.savefig("plot_small.png", dpi=300, bbox_inches="tight")


df = pd.read_csv("times_large.csv")

sizes = df["N"].astype(int).tolist()

plt.figure(figsize=(10, 6))
plt.plot(sizes, df["time_seq"], marker="o", label="Sequential")
plt.plot(sizes, df["time_par"], marker="s", label="Parallel")

plt.xscale("log")

plt.xticks(sizes, [str(n) for n in sizes], rotation=45)

plt.xlabel("Size N")
plt.ylabel("Time, s")
plt.legend()
plt.grid(which="both", ls="--", lw=0.5)
plt.tight_layout()

plt.savefig("plot_large.png", dpi=300, bbox_inches="tight")
