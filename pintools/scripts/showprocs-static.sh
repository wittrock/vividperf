
# Create the DB
#env LD_LIBRARY_PATH=../wt-dev/build_posix/.libs:../wt-dev/build_posix/ext/compressors/snappy/.libs/  pin.sh  -t $CUSTOM_PINTOOLS_HOME/obj-intel64/showprocs-static.so -o static-procs.out -- ./db_bench_wiredtiger --cache_size=534217728 --threads=1 --use_lsm=0 --db=/tmpfs/leveldb --benchmarks=fillseq,fillseq,fillseq --value_size=62 

# Create the DB
env LD_LIBRARY_PATH=../wt-dev/build_posix/.libs:../wt-dev/build_posix/ext/compressors/snappy/.libs/ ./db_bench_wiredtiger --cache_size=534217728 --threads=1 --use_lsm=0 --db=/tmpfs/leveldb --benchmarks=fillseq --value_size=62 



# Read from the DB sequentially
#env LD_LIBRARY_PATH=../wt-dev/build_posix/.libs:../wt-dev/build_posix/ext/compressors/snappy/.libs/  ./db_bench_wiredtiger --cache_size=534217728  --use_existing_db=1 --threads=1 --use_lsm=0 --db=/tmpfs/leveldb --reads=100000000 --benchmarks=readseq --value_size=62 

# Read from the DB sequentially
#env LD_LIBRARY_PATH=../wt-dev/build_posix/.libs:../wt-dev/build_posix/ext/compressors/snappy/.libs/  pin.sh  -t $CUSTOM_PINTOOLS_HOME/obj-intel64/showprocs-static.so -o static-procs.out --  ./db_bench_wiredtiger --cache_size=534217728  --use_existing_db=1 --threads=1 --use_lsm=0 --db=/tmpfs/leveldb --reads=100000000 --benchmarks=readseq --value_size=62 


# Read from the DB randomly
env LD_LIBRARY_PATH=../wt-dev/build_posix/.libs:../wt-dev/build_posix/ext/compressors/snappy/.libs/  ./db_bench_wiredtiger --cache_size=534217728  --use_existing_db=1 --threads=1 --use_lsm=0 --db=/tmpfs/leveldb --reads=1000000 --benchmarks=readrandom --value_size=62 

# Read from the DB randomly
env LD_LIBRARY_PATH=../wt-dev/build_posix/.libs:../wt-dev/build_posix/ext/compressors/snappy/.libs/  pin.sh  -t $CUSTOM_PINTOOLS_HOME/obj-intel64/procinstr.so -i procs.in --  ./db_bench_wiredtiger --cache_size=534217728  --use_existing_db=1 --threads=1 --use_lsm=0 --db=/tmpfs/leveldb --reads=1000000 --benchmarks=readrandom --value_size=62 
