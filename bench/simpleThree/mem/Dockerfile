
FROM bench-sysbench

WORKDIR /bench

ENTRYPOINT ["/usr/bin/env", "bash", "-lc", "mkdir -p /results && sysbench memory --threads=4 --time=20 run | tee /results/memory_sysbench.txt"]
