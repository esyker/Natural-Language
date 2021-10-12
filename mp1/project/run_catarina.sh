#!/bin/bash

mkdir -p compiled images

for i in sources/*.txt tests/*.txt; do
	echo "Compiling: $i"
    fstcompile --isymbols=syms.txt --osymbols=syms.txt $i | fstarcsort > compiled/$(basename $i ".txt").fst
done

echo "Compiling A2R"
fstinvert compiled/R2A.fst > compiled/A2R.fst

echo "Compiling birthR2A"
fstcompose compiled/R2A.fst compiled/d2dd.fst compiled/day.fst
fstcompose compiled/R2A.fst compiled/d2dddd.fst compiled/year.fst
fstconcat compiled/day.fst compiled/copy.fst compiled/day_.fst
fstconcat compiled/day_.fst compiled/day_.fst compiled/month.fst
fstconcat compiled/month.fst compiled/year.fst compiled/birthR2A.fst

echo "Compiling birthA2T"
fstclosure compiled/copy.fst compiled/copy_multiple.fst
fstconcat compiled/copy.fst compiled/copy.fst compiled/copy_day.fst
fstconcat compiled/copy_day.fst compiled/copy.fst compiled/copy_day_.fst
fstconcat compiled/copy_day_.fst compiled/mm2mmm.fst compiled/mmm.fst
fstconcat compiled/mmm.fst compiled/copy_multiple.fst compiled/birthA2T.fst



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

echo "Testing the transducer 'd2dd' with the input 'tests/753.txt' (generating pdf)"
fstcompose compiled/753.fst compiled/d2dd.fst | fstshortestpath > compiled/d2dd_753.fst

echo "Testing the transducer 'd2dd' with the input 'tests/8000.txt' (generating pdf)"
fstcompose compiled/8000.fst compiled/d2dd.fst | fstshortestpath > compiled/d2dd_8000.fst

echo "Testing the transducer 'd2dd' with the input 'tests/876543.txt' (generating pdf)"
fstcompose compiled/876543.fst compiled/d2dd.fst | fstshortestpath > compiled/d2dd_876543.fst


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

echo "Testing the transducer 'd2dddd' with the input 'tests/876543.txt' (generating pdf)"
fstcompose compiled/876543.fst compiled/d2dddd.fst | fstshortestpath > compiled/d2dddd_876543.fst


echo "Testing the transducer 'copy' with the input 'tests/8.txt' (generating pdf)"
fstcompose compiled/8.fst compiled/copy.fst | fstshortestpath > compiled/copy_8.fst

echo "Testing the transducer 'copy' with the input 'tests/62.txt' (generating pdf)"
fstcompose compiled/62.fst compiled/copy.fst | fstshortestpath > compiled/copy_62.fst


echo "Testing the transducer 'skip' with the input 'tests/8.txt' (generating pdf)"
fstcompose compiled/8.fst compiled/skip.fst | fstshortestpath > compiled/skip_8.fst

echo "Testing the transducer 'skip' with the input 'tests/62.txt' (generating pdf)"
fstcompose compiled/62.fst compiled/skip.fst | fstshortestpath > compiled/skip_62.fst


echo "Testing the transducer 'date2year' with the input 'tests/08_09_2013.txt' (generating pdf)"
fstcompose compiled/08_09_2013.fst compiled/date2year.fst | fstshortestpath > compiled/date2year_08_09_2013.fst


echo "Testing the transducer 'leap' with the input 'tests/1901.txt' (generating pdf)"
fstcompose compiled/1901.fst compiled/leap.fst | fstshortestpath > compiled/leap_1901.fst

echo "Testing the transducer 'leap' with the input 'tests/1904.txt' (generating pdf)"
fstcompose compiled/1904.fst compiled/leap.fst | fstshortestpath > compiled/leap_1904.fst

echo "Testing the transducer 'leap' with the input 'tests/2000.txt' (generating pdf)"
fstcompose compiled/2000.fst compiled/leap.fst | fstshortestpath > compiled/leap_2000.fst

echo "Testing the transducer 'leap' with the input 'tests/2099.txt' (generating pdf)"
fstcompose compiled/2099.fst compiled/leap.fst | fstshortestpath > compiled/leap_2099.fst


echo "Testing the transducer 'R2A' with the input 'tests/I.txt' (generating pdf)"
fstcompose compiled/I.fst compiled/R2A.fst | fstshortestpath > compiled/r2a_I.fst

echo "Testing the transducer 'R2A' with the input 'tests/XL.txt' (generating pdf)"
fstcompose compiled/XL.fst compiled/R2A.fst | fstshortestpath > compiled/r2a_XL.fst

echo "Testing the transducer 'R2A' with the input 'tests/CM.txt' (generating pdf)"
fstcompose compiled/CM.fst compiled/R2A.fst | fstshortestpath > compiled/r2a_CM.fst

echo "Testing the transducer 'R2A' with the input 'tests/VIII.txt' (generating pdf)"
fstcompose compiled/VIII.fst compiled/R2A.fst | fstshortestpath > compiled/r2a_VIII.fst

echo "Testing the transducer 'R2A' with the input 'tests/CIX.txt' (generating pdf)"
fstcompose compiled/CIX.fst compiled/R2A.fst | fstshortestpath > compiled/r2a_CIX.fst

echo "Testing the transducer 'R2A' with the input 'tests/MMXIII.txt' (generating pdf)"
fstcompose compiled/MMXIII.fst compiled/R2A.fst | fstshortestpath > compiled/r2a_MMXIII.fst

echo "Testing the transducer 'R2A' with the input 'tests/MMMCMXCIX.txt' (generating pdf)"
fstcompose compiled/MMMCMXCIX.fst compiled/R2A.fst | fstshortestpath > compiled/r2a_MMMCMXCIX.fst


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

echo "Testing the transducer 'd2dd' with the input 'tests/753.txt' (stdout)"
fstcompose compiled/753.fst compiled/d2dd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dd' with the input 'tests/8000.txt' (stdout)"
fstcompose compiled/8000.fst compiled/d2dd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dd' with the input 'tests/876543.txt' (stdout)"
fstcompose compiled/876543.fst compiled/d2dd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt


echo "Testing the transducer 'd2dddd' with the input 'tests/8.txt' (stdout)"
fstcompose compiled/8.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dddd' with the input 'tests/08.txt' (stdout)"
fstcompose compiled/08.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dddd' with the input 'tests/62.txt' (stdout)"
fstcompose compiled/62.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dddd' with the input 'tests/753.txt' (stdout)"
fstcompose compiled/753.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dddd' with the input 'tests/313.txt' (stdout)"
fstcompose compiled/313.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dddd' with the input 'tests/8000.txt' (stdout)"
fstcompose compiled/8000.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dddd' with the input 'tests/876543.txt' (stdout)"
fstcompose compiled/876543.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt


echo "Testing the transducer 'copy' with the input 'tests/8.txt' (stdout)"
fstcompose compiled/8.fst compiled/copy.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'copy' with the input 'tests/62.txt' (stdout)"
fstcompose compiled/62.fst compiled/copy.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt


echo "Testing the transducer 'skip' with the input 'tests/skip.txt' (stdout)"
fstcompose compiled/test_skip.fst compiled/skip.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'skip' with the input 'tests/8.txt' (stdout)"
fstcompose compiled/8.fst compiled/skip.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'skip' with the input 'tests/62.txt' (stdout)"
fstcompose compiled/62.fst compiled/skip.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt


echo "Testing the transducer 'date2year' with the input 'tests/08_09_2013.txt' (stdout)"
fstcompose compiled/08_09_2013.fst compiled/date2year.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt


echo "Testing the transducer 'leap' with the input 'tests/1901.txt' (stdout)"
fstcompose compiled/1901.fst compiled/leap.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'leap' with the input 'tests/1904.txt' (stdout)"
fstcompose compiled/1904.fst compiled/leap.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'leap' with the input 'tests/2000.txt' (stdout)"
fstcompose compiled/2000.fst compiled/leap.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'leap' with the input 'tests/2099.txt' (stdout)"
fstcompose compiled/2099.fst compiled/leap.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt


echo "Testing the transducer 'R2A' with the input 'tests/I.txt' (stdout)"
fstcompose compiled/I.fst compiled/R2A.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'R2A' with the input 'tests/XL.txt' (stdout)"
fstcompose compiled/XL.fst compiled/R2A.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'R2A' with the input 'tests/CM.txt' (stdout)"
fstcompose compiled/CM.fst compiled/R2A.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'R2A' with the input 'tests/VIII.txt' (stdout)"
fstcompose compiled/VIII.fst compiled/R2A.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'R2A' with the input 'tests/CIX.txt' (stdout)"
fstcompose compiled/CIX.fst compiled/R2A.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'R2A' with the input 'tests/MMXIII.txt' (stdout)"
fstcompose compiled/MMXIII.fst compiled/R2A.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'R2A' with the input 'tests/MMMCMXCIX.txt' (stdout)"
fstcompose compiled/MMMCMXCIX.fst compiled/R2A.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt


echo "Testing the transducer 'A2R' with the input 'tests/8.txt' (stdout)"
fstcompose compiled/8.fst compiled/A2R.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'A2R' with the input 'tests/109.txt' (stdout)"
fstcompose compiled/109.fst compiled/A2R.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'A2R' with the input 'tests/2013.txt' (stdout)"
fstcompose compiled/2013.fst compiled/A2R.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'A2R' with the input 'tests/3999.txt' (stdout)"
fstcompose compiled/3999.fst compiled/A2R.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt


echo "Testing the transducer 'birthR2A' with the input 'tests/VIII.txt' (stdout)"
fstcompose compiled/VIII_IX_CCCXIII.fst compiled/birthR2A.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt


echo "Testing the transducer 'birthA2T' with the input 'tests/08_09_0313.txt' (stdout)"
fstcompose compiled/08_09_0313.fst compiled/birthA2T.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

