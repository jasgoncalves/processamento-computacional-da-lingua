#!/bin/bash

mkdir -p compiled images

for i in sources/*.txt; do
	echo "Compiling ....: $i"
    fstcompile --isymbols=syms.txt --osymbols=syms.txt $i | fstarcsort > compiled/$(basename $i ".txt").fst
done

# 1. d) Creating date2year
echo "Creating .....: compiled/date2year.fst"
fstconcat compiled/skip.fst compiled/skip.fst | fstconcat - compiled/d2dddd.fst | fstrmepsilon | fstarcsort --sort_type=olabel > compiled/date2year.fst

# 1. e) Creating date2norm
echo "Creating .....: compiled/date2norm.fst"
fstconcat compiled/d2dd.fst compiled/dash.fst | fstconcat - compiled/d2dd.fst  | fstconcat - compiled/dash.fst | fstconcat - compiled/d2dddd.fst | fstrmepsilon | fstarcsort --sort_type=olabel > compiled/date2norm.fst

# 1. f) Creating bissexto
echo "Creating .....: compiled/bissexto.fst"
fstconcat compiled/bissexto_4multiplesupto99.fst compiled/bissexto_skipdoublezero.fst | fstconcat - compiled/bissexto_yes.fst | fstrmepsilon > compiled/bissexto_400multiples.fst
fstconcat compiled/bissexto_skip.fst compiled/bissexto_skip.fst | fstconcat - compiled/bissexto_4multiplesupto99.fst | fstconcat - compiled/bissexto_yes.fst | fstrmepsilon > compiled/bissexto_4multiples.fst
fstconcat compiled/bissexto_negative4multiplesupto99.fst compiled/bissexto_skipdoublezero.fst | fstconcat - compiled/bissexto_no.fst | fstrmepsilon > compiled/bissexto_non400multiples.fst
fstconcat compiled/bissexto_skip.fst compiled/bissexto_skip.fst | fstconcat - compiled/bissexto_negative4multiplesupto99.fst | fstconcat - compiled/bissexto_no.fst | fstrmepsilon > compiled/bissexto_non4multiples.fst
fstunion compiled/bissexto_400multiples.fst compiled/bissexto_4multiples.fst | fstunion - compiled/bissexto_non400multiples.fst | fstunion - compiled/bissexto_non4multiples.fst | fstrmepsilon > compiled/bissexto.fst

# 2. a) Creating r2a
echo "Creating .....: compiled/r2a.fst"
fstunion compiled/r2a_centenas.fst compiled/r2a_zero.fst | fstrmepsilon > compiled/r2a_centenas_zero.fst
fstunion compiled/r2a_dezenas.fst compiled/r2a_zero.fst | fstrmepsilon > compiled/r2a_dezenas_zero.fst
fstunion compiled/r2a_unidades.fst compiled/r2a_zero.fst | fstrmepsilon > compiled/r2a_unidades_zero.fst
fstconcat compiled/r2a_milhares.fst compiled/r2a_centenas_zero.fst | fstconcat - compiled/r2a_dezenas_zero.fst | fstconcat - compiled/r2a_unidades_zero.fst | fstrmepsilon > compiled/r2a_trans_milhares.fst
fstconcat compiled/r2a_centenas.fst compiled/r2a_dezenas_zero.fst | fstconcat - compiled/r2a_unidades_zero.fst | fstrmepsilon > compiled/r2a_trans_centenas.fst
fstconcat compiled/r2a_dezenas.fst compiled/r2a_unidades_zero.fst | fstrmepsilon > compiled/r2a_trans_dezenas.fst
fstunion compiled/r2a_trans_milhares.fst compiled/r2a_trans_centenas.fst | fstunion - compiled/r2a_trans_dezenas.fst  | fstunion - compiled/r2a_unidades.fst | fstrmepsilon > compiled/r2a.fst

# 2. b) Creating a2r
echo "Creating .....: compiled/a2r.fst"
fstinvert compiled/r2a.fst > compiled/a2r.fst

# 3. a) Creating date_a2t
echo "Creating .....: compiled/date_a2t.fst"
fstconcat compiled/d2dd.fst compiled/dash.fst | fstconcat - compiled/mm2mmm.fst | fstconcat - compiled/dash.fst | fstconcat - compiled/d2dddd.fst | fstarcsort --sort_type=olabel > compiled/date_a2t.fst

# 3. b) Creating date_r2a
echo "Creating .....: compiled/date_r2a.fst"
fstconcat compiled/r2a.fst compiled/dash.fst | fstconcat - compiled/r2a.fst | fstconcat - compiled/dash.fst | fstconcat - compiled/r2a.fst | fstarcsort --sort_type=olabel > compiled/date_r2a.fst

# 3. c) Creating date_t2r
echo "Creating .....: compiled/date_t2r.fst"
fstcompose compiled/date_r2a.fst compiled/date2norm.fst | fstcompose - compiled/date_a2t.fst | fstinvert > compiled/date_t2r.fst

# 3. d) Creating date_r2bissexto
echo "Creating .....: compiled/date_r2bissexto.fst"
fstcompose compiled/date_r2a.fst compiled/date2norm.fst | fstcompose - compiled/date2year.fst | fstcompose - compiled/bissexto.fst > compiled/date_r2bissexto.fst

# Creating PDF versions of each transducer
for i in compiled/*.fst; do
	echo "Creating image: images/$(basename $i '.fst').pdf"
    fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/$(basename $i '.fst').pdf
done

# Tests Group4

echo -e "\nStarting Tests Group 4"
echo "----------------------"

mkdir -p compiled/tests images/tests

for i in  $(dir tests/*.txt); do
    echo -e "Compiling: $i"
    fstcompile --isymbols=syms.txt --osymbols=syms.txt $i | fstarcsort > compiled/tests/$(basename $i ".txt").fst
    #date_at2
    echo -e "Testing the transducer 'date_a2t' with the input 'tests/$(basename $i ".txt").fst' (generating pdf)"
    fstcompose compiled/tests/$(basename $i ".txt").fst compiled/date_a2t.fst | fstshortestpath | fstrmepsilon > compiled/tests/$(basename $i ".txt")_date_a2t.fst
    echo -e "Creating image: images/tests/$(basename $i '.txt')_date_a2t.pdf"
    fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt compiled/tests/$(basename $i ".txt")_date_a2t.fst | dot -Tpdf > images/tests/$(basename $i '.txt')_date_a2t.fst.pdf
    # stdout
    fstcompose compiled/tests/$(basename $i ".txt").fst compiled/date_a2t.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
    #date_t2r
    echo -e "Testing the transducer 'date_t2r' with the input 'tests/$(basename $i ".txt")_date_a2t.fst' (generating pdf)"
    fstcompose compiled/tests/$(basename $i ".txt")_date_a2t.fst compiled/date_t2r.fst | fstshortestpath | fstrmepsilon > compiled/tests/$(basename $i ".txt")_date_t2r.fst
    echo -e "Creating image: images/tests/$(basename $i '.txt')_date_t2r.pdf"
    fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt compiled/tests/$(basename $i ".txt")_date_t2r.fst | dot -Tpdf > images/tests/$(basename $i '.txt')_date_t2r.fst.pdf
    # stdout
    fstcompose compiled/tests/$(basename $i ".txt")_date_a2t.fst compiled/date_t2r.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
    # date_r2a
    echo -e "Testing the transducer 'date_r2a' with the input 'tests/$(basename $i ".txt")_date_t2r.fst' (generating pdf)"
    fstcompose compiled/tests/$(basename $i ".txt")_date_t2r.fst compiled/date_r2a.fst | fstshortestpath | fstrmepsilon > compiled/tests/$(basename $i ".txt")_date_r2a.fst 
    echo -e "Creating image: images/tests/$(basename $i '.txt')_date_r2a.pdf"
    fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt compiled/tests/$(basename $i ".txt")_date_r2a.fst | dot -Tpdf > images/tests/$(basename $i '.txt')_date_r2a.fst.pdf
    # stdout
    fstcompose compiled/tests/$(basename $i ".txt")_date_t2r.fst compiled/date_r2a.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
    # date_r2bissexto
    echo -e "Testing the transducer 'date_r2bissexto' with the input 'tests/$(basename $i ".txt")_date_date_t2r.fst' (generating pdf)"
    fstcompose compiled/tests/$(basename $i ".txt")_date_t2r.fst compiled/date_r2bissexto.fst | fstshortestpath | fstrmepsilon > compiled/tests/$(basename $i ".txt")_date_r2bissexto.fst
    echo -e "Creating image: images/tests/$(basename $i '.txt')_date_r2bissexto.pdf"
    fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt compiled/tests/$(basename $i ".txt")_date_r2bissexto.fst | dot -Tpdf > images/tests/$(basename $i '.txt')_date_r2bissexto.fst.pdf
    # stdout
    fstcompose compiled/tests/$(basename $i ".txt")_date_t2r.fst compiled/date_r2bissexto.fst | fstshortestpath | fstproject --project_type=output | fstrmepsilon | fsttopsort | fstprint --acceptor --isymbols=./syms.txt
done