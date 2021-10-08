#!/bin/bash

mkdir -p compiled images compiled/tests images/tests

for i in sources/*.txt; do
	echo "Compiling: $i"
    fstcompile --isymbols=syms.txt --osymbols=syms.txt $i | fstarcsort > compiled/$(basename $i ".txt").fst
done

# 1. d) Creating date2year
echo "Creating date2year"
fstconcat compiled/skip.fst compiled/skip.fst | fstconcat - compiled/skip.fst  | fstconcat - compiled/skip.fst | fstconcat - compiled/skip.fst | fstconcat - compiled/skip.fst | fstconcat - compiled/d2dddd.fst  > compiled/date2year.fst

# # 1. e) Creating date2norm
echo "Creating date2norm"
fstconcat compiled/d2dd.fst compiled/dash.fst | fstconcat - compiled/d2dd.fst  | fstconcat - compiled/dash.fst | fstconcat - compiled/d2dddd.fst | fstrmepsilon > compiled/date2norm.fst

# 1. f) Creating bissexto
echo "Creating bissexto"
fstconcat compiled/bissexto_4multiplesupto99.fst compiled/bissexto_skipdoublezero.fst | fstconcat - compiled/bissexto_yes.fst | fstrmepsilon > compiled/bissexto_400multiples.fst
fstconcat compiled/bissexto_skip.fst compiled/bissexto_skip.fst | fstconcat - compiled/bissexto_4multiplesupto99.fst | fstconcat - compiled/bissexto_yes.fst | fstrmepsilon > compiled/bissexto_4multiples.fst
fstconcat compiled/bissexto_negative4multiplesupto99.fst compiled/bissexto_skipdoublezero.fst | fstconcat - compiled/bissexto_no.fst | fstrmepsilon > compiled/bissexto_non400multiples.fst
fstconcat compiled/bissexto_skip.fst compiled/bissexto_skip.fst | fstconcat - compiled/bissexto_negative4multiplesupto99.fst | fstconcat - compiled/bissexto_no.fst | fstrmepsilon > compiled/bissexto_non4multiples.fst
fstunion compiled/bissexto_400multiples.fst compiled/bissexto_4multiples.fst | fstunion - compiled/bissexto_non400multiples.fst | fstunion - compiled/bissexto_non4multiples.fst | fstrmepsilon > compiled/bissexto.fst

# 2. a) Creating r2a
echo "Creating r2a"
fstunion compiled/r2a_centenas.fst compiled/r2a_zero.fst | fstrmepsilon > compiled/r2a_centenas_zero.fst
fstunion compiled/r2a_dezenas.fst compiled/r2a_zero.fst | fstrmepsilon > compiled/r2a_dezenas_zero.fst
fstunion compiled/r2a_unidades.fst compiled/r2a_zero.fst | fstrmepsilon > compiled/r2a_unidades_zero.fst
fstconcat compiled/r2a_milhares.fst compiled/r2a_centenas_zero.fst | fstconcat - compiled/r2a_dezenas_zero.fst | fstconcat - compiled/r2a_unidades_zero.fst | fstrmepsilon > compiled/r2a_trans_milhares.fst
fstconcat compiled/r2a_centenas.fst compiled/r2a_dezenas_zero.fst | fstconcat - compiled/r2a_unidades_zero.fst | fstrmepsilon > compiled/r2a_trans_centenas.fst
fstconcat compiled/r2a_dezenas.fst compiled/r2a_unidades_zero.fst | fstrmepsilon > compiled/r2a_trans_dezenas.fst
fstunion compiled/r2a_trans_milhares.fst compiled/r2a_trans_centenas.fst | fstunion - compiled/r2a_trans_dezenas.fst  | fstunion - compiled/r2a_unidades.fst | fstrmepsilon > compiled/r2a.fst

# 2. b) Creating a2r
echo "Creating a2r"
fstconcat compiled/a2r_milhares.fst compiled/a2r_centenas.fst | fstconcat - compiled/a2r_dezenas.fst | fstconcat - compiled/a2r_unidades.fst > compiled/a2r_num_milhares.fst
fstconcat compiled/a2r_centenas.fst compiled/a2r_dezenas.fst | fstconcat - compiled/a2r_unidades.fst > compiled/a2r_num_centenas.fst
fstconcat compiled/a2r_dezenas.fst compiled/a2r_unidades.fst > compiled/a2r_num_dezenas.fst
fstunion compiled/a2r_num_milhares.fst compiled/a2r_num_centenas.fst | fstunion - compiled/a2r_num_dezenas.fst | fstunion - compiled/a2r_unidades.fst > compiled/a2r.fst

# 3. a) Creating date_a2t
echo "Creating date_a2t"
fstconcat compiled/d2dd.fst compiled/dash.fst | fstconcat - compiled/mm2mmm.fst | fstconcat - compiled/dash.fst | fstconcat - compiled/d2dddd.fst > compiled/date_a2t.fst

# 3. b) Creating date_r2a
echo "Creating date_r2a"
fstconcat compiled/r2a.fst compiled/dash.fst | fstconcat - compiled/r2a.fst | fstconcat - compiled/dash.fst | fstconcat - compiled/r2a.fst > compiled/date_r2a.fst

# 3. b) Creating date_t2r
echo "Creating date_t2r"
fstinvert compiled/mm2mmm.fst | fstcompose - compiled/a2r.fst > compiled/mmm2r.fst
fstconcat compiled/a2r.fst compiled/dash.fst | fstconcat - compiled/mmm2r.fst | fstconcat - compiled/dash.fst | fstconcat - compiled/a2r.fst > compiled/date_t2r.fst

# 3. d) Creating date_r2bissexto
echo "Creating date_r2bissexto"
fstarcsort --sort_type=olabel compiled/date_r2a.fst compiled/date_r2a_sorted.fst
fstarcsort --sort_type=olabel compiled/date2norm.fst compiled/date2norm_sorted.fst
fstcompose compiled/date_r2a_sorted.fst compiled/date2norm_sorted.fst | fstcompose - compiled/date2year.fst | fstcompose - compiled/bissexto.fst > compiled/date_r2bissexto.fst


for folder in $(dir tests); do
    mkdir -p compiled/tests/$folder
	for i in  $(dir tests/$folder/*.txt); do
        echo "Compiling: $i"
        fstcompile --isymbols=syms.txt --osymbols=syms.txt $i | fstarcsort > compiled/tests/$folder/$(basename $i ".txt").fst
    done
done

for folder in $(dir compiled/tests); do
    mkdir -p compiled/tests/$folder/results
	for i in  $(dir compiled/tests/$folder/*.fst); do
        echo "Testing the transducer '$folder' with the input 'tests/$(basename $i ".fst").txt' (generating pdf)"
        fstcompose $i compiled/$folder.fst | fstshortestpath > compiled/tests/$folder/results/resp_$(basename $i ".txt").fst
    done
done

# Creating PDF versions of each transducer
for i in compiled/*.fst; do
	echo "Creating image: images/$(basename $i '.fst').pdf"
    fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/$(basename $i '.fst').pdf
done

for folder in $(dir compiled/tests); do
    # Creating PDF versions of each transducer
    mkdir -p images/tests/$folder
	for i in  $(dir compiled/tests/$folder/*.fst); do
        echo "Creating image: images/tests/$folder/$i"
        fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/tests/$folder/$(basename $i '.fst').pdf
    done
    # Creating PDF versions of each transducer
    mkdir -p images/tests/$folder/results
    for i in  $(dir compiled/tests/$folder/results/*.fst); do
        echo "Creating image: images/tests/$folder/$i"
        fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/tests/$folder/results/$(basename $i '.fst').pdf
    done
done

for folder in $(dir compiled/tests); do
	for i in  $(dir compiled/tests/$folder/*.fst); do
        echo "Testing the transducer '$folder' with the input 'tests/$(basename $i ".fst").txt' (stdout)"
        fstcompose $i compiled/$folder.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
    done
done

# # 3. a)
# echo "Testing the transducer 'date_a2t' with the input 'tests/date_a2t.txt' (stdout)"
# fstcompose compiled/95000a.fst compiled/date_a2t.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
# # 3. b)
# echo "Testing the transducer 'date_r2a' with the input 'tests/test_a2r.txt' (stdout)"
# fstcompose compiled/95000d.fst compiled/date_r2a.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
# # 3. c)
# echo "Testing the transducer 'date_t2r' with the input 'tests/date_t2r.txt' (stdout)"
# fstcompose compiled/95000c.fst compiled/date_t2r.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
# # 3. c)
# echo "Testing the transducer 'date_r2bissexto' with the input 'tests/95000c.txt' (stdout)"
# fstcompose compiled/95000d.fst compiled/date_r2bissexto.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
