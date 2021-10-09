#!/bin/bash

mkdir -p compiled images

for i in sources/*.txt tests/*.txt; do
	echo "Compiling: $i"
    fstcompile --isymbols=syms.txt --osymbols=syms.txt $i | fstarcsort > compiled/$(basename $i ".txt").fst
done


# TODO

echo "Testing the transducer 'mm2mmm' with the input 'tests/test_mm2mmm.txt' (generating pdf)"
fstcompose compiled/test_mm2mmm.fst compiled/mm2mmm.fst | fstshortestpath > compiled/result_mm2mmm.fst

echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (generating pdf)"
fstcompose compiled/test_d2dd.fst compiled/d2dd.fst | fstshortestpath > compiled/result_d2dd.fst

echo "Testing the transducer 'd2dd' with the input 'tests/8.txt' (generating pdf)"
fstcompose compiled/8.fst compiled/d2dd.fst | fstshortestpath > compiled/d2dd_8.fst

echo "Testing the transducer 'd2dd' with the input 'tests/08.txt' (generating pdf)"
fstcompose compiled/08.fst compiled/d2dd.fst | fstshortestpath > compiled/d2dd_08.fst

echo "Testing the transducer 'd2dd' with the input 'tests/62.txt' (generating pdf)"
fstcompose compiled/62.fst compiled/d2dd.fst | fstshortestpath > compiled/d2dd_62.fst

echo "Testing the transducer 'd2dddd' with the input 'tests/8.txt' (generating pdf)"
fstcompose compiled/8.fst compiled/d2dddd.fst | fstshortestpath > compiled/d2dddd_8.fst

echo "Testing the transducer 'd2dddd' with the input 'tests/08.txt' (generating pdf)"
fstcompose compiled/08.fst compiled/d2dddd.fst | fstshortestpath > compiled/d2dddd_08.fst

echo "Testing the transducer 'd2dddd' with the input 'tests/62.txt' (generating pdf)"
fstcompose compiled/62.fst compiled/d2dddd.fst | fstshortestpath > compiled/d2dddd_62.fst

echo "Testing the transducer 'd2dddd' with the input 'tests/753.txt' (generating pdf)"
fstcompose compiled/753.fst compiled/d2dddd.fst | fstshortestpath > compiled/d2dddd_753.fst

echo "Testing the transducer 'd2dddd' with the input 'tests/8000.txt' (generating pdf)"
fstcompose compiled/8000.fst compiled/d2dddd.fst | fstshortestpath > compiled/d2dddd_8000.fst

echo "Testing the transducer 'copy' with the input 'tests/8.txt' (generating pdf)"
fstcompose compiled/8.fst compiled/copy.fst | fstshortestpath > compiled/copy_8.fst

echo "Testing the transducer 'copy' with the input 'tests/62.txt' (generating pdf)"
fstcompose compiled/62.fst compiled/copy.fst | fstshortestpath > compiled/copy_62.fst



for i in compiled/*.fst; do
	echo "Creating image: images/$(basename $i '.fst').pdf"
    fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/$(basename $i '.fst').pdf
done

echo "Testing the transducer 'mm2mmm' with the input 'tests/test_mm2mmm.txt' (stdout)"
fstcompose compiled/test_mm2mmm.fst compiled/mm2mmm.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt


echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (stdout)"
fstcompose compiled/test_d2dd.fst compiled/d2dd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dd' with the input 'tests/8.txt' (stdout)"
fstcompose compiled/8.fst compiled/d2dd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dd' with the input 'tests/08.txt' (stdout)"
fstcompose compiled/08.fst compiled/d2dd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dd' with the input 'tests/62.txt' (stdout)"
fstcompose compiled/62.fst compiled/d2dd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dddd' with the input 'tests/8.txt' (stdout)"
fstcompose compiled/8.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dddd' with the input 'tests/08.txt' (stdout)"
fstcompose compiled/08.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dddd' with the input 'tests/62.txt' (stdout)"
fstcompose compiled/62.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dddd' with the input 'tests/753.txt' (stdout)"
fstcompose compiled/753.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dddd' with the input 'tests/8000.txt' (stdout)"
fstcompose compiled/8000.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'copy' with the input 'tests/8.txt' (stdout)"
fstcompose compiled/8.fst compiled/copy.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'copy' with the input 'tests/62.txt' (stdout)"
fstcompose compiled/62.fst compiled/copy.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'skip' with the input 'tests/skip.txt' (stdout)"
fstcompose compiled/test_skip.fst compiled/skip.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt