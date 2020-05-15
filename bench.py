import matplotlib.pyplot as plt
import subprocess
import regex as re
from datetime import timedelta
import numpy as np

codes = {
    "python": ["python.py", "python_numpy.py", "python_numba.py"][::-1],
    "julia": ["julia.jl"],
    "c": ["no_opt_c", "opt_c", "fast_c"],
    "fortran": ["no_opt_fort", "opt_fort", "fast_fort"]
}
time_regex = re.compile("\(h:mm:ss or m:ss\): (\d*):(\d*.\d*)")
mem_regex = re.compile("Maximum resident set size \(kbytes\): (\d*)")


class bench:
    def __init__(self, language, run):
        self.language = language
        self.run = run

    def capture(self):
        if self.language == "python":
            result = subprocess.run(
                ["/usr/bin/time", "-v", "python", "./" + self.run],
                capture_output=True)
            self.output = result.stderr.decode("utf-8")
        elif self.language == "julia":
            result = subprocess.run(
                ["/usr/bin/time", "-v", "julia", "./" + self.run],
                capture_output=True)
            self.output = result.stderr.decode("utf-8")
        else:
            result = subprocess.run(["/usr/bin/time", "-v", "./" + self.run],
                                    capture_output=True)
            self.output = result.stderr.decode("utf-8")
        subprocess.run(["rm", "set.ppm"])
        return

    def process(self):
        print(self.output)
        mins = time_regex.search(self.output).group(1)
        secs = time_regex.search(self.output).group(2)
        self.time = timedelta(minutes=float(mins), seconds=float(secs))
        self.mem = int(mem_regex.search(self.output).group(1))

    def measure(self):
        self.capture()
        self.process()


benches = {
    language: {run: bench(language, run)
               for run in codes[language]}
    for language in codes.keys()
}

for l in benches:
    for r in benches[l]:
        benches[l][r].measure()

c_time = benches["c"]["opt_c"].time
c_mem = float(benches["c"]["opt_c"].mem)
times = {
    language:
    {run: benches[language][run].time / c_time
     for run in codes[language]}
    for language in codes.keys()
}

mems = {
    language:
    {run: benches[language][run].mem / c_mem
     for run in codes[language]}
    for language in codes.keys()
}
labs = []
time_data = []
mem_data = []
for language in codes.keys():
    for run in codes[language]:
        labs.append(benches[language][run].run)
        time_data.append(times[language][run])
        mem_data.append(mems[language][run])

X = np.arange(len(time_data))
plt.bar(X, time_data)
plt.xticks(X, labs, rotation=45, size=12)
plt.title(f"Performance relative to opt c: {c_time} seconds", size=20)
plt.ylabel("Normalized Time", size=15)
plt.axhline(1, linestyle="--", color="grey")
plt.yticks(np.arange(max(time_data) + 2))
plt.tight_layout()
plt.savefig("bench_time.png", dpi=300)
plt.close()

plt.bar(X, mem_data)
plt.xticks(X, labs, rotation=45, size=12)
plt.title(f"Performance relative to opt c: {c_mem} kb", size=20)
plt.ylabel("Normalized Memory Usage", size=15)
plt.axhline(1, linestyle="--", color="grey")
plt.yscale("log")
plt.tight_layout()
plt.savefig("bench_mem.png", dpi=300)
plt.close()
