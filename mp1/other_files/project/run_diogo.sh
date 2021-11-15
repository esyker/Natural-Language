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

echo "Compiling birthT2R"
fstinvert compiled/mm2mmm.fst > compiled/mmm2mm.fst
fstinvert compiled/d2dd.fst > compiled/dd2d.fst
fstinvert compiled/d2dddd.fst > compiled/dddd2d.fst
fstcompose compiled/dd2d.fst compiled/A2R.fst compiled/dd2R.fst
fstcompose compiled/dddd2d.fst compiled/A2R.fst compiled/dddd2R.fst
fstcompose compiled/mmm2mm.fst compiled/dd2R.fst compiled/mmm2R.fst
fstconcat compiled/dd2R.fst compiled/copy.fst compiled/day_.fst
fstconcat compiled/mmm2R.fst compiled/copy.fst compiled/month_.fst
fstconcat compiled/day_.fst compiled/month_.fst compiled/day_month_.fst
fstconcat compiled/day_month_.fst compiled/dddd2R.fst compiled/birthT2R.fst

echo "Compiling birthR2L"
fstcompose compiled/birthR2A.fst compiled/date2year.fst compiled/birthR2year.fst
fstcompose compiled/birthR2year.fst compiled/leap.fst compiled/birthR2L.fst

# TODO

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
fstcompose compiled/I.fst compiled/R2A.fst | fstshortestpath > compiled/R2A_I.fst

echo "Testing the transducer 'R2A' with the input 'tests/XL.txt' (generating pdf)"
fstcompose compiled/XL.fst compiled/R2A.fst | fstshortestpath > compiled/R2A_XL.fst

echo "Testing the transducer 'R2A' with the input 'tests/CM.txt' (generating pdf)"
fstcompose compiled/CM.fst compiled/R2A.fst | fstshortestpath > compiled/R2A_CM.fst

echo "Testing the transducer 'R2A' with the input 'tests/VIII.txt' (generating pdf)"
fstcompose compiled/VIII.fst compiled/R2A.fst | fstshortestpath > compiled/R2A_VIII.fst

echo "Testing the transducer 'R2A' with the input 'tests/CIX.txt' (generating pdf)"
fstcompose compiled/CIX.fst compiled/R2A.fst | fstshortestpath > compiled/R2A_CIX.fst

echo "Testing the transducer 'R2A' with the input 'tests/MMXIII.txt' (generating pdf)"
fstcompose compiled/MMXIII.fst compiled/R2A.fst | fstshortestpath > compiled/R2A_MMXIII.fst

echo "Testing the transducer 'R2A' with the input 'tests/MMMCMXCIX.txt' (generating pdf)"
fstcompose compiled/MMMCMXCIX.fst compiled/R2A.fst | fstshortestpath > compiled/R2A_MMMCMXCIX.fst

echo "Testing the transducer 'A2R' with the input 'tests/8.txt' (generating pdf)"
fstcompose compiled/8.fst compiled/A2R.fst | fstshortestpath > compiled/A2R_8.fst

echo "Testing the transducer 'A2R' with the input 'tests/109.txt' (generating pdf)"
fstcompose compiled/109.fst compiled/A2R.fst | fstshortestpath > compiled/A2R_109.fst

echo "Testing the transducer 'A2R' with the input 'tests/2013.txt' (generating pdf)"
fstcompose compiled/2013.fst compiled/A2R.fst | fstshortestpath > compiled/A2R_2013.fst

echo "Testing the transducer 'A2R' with the input 'tests/3999.txt' (generating pdf)"
fstcompose compiled/3999.fst compiled/A2R.fst | fstshortestpath > compiled/A2R_3999.fst

echo "Testing the transducer 'birthR2A' with the input 'tests/VIII.txt' (generating pdf)"
fstcompose compiled/VIII_IX_CCCXIII.fst compiled/birthR2A.fst | fstshortestpath > compiled/birthR2A_VIII.fst

echo "Testing the transducer 'birthA2T' with the input 'tests/08_09_0313.txt' (generating pdf)"
fstcompose compiled/08_09_0313.fst compiled/birthA2T.fst | fstshortestpath > compiled/birthA2T_08_09_0313.fst

