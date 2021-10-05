#!/bin/bash

mkdir -p compiled images

for i in sources/*.txt tests/*.txt; do
	echo "Compiling: $i"
    fstcompile --isymbols=syms.txt --osymbols=syms.txt $i | fstarcsort > compiled/$(basename $i ".txt").fst
done

fstconcat compiled/d2dd.fst compiled/dash.fst | fstconcat - compiled/d2dd.fst  | fstconcat - compiled/dash.fst | fstconcat - compiled/d2dddd.fst | fstrmepsilon > compiled/date2norm.fst
fstconcat compiled/skip.fst compiled/skip.fst | fstconcat - compiled/skip.fst  | fstconcat - compiled/skip.fst | fstconcat - compiled/skip.fst  | fstconcat - compiled/d2dddd.fst  > compiled/date2year.fst
# 2. a)
fstconcat compiled/r2a_milhares.fst compiled/r2a_centenas.fst | fstconcat - compiled/r2a_dezenas.fst | fstconcat - compiled/r2a_unidades.fst > compiled/r2a.fst

# TODO
echo "Testing the transducer 'converter' with the input 'tests/numeroR.txt' (generating pdf)"
fstcompose compiled/numeroR.fst compiled/converter.fst | fstshortestpath > compiled/numeroA.fst
echo "Testing the transducer 'mm2mmm' with the input 'tests/test_mm2mmm.txt' (generating pdf)"
fstcompose compiled/test_mm2mmm.fst compiled/mm2mmm.fst | fstshortestpath > compiled/resp_mm2mmm.fst
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (generating pdf)"
fstcompose compiled/test_d2dd_0.fst compiled/d2dd.fst | fstshortestpath > compiled/resp_d2dd.fst
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (generating pdf)"
fstcompose compiled/test_d2dd_8.fst compiled/d2dd.fst | fstshortestpath > compiled/resp_d2dd.fst
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (generating pdf)"
fstcompose compiled/test_d2dd_13.fst compiled/d2dd.fst | fstshortestpath > compiled/resp_d2dd.fst
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (generating pdf)"
fstcompose compiled/test_d2dd_46.fst compiled/d2dd.fst | fstshortestpath > compiled/resp_d2dd.fst
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (generating pdf)"
fstcompose compiled/test_d2dd_194.fst compiled/d2dd.fst | fstshortestpath > compiled/resp_d2dd.fst
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (generating pdf)"
fstcompose compiled/test_d2dd_2579.fst compiled/d2dd.fst | fstshortestpath > compiled/resp_d2dd.fst
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (generating pdf)"
fstcompose compiled/test_d2dd_97531.fst compiled/d2dd.fst | fstshortestpath > compiled/resp_d2dd.fst
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (generating pdf)"
fstcompose compiled/test_d2dd_0.fst compiled/d2dddd.fst | fstshortestpath > compiled/resp_d2dddd.fst
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (generating pdf)"
fstcompose compiled/test_d2dd_8.fst compiled/d2dddd.fst | fstshortestpath > compiled/resp_d2dddd.fst
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (generating pdf)"
fstcompose compiled/test_d2dd_13.fst compiled/d2dddd.fst | fstshortestpath > compiled/resp_d2dddd.fst
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (generating pdf)"
fstcompose compiled/test_d2dd_46.fst compiled/d2dddd.fst | fstshortestpath > compiled/resp_d2dddd.fst
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (generating pdf)"
fstcompose compiled/test_d2dd_194.fst compiled/d2dddd.fst | fstshortestpath > compiled/resp_d2dddd.fst
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (generating pdf)"
fstcompose compiled/test_d2dd_2579.fst compiled/d2dddd.fst | fstshortestpath > compiled/resp_d2dddd.fst
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (generating pdf)"
fstcompose compiled/test_d2dd_97531.fst compiled/d2dddd.fst | fstshortestpath > compiled/resp_d2dddd.fst
echo "Testing the transducer 'date2norm' with the input 'tests/test_date2norm.txt' (generating pdf)"
fstcompose compiled/test_date2norm_892013.fst compiled/date2norm.fst | fstshortestpath > compiled/resp_date2norm.fst
echo "Testing the transducer 'date2norm' with the input 'tests/test_date2norm.txt' (generating pdf)"
fstcompose compiled/test_date2norm_089900.fst compiled/date2norm.fst | fstshortestpath > compiled/resp_date2norm.fst
echo "Testing the transducer 'date2year' with the input 'compiled/resp_date2norm.fst' (generating pdf)"
fstcompose compiled/resp_date2norm.fst compiled/date2year.fst | fstshortestpath > compiled/resp_date2year.fst
# 2. a)
echo "Testing the transducer 'r2a' with the input 'tests/test_r2a.txt' (generating pdf)"
fstcompose compiled/test_r2a.fst compiled/r2a.fst | fstshortestpath > compiled/resp_r2a.fst

# Creating PDF versions of each transducer
for i in compiled/*.fst; do
	echo "Creating image: images/$(basename $i '.fst').pdf"
    fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/$(basename $i '.fst').pdf
done

# Testing
echo "Testing the transducer 'converter' with the input 'tests/numeroR.txt' (stdout)"
fstcompose compiled/numeroR.fst compiled/converter.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
echo "Testing the transducer 'mm2mmm' with the input 'tests/test_mm2mmm.txt' (stdout)"
fstcompose compiled/test_mm2mmm.fst compiled/mm2mmm.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (stdout)"
fstcompose compiled/test_d2dd_0.fst compiled/d2dd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (stdout)"
fstcompose compiled/test_d2dd_8.fst compiled/d2dd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (stdout)"
fstcompose compiled/test_d2dd_13.fst compiled/d2dd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (stdout)"
fstcompose compiled/test_d2dd_46.fst compiled/d2dd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (stdout)"
fstcompose compiled/test_d2dd_194.fst compiled/d2dd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (stdout)"
fstcompose compiled/test_d2dd_2579.fst compiled/d2dd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (stdout)"
fstcompose compiled/test_d2dd_97531.fst compiled/d2dd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
echo "Testing the transducer 'd2dddd' with the input 'tests/test_d2dd.txt' (stdout)"
fstcompose compiled/test_d2dd_0.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
echo "Testing the transducer 'd2dddd' with the input 'tests/test_d2dd.txt' (stdout)"
fstcompose compiled/test_d2dd_8.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
echo "Testing the transducer 'd2dddd' with the input 'tests/test_d2dd.txt' (stdout)"
fstcompose compiled/test_d2dd_13.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
echo "Testing the transducer 'd2dddd' with the input 'tests/test_d2dd.txt' (stdout)"
fstcompose compiled/test_d2dd_46.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
echo "Testing the transducer 'd2dddd' with the input 'tests/test_d2dd.txt' (stdout)"
fstcompose compiled/test_d2dd_194.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (stdout)"
fstcompose compiled/test_d2dd_2579.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (stdout)"
fstcompose compiled/test_d2dd_97531.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
echo "Testing the transducer 'date2norm' with the input 'tests/test_date2norm_089900.txt' (stdout)"
fstcompose compiled/test_date2norm_089900.fst compiled/date2norm.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
echo "Testing the transducer 'date2norm' with the input 'tests/test_date2norm_892013.txt' (stdout)"
fstcompose compiled/test_date2norm_892013.fst compiled/date2norm.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
echo "Testing the transducer 'date2year' with the input 'compiled/resp_date2norm.fst' (stdout)"
fstcompose compiled/resp_date2norm.fst compiled/date2year.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
# 2. a)
echo "Testing the transducer 'r2a' with the input 'compiled/resp_r2a.fst' (stdout)"
fstcompose compiled/test_r2a.fst compiled/r2a.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
