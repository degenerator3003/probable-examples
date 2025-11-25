
FROM bench-sysbench

WORKDIR /bench

ENTRYPOINT ["/usr/bin/env", "bash", "-lc", "mkdir -p /results && dd if=/dev/zero of=/results/testfile.bin bs=4M count=512 conv=fdatasync 2> /results/disk_dd.txt"]
