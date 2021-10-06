#!/bin/bash

mkdir -p compiled images

for i in sources/*.txt tests/*.txt; do
	echo "Compiling: $i"
    fstcompile --isymbols=syms.txt --osymbols=syms.txt $i | fstarcsort > compiled/$(basename $i ".txt").fst
done

# 1. e)
fstconcat compiled/d2dd.fst compiled/dash.fst | fstconcat - compiled/d2dd.fst  | fstconcat - compiled/dash.fst | fstconcat - compiled/d2dddd.fst | fstrmepsilon > compiled/date2norm.fst
# 1. d)
fstconcat compiled/skip.fst compiled/skip.fst | fstconcat - compiled/skip.fst  | fstconcat - compiled/skip.fst | fstconcat - compiled/skip.fst  | fstconcat - compiled/d2dddd.fst  > compiled/date2year.fst

# 2. a)
fstconcat compiled/r2a_milhares.fst compiled/r2a_centenas.fst | fstconcat - compiled/r2a_dezenas.fst | fstconcat - compiled/r2a_unidades.fst > compiled/r2a.fst
# 2. b)
fstconcat compiled/a2r_milhares.fst compiled/a2r_centenas.fst | fstconcat - compiled/a2r_dezenas.fst | fstconcat - compiled/a2r_unidades.fst > compiled/a2r_num_milhares.fst
fstconcat compiled/a2r_centenas.fst compiled/a2r_dezenas.fst | fstconcat - compiled/a2r_unidades.fst > compiled/a2r_num_centenas.fst
fstconcat compiled/a2r_dezenas.fst compiled/a2r_unidades.fst > compiled/a2r_num_dezenas.fst
fstunion compiled/a2r_num_milhares.fst compiled/a2r_num_centenas.fst | fstunion - compiled/a2r_num_dezenas.fst | fstunion - compiled/a2r_unidades.fst > compiled/a2r.fst

# 3. a)
fstconcat compiled/d2dd.fst compiled/dash.fst | fstconcat - compiled/mm2mmm.fst | fstconcat - compiled/dash.fst | fstconcat - compiled/d2dddd.fst > compiled/date_a2t.fst
# 3. b)
fstconcat compiled/r2a.fst compiled/dash.fst | fstconcat - compiled/r2a.fst | fstconcat - compiled/dash.fst | fstconcat - compiled/r2a.fst > compiled/date_r2a.fst
# 3. b)
fstinvert compiled/mm2mmm.fst | fstcompose - compiled/a2r.fst > compiled/mmm2r.fst
fstconcat compiled/a2r.fst compiled/dash.fst | fstconcat - compiled/mmm2r.fst | fstconcat - compiled/dash.fst | fstconcat - compiled/a2r.fst > compiled/date_t2r.fst

# 1. a)
echo "Testing the transducer 'mm2mmm' with the input 'tests/test_mm2mmm.txt' (generating pdf)"
fstcompose compiled/test_mm2mmm.fst compiled/mm2mmm.fst | fstshortestpath > compiled/resp_mm2mmm.fst
# 1. b)
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd_8.txt' (generating pdf)"
fstcompose compiled/test_d2dd_8.fst compiled/d2dd.fst | fstshortestpath > compiled/resp_d2dd.fst
# 1. c)
echo "Testing the transducer 'd2dddd' with the input 'tests/test_d2dd_8.txt' (generating pdf)"
fstcompose compiled/test_d2dd_8.fst compiled/d2dddd.fst | fstshortestpath > compiled/resp_d2dddd.fst
# 1. e)
echo "Testing the transducer 'date2norm' with the input 'tests/test_date2norm_892013.txt' (generating pdf)"
fstcompose compiled/test_date2norm_892013.fst compiled/date2norm.fst | fstshortestpath > compiled/resp_date2norm.fst
# 1. d)
echo "Testing the transducer 'date2year' with the input 'compiled/resp_date2norm.fst' (generating pdf)"
fstcompose compiled/resp_date2norm.fst compiled/date2year.fst | fstshortestpath > compiled/resp_date2year.fst

# 2. a)
echo "Testing the transducer 'r2a' with the input 'tests/test_r2a.txt' (generating pdf)"
fstcompose compiled/test_r2a.fst compiled/r2a.fst | fstshortestpath > compiled/resp_r2a.fst
# 2. b)
echo "Testing the transducer 'a2r' with the input 'tests/test_a2r.txt' (generating pdf)"
fstcompose compiled/test_a2r.fst compiled/a2r.fst | fstshortestpath > compiled/resp_a2r.fst

# 3. a)
echo "Testing the transducer 'date_a2t' with the input 'tests/date_a2t.txt' (generating pdf)"
fstcompose compiled/95000a.fst compiled/date_a2t.fst | fstshortestpath > compiled/95000_date_a2t.fst
# 3. b)
echo "Testing the transducer 'date_r2a' with the input 'tests/date_a2t.txt' (generating pdf)"
fstcompose compiled/95000b.fst compiled/date_r2a.fst | fstshortestpath > compiled/95000_date_r2a.fst
# 3. c)
echo "Testing the transducer 'date_t2r' with the input 'tests/date_t2r.txt' (generating pdf)"
fstcompose compiled/95000c.fst compiled/date_t2r.fst | fstshortestpath > compiled/95000_date_t2r.fst

# Creating PDF versions of each transducer
for i in compiled/*.fst; do
	echo "Creating image: images/$(basename $i '.fst').pdf"
    fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/$(basename $i '.fst').pdf
done

# 1. a)
echo "Testing the transducer 'mm2mmm' with the input 'tests/test_mm2mmm.txt' (stdout)"
fstcompose compiled/test_mm2mmm.fst compiled/mm2mmm.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
# 1. b)
echo "Testing the transducer 'd2dd' with the input 'tests/test_d2dd.txt' (stdout)"
fstcompose compiled/test_d2dd_8.fst compiled/d2dd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
# 1. c)
echo "Testing the transducer 'd2dddd' with the input 'tests/test_d2dd_8.txt' (stdout)"
fstcompose compiled/test_d2dd_8.fst compiled/d2dddd.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
# 1. e)
echo "Testing the transducer 'date2norm' with the input 'tests/test_date2norm_892013.txt' (stdout)"
fstcompose compiled/test_date2norm_892013.fst compiled/date2norm.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
# 1. d)
echo "Testing the transducer 'date2year' with the input 'compiled/resp_date2norm.fst' (stdout)"
fstcompose compiled/resp_date2norm.fst compiled/date2year.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

# 2. a)
echo "Testing the transducer 'r2a' with the input 'tests/test_r2a.txt' (stdout)"
fstcompose compiled/test_r2a.fst compiled/r2a.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
# 2. b)
echo "Testing the transducer 'a2r' with the input 'tests/test_a2r.txt' (stdout)"
fstcompose compiled/test_a2r.fst compiled/a2r.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt

# 3. a)
echo "Testing the transducer 'date_a2t' with the input 'tests/date_a2t.txt' (stdout)"
fstcompose compiled/95000a.fst compiled/date_a2t.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
# 3. b)
echo "Testing the transducer 'date_r2a' with the input 'tests/test_a2r.txt' (stdout)"
fstcompose compiled/95000b.fst compiled/date_r2a.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
# 3. c)
echo "Testing the transducer 'date_t2r' with the input 'tests/date_t2r.txt' (stdout)"
fstcompose compiled/95000c.fst compiled/date_t2r.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
