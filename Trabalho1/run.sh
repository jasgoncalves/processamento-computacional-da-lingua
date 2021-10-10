#!/bin/bash

mkdir -p compiled images compiled/tests images/tests compiled/tests/group4 images/tests/group4

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
fstinvert compiled/r2a.fst > compiled/a2r.fst
# fstconcat compiled/a2r_milhares.fst compiled/a2r_centenas.fst | fstconcat - compiled/a2r_dezenas.fst | fstconcat - compiled/a2r_unidades.fst > compiled/a2r_num_milhares.fst
# fstconcat compiled/a2r_centenas.fst compiled/a2r_dezenas.fst | fstconcat - compiled/a2r_unidades.fst > compiled/a2r_num_centenas.fst
# fstconcat compiled/a2r_dezenas.fst compiled/a2r_unidades.fst > compiled/a2r_num_dezenas.fst
# fstunion compiled/a2r_num_milhares.fst compiled/a2r_num_centenas.fst | fstunion - compiled/a2r_num_dezenas.fst > compiled/a2r.fst

# 3. a) Creating date_a2t
echo "Creating date_a2t"
fstconcat compiled/d2dd.fst compiled/dash.fst | fstconcat - compiled/mm2mmm.fst | fstconcat - compiled/dash.fst | fstconcat - compiled/d2dddd.fst > compiled/date_a2t.fst

# 3. b) Creating date_r2a
echo "Creating date_r2a"
fstconcat compiled/r2a.fst compiled/dash.fst | fstconcat - compiled/r2a.fst | fstconcat - compiled/dash.fst | fstconcat - compiled/r2a.fst > compiled/date_r2a.fst

# 3. c) Creating date_t2r
echo "Creating date_t2r"
fstinvert compiled/mm2mmm.fst | fstcompose - compiled/a2r.fst > compiled/mmm2r.fst
fstconcat compiled/a2r.fst compiled/dash.fst | fstconcat - compiled/mmm2r.fst | fstconcat - compiled/dash.fst | fstconcat - compiled/a2r.fst > compiled/date_t2r.fst

# # 3. d) Creating date_r2bissexto
# echo "Creating date_r2bissexto"
# fstarcsort --sort_type=olabel compiled/date_r2a.fst compiled/date_r2a_sorted.fst
# fstarcsort --sort_type=olabel compiled/date2norm.fst compiled/date2norm_sorted.fst
# fstcompose compiled/date_r2a_sorted.fst compiled/date2norm_sorted.fst | fstcompose - compiled/date2year.fst | fstcompose - compiled/bissexto.fst > compiled/date_r2bissexto.fst

mkdir -p compiled/tests images/tests compiled/tests images/tests

for folder in $(dir tests); do
    mkdir -p compiled/tests/$folder
    for i in  $(dir tests/$folder/*.txt); do
        echo "Compiling: $i"
        fstcompile --isymbols=syms.txt --osymbols=syms.txt $i | fstarcsort > compiled/tests/$folder/$(basename $i ".txt").fst
    done
done

for folder in $(dir compiled/tests); do
    if [ $folder != 'group4' ]; then
        mkdir -p compiled/tests/$folder/results
        for i in  $(dir compiled/tests/$folder/*.fst); do
            echo "Testing the transducer '$folder' with the input 'tests/$(basename $i ".fst").txt' (generating pdf)"
            fstcompose $i compiled/$folder.fst | fstshortestpath > compiled/tests/$folder/results/resp_$(basename $i ".txt").fst
        done
    fi
done

# Creating PDF versions of each transducer
for i in compiled/*.fst; do
	echo "Creating image: images/$(basename $i '.fst').pdf"
    fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/$(basename $i '.fst').pdf
done

for folder in $(dir compiled/tests); do
    if [ $folder != 'group4' ]; then
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
    fi
done

for folder in $(dir compiled/tests); do
    if [ $folder != 'group4' ]; then
        for i in  $(dir compiled/tests/$folder/*.fst); do
            echo "Testing the transducer '$folder' with the input 'tests/$(basename $i ".fst").txt' (stdout)"
            fstcompose $i compiled/$folder.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
        done
    fi
done

# Tests Group4

echo -e "\nStarting Tests Group 4"
echo "----------------------"~

mkdir -p compiled/tests/group4 images/tests/group4

for i in  $(dir tests/group4/*.txt); do
    echo -e "Compiling: $i"
    fstcompile --isymbols=syms.txt --osymbols=syms.txt $i | fstarcsort > compiled/tests/group4/$(basename $i ".txt").fst
    echo -e "Testing the transducer 'date_a2t' with the input 'tests/group4/$(basename $i ".txt").fst' (generating pdf)"
    fstcompose compiled/tests/group4/$(basename $i ".txt").fst compiled/date_a2t.fst | fstshortestpath | fstrmepsilon | fsttopsort  > compiled/tests/group4/$(basename $i ".txt")_date_a2t.fst
    # stdout
    fstcompose compiled/tests/group4/$(basename $i ".txt").fst compiled/date_a2t.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
    echo -e "Testing the transducer 'date_t2r' with the input 'tests/group4/$(basename $i ".txt")_date_a2t.fst' (generating pdf)"
    fstcompose compiled/tests/group4/$(basename $i ".txt")_date_a2t.fst compiled/date_t2r.fst | fstshortestpath | fstrmepsilon | fsttopsort  > compiled/tests/group4/$(basename $i ".txt")_date_t2r.fst
    # stdout
    fstcompose compiled/tests/group4/$(basename $i ".txt")_date_a2t.fst compiled/date_t2r.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
    echo -e "Testing the transducer 'date_r2a' with the input 'tests/group4/$(basename $i ".txt")_date_t2r.fst' (generating pdf)"
    fstcompose compiled/tests/group4/$(basename $i ".txt")_date_t2r.fst compiled/date_r2a.fst | fstshortestpath | fstrmepsilon | fsttopsort  > compiled/tests/group4/$(basename $i ".txt")_date_r2a.fst 
    # stdout
    fstcompose compiled/tests/group4/$(basename $i ".txt")_date_t2r.fst compiled/date_r2a.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
    echo -e "Testing the transducer 'date_r2bissexto' with the input 'tests/group4/$(basename $i ".txt")_date_date_t2r.fst' (generating pdf)"
    fstcompose compiled/tests/group4/$(basename $i ".txt")_date_t2r.fst compiled/date_r2bissexto.fst | fstshortestpath | fstrmepsilon | fsttopsort > compiled/tests/group4/$(basename $i ".txt")_r2bissexto.fst
    # stdout
    fstcompose compiled/tests/group4/$(basename $i ".txt")_date_t2r.fst compiled/date_r2bissexto.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
done

for i in  $(dir compiled/tests/group4/*.fst); do
    echo -e "Creating image: images/tests/group4/$(basename $i '.fst').pdf"
    fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/tests/group4/$(basename $i '.fst').pdf
done