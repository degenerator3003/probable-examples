FROM bench-sysbench  

WORKDIR /bench

# Same logic that was in docker-compose command, but now inside image
ENTRYPOINT ["/usr/bin/env", "bash", "-lc", "mkdir -p /results && sysbench cpu --threads=4 --time=20 run | tee /results/cpu_sysbench.txt"]

