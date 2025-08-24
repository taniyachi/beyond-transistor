# beyond-transistor
software implementation of multiple LUT device architecture .
1-Install theses packages before running the tests:
sudo apt-get install libbz2-dev libdivsufsort-dev libjsoncpp-dev libssl-dev libmpfr-dev
2- then git clone
3- cd directory
4- cd cpp
5- make
6- mkdir test
7- make iid
8- ./ea_iid -i -v -l 0,1000000 tests/bits1m.bin > result.txt
9- ./ea_non_iid -i -v -l 0,1000000 tests/bits1m.bin > result_noniid.txt
results of IID tests are to ensure while results of non-IID assumps the worst case, each will give a numerical value between 0 and 1; the closer it gets to 1 indicates the strength of entropy in the TRNG design.
