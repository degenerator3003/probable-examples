# i1: base OS
FROM ubuntu:24.04

# i2: base + tools for benchmarks
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        sysbench \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Default shell
SHELL ["/bin/bash", "-lc"]