echo "Testing the transducer 'birthR2L' with the input 'tests/IV_V_MMMCMXCIX.txt' (generating pdf)"
fstcompose compiled/IV_V_MMMCMXCIX.fst compiled/birthR2L.fst | fstshortestpath > compiled/birthR2L_IV_V_MMMCMXCIX.fst

echo "Testing the transducer 'birthR2A' with the input 'tests/86976birthR2A.txt' (generating pdf)"
fstcompose compiled/86976birthR2A.fst compiled/birthR2A.fst | fstshortestpath > compiled/birthR2A_86976birthR2A.fst

echo "Testing the transducer 'birthR2A' with the input 'tests/89423birthR2A.txt' (generating pdf)"
fstcompose compiled/89423birthR2A.fst compiled/birthR2A.fst | fstshortestpath > compiled/birthR2A_89423birthR2A.fst

echo "Testing the transducer 'birthA2T' with the input 'tests/86976birthA2T.txt' (generating pdf)"
fstcompose compiled/86976birthA2T.fst compiled/birthA2T.fst | fstshortestpath > compiled/birthA2T_86976birthA2T.fst

echo "Testing the transducer 'birthA2T' with the input 'tests/89423birthA2T.txt' (generating pdf)"
fstcompose compiled/89423birthA2T.fst compiled/birthA2T.fst | fstshortestpath > compiled/birthA2T_894223birthT2R.fst

echo "Testing the transducer 'birthT2R' with the input 'tests/86976birthT2R.txt' (generating pdf)"
fstcompose compiled/86976birthT2R.fst compiled/birthT2R.fst | fstshortestpath  > compiled/birthT2R_86876birthT2R.fst

echo "Testing the transducer 'birthT2R' with the input 'tests/89423birthT2R.txt' (generating pdf)"
fstcompose compiled/89423birthT2R.fst compiled/birthT2R.fst | fstshortestpath  > compiled/birthT2R_894223birthT2R.fst

echo "Testing the transducer 'birthR2L' with the input 'tests/86976birthR2L.txt' (generating pdf)"
fstcompose compiled/86976birthR2L.fst compiled/birthR2L.fst | fstshortestpath  > compiled/birthR2L_86976birthR2L.fst

echo "Testing the transducer 'birthR2L' with the input 'tests/89423birthR2L.txt' (generating pdf)"
fstcompose compiled/89423birthR2L.fst compiled/birthR2L.fst | fstshortestpath  > compiled/birthR2L_894223birthR2L.fst

for i in compiled/*.fst; do
	echo "Creating image: images/$(basename $i '.fst').pdf"
    fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/$(basename $i '.fst').pdf
done

echo "Testing the transducer 'd2dd' with the input 'tests/8.txt' (stdout)"
fstcompose compiled/8.fst compiled/d2dd.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dd' with the input 'tests/08.txt' (stdout)"
fstcompose compiled/08.fst compiled/d2dd.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dd' with the input 'tests/62.txt' (stdout)"
fstcompose compiled/62.fst compiled/d2dd.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dd' with the input 'tests/753.txt' (stdout)"
fstcompose compiled/753.fst compiled/d2dd.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dd' with the input 'tests/8000.txt' (stdout)"
fstcompose compiled/8000.fst compiled/d2dd.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dd' with the input 'tests/876543.txt' (stdout)"
fstcompose compiled/876543.fst compiled/d2dd.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dddd' with the input 'tests/8.txt' (stdout)"
fstcompose compiled/8.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dddd' with the input 'tests/08.txt' (stdout)"
fstcompose compiled/08.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dddd' with the input 'tests/62.txt' (stdout)"
fstcompose compiled/62.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dddd' with the input 'tests/753.txt' (stdout)"
fstcompose compiled/753.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dddd' with the input 'tests/8000.txt' (stdout)"
fstcompose compiled/8000.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'd2dddd' with the input 'tests/876543.txt' (stdout)"
fstcompose compiled/876543.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt


echo "Testing the transducer 'copy' with the input 'tests/8.txt' (stdout)"
fstcompose compiled/8.fst compiled/copy.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'copy' with the input 'tests/62.txt' (stdout)"
fstcompose compiled/62.fst compiled/copy.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'skip' with the input 'tests/8.txt' (stdout)"
fstcompose compiled/8.fst compiled/skip.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'skip' with the input 'tests/62.txt' (stdout)"
fstcompose compiled/62.fst compiled/skip.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt


echo "Testing the transducer 'date2year' with the input 'tests/08_09_2013.txt' (stdout)"
fstcompose compiled/08_09_2013.fst compiled/date2year.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt


echo "Testing the transducer 'leap' with the input 'tests/1901.txt' (stdout)"
fstcompose compiled/1901.fst compiled/leap.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'leap' with the input 'tests/1904.txt' (stdout)"
fstcompose compiled/1904.fst compiled/leap.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'leap' with the input 'tests/2000.txt' (stdout)"
fstcompose compiled/2000.fst compiled/leap.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'leap' with the input 'tests/2099.txt' (stdout)"
fstcompose compiled/2099.fst compiled/leap.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt


echo "Testing the transducer 'R2A' with the input 'tests/I.txt' (stdout)"
fstcompose compiled/I.fst compiled/R2A.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'R2A' with the input 'tests/XL.txt' (stdout)"
fstcompose compiled/XL.fst compiled/R2A.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'R2A' with the input 'tests/CM.txt' (stdout)"
fstcompose compiled/CM.fst compiled/R2A.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'R2A' with the input 'tests/VIII.txt' (stdout)"
fstcompose compiled/VIII.fst compiled/R2A.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'R2A' with the input 'tests/CIX.txt' (stdout)"
fstcompose compiled/CIX.fst compiled/R2A.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'R2A' with the input 'tests/MMXIII.txt' (stdout)"
fstcompose compiled/MMXIII.fst compiled/R2A.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'R2A' with the input 'tests/MMMCMXCIX.txt' (stdout)"
fstcompose compiled/MMMCMXCIX.fst compiled/R2A.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt


echo "Testing the transducer 'A2R' with the input 'tests/8.txt' (stdout)"
fstcompose compiled/8.fst compiled/A2R.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'A2R' with the input 'tests/109.txt' (stdout)"
fstcompose compiled/109.fst compiled/A2R.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'A2R' with the input 'tests/2013.txt' (stdout)"
fstcompose compiled/2013.fst compiled/A2R.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'A2R' with the input 'tests/3999.txt' (stdout)"
fstcompose compiled/3999.fst compiled/A2R.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt


echo "Testing the transducer 'birthR2A' with the input 'tests/VIII_IX_CCCXIII.txt' (stdout)"
fstcompose compiled/VIII_IX_CCCXIII.fst compiled/birthR2A.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt


echo "Testing the transducer 'birthA2T' with the input 'tests/08_09_0313.txt' (stdout)"
fstcompose compiled/08_09_0313.fst compiled/birthA2T.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'birthR2L' with the input 'tests/IV_V_MMMCMXCIX.txt' (stdout)"
fstcompose compiled/IV_V_MMMCMXCIX.fst compiled/birthR2L.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'birthR2A' with the input 'tests/86976birthR2A.txt' (stdout)"
fstcompose compiled/86976birthR2A.fst compiled/birthR2A.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'birthR2A' with the input 'tests/89423birthR2A.txt' (stdout)"
fstcompose compiled/89423birthR2A.fst compiled/birthR2A.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'birthA2T' with the input 'tests/86976birthA2T.txt' (stdout)"
fstcompose compiled/86976birthA2T.fst compiled/birthA2T.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'birthA2T' with the input 'tests/89423birthA2T.txt' (stdout)"
fstcompose compiled/89423birthA2T.fst compiled/birthA2T.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'birthT2R' with the input 'tests/86976birthT2R.txt' (stdout)"
fstcompose compiled/86976birthT2R.fst compiled/birthT2R.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'birthT2R' with the input 'tests/89423birthT2R.txt' (stdout)"
fstcompose compiled/89423birthT2R.fst compiled/birthT2R.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'birthR2L' with the input 'tests/86976birthR2L.txt' (stdout)"
fstcompose compiled/86976birthR2L.fst compiled/birthR2L.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

echo "Testing the transducer 'birthR2L' with the input 'tests/89423birthR2L.txt' (stdout)"
fstcompose compiled/89423birthR2L.fst compiled/birthR2L.fst | fstshortestpath | fstproject --project_output=true | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
