# JBioSeqTools - python library

#### JBioSeqTools is the Python library for gene sequence downloading, optimization, structure prediction, vector building, and visualization


<p align="right">
<img  src="https://github.com/jkubis96/GEDSpy/blob/main/fig/logo_jbs.PNG?raw=true" alt="drawing" width="250" />
</p>


### Author: Jakub Kubiś 

<div align="left">
 Institute of Bioorganic Chemistry<br />
 Polish Academy of Sciences<br />
 Department of Molecular Neurobiology<br />
</div>


## Description


<div align="justify"> JBioSeqTools is the Python library for biological sequence optimization (GC % content & codon frequency), restriction places removal, DNA/RNA structure prediction, and RNAi selection. It also allows the building of many plasmid vectors with the possibility of choosing sequences such as transcript, promoter, enhancer, molecular fluorescent tag, etc. Finally, the user obtains a ready-for-order construct with a whole sequence and visualization.
</div>

</br>

Used databases:
* GeneScript [https://www.genscript.com/?src=google&gclid=Cj0KCQiAkMGcBhCSARIsAIW6d0CGxHmZO8EAYVQSwgk5e3YSRhKZ882vnylGUxfWuhareHFkJP4h4rgaAvTNEALw_wcB]
* VectorBuilder [https://en.vectorbuilder.com/]
* UTRdb [https://utrdb.cloud.ba.infn.it/utrdb/index_107.html]
* NCBI refseq_select_rna [ftp.ncbi.nlm.nih.gov]

<br />

<br />

## Table of contents

[Installation](#installation) \
[Usage](#usage)
1. [seq_tools - part of the library containing sequence optimization, structure prediction, and visualization](#seq_tools) \
1.1. [Import part of library](#import-seq_tools) \
1.2. [Loading metadata](#loading-metadata) \
1.3. [Downloading reference sequences with gene name](#downloading-ref) \
1.4. [Downloading  sequences with accession numbers](#downloading-accession) \
1.5. [Creating FASTA format *.FASTA](#creating-fasta) \
1.6. [Loading FASTA format from file *.FASTA](#loading-fasta) \
1.7. [Writing to FASTA format *.FASTA](#writing-fasta) \
1.8. [Conducting Multiple Alignments Analysis (MUSCLE) form FASTA](#muscle) \
1.9. [Display alignment plot](#alignment-plot) \
1.10. [Decoding alignment file](#decoding-alignment) \
1.11. [Writing to ALIGN format *.ALIGN](#writing-align) \
1.12. [Extracting consensus parts of alignments](#extracting-consensuse) \
1.13. [Passing sequence from an external source](#passing-sequence) \
1.14. [Clearing junk characters from the sequence](#clearing-sequence) \
1.15. [Checking that the sequence is coding protein (CDS)](#checking-cds) \
1.16. [Checking that all bases in sequence are contained in the UPAC code](#checking-upac) \
1.17. [Reversing the DNA / RNA sequence: 5' --> 3' and 3' --> 5'](#reversing) \
1.18. [Complementing the DNA / RNA second strand sequence](#complementing) \
1.19. [Changing DNA to RNA sequence](#dna-rna) \
1.20. [Changing RNA to DNA sequence](#rna-dna) \
1.21. [Changing DNA or RNA sequence to amino acid / protein sequence](#dna-protein) \
1.22. [Prediction of RNA / DNA sequence secondary structure](#prediction) \
1.23. [Prediction of RNAi on the provided sequence](#rnai-prediction) \
1.24. [Correcting of RNAi_data for complementarity to the loop sequence](#correcting-loop) \
1.25. [Correcting of RNAi_data for complementarity to the additional external sequence](#correcting-sequence) \
1.26. [Codon optimization](#optimize) \
1.27. [Checking susceptibility to restriction enzymes](#resctriction) \
1.28. [Checking and removing susceptibility to restriction enzymes](#resctriction-remove) 
2. [vector_build - part of the library containing building plasmid vectors with optimization elements from seq_tools](#vector-build) \
2.1. [Import part of library](#import-vector_build) \
2.2. [Creating vector plasmid](#creating-vector) \
2.2.1 [Creating expression of the plasmid vector](#expression) \
2.2.2 [Creating RNAi / RNAi + expression of the plasmid vector](#rnai) \
2.2.3 [Creating plasmid vector of in-vitro transcription of mRNA](#transcript-mrna) \
2.2.4 [Creating plasmid vector of in-vitro transcription of RNAi](#transcription-rnai) \
2.3. [Creating vector plasmid from FASTA - display existing or custom editing FASTA file](#vector-fasta) \
2.3.1 [Loading fasta from the file](#fasta2-loading) \
2.3.2 [Converting the FASTA string to the data frame](#fasta-df) \
2.3.3 [Decoding information form headers for the vector graph creating](#headers) \
2.3.4 [Creating graph of the plasmid vector](#graph)

<br />

<br />

# Installation <a id="installation"></a>

#### In command line write:

```
pip install JBioSeqTools
```

* During the first library loading additional requirements will be installed (BLAST, MUSCLE) and metadata downloaded.

<br />

<br />


# Usage <a id="usage"></a>

<br />

### 1. seq_tools - part of the library containing sequence optimization, structure prediction, and visualization <a id="seq_tools"></a>

#### 1.1. Import part of library <a id="import-seq_tools"></a>

```
from jbst import seq_tools as st
```

<br />

#### 1.2. Loading metadata <a id="loading-metadata"></a>

```
metadata = st.load_metadata() 
```


<br />

#### 1.3. Downloading reference sequences with gene name <a id="downloading-ref"></a>

```
data_dict = st.get_sequences_gene(gene_name, species = 'human', max_results = 20)
```

<br />

#### 1.4. Downloading  sequences with accession numbers <a id="downloading-accession"></a>

```
data_dict = st.get_sequences_accesion(accesion_list)
```

<br />

#### 1.5. Creating FASTA format *.FASTA <a id="creating-fasta"></a>

```
fasta_string = st.generate_fasta_string(data_dict)
```


<br />

#### 1.6. Loading FASTA format from file *.FASTA <a id="loading-fasta"></a>

```
fasta_string = st.load_fasta(path)
```

<br />

#### 1.7. Writing to FASTA format *.FASTA <a id="writing-fasta"></a>

```
st.write_fasta(fasta_string, path = None, name = 'fasta_file')
```


<br />

#### 1.8. Conducting Multiple Alignments Analysis (MUSCLE) form FASTA <a id="muscle"></a>

```
alignment_file = st.MuscleMultipleSequenceAlignment(fasta_string, output = None, gapopen = 10, gapextend = 0.5)
```


<br />

#### 1.9. Display alignment plot <a id="alignment-plot"></a>

```
alignment_plot = st.DisplayAlignment(alignment_file, color_scheme="Taylor", wrap_length=80, show_grid=True, show_consensus=True)
alignment_plot.savefig("alignment_plot.svg")
```

##### Example of the alignment graph:

<p align="center">
<img  src="https://github.com/jkubis96/JBioSeqTools/blob/v.2/fig/alignments.jpg?raw=true" alt="drawing" width="600" />
</p>




<br />

#### 1.10. Decoding alignment file <a id="decoding-alignment"></a>

```
decoded_alignment_file = st.decode_alignments(alignment_file)
```

##### Example output:

```
print(decoded_alignment_file)

Homo_sapiens_survival_of_motor_neuron_1,_telomeric_(SMN1),_transcript_variant_b,_mRNA | -CCACAAATGTGGGAGGGCGATAACCACTCGTAG-AAAGCGTGAGAAGTTACTACAAGC-G-G-TCCTCCC--G-GCCACCG-TACT-G-TT-C--C-----GCTCC-C-AGAAGCC--C--CGGGCGGCGG-AAGTCGTCACTCTTAAGAAGGGACGGGGCCCCACGCTG-CGCACCCGCGGGT-TTGCTATGGCGATGAGCAGCGG-C-GGCAGTGG-TGGC-G-G-CGTCCCGGAGC-A-G-GAGGATT-CCG-TGCT-G-TTCCGGCGCGGCA-CAGGCCAGAGCGATGATTCTGACATTTGGGATGATACAGCACTGATAAAAGCAT-ATGATAAAGCTGTGGCTT-CATTTAAGCATGCTCTAAAGAATGGTGACATTTGTGAAACTTCGGGTAAACCAAAA-ACCACA-CCTAAAAGAAAACCTGCTAAGAAGAATAAAAGCCAAAAGAAGAATACTGCAGCTTCCTT-ACAACAGTGGAAAGTTGGG-GACAAATGTTCTGCCATTTGGTCAGAAGACGGTTGCATTTACCCAGCTACCATTGC-TTCAATTGATTTTAAGAGAGAAACCTGTGTTGTGGTTTACACTGGATATGGAAATAGAGAGGAGCAAAATC-TGTCCGATCTACTTTCCCCAATCTGTGAAGTAGCTAATAATATAGAACA-AA-ATGCTCAAGAGAATGAAAATGAAAGCCAAGTTT-CAACAGATGAA-AGTGAGA-ACT-C-C-AGGTCTC-CT-GGAAATAAATCAGATA-ACATCAAGCCCAAATCTGCTCCATGGAA-CTC-TTTTCTCCCTCCACCACCCCCC-ATGCCAGGGCCAAGACTGGGACCAGGAAAG--A--T--A-A-TT------C-C--C--C-C-A-C-----C-A-C--C--T---C-C-C--A---T---A---T-G-T--C--C-A-----------G------A-T---T-----C-------T--C---T---T----GA-T--------GATG---CTGATGCTTTGGG-AAGTATGTTAATTTCAT-GGTACATGAGTGGCTATCATACTGGCTATTATATGGGTTTCAGACAAAATCAAAAAGAAGGAAGGTGCTCACATTCCTTAAATTAAGG-AGAAATGCTGGCATAGAGCAGCACTAAATGAC-ACCACTAAAGAAACGAT-CAGAC-A-GATCT--GGA-ATGTGAAGCGTTATAGAAGATAACTGGCCTCATTTCTTCAAAATATCAAGTGTTGGGA-AAGAAAAAAGGA-AGTGGAATGGGTAACTCTTCTTGATTAAAAGTTATGTAATAAC-CAAAT-G-C-AATGTGAAATATTTTACTGGACTCTATTTTGAAAAACCATCTGTAAAAGAC-TGGGG-TGGGGGTGGGAGGCCAGCACGGTGGTGAGGCAGTTGAGAAAATTTGAATGTGGATTAG-ATTTTG-AATGATATTG-GATAATTATTGGTAATTTTATGAGCTGTGAG-AAGGGTGTTGTAGTTTATAAAAGACTGTCTTAATTTGCATACTTAAGCATTTAGGAATGAAGTGTTAGAGTGTCTTA-AAATGTTTCAAATGGTTTAA--CAAAATGTATGTGAGGCGTATGTGGCA-AAATGTTACAGAATCTAACTGGTGGACATGGCTGTTCATT-GTACTGTTT----TTTTCTATCTTCTATATG--TTTAAAAGTATATAATAAAAATATTTAATTTTTTTTTAAAAAAAAAAAAAAAAA----AA
Homo_sapiens_survival_of_motor_neuron_1,_telomeric_(SMN1),_transcript_variant_d,_mRNA | ----------------G-------C----------A---------------C--C---C-G-----C------G-G-----G-T--T----T----------GCT-----A----------T--G--G-C-G--A-T-G----------------A----G--C-A-G----CG-----GCG-G-----C-A----G-TG-------G-T--G-----G----C-G-G-CGTCCCGGAGC-A-G-GAGGATT-CCG-TGCT-G-TTCCGGCGCGGCA-CAGGCCAGAGCGATGATTCTGACATTTGGGATGATACAGCACTGATAAAAGCAT-ATGATAAAGCTGTGGCTT-CATTTAAGCATGCTCTAAAGAATGGTGACATTTGTGAAACTTCGGGTAAACCAAAA-ACCACA-CCTAAAAGAAAACCTGCTAAGAAGAATAAAAGCCAAAAGAAGAATACTGCAGCTTCCTT-ACAACAGTGGAAAGTTGGG-GACAAATGTTCTGCCATTTGGTCAGAAGACGGTTGCATTTACCCAGCTACCATTGC-TTCAATTGATTTTAAGAGAGAAACCTGTGTTGTGGTTTACACTGGATATGGAAATAGAGAGGAGCAAAATC-TGTCCGATCTACTTTCCCCAATCTGTGAAGTAGCTAATAATATAGAACA-AA-ATGCTCAAGAGAATGAAAATGAAAGCCAAGTTT-CAACAGATGAA-AGTGAGA-ACT-C-C-AGGTCTC-CT-GGAAATAAATCAGATA-ACATCAAGCCCAAATCTGCTCCATGGAA-CTC-TTTTCTCCCTCCACCACCCCCC-ATGCCAGGGCCAAGACTGGGACCAGGAAAGCCAGGTCTAAAATTCAATGGCCCACCACCGCCA-C-CGC-C-ACCACCAC-CACCCCACTTACTAT-C-ATGCTGGCTG-CCTCCATTTC-CTTCTGGACCACCAATAATTCCC-CCA-CCACCTCCCA--TATGT-CCAGA-T-TCTCTT-GATGATGCTGATGCTTTGGG-AAGTATGTTAATTTCAT-GGTACATGAGTGGCTATCATACTGGCTATTATATGGGTTTCAGACAAAATCAAAAAGAAGGAAGGTGCTCACATTCCTTAAATTAAGG-AGAAATGCTGGCATAGAGCAGCACTAAATGAC-ACCACTAAAGAAACGAT-CAGAC-A-GATCT--GGA-ATGTGAAGCGTTATAGAAGATAACTGGCCTCATTTCTTCAAAATATCAAGTGTTGGGA-AAGAAAAAAGGA-AGTGGAATGGGTAACTCTTCTTGATTAAAAGTTATGTAATAAC-CAAAT-G-C-AATGTGAAATATTTTACTGGACTCTATTTTGAAAAACCATCTGTAAAAGAC-TGGGG-TGGGGGTGGGAGGCCAGCACGGTGGTGAGGCAGTTGAGAAAATTTGAATGTGGATTAG-ATTTTG-AATGATATTG-GATAATTATTGGTAATTTTATGAGCTGTGAG-AAGGGTGTTGTAGTTTATAAAAGACTGTCTTAATTTGCATACTTAAGCATTTAGGAATGAAGTGTTAGAGTGTCTTA-AAATGTTTCAAATGGTTTAA--CAAAATGTATGTGAGGCGTATGTGGCA-AAATGTTACAGAATCTAACTGGTGGACATGGCTGTTCATT-GTACTGTTT----TTTTCTATCTTCTATATG--TTTAAAAGTATATAATAAAAATATTTAATTTTTTTTT------------A-A-AT-T-A-
Homo_sapiens_survival_of_motor_neuron_1,_telomeric_(SMN1),_transcript_variant_a,_mRNA | -CCACAAATGTGGGAGGGCGATAACCACTCGTAG-AAAGCGTGAGAAGTTACTACAAGC-G-G-TCCTCCC--G-GCCACCG-TACT-G-TT-C--C-----GCTCC-C-AGAAGCC--C--CGGGCGGCGG-AAGTCGTCACTCTTAAGAAGGGACGGGGCCCCACGCTG-CGCACCCGCGGGT-TTGCTATGGCGATGAGCAGCGG-C-GGCAGTGG-TGGC-G-G-CGTCCCGGAGC-A-G-GAGGATT-CCG-TGCT-G-TTCCGGCGCGGCA-CAGGCCAGAGCGATGATTCTGACATTTGGGATGATACAGCACTGATAAAAGCAT-ATGATAAAGCTGTGGCTT-CATTTAAGCATGCTCTAAAGAATGGTGACATTTGTGAAACTTCGGGTAAACCAAAA-ACCACA-CCTAAAAGAAAACCTGCTAAGAAGAATAAAAGCCAAAAGAAGAATACTGCAGCTTCCTT-ACAACAGTGGAAAGTTGGG-GACAAATGTTCTGCCATTTGGTCAGAAGACGGTTGCATTTACCCAGCTACCATTGC-TTCAATTGATTTTAAGAGAGAAACCTGTGTTGTGGTTTACACTGGATATGGAAATAGAGAGGAGCAAAATC-TGTCCGATCTACTTTCCCCAATCTGTGAAGTAGCTAATAATATAGAACA-AA-ATGCTCAAGAGAATGAAAATGAAAGCCAAGTTT-CAACAGATGAA-AGTGAGA-ACT-C-C-AGGTCTC-CT-GGAAATAAATCAGATA-ACATCAAGCCCAAATCTGCTCCATGGAA-CTC-TTTTCTCCCTCCACCACCCCCC-ATGCCAGGGCCAAGACTGGGACCAGGAAAGCCAGGTCTAAAATTCAATGGCCCACCACCGCCA-C-CGC-C-ACCACCAC-CACCCCACTTACTAT-C-ATGCTGGCTG-CCTCCATTTC-CTTCTGGACCACCAATAATTCCC-CCA-CCACCTCCCA--TATGT-CCAGA-T-TCTCTT-GATGATGCTGATGCTTTGGG-AAGTATGTTAATTTCAT-GGTACATGAGTGGCTATCATACTGGCTATTATAT--G-----GA-A-A-T----------------G---------C------T--GGCAT--A-G--AGC--A--GCA-C--TAAATGAC-ACCACTAAAGAAACGAT-CAGAC-A-GATCT--GGA-ATGTGAAGCGTTATAGAAGATAACTGGCCTCATTTCTTCAAAATATCAAGTGTTGGGA-AAGAAAAAAGGA-AGTGGAATGGGTAACTCTTCTTGATTAAAAGTTATGTAATAAC-CAAAT-G-C-AATGTGAAATATTTTACTGGACTCTATTTTGAAAAACCATCTGTAAAAGAC-TGGGG-TGGGGGTGGGAGGCCAGCACGGTGGTGAGGCAGTTGAGAAAATTTGAATGTGGATTAG-ATTTTG-AATGATATTG-GATAATTATTGGTAATTTTATGAGCTGTGAG-AAGGGTGTTGTAGTTTATAAAAGACTGTCTTAATTTGCATACTTAAGCATTTAGGAATGAAGTGTTAGAGTGTCTTA-AAATGTTTCAAATGGTTTAA--CAAAATGTATGTGAGGCGTATGTGGCA-AAATGTTACAGAATCTAACTGGTGGACATGGCTGTTCATT-GTACTGTTT----TTTTCTATCTTCTATATG--TTTAAAAGTATATAATAAAAATATTTAATTTTTTTTT------------A-A-A------
Mus_musculus_survival_motor_neuron_1_(Smn1),_transcript_variant_2,_mRNA               | G--AC---T-T-----G----TAACT-CTT-TAGCA--G--T--G---TT-CT-C---CTGTATTTCT-TTAAGTG--A--GTTATTAAATTCCTTCTTTATG-TCCTCTA----CCATCATC-A-TG-T-GAAA-T-G-C-TT-TT-A--A---AT-----CC-A-G--GTC-TA-C--C---TTTT-C-A--G-G-TG-----T-GTTAGG-A-T-GCC--CTG-GAC-T---GG-GCGAAGTG-GGA-----G-TGCTGGGTTCT-G-AT-G-A-T-GG-T-GA-TGATGATTCTGACATTTGGGATGATACAGCATTGATAAAAGC-TTATGATAAAGCTGTGGCTTCC-TTTAAGCATGCTCTAAAGAACGGTGACATTTGTGAAACTCCAGATAAGCCAAAAGG-CACAGCC-AGAAGAAAACCTGCCAAGAAGAATAAAAGCCAAAAGAAGAATGCCACAACTCCCTTGA-AACAGTGGAAAGTT-GGTGACAAGTGTTCTGCTGTTTGGTCAGAAGACGGCTGCATTTACCCAGCTACTATTACGTCC-ATTGACTTTAAGAGAGAAACCTGTGTCGTGGTTTATACTGGATATGGAAACAGAGAGGAGCAAAA-CTTATCTGACCTACTTTCCCCGACCTGTGAAGTAGCTAATAGTACAGAACAGAACA--CTC-AG-G-A-G-A-ATGAAAGTCAAGTTTCC-ACAGACG-ACAGTGA-ACACTCCTCCAGA--TCGCTCAGAAGT-AA--AG-CACACAGCAAGTCCAAAGCTGCTCCGTGG-ACCTCAT-TTCTTCCTCCACCA-CCCCCAATGCCAGGGTCAGGATTAGGACCAGGAAAGCCAGGTCTAAAATTCAACGGCCCGCCGCCGCCGCCTC-CACTACC-CC-CTC-CCCC-CTT-CC-TGCCGTGCTGGATGCCC-CCGTT-CCCTTCAGGACCACCAATAA-TCCCGCCACCC-CCTCCCATCT-C-TCCC-GACTGT--C-TGGATGACACTGATGCCCTGGGCA-GTATGCTAATCTC-TTGGTACATGAGTGGCTACCACACTGGCTACTATATGGGTTTCAGACAAAAT-A-A-A--A--AA---G--------------A--A-GG-A-A-A-G-T-GC-T----CA-C----A-T-ACAA--ATT-AAG-AA-G-TTCAG-CTCTG-TCTCAGGAGATG-G--G-G---T----G-T--C-GG--T-G-T-C--C----C-T---G-GTC-G-ACAAG-----A--ACA--G-A-C-G-T--CTC--CTCG-TC---A-TCA-GT-G-GACTC---TTGGCTAA-GTG-G-TG---T-C--G--TC-A-T-C--A-G-C-ATCT-C------CCC---GCT---G-TGGGA-GTC--CA---T--C----CA-TC-------C-T-AA-GT---C-AGCA----GCA--G--A--GCG-T-G-C-CTGG---------G-GC-GTGAGCA--G-T-T-G--G---A-G-G-GAC---C-------G-A--C-C-AG----T-GG-A-G---TG-T-GCGTGTC--GGAAG-G---C--A-G-TCT-ACCC---A-GT-CGTGA--C-T--G-AGCACAAATG-TGCA-A-T-T----G-T---CAT---T-TTC-TTAGCA-TG-TCAAGATTTT-TA---T-TA-ATGCCTTTAGAA-T-TA-AAT-AAAA-G-TC--C-T-TTTTT----------G-A-A-ATCTTG-
Mus_musculus_survival_motor_neuron_1_(Smn1),_transcript_variant_1,_mRNA               | ----------------G----T--C-A-T--T-G-A--G--T--GA-G---C--C---C-G-G---C-----A--G---C-G---------T-C--C-----G-T-------------------G--G-T----A---G-C--------------A--G-G-CC-ATG--G-CG-A-T-G-G-G-----C-A----G-TG-------G-C-GG-A---G----C-GGG-C-TC-C-GAGC-A-G-GAAGA-TAC-GGTGCT-G-TTCCGGCGTGGCACC-GGCCAGAGTGATGATTCTGACATTTGGGATGATACAGCATTGATAAAAGC-TTATGATAAAGCTGTGGCTTCC-TTTAAGCATGCTCTAAAGAACGGTGACATTTGTGAAACTCCAGATAAGCCAAAAGG-CACAGCC-AGAAGAAAACCTGCCAAGAAGAATAAAAGCCAAAAGAAGAATGCCACAACTCCCTTGA-AACAGTGGAAAGTT-GGTGACAAGTGTTCTGCTGTTTGGTCAGAAGACGGCTGCATTTACCCAGCTACTATTACGTCC-ATTGACTTTAAGAGAGAAACCTGTGTCGTGGTTTATACTGGATATGGAAACAGAGAGGAGCAAAA-CTTATCTGACCTACTTTCCCCGACCTGTGAAGTAGCTAATAGTACAGAACAGAACA--CTC-AG-G-A-G-A-ATGAAAGTCAAGTTTCC-ACAGACG-ACAGTGA-ACACTCCTCCAGA--TCGCTCAGAAGT-AA--AG-CACACAGCAAGTCCAAAGCTGCTCCGTGG-ACCTCAT-TTCTTCCTCCACCA-CCCCCAATGCCAGGGTCAGGATTAGGACCAGGAAAGCCAGGTCTAAAATTCAACGGCCCGCCGCCGCCGCCTC-CACTACC-CC-CTC-CCCC-CTT-CC-TGCCGTGCTGGATGCCC-CCGTT-CCCTTCAGGACCACCAATAA-TCCCGCCACCC-CCTCCCATCT-C-TCCC-GACTGT--C-TGGATGACACTGATGCCCTGGGCA-GTATGCTAATCTC-TTGGTACATGAGTGGCTACCACACTGGCTACTATATGGGTTTCAGACAAAAT-A-A-A--A--AA---G--------------A--A-GG-A-A-A-G-T-GC-T----CA-C----A-T-ACAA--ATT-AAG-AA-G-TTCAG-CTCTG-TCTCAGGAGATG-G--G-G---T----G-T--C-GG--T-G-T-C--C----C-T---G-GTC-G-ACAAG-----A--ACA--G-A-C-G-T--CTC--CTCG-TC---A-TCA-GT-G-GACTC---TTGGCTAA-GTG-G-TG---T-C--G--TC-A-T-C--A-G-C-ATCT-C------CCC---GCT---G-TGGGA-GTC--CA---T--C----CA-TC-------C-T-AA-GT---C-AGCA----GCA--G--A--GCG-T-G-C-CTGG---------G-GC-GTGAGCA--G-T-T-G--G---A-G-G-GAC---C-------G-A--C-C-AG----T-GG-A-G---TG-T-GCGTGTC--GGAAG-G---C--A-G-TCT-ACCC---A-GT-CGTGA--C-T--G-AGCACAAATG-TGCA-A-T-T----G-T---CAT---T-TTC-TTAGCA-TG-TCAAGATTTT-TA---T-TA-ATGCCTTTAGAA-T-TA-AAT-AAAA-G-TC--C-T-TTTTT----------G-A-A-ATCTTG-
```



<br />

#### 1.11. Writing to ALIGN format *.ALIGN <a id="writing-align"></a>

```
st.write_alignments(decoded_alignment_file, path = None, name = 'alignments_file')
```


<br />

#### 1.12. Extracting consensus parts of alignments <a id="extracting-consensuse"></a>

```
consensuse = st.ExtractConsensuse(alignment_file, refseq_sequences = None)
```



<br />

#### 1.13. Passing sequence from an external source <a id="passing-sequence"></a>

```
sequence = st.load_sequence()
```



<br />

#### 1.14. Clearing junk characters from the sequence <a id="clearing-sequence"></a>

```
sequence = st.clear_sequence(sequence)
```


<br />

#### 1.15. Checking that the sequence is coding protein (CDS) <a id="checking-cds"></a>

```
dec_coding = st.check_coding(sequence)
```


<br />

#### 1.16. Checking that all bases in sequence are contained in the UPAC code <a id="checking-upac"></a>

```
dec_upac = st.check_upac(sequence)
```


<br />

#### 1.17. Reversing the DNA / RNA sequence: 5' --> 3' and 3' --> 5' <a id="reversing"></a>

```
reversed_sequence = st.reverse(sequence) 
```


<br />

#### 1.18. Complementing the DNA / RNA second strand sequence <a id="complementing"></a>

```
complementary_sequence = st.complement(sequence)
```

<br />

#### 1.19. Changing DNA to RNA sequence <a id="dna-rna"></a>

```
rna_sequence = st.dna_to_rna(sequence, enrichment= False)
```

<br />

#### 1.20. Changing RNA to DNA sequence <a id="rna-dna"></a>

```
dna_sequence = st.rna_to_dna(rna_sequence)
```

<br />

#### 1.21. Changing DNA or RNA sequence to amino acid / protein sequence <a id="dna-protein"></a>

```
protein_sequence = st.seuqence_to_protein(dna_sequence, metadata)
```


<br />

#### 1.22. Prediction of RNA / DNA sequence secondary structure <a id="prediction"></a>

```
predisted_structure, dot_structure1 = st.predict_structure(sequence, show_plot = True)
predisted_structure.savefig('predicted_structure.svg')

```

##### Example of structure prediction graph:

* shRNA

<p align="center">
<img  src="https://raw.githubusercontent.com/jkubis96/JBioSeqTools/3fb8a369a9c893d65589a92680fcb1e0cbcefa87/fig/smn1_sh_structure.svg" alt="drawing" width="600" />
</p>


* mRNA

<p align="center">
<img  src="https://raw.githubusercontent.com/jkubis96/JBioSeqTools/3fb8a369a9c893d65589a92680fcb1e0cbcefa87/fig/smn1_structure.svg" alt="drawing" width="600" />
</p>


<br />

#### 1.23. Prediction of RNAi on the provided sequence <a id="rnai-prediction"></a>

```
RNAi_data =  st.FindRNAi(sequence, metadata, length = 23, n = 200, max_repeat_len = 3, max_off = 1, species = 'human', output = None, database_name = "refseq_select_rna",  evalue = 1e-3, outfmt =  5, word_size = 7, max_hsps = 20, reward = 1, penalty = -3, gapopen = 5, gapextend = 2, dust = "no", extension = 'xml')    
```


<br />

##### Example of data frame output:

|RNAi_name|RNAi_seq               |target                                      |e-value       |bit_score  |alignment_length|target_seq                 |target_gene_name|species         |specificity|complemenatry_regions|complemenatry_pct  |RNAi_sense             |repeated_motif|repeated_motif_pct|score|GC%  |
|---------|-----------------------|--------------------------------------------|--------------|-----------|----------------|---------------------------|--------------- |----------------|-----------|---------------------|-------------------|-----------------------|--------------|------------------|-----|-----|
|RNAi_66  |TGATTTTGTCTGAAACCCATATA|['Homo sapiens survival of motor neuron 1']|[2.07974e-05] |  [46.087] |     [23]       |['TGATTTTGTCTGAAACCCATATA']|    ['SMN1']    |['Homo sapiens']|     1     |['ATAT', 'TATA']     |0.34782608695652173|TATATGGGTTTCAGACAAAATCA|['TTTT']      |        0.17      |0.0  |17.04|
|RNAi_11  |TTGATTTTGTCTGAAACCCATAT|['Homo sapiens survival of motor neuron 1']|[2.07974e-05] |  [46.087] |     [23]       |['TTGATTTTGTCTGAAACCCATAT']|    ['SMN1']    |['Homo sapiens']|     1     |['ATAT']             |0.17391304347826086|ATATGGGTTTCAGACAAAATCAA|['TTTTTT']    |        0.26      |-3.0 |17.04|

<br />

Columns explanation:
* RNAi_name - name added by algorithms in the course of searching and predicting RNAi's
* RNAi_seq - the sequence of RNAi (reverse-complementary to a sequence that should be silenced)
* target - name of the targeted sequence
* e-value (expect value) - the probability of finding the observed alignment or a better one by random chance
* bit_score - statistical measure that provides an indication of the significance of a sequence alignment
* alignment_length - size of the alignment complementarity to the blasted sequence
* target_seq - part of the blasted sequence complementary to the RNAi_seq (in the same rotation as RNAi)
* target_gene_name - list of genes to which the RNAi is complementary
* species - list of species to which the gene sequence is complementary
* specificity - number of genes to which the RNAi is complementary
* complemenatry_regions - complementary part of RNAi inside the RNAi sequence
* complemenatry_pct - percent of complementary nucleotides inside RNAi
* RNAi_sense - sense strand of RNAi (reverse-complement to the RNAi_seq)
* repeated_motif - sequences with repeated sequences of the same nucleotide inside RNAi
* repeated_motif_pct - percent of nucleotides from sequences with repeated sequences of the same nucleotide inside RNAi
* score - algorithmically given points to particular RNAi sequences based on knowledge from previous works and papers: \
	-DOI:10.1093/nar/gkn902 \
	-DOI:10.1093/nar/gkh247 \
	-DOI:10.1038/nbt936 \
	-DOI:10.1016/j.bbrc.2004.02.157
	
* GC% - percent content of G and C nucleotides in RNAi sequence (best target between 35-55%)

<br />


#### 1.24. Correcting of RNAi_data for complementarity to the loop sequence <a id="correcting-loop"></a>

```
RNAi_data = st.loop_complementary_adjustment(RNAi_data, loop_seq, min_length=3)
```

<br />


##### Example of data frame output:

|RNAi_name|RNAi_seq               |target                                      |e-value       |bit_score  |alignment_length|target_seq                 |target_gene_name|species         |specificity|complemenatry_regions|complemenatry_pct  |RNAi_sense             |repeated_motif|repeated_motif_pct|score|GC%  |sense_loop_complementary|sense_loop_complementary_pct|antisense_loop_complementary|antisense_loop_complementary_pct|
|---------|-----------------------|--------------------------------------------|--------------|-----------|----------------|---------------------------|--------------- |----------------|-----------|---------------------|-------------------|-----------------------|--------------|------------------|-----|-----|------------------------|----------------------------|----------------------------|--------------------------------|
|RNAi_66  |TGATTTTGTCTGAAACCCATATA|['Homo sapiens survival of motor neuron 1'] |[2.07974e-05] |  [46.087] |     [23]       |['TGATTTTGTCTGAAACCCATATA']|    ['SMN1']    |['Homo sapiens']|     1     |['ATAT', 'TATA']     |0.34782608695652173|TATATGGGTTTCAGACAAAATCA|['TTTT']      |        0.17      |0.0  |17.04|[]                      |0.0                         |[]                          |0.0                             |
|RNAi_11  |TTGATTTTGTCTGAAACCCATAT|['Homo sapiens survival of motor neuron 1'] |[2.07974e-05] |  [46.087] |     [23]       |['TTGATTTTGTCTGAAACCCATAT']|    ['SMN1']    |['Homo sapiens']|     1     |['ATAT']             |0.17391304347826086|ATATGGGTTTCAGACAAAATCAA|['TTTTTT']    |        0.26      |-3.0 |17.04|[]                      |0.0                         |[]                          |0.0                             |

<br />

Columns explanation:
* RNAi_name - name added by algorithms in the course of searching and predicting RNAi's
* RNAi_seq - the sequence of RNAi (reverse-complementary to a sequence that should be silenced)
* target - name of the targeted sequence
* e-value (expect value) - the probability of finding the observed alignment or a better one by random chance
* bit_score - statistical measure that provides an indication of the significance of a sequence alignment
* alignment_length - size of the alignment complementarity to the blasted sequence
* target_seq - part of the blasted sequence complementary to the RNAi_seq (in the same rotation as RNAi)
* target_gene_name - list of genes to which the RNAi is complementary
* species - list of species to which the gene sequence is complementary
* specificity - number of genes to which the RNAi is complementary
* complemenatry_regions - complementary part of RNAi inside the RNAi sequence
* complemenatry_pct - percent of complementary nucleotides inside RNAi
* RNAi_sense - sense strand of RNAi (reverse-complement to the RNAi_seq)
* repeated_motif - sequences with repeated sequences of the same nucleotide inside RNAi
* repeated_motif_pct - percent of nucleotides from sequences with repeated sequences of the same nucleotide inside RNAi
* score - algorithmically given points to particular RNAi sequences based on knowledge from previous works and papers: \
	-DOI:10.1093/nar/gkn902 \
	-DOI:10.1093/nar/gkh247 \
	-DOI:10.1038/nbt936 \
	-DOI:10.1016/j.bbrc.2004.02.157 
	
* GC% - percent content of G and C nucleotides in RNAi sequence (best target between 35-55%)
* sense_loop_complementary - part of sense strand RNAi complementary to the loop
* sense_loop_complementary_pct - percent of nucleotides from the sense strand of RNAi complementary to the loop
* antisense_loop_complementary - part of antisense strand RNAi complementary to the loop
* antisense_loop_complementary_pct - percent of nucleotides from the antisense strand of RNAi complementary to the loop



<br />

#### 1.25. Correcting of RNAi_data for complementarity to the additional external sequence <a id="correcting-sequence"></a>

```
RNAi_data = st.remove_specific_to_sequence(RNAi_data, sequence, min_length=4)
```

<br />

##### Example of data frame output:


|RNAi_name|RNAi_seq               |target                                      |e-value       |bit_score  |alignment_length|target_seq                 |target_gene_name|species         |specificity|complemenatry_regions|complemenatry_pct  |RNAi_sense             |repeated_motif|repeated_motif_pct|score|GC%  |sense_loop_complementary|sense_loop_complementary_pct|antisense_loop_complementary|antisense_loop_complementary_pct|
|---------|-----------------------|--------------------------------------------|--------------|-----------|----------------|---------------------------|--------------- |----------------|-----------|---------------------|-------------------|-----------------------|--------------|------------------|-----|-----|------------------------|----------------------------|----------------------------|--------------------------------|
|RNAi_183 |TTTGATTTTGTCTGAAACCCATA|['Homo sapiens survival of motor neuron 1'] |[2.07974e-05] |  [46.087] |     [23]       |['TTTGATTTTGTCTGAAACCCATA']|    ['SMN1']    |['Homo sapiens']|     1     |[]                   |0.0                |TATGGGTTTCAGACAAAATCAAA|['TTTTTTT']   |        0.3       |0    |17.04|[]                      |0.0                         |[]                          |0.0                             |
|RNAi_164 |TTTTGATTTTGTCTGAAACCCAT|['Homo sapiens survival of motor neuron 1'] |[2.07974e-05] |  [46.087] |     [23]       |['TTTTGATTTTGTCTGAAACCCAT']|    ['SMN1']    |['Homo sapiens']|     1     |[]                   |0.0                |ATGGGTTTCAGACAAAATCAAAA|['TTTTTTTT']  |        0.35      |1.0  |17.04|[]                      |0.0                         |[]                          |0.0                             |

<br />

* Data reduced by RNAi records with too high complementarity of the provided sequence
* Columns explanation as in the paragraphs 1.23  and / or 1.24

<br />
<br />


#### 1.26. Codon optimization <a id="optimize"></a>

```
optimized_data = st.codon_otymization(sequence, metadata, species = 'human')
```


<br />


#### 1.27. Checking susceptibility to restriction enzymes <a id="resctriction"></a>

```
all_restriction_places, reduced_restriction_places_with_indexes = st.check_restriction(sequence, metadata)
```



<br />


#### 1.28. Checking and removing susceptibility to restriction enzymes <a id="resctriction-remove"></a>

```
repaired_sequence_data = st.sequence_restriction_removal(sequence, metadata, restriction_places = [], species = 'human')
```

<br />

### 2. vector_build - part of the library containing building plasmid vectors with optimization elements from seq_tools <a id="vector-build"></a>

#### 2.1. Import part of library <a id="import-vector_build"></a>

<br />

```
from jbst import vector_build as vb
```
<br />

#### 2.2. Creating vector plasmid <a id="creating-vector"></a>

<br />

```
project = vb.vector_create_on_dict(metadata, input_dict, show_plot=True)
```


<br />


#### 2.2.1 Creating expression of the plasmid vector <a id="expression"></a>

##### Empty input dictionary schema:


```
input_dict = {
    
    # REQUIRED!
    # name of current project (defined by user)
    'project_name':''
    
    # REQUIRED!
    # avaiable of vector types (ssAAV / scAAV / lentiviral / regular)
    'vector_type':'',
    
    # REQUIRED!
    # in this case 'vector_function':'expression'
    'vector_function':'expression',
    
    # REQUIRED!
    # avaiable options (human / mouse / rat / both (mouse + human) / both2 (rat + human) / multi (mouse + rat + human))
    # 'both / both2 / multi' - creating vector function adjusted for all species taking into consideration most adjustments for Homo sapiens
    'species':'human',
    
    # list of coding sequences (CDS) provided to make expression from the vector
    # the CSD sequences the user can obtain from ...
    # amount of sequences is not restricted as the user must remember that the length of whole vector is limited
    # excide the relevant vector size can decrease vector working
    # if the user wants to not include any sequences only fluorescent_tag, provide ['']
    # sequences orientation 5' ---> 3' - sense
    'sequences':[''],
    # list of names of coding sequences
    # amount of names should be equal with amount of sequences
    # if provided no sequences, provide ['']
    'sequences_names':[''],
    
    # REQUIRED!
    # sequence of provided promoter
    # name and sequence the user can take from metadata['promoters'] (load_metadata())
    # for coding sequences the user should choose the promoter of coding genes (metadata['promoters']['type'] == 'coding')
    # sequence orientation 5' ---> 3' - sense
    'promoter_sequence':'',
    # REQUIRED!
    # name of provided promoter sequence
    'promoter_name':'',
    
    # POSSIBLE!
    # sequence of provided enhancer
    # name and sequence the user can take from metadata['regulators'] (load_metadata())
    # sequence orientation 5' ---> 3' - sense
    'regulator_sequence':'',
    # POSSIBLE!
    # name of provided enhancer sequence
    'regulator_name':'',
    
    # REQUIRED!
    # sequence of provided polyA signal
    # name and sequence the user can take from metadata['polya_seq'] (load_metadata())
    'polya_sequence':'',
    # REQUIRED!
    # name of provided polyA signal sequence
    'polya_name':'',
    
    
    # REQUIRED if more than one sequence of transcripts!
    # sequences of provided linkers
    # number of linkers_sequences should be equal number of sequences (transcripts) - 1. One linker for each pair of sequences.
    # name and sequence the user can take from metadata['linkers'] (load_metadata())
    # if the number of transcript sequences is equal 1 then provide empty list []
    # if the user wants to not provide any linkers between the transcript sequences, provide an empty string '' for each pair of transcripts where the user wants to avoid linker; empty strings '' provide inside the list ['']
    # sequence orientation 5' ---> 3' - sense
    'linkers_sequences':[''],
    # REQUIRED if more than one sequence!
    # names of provided linkers
    # if the number of transcript sequences is equal 1 then provide empty list []
    # if the user wants to not provide any linkers between the transcript sequences, provide an empty string '' for each pair of transcripts where the user wants to avoid linker; empty strings '' provide inside the list ['']
    'linkers_names':[''],
    
    # POSSIBLE!
    # sequence of provided fluorescent tag
    # name and sequence the user can take from metadata['fluorescent_tag'] (load_metadata())
    # if the user does not need fluorescent tag, provide ''
    # sequence orientation 5' ---> 3' - sense
    'fluorescence_sequence':'',
    # POSSIBLE!
    # name of provided fluorescent tag
    # if the user does not need fluorescent tag, provide ''
    'fluorescence_name':'',
    
    # WARNING! If the user wants to use an additional promoter for the fluorescent tag expression, provide data for fluorescence_promoter_sequence & fluorescence_polya_sequence!
    
    # POSSIBLE!
    # sequence of provided fluorescence promoter
    # name and sequence the user can take from metadata['promoters'] (load_metadata())
    # if the user does not need additional promoter for fluorescent tag, provide ''
    # sequence orientation 5' ---> 3' - sense
    'fluorescence_promoter_sequence':'',
    # POSSIBLE!
    # name of provided fluorescence promoter
    # if the user does not need additional promoter for fluorescent tag, provide ''
    'fluorescence_promoter_name':'',
    
    # POSSIBLE!
    # sequence of provided fluorescence polyA signal
    # name and sequence the user can take from metadata['polya_seq'] (load_metadata())
    # if the user does not need additional promoter for fluorescent tag, provide ''
    # sequence orientation 5' ---> 3' - sense
    'fluorescence_polya_sequence':'',
    # POSSIBLE!
    # name of provided fluorescence polyA signal
    # if the user does not need additional promoter for fluorescent tag, provide ''
    'fluorescence_polya_name':'',
    
    
    # WARNING! If provided sequences for transcripts (> 0) and do not need additional promoter for fluorescent tag, provide fluorescence_linker_sequence or provide empty string ''.

    # POSSIBLE!
    # sequence of provided fluorescence tag linker
    # name and sequence the user can take from metadata['linkers'] (load_metadata())
    # if the user has provided additional promoter, so the fluorescence_linker_sequence is not needed, provide ''
    # sequence orientation 5' ---> 3' - sense
    'fluorescence_linker_sequence':'',
    # POSSIBLE!
    # name of provided fluorescence tag linker
    # if the user has provided additional promoter, so the fluorescence_linker_sequence is not needed, provide ''
    'fluorescence_linker_name':'',
    
    # REQUIRED!
    # sequence of provided selection marker
    # name and sequence the user can take from metadata['selection_markers'] (load_metadata())
    # sequence orientation 5' ---> 3' - sense
    'selection_marker_sequence':'',
    # REQUIRED!
    # name of provided selection marker
    'selection_marker_name':'',
    
    # POSSIBLE!
    # restriction enzymes protection of transcript sequences
    # enzymes the user can take from metadata['restriction'] (load_metadata())
    # if do not need any restriction places protection, provide an empty list []
    'restriction_list':[],
    
    # REQUIRED!
    # available options (True / False)
    # decision; if the user wants the transcription sequences optimized based on the provided species
    'optimize':True
}

```


<br />


##### Example dictionary:

```

input_dict = {
    
    'project_name':'test_expression',
    'vector_type':'ssAAV',
    'vector_function':'expression',
    'species':'human',
    'sequences':['ATGGCGATGAGCAGCGGCGGCAGTGGTGGCGGCGTCCCGGAGCAGGAGGATTCCGTGCTGTTCCGGCGCGGCACAGGCCAGAGCGATGATTCTGACATTTGGGATGATACAGCACTGATAAAAGCATATGATAAAGCTGTGGCTTCATTTAAGCATGCTCTAAAGAATGGTGACATTTGTGAAACTTCGGGTAAACCAAAAACCACACCTAAAAGAAAACCTGCTAAGAAGAATAAAAGCCAAAAGAAGAATACTGCAGCTTCCTTACAACAGTGGAAAGTTGGGGACAAATGTTCTGCCATTTGGTCAGAAGACGGTTGCATTTACCCAGCTACCATTGCTTCAATTGATTTTAAGAGAGAAACCTGTGTTGTGGTTTACACTGGATATGGAAATAGAGAGGAGCAAAATCTGTCCGATCTACTTTCCCCAATCTGTGAAGTAGCTAATAATATAGAACAAAATGCTCAAGAGAATGAAAATGAAAGCCAAGTTTCAACAGATGAAAGTGAGAACTCCAGGTCTCCTGGAAATAAATCAGATAACATCAAGCCCAAATCTGCTCCATGGAACTCTTTTCTCCCTCCACCACCCCCCATGCCAGGGCCAAGACTGGGACCAGGAAAGCCAGGTCTAAAATTCAATGGCCCACCACCGCCACCGCCACCACCACCACCCCACTTACTATCATGCTGGCTGCCTCCATTTCCTTCTGGACCACCAATAATTCCCCCACCACCTCCCATATGTCCAGATTCTCTTGATGATGCTGATGCTTTGGGAAGTATGTTAATTTCATGGTACATGAGTGGCTATCATACTGGCTATTATATGTTTCCTGAGGCCTCCCTAAAAGCCGAGCAGATGCCAGCACCATGCTTCCTGTAA',
                 'ATGGCGATGAGCAGCGGCGGCAGTGGTGGCGGCGTCCCGGAGCAGGAGGATTCCGTGCTGTTCCGGCGCGGCACAGGCCAGAGCGATGATTCTGACATTTGGGATGATACAGCACTGATAAAAGCATATGATAAAGCTGTGGCTTCATTTAAGCATGCTCTAAAGAATGGTGACATTTGTGAAACTTCGGGTAAACCAAAAACCACACCTAAAAGAAAACCTGCTAAGAAGAATAAAAGCCAAAAGAAGAATACTGCAGCTTCCTTACAACAGTGGAAAGTTGGGGACAAATGTTCTGCCATTTGGTCAGAAGACGGTTGCATTTACCCAGCTACCATTGCTTCAATTGATTTTAAGAGAGAAACCTGTGTTGTGGTTTACACTGGATATGGAAATAGAGAGGAGCAAAATCTGTCCGATCTACTTTCCCCAATCTGTGAAGTAGCTAATAATATAGAACAAAATGCTCAAGAGAATGAAAATGAAAGCCAAGTTTCAACAGATGAAAGTGAGAACTCCAGGTCTCCTGGAAATAAATCAGATAACATCAAGCCCAAATCTGCTCCATGGAACTCTTTTCTCCCTCCACCACCCCCCATGCCAGGGCCAAGACTGGGACCAGGAAAGCCAGGTCTAAAATTCAATGGCCCACCACCGCCACCGCCACCACCACCACCCCACTTACTATCATGCTGGCTGCCTCCATTTCCTTCTGGACCACCAATAATTCCCCCACCACCTCCCATATGTCCAGATTCTCTTGATGATGCTGATGCTTTGGGAAGTATGTTAATTTCATGGTACATGAGTGGCTATCATACTGGCTATTATATGTTTCCTGAGGCCTCCCTAAAAGCCGAGCAGATGCCAGCACCATGCTTCCTGTAA'],
    'sequences_names':['SMN1','SMN2'],
    'promoter_sequence':'GGGCTGGAAGCTACCTTTGACATCATTTCCTCTGCGAATGCATGTATAATTTCTACAGAACCTATTAGAAAGGATCACCCAGCCTCTGCTTTTGTACAACTTTCCCTTAAAAAACTGCCAATTCCACTGCTGTTTGGCCCAATAGTGAGAACTTTTTCCTGCTGCCTCTTGGTGCTTTTGCCTATGGCCCCTATTCTGCCTGCTGAAGACACTCTTGCCAGCATGGACTTAAACCCCTCCAGCTCTGACAATCCTCTTTCTCTTTTGTTTTACATGAAGGGTCTGGCAGCCAAAGCAATCACTCAAAGTTCAAACCTTATCATTTTTTGCTTTGTTCCTCTTGGCCTTGGTTTTGTACATCAGCTTTGAAAATACCATCCCAGGGTTAATGCTGGGGTTAATTTATAACTAAGAGTGCTCTAGTTTTGCAATACAGGACATGCTATAAAAATGGAAAGAT',
    'promoter_name':'TBG',
    'regulator_sequence':'CGATAATCAACCTCTGGATTACAAAATTTGTGAAAGATTGACTGGTATTCTTAACTATGTTGCTCCTTTTACGCTATGTGGATACGCTGCTTTAATGCCTTTGTATCATGCTATTGCTTCCCGTATGGCTTTCATTTTCTCCTCCTTGTATAAATCCTGGTTGCTGTCTCTTTATGAGGAGTTGTGGCCCGTTGTCAGGCAACGTGGCGTGGTGTGCACTGTGTTTGCTGACGCAACCCCCACTGGTTGGGGCATTGCCACCACCTGTCAGCTCCTTTCCGGGACTTTCGCTTTCCCCCTCCCTATTGCCACGGCGGAACTCATCGCCGCCTGCCTTGCCCGCTGCTGGACAGGGGCTCGGCTGTTGGGCACTGACAATTCCGTGGTGTTGTCGGGGAAGCTGACGTCCTTTCCATGGCTGCTCGCCTGTGTTGCCACCTGGATTCTGCGCGGGACGTCCTTCTGCTACGTCCCTTCGGCCCTCAATCCAGCGGACCTTCCTTCCCGCGGCCTGCTGCCGGCTCTGCGGCCTCTTCCGCGTCTTCGCCTTCGCCCTCAGACGAGTCGGATCTCCCTTTGGGCCGCCTCCCCGCATCGG',
    'regulator_name':'WPRE',
    'polya_sequence':'CAGACATGATAAGATACATTGATGAGTTTGGACAAACCACAACTAGAATGCAGTGAAAAAAATGCTTTATTTGTGAAATTTGTGATGCTATTGCTTTATTTGTAACCATTATAAGCTGCAATAAACAAGTTAACAACAACAATTGCATTCATTTTATGTTTCAGGTTCAGGGGGAGGTGTGGGAGGTTTTTTAAAGCAAGTAAAACCTCTACAAATGTGGTA',
    'polya_name':'SV40_late',
    'linkers_sequences':['GGAAGCGGAGAGGGCAGGGGAAGTCTTCTAACATGCGGGGACGTGGAGGAAAATCCCGGCCCC'],
    'linkers_names':['T2A'],
    'fluorescence_sequence':'ATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCTGGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGAGGGCGATGCCACCTACGGCAAGCTGACCCTGAAGTTCATCTGCACCACCGGCAAGCTGCCCGTGCCCTGGCCCACCCTCGTGACCACCCTGACCTACGGCGTGCAGTGCTTCAGCCGCTACCCCGACCACATGAAGCAGCACGACTTCTTCAAGTCCGCCATGCCCGAAGGCTACGTCCAGGAGCGCACCATCTTCTTCAAGGACGACGGCAACTACAAGACCCGCGCCGAGGTGAAGTTCGAGGGCGACACCCTGGTGAACCGCATCGAGCTGAAGGGCATCGACTTCAAGGAGGACGGCAACATCCTGGGGCACAAGCTGGAGTACAACTACAACAGCCACAACGTCTATATCATGGCCGACAAGCAGAAGAACGGCATCAAGGTGAACTTCAAGATCCGCCACAACATCGAGGACGGCAGCGTGCAGCTCGCCGACCACTACCAGCAGAACACCCCCATCGGCGACGGCCCCGTGCTGCTGCCCGACAACCACTACCTGAGCACCCAGTCCGCCCTGAGCAAAGACCCCAACGAGAAGCGCGATCACATGGTCCTGCTGGAGTTCGTGACCGCCGCCGGGATCACTCTCGGCATGGACGAGCTGTACAAGTAA',
    'fluorescence_name':'EGFP',
    'fluorescence_promoter_sequence':'CTCGACATTGATTATTGACTAGTTATTAATAGTAATCAATTACGGGGTCATTAGTTCATAGCCCATATATGGAGTTCCGCGTTACATAACTTACGGTAAATGGCCCGCCTGGCTGACCGCCCAACGACCCCCGCCCATTGACGTCAATAATGACGTATGTTCCCATAGTAACGCCAATAGGGACTTTCCATTGACGTCAATGGGTGGAGTATTTACGGTAAACTGCCCACTTGGCAGTACATCAAGTGTATCATATGCCAAGTACGCCCCCTATTGACGTCAATGACGGTAAATGGCCCGCCTGGCATTATGCCCAGTACATGACCTTATGGGACTTTCCTACTTGGCAGTACATCTACGTATTAGTCATCGCTATTACCATGGTCGAGGTGAGCCCCACGTTCTGCTTCACTCTCCCCATCTCCCCCCCCTCCCCACCCCCAATTTTGTATTTATTTATTTTTTAATTATTTTGTGCAGCGATGGGGGCGGGGGGGGGGGGGGGGCGCGCGCCAGGCGGGGCGGGGCGGGGCGAGGGGCGGGGCGGGGCGAGGCGGAGAGGTGCGGCGGCAGCCAATCAGAGCGGCGCGCTCCGAAAGTTTCCTTTTATGGCGAGGCGGCGGCGGCGGCGGCCCTATAAAAAGCGAAGCGCGCGGCGGGCGGGAGTCGCTGCGCGCTGCCTTCGCCCCGTGCCCCGCTCCGCCGCCGCCTCGCGCCGCCCGCCCCGGCTCTGACTGACCGCGTTACTCCCACAGGTGAGCGGGCGGGACGGCCCTTCTCCTCCGGGCTGTAATTAGCGCTTGGTTTAATGACGGCTTGTTTCTTTTCTGTGGCTGCGTGAAAGCCTTGAGGGGCTCCGGGAGGGCCCTTTGTGCGGGGGGAGCGGCTCGGGGGGTGCGTGCGTGTGTGTGTGCGTGGGGAGCGCCGCGTGCGGCTCCGCGCTGCCCGGCGGCTGTGAGCGCTGCGGGCGCGGCGCGGGGCTTTGTGCGCTCCGCAGTGTGCGCGAGGGGAGCGCGGCCGGGGGCGGTGCCCCGCGGTGCGGGGGGGGCTGCGAGGGGAACAAAGGCTGCGTGCGGGGTGTGTGCGTGGGGGGGTGAGCAGGGGGTGTGGGCGCGTCGGTCGGGCTGCAACCCCCCCTGCACCCCCCTCCCCGAGTTGCTGAGCACGGCCCGGCTTCGGGTGCGGGGCTCCGTACGGGGCGTGGCGCGGGGCTCGCCGTGCCGGGCGGGGGGTGGCGGCAGGTGGGGGTGCCGGGCGGGGCGGGGCCGCCTCGGGCCGGGGAGGGCTCGGGGGAGGGGCGCGGCGGCCCCCGGAGCGCCGGCGGCTGTCGAGGCGCGGCGAGCCGCAGCCATTGCCTTTTATGGTAATCGTGCGAGAGGGCGCAGGGACTTCCTTTGTCCCAAATCTGTGCGGAGCCGAAATCTGGGAGGCGCCGCCGCACCCCCTCTAGCGGGCGCGGGGCGAAGCGGTGCGGCGCCGGCAGGAAGGAAATGGGCGGGGAGGGCCTTCGTGCGTCGCCGCGCCGCCGTCCCCTTCTCCCTCTCCAGCCTCGGGGCTGTCCGCGGGGGGACGGCTGCCTTCGGGGGGGACGGGGCAGGGCGGGGTTCGGCTTCTGGCGTGTGACCGGCGGCTCTAGAGCCTCTGCTAACCATGTTCATGCCTTCTTCTTTTTCCTACAGCTCCTGGGCAACGTGCTGGTTATTGTGCTGTCTCATCATTTTGGCAAAGAATTG',
    'fluorescence_promoter_name':'CAG',
    'fluorescence_polya_sequence':'CTGTGCCTTCTAGTTGCCAGCCATCTGTTGTTTGCCCCTCCCCCGTGCCTTCCTTGACCCTGGAAGGTGCCACTCCCACTGTCCTTTCCTAATAAAATGAGGAAATTGCATCGCATTGTCTGAGTAGGTGTCATTCTATTCTGGGGGGTGGGGTGGGGCAGGACAGCAAGGGGGAGGATTGGGAAGAGAATAGCAGGCATGCTGGGGA',
    'fluorescence_polya_name':'bGH',
    'fluorescence_linker_sequence':'GGAAGCGGAGAGGGCAGGGGAAGTCTTCTAACATGCGGGGACGTGGAGGAAAATCCCGGCCCC',
    'fluorescence_linker_name':'T2A',
    'selection_marker_sequence':'ATGAGTATTCAACATTTCCGTGTCGCCCTTATTCCCTTTTTTGCGGCATTTTGCCTTCCTGTTTTTGCTCACCCAGAAACGCTGGTGAAAGTAAAAGATGCTGAAGATCAGTTGGGTGCACGAGTGGGTTACATCGAACTGGATCTCAACAGCGGTAAGATCCTTGAGAGTTTTCGCCCCGAAGAACGTTTTCCAATGATGAGCACTTTTAAAGTTCTGCTATGTGGCGCGGTATTATCCCGTATTGACGCCGGGCAAGAGCAACTCGGTCGCCGCATACACTATTCTCAGAATGACTTGGTTGAGTACTCACCAGTCACAGAAAAGCATCTTACGGATGGCATGACAGTAAGAGAATTATGCAGTGCTGCCATAACCATGAGTGATAACACTGCGGCCAACTTACTTCTGACAACGATCGGAGGACCGAAGGAGCTAACCGCTTTTTTGCACAACATGGGGGATCATGTAACTCGCCTTGATCGTTGGGAACCGGAGCTGAATGAAGCCATACCAAACGACGAGCGTGACACCACGATGCCTGTAGCAATGGCAACAACGTTGCGCAAACTATTAACTGGCGAACTACTTACTCTAGCTTCCCGGCAACAATTAATAGACTGGATGGAGGCGGATAAAGTTGCAGGACCACTTCTGCGCTCGGCCCTTCCGGCTGGCTGGTTTATTGCTGATAAATCTGGAGCCGGTGAGCGTGGAAGCCGCGGTATCATTGCAGCACTGGGGCCAGATGGTAAGCCCTCCCGTATCGTAGTTATCTACACGACGGGGAGTCAGGCAACTATGGATGAACGAAATAGACAGATCGCTGAGATAGGTGCCTCACTGATTAAGCATTGGTAA',
    'selection_marker_name':'Ampicillin',
    'restriction_list':['RsaI', 'MnlI', 'AciI', 'AluI', 'BmrI'],
    'optimize':True
}

```

<br />

##### Output:

```
# Name of the project
project['project']
```

``` 
# Graph of the designed vector
vector_plot = project['vector']['graph']
vector_plot.savefig('expression_vector.svg')
```
<br />

Example return:

<p align="center">
<img  src="https://raw.githubusercontent.com/jkubis96/JBioSeqTools/3fb8a369a9c893d65589a92680fcb1e0cbcefa87/fig/expression_vector.svg" alt="drawing" width="600" />
</p>

<br />

```
# Complete FASTA file of the designed vecotr
project['vector']['full_fasta']
```

Example return:

```
>test_expression_ssAAV_expression_8780nc
CTGCGCGCTCGCTCGCTCACTGAGGCCGCCCGGGCAAAGCCCGGGCGTCGGGCGACCTTTGGTCGCCCGGCCTCAGTGAGCGAGCGAGCGCGCAGAGAGGGAGTGGCCAACTCCATCACTAGGGGTTCCTTCTAGACAACTTTGTATAGAAAAGTTGGGGCTGGAAGCTACCTTTGACATCATTTCCTCTGCGAATGCATGTATAATTTCTACAGAACCTATTAGAAAGGATCACCCAGCCTCTGCTTTTGTACAACTTTCCCTTAAAAAACTGCCAATTCCACTGCTGTTTGGCCCAATAGTGAGAACTTTTTCCTGCTGCCTCTTGGTGCTTTTGCCTATGGCCCCTATTCTGCCTGCTGAAGACACTCTTGCCAGCATGGACTTAAACCCCTCCAGCTCTGACAATCCTCTTTCTCTTTTGTTTTACATGAAGGGTCTGGCAGCCAAAGCAATCACTCAAAGTTCAAACCTTATCATTTTTTGCTTTGTTCCTCTTGGCCTTGGTTTTGTACATCAGCTTTGAAAATACCATCCCAGGGTTAATGCTGGGGTTAATTTATAACTAAGAGTGCTCTAGTTTTGCAATACAGGACATGCTATAAAAATGGAAAGATCAAGTTTGTACAAAAAAGCAGGCTGCCACCATGGCTATGTCTAGCGGAGGCTCTGGAGGAGGAGTTCCTGAACAGGAGGACTCTGTGCTGTTCCGGAGGGGCACAGGACAAAGCGATGACAGCGACATCTGGGACGACACAGCTCTGATTAAGGCCTACGACAAGGCCGTGGCCAGCTTCAAGCACGCCCTGAAGAACGGCGACATCTGCGAGACCAGCGGAAAGCCTAAAACCACCCCTAAGAGAAAGCCTGCTAAAAAGAACAAGAGCCAGAAGAAGAACACCGCTGCCAGCCTGCAGCAGTGGAAGGTGGGCGACAAGTGCAGCGCCATTTGGAGCGAGGACGGATGTATCTACCCTGCCACAATCGCCAGCATCGACTTCAAGCGGGAGACCTGCGTGGTGGTGTATACCGGCTACGGCAACAGGGAAGAGCAGAACCTGAGCGACCTGCTGAGCCCTATTTGCGAGGTGGCCAATAACATCGAGCAGAACGCCCAGGAGAACGAGAACGAGAGCCAGGTGAGCACCGACGAGAGCGAGAACAGCCGGAGCCCCGGCAATAAGAGCGACAACATCAAGCCCAAGAGCGCCCCCTGGAACTCTTTCCTGCCCCCCCCCCCCCCCATGCCTGGACCTAGATTGGGACCTGGAAAACCTGGACTGAAATTCAACGGCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCATTTGCTGTCTTGTTGGCTGCCCCCCTTCCCTTCTGGACCCCCCATTATCCCCCCCCCCCCCCCCATCTGTCCTGATTCTCTGGACGACGCCGATGCTTTGGGCTCTATGCTGATCTCTTGGTATATGAGCGGCTACCACACCGGCTACTACATGTTCCCCGAGGCCAGCCTGAAGGCCGAGCAGATGCCCGCTCCTTGTTTTCTGGGAAGCGGAGAGGGCAGGGGAAGTCTTCTAACATGCGGGGACGTGGAGGAAAATCCCGGCCCCATGGCTATGTCTAGCGGAGGCTCTGGAGGAGGAGTTCCTGAACAGGAGGACTCTGTGCTGTTCCGGAGGGGCACAGGACAAAGCGATGACAGCGACATCTGGGACGACACAGCTCTGATTAAGGCCTACGACAAGGCCGTGGCCAGCTTCAAGCACGCCCTGAAGAACGGCGACATCTGCGAGACCAGCGGAAAGCCTAAAACCACCCCTAAGAGAAAGCCTGCTAAAAAGAACAAGAGCCAGAAGAAGAACACCGCTGCCAGCCTGCAGCAGTGGAAGGTGGGCGACAAGTGCAGCGCCATTTGGAGCGAGGACGGATGTATCTACCCTGCCACAATCGCCAGCATCGACTTCAAGCGGGAGACCTGCGTGGTGGTGTATACCGGCTACGGCAACAGGGAAGAGCAGAACCTGAGCGACCTGCTGAGCCCTATTTGCGAGGTGGCCAATAACATCGAGCAGAACGCCCAGGAGAACGAGAACGAGAGCCAGGTGAGCACCGACGAGAGCGAGAACAGCCGGAGCCCCGGCAATAAGAGCGACAACATCAAGCCCAAGAGCGCCCCCTGGAACTCTTTCCTGCCCCCCCCCCCCCCCATGCCTGGACCTAGATTGGGACCTGGAAAACCTGGACTGAAATTCAACGGCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCATTTGCTGTCTTGTTGGCTGCCCCCCTTCCCTTCTGGACCCCCCATTATCCCCCCCCCCCCCCCCATCTGTCCTGATTCTCTGGACGACGCCGATGCTTTGGGCTCTATGCTGATCTCTTGGTATATGAGCGGCTACCACACCGGCTACTACATGTTCCCCGAGGCCAGCCTGAAGGCCGAGCAGATGCCCGCTCCTTGTTTTCTGTGACAGACATGATAAGATACATTGATGAGTTTGGACAAACCACAACTAGAATGCAGTGAAAAAAATGCTTTATTTGTGAAATTTGTGATGCTATTGCTTTATTTGTAACCATTATAAGCTGCAATAAACAAGTTAACAACAACAATTGCATTCATTTTATGTTTCAGGTTCAGGGGGAGGTGTGGGAGGTTTTTTAAAGCAAGTAAAACCTCTACAAATGTGGTACTCGACATTGATTATTGACTAGTTATTAATAGTAATCAATTACGGGGTCATTAGTTCATAGCCCATATATGGAGTTCCGCGTTACATAACTTACGGTAAATGGCCCGCCTGGCTGACCGCCCAACGACCCCCGCCCATTGACGTCAATAATGACGTATGTTCCCATAGTAACGCCAATAGGGACTTTCCATTGACGTCAATGGGTGGAGTATTTACGGTAAACTGCCCACTTGGCAGTACATCAAGTGTATCATATGCCAAGTACGCCCCCTATTGACGTCAATGACGGTAAATGGCCCGCCTGGCATTATGCCCAGTACATGACCTTATGGGACTTTCCTACTTGGCAGTACATCTACGTATTAGTCATCGCTATTACCATGGTCGAGGTGAGCCCCACGTTCTGCTTCACTCTCCCCATCTCCCCCCCCTCCCCACCCCCAATTTTGTATTTATTTATTTTTTAATTATTTTGTGCAGCGATGGGGGCGGGGGGGGGGGGGGGGCGCGCGCCAGGCGGGGCGGGGCGGGGCGAGGGGCGGGGCGGGGCGAGGCGGAGAGGTGCGGCGGCAGCCAATCAGAGCGGCGCGCTCCGAAAGTTTCCTTTTATGGCGAGGCGGCGGCGGCGGCGGCCCTATAAAAAGCGAAGCGCGCGGCGGGCGGGAGTCGCTGCGCGCTGCCTTCGCCCCGTGCCCCGCTCCGCCGCCGCCTCGCGCCGCCCGCCCCGGCTCTGACTGACCGCGTTACTCCCACAGGTGAGCGGGCGGGACGGCCCTTCTCCTCCGGGCTGTAATTAGCGCTTGGTTTAATGACGGCTTGTTTCTTTTCTGTGGCTGCGTGAAAGCCTTGAGGGGCTCCGGGAGGGCCCTTTGTGCGGGGGGAGCGGCTCGGGGGGTGCGTGCGTGTGTGTGTGCGTGGGGAGCGCCGCGTGCGGCTCCGCGCTGCCCGGCGGCTGTGAGCGCTGCGGGCGCGGCGCGGGGCTTTGTGCGCTCCGCAGTGTGCGCGAGGGGAGCGCGGCCGGGGGCGGTGCCCCGCGGTGCGGGGGGGGCTGCGAGGGGAACAAAGGCTGCGTGCGGGGTGTGTGCGTGGGGGGGTGAGCAGGGGGTGTGGGCGCGTCGGTCGGGCTGCAACCCCCCCTGCACCCCCCTCCCCGAGTTGCTGAGCACGGCCCGGCTTCGGGTGCGGGGCTCCGTACGGGGCGTGGCGCGGGGCTCGCCGTGCCGGGCGGGGGGTGGCGGCAGGTGGGGGTGCCGGGCGGGGCGGGGCCGCCTCGGGCCGGGGAGGGCTCGGGGGAGGGGCGCGGCGGCCCCCGGAGCGCCGGCGGCTGTCGAGGCGCGGCGAGCCGCAGCCATTGCCTTTTATGGTAATCGTGCGAGAGGGCGCAGGGACTTCCTTTGTCCCAAATCTGTGCGGAGCCGAAATCTGGGAGGCGCCGCCGCACCCCCTCTAGCGGGCGCGGGGCGAAGCGGTGCGGCGCCGGCAGGAAGGAAATGGGCGGGGAGGGCCTTCGTGCGTCGCCGCGCCGCCGTCCCCTTCTCCCTCTCCAGCCTCGGGGCTGTCCGCGGGGGGACGGCTGCCTTCGGGGGGGACGGGGCAGGGCGGGGTTCGGCTTCTGGCGTGTGACCGGCGGCTCTAGAGCCTCTGCTAACCATGTTCATGCCTTCTTCTTTTTCCTACAGCTCCTGGGCAACGTGCTGGTTATTGTGCTGTCTCATCATTTTGGCAAAGAATTGATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCTGGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGAGGGCGATGCCACCTACGGCAAGCTGACCCTGAAGTTCATCTGCACCACCGGCAAGCTGCCCGTGCCCTGGCCCACCCTCGTGACCACCCTGACCTACGGCGTGCAGTGCTTCAGCCGCTACCCCGACCACATGAAGCAGCACGACTTCTTCAAGTCCGCCATGCCCGAAGGCTACGTCCAGGAGCGCACCATCTTCTTCAAGGACGACGGCAACTACAAGACCCGCGCCGAGGTGAAGTTCGAGGGCGACACCCTGGTGAACCGCATCGAGCTGAAGGGCATCGACTTCAAGGAGGACGGCAACATCCTGGGGCACAAGCTGGAGTACAACTACAACAGCCACAACGTCTATATCATGGCCGACAAGCAGAAGAACGGCATCAAGGTGAACTTCAAGATCCGCCACAACATCGAGGACGGCAGCGTGCAGCTCGCCGACCACTACCAGCAGAACACCCCCATCGGCGACGGCCCCGTGCTGCTGCCCGACAACCACTACCTGAGCACCCAGTCCGCCCTGAGCAAAGACCCCAACGAGAAGCGCGATCACATGGTCCTGCTGGAGTTCGTGACCGCCGCCGGGATCACTCTCGGCATGGACGAGCTGTACAAGTAAACCCAGCTTTCTTGTACAAAGTGGGAATTCCGATAATCAACCTCTGGATTACAAAATTTGTGAAAGATTGACTGGTATTCTTAACTATGTTGCTCCTTTTACGCTATGTGGATACGCTGCTTTAATGCCTTTGTATCATGCTATTGCTTCCCGTATGGCTTTCATTTTCTCCTCCTTGTATAAATCCTGGTTGCTGTCTCTTTATGAGGAGTTGTGGCCCGTTGTCAGGCAACGTGGCGTGGTGTGCACTGTGTTTGCTGACGCAACCCCCACTGGTTGGGGCATTGCCACCACCTGTCAGCTCCTTTCCGGGACTTTCGCTTTCCCCCTCCCTATTGCCACGGCGGAACTCATCGCCGCCTGCCTTGCCCGCTGCTGGACAGGGGCTCGGCTGTTGGGCACTGACAATTCCGTGGTGTTGTCGGGGAAGCTGACGTCCTTTCCATGGCTGCTCGCCTGTGTTGCCACCTGGATTCTGCGCGGGACGTCCTTCTGCTACGTCCCTTCGGCCCTCAATCCAGCGGACCTTCCTTCCCGCGGCCTGCTGCCGGCTCTGCGGCCTCTTCCGCGTCTTCGCCTTCGCCCTCAGACGAGTCGGATCTCCCTTTGGGCCGCCTCCCCGCATCGGGAATTCCTAGAGCTCGCTGATCAGCCTCGACTGTGCCTTCTAGTTGCCAGCCATCTGTTGTTTGCCCCTCCCCCGTGCCTTCCTTGACCCTGGAAGGTGCCACTCCCACTGTCCTTTCCTAATAAAATGAGGAAATTGCATCGCATTGTCTGAGTAGGTGTCATTCTATTCTGGGGGGTGGGGTGGGGCAGGACAGCAAGGGGGAGGATTGGGAAGAGAATAGCAGGCATGCTGGGGAGGGCCGCCTGCGCGCTCGCTCGCTCACTGAGGCCGCCCGGGCAAAGCCCGGGCGTCGGGCGACCTTTGGTCGCCCGGCCTCAGTGAGCGAGCGAGCGCGCAGAGAGGGAGTGGCCAACTCCATCACTAGGGGTTCCTCTGCCTGCAGGGGCGCCTGATGCGGTATTTTCTCCTTACGCATCTGTGCGGTATTTCACACCGCATACGTCAAAGCAACCATAGTACGCGCCCTGTAGCGGCGCATTAAGCGCGGCGGGGGTGGTGGTTACGCGCAGCGTGACCGCTACACTTGCCAGCGCCTTAGCGCCCGCTCCTTTCGCTTTCTTCCCTTCCTTTCTCGCCACGTTCGCCGGCTTTCCCCGTCAAGCTCTAAATCGGGGGCTCCCTTTAGGGTTCCGATTTAGTGCTTTACGGCACCTCGACCCCAAAAAACTTGATTTGGGTGATGGTTCACGTAGTGGGCCATCGCCCTGATAGACGGTTTTTCGCCCTTTGACGTTGGAGTCCACGTTCTTTAATAGTGGACTCTTGTTCCAAACTGGAACAACACTCAACTCTATCTCGGGCTATTCTTTTGATTTATAAGGGATTTTGCCGATTTCGGTCTATTGGTTAAAAAATGAGCTGATTTAACAAAAATTTAACGCGAATTTTAACAAAATATTAACGTTTACAATTTTATGGTGCACTCTCAGTACAATCTGCTCTGATGCCGCATAGTTAAGCCAGCCCCGACACCCGCCAACACCCGCTGACGCGCCCTGACGGGCTTGTCTGCTCCCGGCATCCGCTTACAGACAAGCTGTGACCGTCTCCGGGAGCTGCATGTGTCAGAGGTTTTCACCGTCATCACCGAAACGCGCGAGACGAAAGGGCCTCGTGATACGCCTATTTTTATAGGTTAATGTCATGATAATAATGGTTTCTTAGACGTCAGGTGGCACTTTTCGGGGAAATGTGCGCGGAACCCCTATTTGTTTATTTTTCTAAATACATTCAAATATGTATCCGCTCATGAGACAATAACCCTGATAAATGCTTCAATAATATTGAAAAAGGAAGAGTATGAGTATTCAACATTTCCGTGTCGCCCTTATTCCCTTTTTTGCGGCATTTTGCCTTCCTGTTTTTGCTCACCCAGAAACGCTGGTGAAAGTAAAAGATGCTGAAGATCAGTTGGGTGCACGAGTGGGTTACATCGAACTGGATCTCAACAGCGGTAAGATCCTTGAGAGTTTTCGCCCCGAAGAACGTTTTCCAATGATGAGCACTTTTAAAGTTCTGCTATGTGGCGCGGTATTATCCCGTATTGACGCCGGGCAAGAGCAACTCGGTCGCCGCATACACTATTCTCAGAATGACTTGGTTGAGTACTCACCAGTCACAGAAAAGCATCTTACGGATGGCATGACAGTAAGAGAATTATGCAGTGCTGCCATAACCATGAGTGATAACACTGCGGCCAACTTACTTCTGACAACGATCGGAGGACCGAAGGAGCTAACCGCTTTTTTGCACAACATGGGGGATCATGTAACTCGCCTTGATCGTTGGGAACCGGAGCTGAATGAAGCCATACCAAACGACGAGCGTGACACCACGATGCCTGTAGCAATGGCAACAACGTTGCGCAAACTATTAACTGGCGAACTACTTACTCTAGCTTCCCGGCAACAATTAATAGACTGGATGGAGGCGGATAAAGTTGCAGGACCACTTCTGCGCTCGGCCCTTCCGGCTGGCTGGTTTATTGCTGATAAATCTGGAGCCGGTGAGCGTGGAAGCCGCGGTATCATTGCAGCACTGGGGCCAGATGGTAAGCCCTCCCGTATCGTAGTTATCTACACGACGGGGAGTCAGGCAACTATGGATGAACGAAATAGACAGATCGCTGAGATAGGTGCCTCACTGATTAAGCATTGGTAACTGTCAGACCAAGTTTACTCATATATACTTTAGATTGATTTAAAACTTCATTTTTAATTTAAAAGGATCTAGGTGAAGATCCTTTTTGATAATCTCATGACCAAAATCCCTTAACGTGAGTTTTCGTTCCACTGAGCGTCAGACCCCGTAGAAAAGATCAAAGGATCTTCTTGAGATCCTTTTTTTCTGCGCGTAATCTGCTGCTTGCAAACAAAAAAACCACCGCTACCAGCGGTGGTTTGTTTGCCGGATCAAGAGCTACCAACTCTTTTTCCGAAGGTAACTGGCTTCAGCAGAGCGCAGATACCAAATACTGTTCTTCTAGTGTAGCCGTAGTTAGGCCACCACTTCAAGAACTCTGTAGCACCGCCTACATACCTCGCTCTGCTAATCCTGTTACCAGTGGCTGCTGCCAGTGGCGATAAGTCGTGTCTTACCGGGTTGGACTCAAGACGATAGTTACCGGATAAGGCGCAGCGGTCGGGCTGAACGGGGGGTTCGTGCACACAGCCCAGCTTGGAGCGAACGACCTACACCGAACTGAGATACCTACAGCGTGAGCTATGAGAAAGCGCCACGCTTCCCGAAGGGAGAAAGGCGGACAGGTATCCGGTAAGCGGCAGGGTCGGAACAGGAGAGCGCACGAGGGAGCTTCCAGGGGGAAACGCCTGGTATCTTTATAGTCCTGTCGGGTTTCGCCACCTCTGACTTGAGCGTCGATTTTTGTGATGCTCGTCAGGGGGGCGGAGCCTATGGAAAAACGCCAGCAACGCGGCCTTTTTACGGTTCCTGGCCTTTTGCTGGCCTTTTGCTCACATGTCCTGCAGGCAG
```
<br />
<br />

```
# The FASTA file is divided into particular elements of the designed vector
project['vector']['fasta']
```

Example return:

```
# test_expression_ssAAV_expression_8780nc

>5`ITR_start:1_stop:130_length:130 visible=True
CTGCGCGCTCGCTCGCTCACTGAGGCCGCCCGGGCAAAGCCCGGGCGTCGGGCGACCTTTGGTCGCCCGGCCTCAGTGAGCGAGCGAGCGCGCAGAGAGGGAGTGGCCAACTCCATCACTAGGGGTTCCT
>backbone_element_start:131_stop:157_length:27 visible=False
TCTAGACAACTTTGTATAGAAAAGTTG
>Promoter : TBG_start:158_stop:617_length:460 visible=True
GGGCTGGAAGCTACCTTTGACATCATTTCCTCTGCGAATGCATGTATAATTTCTACAGAACCTATTAGAAAGGATCACCCAGCCTCTGCTTTTGTACAACTTTCCCTTAAAAAACTGCCAATTCCACTGCTGTTTGGCCCAATAGTGAGAACTTTTTCCTGCTGCCTCTTGGTGCTTTTGCCTATGGCCCCTATTCTGCCTGCTGAAGACACTCTTGCCAGCATGGACTTAAACCCCTCCAGCTCTGACAATCCTCTTTCTCTTTTGTTTTACATGAAGGGTCTGGCAGCCAAAGCAATCACTCAAAGTTCAAACCTTATCATTTTTTGCTTTGTTCCTCTTGGCCTTGGTTTTGTACATCAGCTTTGAAAATACCATCCCAGGGTTAATGCTGGGGTTAATTTATAACTAAGAGTGCTCTAGTTTTGCAATACAGGACATGCTATAAAAATGGAAAGAT
>backbone_element_start:618_stop:641_length:24 visible=False
CAAGTTTGTACAAAAAAGCAGGCT
>Kozak_sequence_start:642_stop:647_length:6 visible=True
GCCACC
>SEQ1 : SMN1_start:648_stop:1532_length:885 visible=True
ATGGCTATGTCTAGCGGAGGCTCTGGAGGAGGAGTTCCTGAACAGGAGGACTCTGTGCTGTTCCGGAGGGGCACAGGACAAAGCGATGACAGCGACATCTGGGACGACACAGCTCTGATTAAGGCCTACGACAAGGCCGTGGCCAGCTTCAAGCACGCCCTGAAGAACGGCGACATCTGCGAGACCAGCGGAAAGCCTAAAACCACCCCTAAGAGAAAGCCTGCTAAAAAGAACAAGAGCCAGAAGAAGAACACCGCTGCCAGCCTGCAGCAGTGGAAGGTGGGCGACAAGTGCAGCGCCATTTGGAGCGAGGACGGATGTATCTACCCTGCCACAATCGCCAGCATCGACTTCAAGCGGGAGACCTGCGTGGTGGTGTATACCGGCTACGGCAACAGGGAAGAGCAGAACCTGAGCGACCTGCTGAGCCCTATTTGCGAGGTGGCCAATAACATCGAGCAGAACGCCCAGGAGAACGAGAACGAGAGCCAGGTGAGCACCGACGAGAGCGAGAACAGCCGGAGCCCCGGCAATAAGAGCGACAACATCAAGCCCAAGAGCGCCCCCTGGAACTCTTTCCTGCCCCCCCCCCCCCCCATGCCTGGACCTAGATTGGGACCTGGAAAACCTGGACTGAAATTCAACGGCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCATTTGCTGTCTTGTTGGCTGCCCCCCTTCCCTTCTGGACCCCCCATTATCCCCCCCCCCCCCCCCATCTGTCCTGATTCTCTGGACGACGCCGATGCTTTGGGCTCTATGCTGATCTCTTGGTATATGAGCGGCTACCACACCGGCTACTACATGTTCCCCGAGGCCAGCCTGAAGGCCGAGCAGATGCCCGCTCCTTGTTTTCTG
>Linker_1 : T2A_start:1533_stop:1595_length:63 visible=True
GGAAGCGGAGAGGGCAGGGGAAGTCTTCTAACATGCGGGGACGTGGAGGAAAATCCCGGCCCC
>SEQ2 : SMN2_start:1596_stop:2483_length:888 visible=True
ATGGCTATGTCTAGCGGAGGCTCTGGAGGAGGAGTTCCTGAACAGGAGGACTCTGTGCTGTTCCGGAGGGGCACAGGACAAAGCGATGACAGCGACATCTGGGACGACACAGCTCTGATTAAGGCCTACGACAAGGCCGTGGCCAGCTTCAAGCACGCCCTGAAGAACGGCGACATCTGCGAGACCAGCGGAAAGCCTAAAACCACCCCTAAGAGAAAGCCTGCTAAAAAGAACAAGAGCCAGAAGAAGAACACCGCTGCCAGCCTGCAGCAGTGGAAGGTGGGCGACAAGTGCAGCGCCATTTGGAGCGAGGACGGATGTATCTACCCTGCCACAATCGCCAGCATCGACTTCAAGCGGGAGACCTGCGTGGTGGTGTATACCGGCTACGGCAACAGGGAAGAGCAGAACCTGAGCGACCTGCTGAGCCCTATTTGCGAGGTGGCCAATAACATCGAGCAGAACGCCCAGGAGAACGAGAACGAGAGCCAGGTGAGCACCGACGAGAGCGAGAACAGCCGGAGCCCCGGCAATAAGAGCGACAACATCAAGCCCAAGAGCGCCCCCTGGAACTCTTTCCTGCCCCCCCCCCCCCCCATGCCTGGACCTAGATTGGGACCTGGAAAACCTGGACTGAAATTCAACGGCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCATTTGCTGTCTTGTTGGCTGCCCCCCTTCCCTTCTGGACCCCCCATTATCCCCCCCCCCCCCCCCATCTGTCCTGATTCTCTGGACGACGCCGATGCTTTGGGCTCTATGCTGATCTCTTGGTATATGAGCGGCTACCACACCGGCTACTACATGTTCCCCGAGGCCAGCCTGAAGGCCGAGCAGATGCCCGCTCCTTGTTTTCTGTGA
>PolyA_signal : SV40_late_start:2484_stop:2705_length:222 visible=True
CAGACATGATAAGATACATTGATGAGTTTGGACAAACCACAACTAGAATGCAGTGAAAAAAATGCTTTATTTGTGAAATTTGTGATGCTATTGCTTTATTTGTAACCATTATAAGCTGCAATAAACAAGTTAACAACAACAATTGCATTCATTTTATGTTTCAGGTTCAGGGGGAGGTGTGGGAGGTTTTTTAAAGCAAGTAAAACCTCTACAAATGTGGTA
>2nd_promoter : CAG_start:2706_stop:4438_length:1733 visible=True
CTCGACATTGATTATTGACTAGTTATTAATAGTAATCAATTACGGGGTCATTAGTTCATAGCCCATATATGGAGTTCCGCGTTACATAACTTACGGTAAATGGCCCGCCTGGCTGACCGCCCAACGACCCCCGCCCATTGACGTCAATAATGACGTATGTTCCCATAGTAACGCCAATAGGGACTTTCCATTGACGTCAATGGGTGGAGTATTTACGGTAAACTGCCCACTTGGCAGTACATCAAGTGTATCATATGCCAAGTACGCCCCCTATTGACGTCAATGACGGTAAATGGCCCGCCTGGCATTATGCCCAGTACATGACCTTATGGGACTTTCCTACTTGGCAGTACATCTACGTATTAGTCATCGCTATTACCATGGTCGAGGTGAGCCCCACGTTCTGCTTCACTCTCCCCATCTCCCCCCCCTCCCCACCCCCAATTTTGTATTTATTTATTTTTTAATTATTTTGTGCAGCGATGGGGGCGGGGGGGGGGGGGGGGCGCGCGCCAGGCGGGGCGGGGCGGGGCGAGGGGCGGGGCGGGGCGAGGCGGAGAGGTGCGGCGGCAGCCAATCAGAGCGGCGCGCTCCGAAAGTTTCCTTTTATGGCGAGGCGGCGGCGGCGGCGGCCCTATAAAAAGCGAAGCGCGCGGCGGGCGGGAGTCGCTGCGCGCTGCCTTCGCCCCGTGCCCCGCTCCGCCGCCGCCTCGCGCCGCCCGCCCCGGCTCTGACTGACCGCGTTACTCCCACAGGTGAGCGGGCGGGACGGCCCTTCTCCTCCGGGCTGTAATTAGCGCTTGGTTTAATGACGGCTTGTTTCTTTTCTGTGGCTGCGTGAAAGCCTTGAGGGGCTCCGGGAGGGCCCTTTGTGCGGGGGGAGCGGCTCGGGGGGTGCGTGCGTGTGTGTGTGCGTGGGGAGCGCCGCGTGCGGCTCCGCGCTGCCCGGCGGCTGTGAGCGCTGCGGGCGCGGCGCGGGGCTTTGTGCGCTCCGCAGTGTGCGCGAGGGGAGCGCGGCCGGGGGCGGTGCCCCGCGGTGCGGGGGGGGCTGCGAGGGGAACAAAGGCTGCGTGCGGGGTGTGTGCGTGGGGGGGTGAGCAGGGGGTGTGGGCGCGTCGGTCGGGCTGCAACCCCCCCTGCACCCCCCTCCCCGAGTTGCTGAGCACGGCCCGGCTTCGGGTGCGGGGCTCCGTACGGGGCGTGGCGCGGGGCTCGCCGTGCCGGGCGGGGGGTGGCGGCAGGTGGGGGTGCCGGGCGGGGCGGGGCCGCCTCGGGCCGGGGAGGGCTCGGGGGAGGGGCGCGGCGGCCCCCGGAGCGCCGGCGGCTGTCGAGGCGCGGCGAGCCGCAGCCATTGCCTTTTATGGTAATCGTGCGAGAGGGCGCAGGGACTTCCTTTGTCCCAAATCTGTGCGGAGCCGAAATCTGGGAGGCGCCGCCGCACCCCCTCTAGCGGGCGCGGGGCGAAGCGGTGCGGCGCCGGCAGGAAGGAAATGGGCGGGGAGGGCCTTCGTGCGTCGCCGCGCCGCCGTCCCCTTCTCCCTCTCCAGCCTCGGGGCTGTCCGCGGGGGGACGGCTGCCTTCGGGGGGGACGGGGCAGGGCGGGGTTCGGCTTCTGGCGTGTGACCGGCGGCTCTAGAGCCTCTGCTAACCATGTTCATGCCTTCTTCTTTTTCCTACAGCTCCTGGGCAACGTGCTGGTTATTGTGCTGTCTCATCATTTTGGCAAAGAATTG
>Fluorescent_tag : EGFP_start:4439_stop:5158_length:720 visible=True
ATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCTGGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGAGGGCGATGCCACCTACGGCAAGCTGACCCTGAAGTTCATCTGCACCACCGGCAAGCTGCCCGTGCCCTGGCCCACCCTCGTGACCACCCTGACCTACGGCGTGCAGTGCTTCAGCCGCTACCCCGACCACATGAAGCAGCACGACTTCTTCAAGTCCGCCATGCCCGAAGGCTACGTCCAGGAGCGCACCATCTTCTTCAAGGACGACGGCAACTACAAGACCCGCGCCGAGGTGAAGTTCGAGGGCGACACCCTGGTGAACCGCATCGAGCTGAAGGGCATCGACTTCAAGGAGGACGGCAACATCCTGGGGCACAAGCTGGAGTACAACTACAACAGCCACAACGTCTATATCATGGCCGACAAGCAGAAGAACGGCATCAAGGTGAACTTCAAGATCCGCCACAACATCGAGGACGGCAGCGTGCAGCTCGCCGACCACTACCAGCAGAACACCCCCATCGGCGACGGCCCCGTGCTGCTGCCCGACAACCACTACCTGAGCACCCAGTCCGCCCTGAGCAAAGACCCCAACGAGAAGCGCGATCACATGGTCCTGCTGGAGTTCGTGACCGCCGCCGGGATCACTCTCGGCATGGACGAGCTGTACAAGTAA
>backbone_element_start:5159_stop:5188_length:30 visible=False
ACCCAGCTTTCTTGTACAAAGTGGGAATTC
>Enhancer : WPRE_start:5189_stop:5786_length:598 visible=True
CGATAATCAACCTCTGGATTACAAAATTTGTGAAAGATTGACTGGTATTCTTAACTATGTTGCTCCTTTTACGCTATGTGGATACGCTGCTTTAATGCCTTTGTATCATGCTATTGCTTCCCGTATGGCTTTCATTTTCTCCTCCTTGTATAAATCCTGGTTGCTGTCTCTTTATGAGGAGTTGTGGCCCGTTGTCAGGCAACGTGGCGTGGTGTGCACTGTGTTTGCTGACGCAACCCCCACTGGTTGGGGCATTGCCACCACCTGTCAGCTCCTTTCCGGGACTTTCGCTTTCCCCCTCCCTATTGCCACGGCGGAACTCATCGCCGCCTGCCTTGCCCGCTGCTGGACAGGGGCTCGGCTGTTGGGCACTGACAATTCCGTGGTGTTGTCGGGGAAGCTGACGTCCTTTCCATGGCTGCTCGCCTGTGTTGCCACCTGGATTCTGCGCGGGACGTCCTTCTGCTACGTCCCTTCGGCCCTCAATCCAGCGGACCTTCCTTCCCGCGGCCTGCTGCCGGCTCTGCGGCCTCTTCCGCGTCTTCGCCTTCGCCCTCAGACGAGTCGGATCTCCCTTTGGGCCGCCTCCCCGCATCGG
>backbone_element_start:5787_stop:5816_length:30 visible=False
GAATTCCTAGAGCTCGCTGATCAGCCTCGA
>2nd_polyA_signal : bGH_start:5817_stop:6024_length:208 visible=True
CTGTGCCTTCTAGTTGCCAGCCATCTGTTGTTTGCCCCTCCCCCGTGCCTTCCTTGACCCTGGAAGGTGCCACTCCCACTGTCCTTTCCTAATAAAATGAGGAAATTGCATCGCATTGTCTGAGTAGGTGTCATTCTATTCTGGGGGGTGGGGTGGGGCAGGACAGCAAGGGGGAGGATTGGGAAGAGAATAGCAGGCATGCTGGGGA
>backbone_element_start:6025_stop:6031_length:7 visible=False
GGGCCGC
>3`ITR_start:6032_stop:6161_length:130 visible=True
CTGCGCGCTCGCTCGCTCACTGAGGCCGCCCGGGCAAAGCCCGGGCGTCGGGCGACCTTTGGTCGCCCGGCCTCAGTGAGCGAGCGAGCGCGCAGAGAGGGAGTGGCCAACTCCATCACTAGGGGTTCCT
>backbone_element_start:6162_stop:7088_length:927 visible=False
CTGCCTGCAGGGGCGCCTGATGCGGTATTTTCTCCTTACGCATCTGTGCGGTATTTCACACCGCATACGTCAAAGCAACCATAGTACGCGCCCTGTAGCGGCGCATTAAGCGCGGCGGGGGTGGTGGTTACGCGCAGCGTGACCGCTACACTTGCCAGCGCCTTAGCGCCCGCTCCTTTCGCTTTCTTCCCTTCCTTTCTCGCCACGTTCGCCGGCTTTCCCCGTCAAGCTCTAAATCGGGGGCTCCCTTTAGGGTTCCGATTTAGTGCTTTACGGCACCTCGACCCCAAAAAACTTGATTTGGGTGATGGTTCACGTAGTGGGCCATCGCCCTGATAGACGGTTTTTCGCCCTTTGACGTTGGAGTCCACGTTCTTTAATAGTGGACTCTTGTTCCAAACTGGAACAACACTCAACTCTATCTCGGGCTATTCTTTTGATTTATAAGGGATTTTGCCGATTTCGGTCTATTGGTTAAAAAATGAGCTGATTTAACAAAAATTTAACGCGAATTTTAACAAAATATTAACGTTTACAATTTTATGGTGCACTCTCAGTACAATCTGCTCTGATGCCGCATAGTTAAGCCAGCCCCGACACCCGCCAACACCCGCTGACGCGCCCTGACGGGCTTGTCTGCTCCCGGCATCCGCTTACAGACAAGCTGTGACCGTCTCCGGGAGCTGCATGTGTCAGAGGTTTTCACCGTCATCACCGAAACGCGCGAGACGAAAGGGCCTCGTGATACGCCTATTTTTATAGGTTAATGTCATGATAATAATGGTTTCTTAGACGTCAGGTGGCACTTTTCGGGGAAATGTGCGCGGAACCCCTATTTGTTTATTTTTCTAAATACATTCAAATATGTATCCGCTCATGAGACAATAACCCTGATAAATGCTTCAATAATATTGAAAAAGGAAGAGT
>Resistance : Ampicillin_start:7089_stop:7949_length:861 visible=True
ATGAGTATTCAACATTTCCGTGTCGCCCTTATTCCCTTTTTTGCGGCATTTTGCCTTCCTGTTTTTGCTCACCCAGAAACGCTGGTGAAAGTAAAAGATGCTGAAGATCAGTTGGGTGCACGAGTGGGTTACATCGAACTGGATCTCAACAGCGGTAAGATCCTTGAGAGTTTTCGCCCCGAAGAACGTTTTCCAATGATGAGCACTTTTAAAGTTCTGCTATGTGGCGCGGTATTATCCCGTATTGACGCCGGGCAAGAGCAACTCGGTCGCCGCATACACTATTCTCAGAATGACTTGGTTGAGTACTCACCAGTCACAGAAAAGCATCTTACGGATGGCATGACAGTAAGAGAATTATGCAGTGCTGCCATAACCATGAGTGATAACACTGCGGCCAACTTACTTCTGACAACGATCGGAGGACCGAAGGAGCTAACCGCTTTTTTGCACAACATGGGGGATCATGTAACTCGCCTTGATCGTTGGGAACCGGAGCTGAATGAAGCCATACCAAACGACGAGCGTGACACCACGATGCCTGTAGCAATGGCAACAACGTTGCGCAAACTATTAACTGGCGAACTACTTACTCTAGCTTCCCGGCAACAATTAATAGACTGGATGGAGGCGGATAAAGTTGCAGGACCACTTCTGCGCTCGGCCCTTCCGGCTGGCTGGTTTATTGCTGATAAATCTGGAGCCGGTGAGCGTGGAAGCCGCGGTATCATTGCAGCACTGGGGCCAGATGGTAAGCCCTCCCGTATCGTAGTTATCTACACGACGGGGAGTCAGGCAACTATGGATGAACGAAATAGACAGATCGCTGAGATAGGTGCCTCACTGATTAAGCATTGGTAA
>backbone_element_start:7950_stop:8119_length:170 visible=False
CTGTCAGACCAAGTTTACTCATATATACTTTAGATTGATTTAAAACTTCATTTTTAATTTAAAAGGATCTAGGTGAAGATCCTTTTTGATAATCTCATGACCAAAATCCCTTAACGTGAGTTTTCGTTCCACTGAGCGTCAGACCCCGTAGAAAAGATCAAAGGATCTTC
>pUC_ori_start:8120_stop:8708_length:589 visible=True
TTGAGATCCTTTTTTTCTGCGCGTAATCTGCTGCTTGCAAACAAAAAAACCACCGCTACCAGCGGTGGTTTGTTTGCCGGATCAAGAGCTACCAACTCTTTTTCCGAAGGTAACTGGCTTCAGCAGAGCGCAGATACCAAATACTGTTCTTCTAGTGTAGCCGTAGTTAGGCCACCACTTCAAGAACTCTGTAGCACCGCCTACATACCTCGCTCTGCTAATCCTGTTACCAGTGGCTGCTGCCAGTGGCGATAAGTCGTGTCTTACCGGGTTGGACTCAAGACGATAGTTACCGGATAAGGCGCAGCGGTCGGGCTGAACGGGGGGTTCGTGCACACAGCCCAGCTTGGAGCGAACGACCTACACCGAACTGAGATACCTACAGCGTGAGCTATGAGAAAGCGCCACGCTTCCCGAAGGGAGAAAGGCGGACAGGTATCCGGTAAGCGGCAGGGTCGGAACAGGAGAGCGCACGAGGGAGCTTCCAGGGGGAAACGCCTGGTATCTTTATAGTCCTGTCGGGTTTCGCCACCTCTGACTTGAGCGTCGATTTTTGTGATGCTCGTCAGGGGGGCGGAGCCTATGGAAA
>backbone_element_start:8709_stop:8780_length:72 visible=False
AACGCCAGCAACGCGGCCTTTTTACGGTTCCTGGCCTTTTGCTGGCCTTTTGCTCACATGTCCTGCAGGCAG
```

<br />
<br />

```
## genes names
project['transcripts']['sequences']['name']

## proteins sequences
project['transcripts']['sequences']['sequence_aa']

## average codon frequency in the input sequence
project['transcripts']['sequences']['vector_sequence_frequence']

## GC% content in the input sequence
project['transcripts']['sequences']['vector_sequence_GC']

############################################################################

## average codon frequency in the output sequence
project['transcripts']['sequences']['optimized_vector_sequence_frequence']

## GC% content in the output sequence
project['transcripts']['sequences']['optimized_vector_sequence_GC']
    
```




<br />


#### 2.2.2 Creating RNAi / RNAi + expression of the plasmid vector <a id="rnai"></a>

##### Empty input dictionary schema:


```
input_dict = {
    
    # REQUIRED!
    # name of current project (defined by user)
    'project_name':'',
    
    # REQUIRED!
    # avaiable of vector types (ssAAV / scAAV / lentiviral / regular)
    'vector_type':'ssAAV',
      
    # REQUIRED!
    # in this case 'vector_function':'rnai'
    'vector_function':'rnai',
    
    # REQUIRED!
    # avaiable options (human / mouse / rat / both (mouse + human) / both2 (rat + human) / multi (mouse + rat + human))
    # 'both / both2 / multi' - creating vector function adjusted for all species taking into consideration most adjustments for Homo sapiens
    'species':'human',
    
    # REQUIRED!
    # sequence of provided non-coding promoter
    # for coding sequences the user should choose the promoter of non-coding genes (metadata['promoters']['type'] == 'non-coding')
    # sequence orientation 5' ---> 3' - sense
    'promoter_ncrna_sequence':'',
    # REQUIRED!
    # name of provided promoter sequence
	'promoter_ncrna_name':'',

    # POSSIBLE!
    # sequence of custom RNAi, which can be provided by user
    # if provided, then the algorithm of RNAi estimation is off
    # if empt '' the algorithm share the best possible RNAi based on 'rnai_gene_name'
    # sequence orientation 5' ---> 3' - sense
    'rnai_sequence':'',
    
    # REQUIRED!
    # name of the target gene for the RNAi searching algorithm (gene name for Homo sapien or Mus musculus)
    # algorithm is working when the rnai_sequence is empty ''
    # if the user defines 'rnai_sequence' this 'rnai_gene_name' is just a name for a user-supplied sequence
    # 'rnai_gene_name' - provide in the HGNC nomenclature
    'rnai_gene_name':'',
    
    # REQUIRED!
    # sequence of the loop to create the structure of the hairpin of shRNA or siRNA depending on the loop sequence
    # algorithm is working when the rnai_sequence is empty ''
    # if the user defines 'rnai_sequence' this 'rnai_gene_name' is just a name for a user-supplied sequence
    # sequence orientation 5' ---> 3' - sense
    'loop_sequence':'',
    
    # WARNING! If the user wants to add additional CDS sequences to parallel transcript expression with silencing by RNAi in one vector; provide sequences, linkers_sequences, promoter_sequence, etc.
    
    # list of coding sequences (CDS) provided to make expression from the vector
    # amount of sequences is not restricted as the user must remember that the length of whole vector is limited
    # excide the relevant vector size can decrease vector working
    # if the user wants to not include any sequences only fluorescent_tag, provide ['']
    # sequences orientation 5' ---> 3' - sense
    'sequences':[''],
    # list of names of coding sequences
    # amount of names should be equal with amount of sequences
    # if provided no sequences, provide ['']
    'sequences_names':[''],
    
    # REQUIRED if more than one sequence of transcripts!
    # sequences of provided linkers
    # number of linkers_sequences should be equal number of sequences (transcripts) - 1. One linker for each pair of sequences.
    # if the number of transcript sequences is equal 1 then provide empty list []
    # if the user wants to not provide any linkers between the transcript sequences, provide an empty string '' for each pair of transcripts where the user wants to avoid linker; empty strings '' provide inside the list ['']
    'linkers_sequences':[''],
    # REQUIRED if transcript sequence occures, if not empty string ''!
    # names of provided linkers
    # if the number of transcript sequences is equal 1 then provide empty list []
    # if the user wants to not provide any linkers between the transcript sequences, provide an empty string '' for each pair of transcripts where the user wants to avoid linker; empty strings '' provide inside the list ['']
    'linkers_names':[''],
    
    # REQUIRED if transcript sequence occurs or fluorescent tag will be included, if not empty string ''!
    # sequence of provided promoter
    # sequence orientation 5' ---> 3' - sense
    'promoter_sequence':'',
    # REQUIRED if transcript sequence occurs or fluorescent tag will be included, if not empty string ''!
    # name of provided promoter sequence
    'promoter_name':'',
    
    # POSSIBLE if transcript sequence occures or fluorescent tag will be included, if not empty string ''!
    # sequence of provided enhancer
    # sequence orientation 5' ---> 3' - sense
    'regulator_sequence':'',
    # POSSIBLE if transcript sequence occures or fluorescent tag will be included, if not empty string ''!
    # name of provided enhancer sequence
    'regulator_name':'',
    
    # REQUIRED if transcript sequence occurs or fluorescent tag will be included, if not empty string ''!
    # sequence of provided polyA signal
    # sequence orientation 5' ---> 3' - sense
    'polya_sequence':'',
    # REQUIRED if transcript sequence occurs or fluorescent tag will be included, if not empty string ''!
    # name of provided polyA singla sequence
    'polya_name':'',
    
    # POSSIBLE!
    # sequence of provided fluorescent tag
    # if the user does not need fluorescent tag, provide ''
    # sequence orientation 5' ---> 3' - sense
    'fluorescence_sequence':'',
    # POSSIBLE!
    # name of provided fluorescent tag
    # if the user does not need fluorescent tag, provide ''
    'fluorescence_name':'',
    
    # WARNING! If provided sequences for transcripts (> 0), provide fluorescence_linker_sequence or provide empty string ''.
    
    # POSSIBLE if transcript sequence occures, if not empty string ''!
    # sequence of provided fluorescence tag linker
    # sequence orientation 5' ---> 3' - sense
    'fluorescence_linker_sequence':'',
    # POSSIBLE if transcript sequence occures, if not empty string ''!
    # name of provided fluorescence tag linker
    'fluorescence_linker_name':'',
    
    # REQUIRED!
    # sequence of provided selection marker
    # sequence orientation 5' ---> 3' - sense
    'selection_marker_sequence':'',
    # REQUIRED!
    # name of provided selection marker
    'selection_marker_name':'',
    
    # POSSIBLE!
    # restriction enzymes protection of transcript sequences
    # if the user does not need any restriction places protection, provide empty list []
    'restriction_list':[],
    
    # REQUIRED!
    # available options (True / False)
    # decision; if the user wants the transcription sequences optimized based on the provided species
    # if the user has omitted the additional transcript sequences, provide False
    'optimize':True
}  



```


<br />


##### Example dictionary:

```
input_dict = {

    'project_name':'test_RNAi',
    'vector_type':'ssAAV',
    'vector_function':'rnai',
    'species':'human',
    'promoter_ncrna_name':'U6',
    'promoter_ncrna_sequence':'GAGGGCCTATTTCCCATGATTCCTTCATATTTGCATATACGATACAAGGCTGTTAGAGAGATAATTGGAATTAATTTGACTGTAAACACAAAGATATTAGTACAAAATACGTGACGTAGAAAGTAATAATTTCTTGGGTAGTTTGCAGTTTTAAAATTATGTTTTAAAATGGACTATCATATGCTTACCGTAACTTGAAAGTATTTCGATTTCTTGGCTTTATATATCTTGTGGAAAGGACGAAACACC',
    'rnai_sequence':'',
    'rnai_gene_name':'PAX3',
    'loop_sequence':'TAGTGAAGCCACAGATGTAC',
    'sequences':['ATGGCGATGAGCAGCGGCGGCAGTGGTGGCGGCGTCCCGGAGCAGGAGGATTCCGTGCTGTTCCGGCGCGGCACAGGCCAGAGCGATGATTCTGACATTTGGGATGATACAGCACTGATAAAAGCATATGATAAAGCTGTGGCTTCATTTAAGCATGCTCTAAAGAATGGTGACATTTGTGAAACTTCGGGTAAACCAAAAACCACACCTAAAAGAAAACCTGCTAAGAAGAATAAAAGCCAAAAGAAGAATACTGCAGCTTCCTTACAACAGTGGAAAGTTGGGGACAAATGTTCTGCCATTTGGTCAGAAGACGGTTGCATTTACCCAGCTACCATTGCTTCAATTGATTTTAAGAGAGAAACCTGTGTTGTGGTTTACACTGGATATGGAAATAGAGAGGAGCAAAATCTGTCCGATCTACTTTCCCCAATCTGTGAAGTAGCTAATAATATAGAACAAAATGCTCAAGAGAATGAAAATGAAAGCCAAGTTTCAACAGATGAAAGTGAGAACTCCAGGTCTCCTGGAAATAAATCAGATAACATCAAGCCCAAATCTGCTCCATGGAACTCTTTTCTCCCTCCACCACCCCCCATGCCAGGGCCAAGACTGGGACCAGGAAAGCCAGGTCTAAAATTCAATGGCCCACCACCGCCACCGCCACCACCACCACCCCACTTACTATCATGCTGGCTGCCTCCATTTCCTTCTGGACCACCAATAATTCCCCCACCACCTCCCATATGTCCAGATTCTCTTGATGATGCTGATGCTTTGGGAAGTATGTTAATTTCATGGTACATGAGTGGCTATCATACTGGCTATTATATGTTTCCTGAGGCCTCCCTAAAAGCCGAGCAGATGCCAGCACCATGCTTCCTGTAA'],
    'sequences_names':['SMN1'],
    'linkers_sequences':[''],
    'linkers_names':[''],
    'promoter_sequence':'GGGCTGGAAGCTACCTTTGACATCATTTCCTCTGCGAATGCATGTATAATTTCTACAGAACCTATTAGAAAGGATCACCCAGCCTCTGCTTTTGTACAACTTTCCCTTAAAAAACTGCCAATTCCACTGCTGTTTGGCCCAATAGTGAGAACTTTTTCCTGCTGCCTCTTGGTGCTTTTGCCTATGGCCCCTATTCTGCCTGCTGAAGACACTCTTGCCAGCATGGACTTAAACCCCTCCAGCTCTGACAATCCTCTTTCTCTTTTGTTTTACATGAAGGGTCTGGCAGCCAAAGCAATCACTCAAAGTTCAAACCTTATCATTTTTTGCTTTGTTCCTCTTGGCCTTGGTTTTGTACATCAGCTTTGAAAATACCATCCCAGGGTTAATGCTGGGGTTAATTTATAACTAAGAGTGCTCTAGTTTTGCAATACAGGACATGCTATAAAAATGGAAAGAT',
    'promoter_name':'TBG',
    'regulator_sequence':'CGATAATCAACCTCTGGATTACAAAATTTGTGAAAGATTGACTGGTATTCTTAACTATGTTGCTCCTTTTACGCTATGTGGATACGCTGCTTTAATGCCTTTGTATCATGCTATTGCTTCCCGTATGGCTTTCATTTTCTCCTCCTTGTATAAATCCTGGTTGCTGTCTCTTTATGAGGAGTTGTGGCCCGTTGTCAGGCAACGTGGCGTGGTGTGCACTGTGTTTGCTGACGCAACCCCCACTGGTTGGGGCATTGCCACCACCTGTCAGCTCCTTTCCGGGACTTTCGCTTTCCCCCTCCCTATTGCCACGGCGGAACTCATCGCCGCCTGCCTTGCCCGCTGCTGGACAGGGGCTCGGCTGTTGGGCACTGACAATTCCGTGGTGTTGTCGGGGAAGCTGACGTCCTTTCCATGGCTGCTCGCCTGTGTTGCCACCTGGATTCTGCGCGGGACGTCCTTCTGCTACGTCCCTTCGGCCCTCAATCCAGCGGACCTTCCTTCCCGCGGCCTGCTGCCGGCTCTGCGGCCTCTTCCGCGTCTTCGCCTTCGCCCTCAGACGAGTCGGATCTCCCTTTGGGCCGCCTCCCCGCATCGG',
    'regulator_name':'WPRE',
    'polya_sequence':'CAGACATGATAAGATACATTGATGAGTTTGGACAAACCACAACTAGAATGCAGTGAAAAAAATGCTTTATTTGTGAAATTTGTGATGCTATTGCTTTATTTGTAACCATTATAAGCTGCAATAAACAAGTTAACAACAACAATTGCATTCATTTTATGTTTCAGGTTCAGGGGGAGGTGTGGGAGGTTTTTTAAAGCAAGTAAAACCTCTACAAATGTGGTA',
    'polya_name':'SV40_late',
    'fluorescence_sequence':'ATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCTGGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGAGGGCGATGCCACCTACGGCAAGCTGACCCTGAAGTTCATCTGCACCACCGGCAAGCTGCCCGTGCCCTGGCCCACCCTCGTGACCACCCTGACCTACGGCGTGCAGTGCTTCAGCCGCTACCCCGACCACATGAAGCAGCACGACTTCTTCAAGTCCGCCATGCCCGAAGGCTACGTCCAGGAGCGCACCATCTTCTTCAAGGACGACGGCAACTACAAGACCCGCGCCGAGGTGAAGTTCGAGGGCGACACCCTGGTGAACCGCATCGAGCTGAAGGGCATCGACTTCAAGGAGGACGGCAACATCCTGGGGCACAAGCTGGAGTACAACTACAACAGCCACAACGTCTATATCATGGCCGACAAGCAGAAGAACGGCATCAAGGTGAACTTCAAGATCCGCCACAACATCGAGGACGGCAGCGTGCAGCTCGCCGACCACTACCAGCAGAACACCCCCATCGGCGACGGCCCCGTGCTGCTGCCCGACAACCACTACCTGAGCACCCAGTCCGCCCTGAGCAAAGACCCCAACGAGAAGCGCGATCACATGGTCCTGCTGGAGTTCGTGACCGCCGCCGGGATCACTCTCGGCATGGACGAGCTGTACAAGTAA',
    'fluorescence_name':'EGFP',
    'fluorescence_linker_sequence':'GGAAGCGGAGAGGGCAGGGGAAGTCTTCTAACATGCGGGGACGTGGAGGAAAATCCCGGCCCC',
    'fluorescence_linker_name':'T2A',
    'selection_marker_sequence':'ATGAGTATTCAACATTTCCGTGTCGCCCTTATTCCCTTTTTTGCGGCATTTTGCCTTCCTGTTTTTGCTCACCCAGAAACGCTGGTGAAAGTAAAAGATGCTGAAGATCAGTTGGGTGCACGAGTGGGTTACATCGAACTGGATCTCAACAGCGGTAAGATCCTTGAGAGTTTTCGCCCCGAAGAACGTTTTCCAATGATGAGCACTTTTAAAGTTCTGCTATGTGGCGCGGTATTATCCCGTATTGACGCCGGGCAAGAGCAACTCGGTCGCCGCATACACTATTCTCAGAATGACTTGGTTGAGTACTCACCAGTCACAGAAAAGCATCTTACGGATGGCATGACAGTAAGAGAATTATGCAGTGCTGCCATAACCATGAGTGATAACACTGCGGCCAACTTACTTCTGACAACGATCGGAGGACCGAAGGAGCTAACCGCTTTTTTGCACAACATGGGGGATCATGTAACTCGCCTTGATCGTTGGGAACCGGAGCTGAATGAAGCCATACCAAACGACGAGCGTGACACCACGATGCCTGTAGCAATGGCAACAACGTTGCGCAAACTATTAACTGGCGAACTACTTACTCTAGCTTCCCGGCAACAATTAATAGACTGGATGGAGGCGGATAAAGTTGCAGGACCACTTCTGCGCTCGGCCCTTCCGGCTGGCTGGTTTATTGCTGATAAATCTGGAGCCGGTGAGCGTGGAAGCCGCGGTATCATTGCAGCACTGGGGCCAGATGGTAAGCCCTCCCGTATCGTAGTTATCTACACGACGGGGAGTCAGGCAACTATGGATGAACGAAATAGACAGATCGCTGAGATAGGTGCCTCACTGATTAAGCATTGGTAA',
    'selection_marker_name':'Ampicillin',
    'restriction_list':['RsaI', 'MnlI', 'AciI', 'AluI', 'BmrI'],
    'optimize':True
}  
```

<br />

##### Output:

```
# Name of project
project['project']
```

``` 
# Graph of the designed vector
vector_plot = project['vector']['graph']
vector_plot.savefig('RNAi_vector.svg')
```

<br />

Example return:


<p align="center">
<img  src="https://raw.githubusercontent.com/jkubis96/JBioSeqTools/3fb8a369a9c893d65589a92680fcb1e0cbcefa87/fig/RNAi_vector.svg" alt="drawing" width="600" />
</p>

<br />

```
# Complete FASTA file of the designed vecotr
project['vector']['full_fasta']
```

Example return:

```
>test_RNAi_ssAAV_rnai_6790nc
CTGCGCGCTCGCTCGCTCACTGAGGCCGCCCGGGCAAAGCCCGGGCGTCGGGCGACCTTTGGTCGCCCGGCCTCAGTGAGCGAGCGAGCGCGCAGAGAGGGAGTGGCCAACTCCATCACTAGGGGTTCCTATCGATGAGGGCCTATTTCCCATGATTCCTTCATATTTGCATATACGATACAAGGCTGTTAGAGAGATAATTGGAATTAATTTGACTGTAAACACAAAGATATTAGTACAAAATACGTGACGTAGAAAGTAATAATTTCTTGGGTAGTTTGCAGTTTTAAAATTATGTTTTAAAATGGACTATCATATGCTTACCGTAACTTGAAAGTATTTCGATTTCTTGGCTTTATATATCTTGTGGAAAGGACGAAACACCGGGCCTTTCCGTTTCGCCTTCACCTTAGTGAAGCCACAGATGTACAGGTGAAGGCGAAACGGAAAGGCTTTTTTTGAATTCCAACTTTGTATAGAAAAGTTGGGGCTGGAAGCTACCTTTGACATCATTTCCTCTGCGAATGCATGTATAATTTCTACAGAACCTATTAGAAAGGATCACCCAGCCTCTGCTTTTGTACAACTTTCCCTTAAAAAACTGCCAATTCCACTGCTGTTTGGCCCAATAGTGAGAACTTTTTCCTGCTGCCTCTTGGTGCTTTTGCCTATGGCCCCTATTCTGCCTGCTGAAGACACTCTTGCCAGCATGGACTTAAACCCCTCCAGCTCTGACAATCCTCTTTCTCTTTTGTTTTACATGAAGGGTCTGGCAGCCAAAGCAATCACTCAAAGTTCAAACCTTATCATTTTTTGCTTTGTTCCTCTTGGCCTTGGTTTTGTACATCAGCTTTGAAAATACCATCCCAGGGTTAATGCTGGGGTTAATTTATAACTAAGAGTGCTCTAGTTTTGCAATACAGGACATGCTATAAAAATGGAAAGATCAAGTTTGTACAAAAAAGCAGGCTGCCACCATGGCTATGTCTAGCGGAGGCTCTGGAGGAGGAGTTCCTGAACAGGAGGACTCTGTGCTGTTCCGGAGGGGCACAGGACAAAGCGATGACAGCGACATCTGGGACGACACAGCTCTGATTAAGGCCTACGACAAGGCCGTGGCCAGCTTCAAGCACGCCCTGAAGAACGGCGACATCTGCGAGACCAGCGGAAAGCCTAAAACCACCCCTAAGAGAAAGCCTGCTAAAAAGAACAAGAGCCAGAAGAAGAACACCGCTGCCAGCCTGCAGCAGTGGAAGGTGGGCGACAAGTGCAGCGCCATTTGGAGCGAGGACGGATGTATCTACCCTGCCACAATCGCCAGCATCGACTTCAAGCGGGAGACCTGCGTGGTGGTGTATACCGGCTACGGCAACAGGGAAGAGCAGAACCTGAGCGACCTGCTGAGCCCTATTTGCGAGGTGGCCAATAACATCGAGCAGAACGCCCAGGAGAACGAGAACGAGAGCCAGGTGAGCACCGACGAGAGCGAGAACAGCCGGAGCCCCGGCAATAAGAGCGACAACATCAAGCCCAAGAGCGCCCCCTGGAACTCTTTCCTGCCCCCCCCCCCCCCCATGCCTGGACCTAGATTGGGACCTGGAAAACCTGGACTGAAATTCAACGGCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCATTTGCTGTCTTGTTGGCTGCCCCCCTTCCCTTCTGGACCCCCCATTATCCCCCCCCCCCCCCCCATCTGTCCTGATTCTCTGGACGACGCCGATGCTTTGGGCTCTATGCTGATCTCTTGGTATATGAGCGGCTACCACACCGGCTACTACATGTTCCCCGAGGCCAGCCTGAAGGCCGAGCAGATGCCCGCTCCTTGTTTTCTGGGAAGCGGAGAGGGCAGGGGAAGTCTTCTAACATGCGGGGACGTGGAGGAAAATCCCGGCCCCATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCTGGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGAGGGCGATGCCACCTACGGCAAGCTGACCCTGAAGTTCATCTGCACCACCGGCAAGCTGCCCGTGCCCTGGCCCACCCTCGTGACCACCCTGACCTACGGCGTGCAGTGCTTCAGCCGCTACCCCGACCACATGAAGCAGCACGACTTCTTCAAGTCCGCCATGCCCGAAGGCTACGTCCAGGAGCGCACCATCTTCTTCAAGGACGACGGCAACTACAAGACCCGCGCCGAGGTGAAGTTCGAGGGCGACACCCTGGTGAACCGCATCGAGCTGAAGGGCATCGACTTCAAGGAGGACGGCAACATCCTGGGGCACAAGCTGGAGTACAACTACAACAGCCACAACGTCTATATCATGGCCGACAAGCAGAAGAACGGCATCAAGGTGAACTTCAAGATCCGCCACAACATCGAGGACGGCAGCGTGCAGCTCGCCGACCACTACCAGCAGAACACCCCCATCGGCGACGGCCCCGTGCTGCTGCCCGACAACCACTACCTGAGCACCCAGTCCGCCCTGAGCAAAGACCCCAACGAGAAGCGCGATCACATGGTCCTGCTGGAGTTCGTGACCGCCGCCGGGATCACTCTCGGCATGGACGAGCTGTACAAGTAACGATAATCAACCTCTGGATTACAAAATTTGTGAAAGATTGACTGGTATTCTTAACTATGTTGCTCCTTTTACGCTATGTGGATACGCTGCTTTAATGCCTTTGTATCATGCTATTGCTTCCCGTATGGCTTTCATTTTCTCCTCCTTGTATAAATCCTGGTTGCTGTCTCTTTATGAGGAGTTGTGGCCCGTTGTCAGGCAACGTGGCGTGGTGTGCACTGTGTTTGCTGACGCAACCCCCACTGGTTGGGGCATTGCCACCACCTGTCAGCTCCTTTCCGGGACTTTCGCTTTCCCCCTCCCTATTGCCACGGCGGAACTCATCGCCGCCTGCCTTGCCCGCTGCTGGACAGGGGCTCGGCTGTTGGGCACTGACAATTCCGTGGTGTTGTCGGGGAAGCTGACGTCCTTTCCATGGCTGCTCGCCTGTGTTGCCACCTGGATTCTGCGCGGGACGTCCTTCTGCTACGTCCCTTCGGCCCTCAATCCAGCGGACCTTCCTTCCCGCGGCCTGCTGCCGGCTCTGCGGCCTCTTCCGCGTCTTCGCCTTCGCCCTCAGACGAGTCGGATCTCCCTTTGGGCCGCCTCCCCGCATCGGACCCAGCTTTCTTGTACAAAGTGGTGATGGCCGGCCGCTTCGAGCAGACATGATAAGATACATTGATGAGTTTGGACAAACCACAACTAGAATGCAGTGAAAAAAATGCTTTATTTGTGAAATTTGTGATGCTATTGCTTTATTTGTAACCATTATAAGCTGCAATAAACAAGTTAACAACAACAATTGCATTCATTTTATGTTTCAGGTTCAGGGGGAGGTGTGGGAGGTTTTTTAAAGCAAGTAAAACCTCTACAAATGTGGTAATCGATAGATCTAGGAACCCCTAGTGATGGAGTTGGCCACTCCCTCTCTGCGCGCTCGCTCGCTCACTGAGGCCGGGCGACCAAAGGTCGCCCGACGCCCGGGCTTTGCCCGGGCGGCCTCAGTGAGCGAGCGAGCGCGCAGCTGCCTGCAGGCAGCTTGGCACTGGCCGTCGTTTTACAACGTCGTGACTGGGAAAACCCTGGCGTTACCCAACTTAATCGCCTTGCAGCACATCCCCCTTTCGCCAGCTGGCGTAATAGCGAAGAGGCCCGCACCGATCGCCCTTCCCAACAGTTGCGCAGCCTGAATGGCGAATGGCGCCTGATGCGGTATTTTCTCCTTACGCATCTGTGCGGTATTTCACACCGCATACGTCAAAGCAACCATAGTACGCGCCCTGTAGCGGCGCATTAAGCGCGGCGGGTGTGGTGGTTACGCGCAGCGTGACCGCTACACTTGCCAGCGCCCTAGCGCCCGCTCCTTTCGCTTTCTTCCCTTCCTTTCTCGCCACGTTCGCCGGCTTTCCCCGTCAAGCTCTAAATCGGGGGCTCCCTTTAGGGTTCCGATTTAGTGCTTTACGGCACCTCGACCCCAAAAAACTTGATTTGGGTGATGGTTCACGTAGTGGGCCATCGCCCTGATAGACGGTTTTTCGCCCTTTGACGTTGGAGTCCACGTTCTTTAATAGTGGACTCTTGTTCCAAACTGGAACAACACTCAACCCTATCTCGGGCTATTCTTTTGATTTATAAGGGATTTTGCCGATTTCGGCCTATTGGTTAAAAAATGAGCTGATTTAACAAAAATTTAACGCGAATTTTAACAAAATATTAACGTTTACAATTTTATGGTGCACTCTCAGTACAATCTGCTCTGATGCCGCATAGTTAAGCCAGCCCCGACACCCGCCAACACCCGCTGACGCGCCCTGACGGGCTTGTCTGCTCCCGGCATCCGCTTACAGACAAGCTGTGACCGTCTCCGGGAGCTGCATGTGTCAGAGGTTTTCACCGTCATCACCGAAACGCGCGAGACGAAAGGGCCTCGTGATACGCCTATTTTTATAGGTTAATGTCATGATAATAATGGTTTCTTAGACGTCAGGTGGCACTTTTCGGGGAAATGTGCGCGGAACCCCTATTTGTTTATTTTTCTAAATACATTCAAATATGTATCCGCTCATGAGACAATAACCCTGATAAATGCTTCAATAATATTGAAAAAGGAAGAGTATGAGTATTCAACATTTCCGTGTCGCCCTTATTCCCTTTTTTGCGGCATTTTGCCTTCCTGTTTTTGCTCACCCAGAAACGCTGGTGAAAGTAAAAGATGCTGAAGATCAGTTGGGTGCACGAGTGGGTTACATCGAACTGGATCTCAACAGCGGTAAGATCCTTGAGAGTTTTCGCCCCGAAGAACGTTTTCCAATGATGAGCACTTTTAAAGTTCTGCTATGTGGCGCGGTATTATCCCGTATTGACGCCGGGCAAGAGCAACTCGGTCGCCGCATACACTATTCTCAGAATGACTTGGTTGAGTACTCACCAGTCACAGAAAAGCATCTTACGGATGGCATGACAGTAAGAGAATTATGCAGTGCTGCCATAACCATGAGTGATAACACTGCGGCCAACTTACTTCTGACAACGATCGGAGGACCGAAGGAGCTAACCGCTTTTTTGCACAACATGGGGGATCATGTAACTCGCCTTGATCGTTGGGAACCGGAGCTGAATGAAGCCATACCAAACGACGAGCGTGACACCACGATGCCTGTAGCAATGGCAACAACGTTGCGCAAACTATTAACTGGCGAACTACTTACTCTAGCTTCCCGGCAACAATTAATAGACTGGATGGAGGCGGATAAAGTTGCAGGACCACTTCTGCGCTCGGCCCTTCCGGCTGGCTGGTTTATTGCTGATAAATCTGGAGCCGGTGAGCGTGGAAGCCGCGGTATCATTGCAGCACTGGGGCCAGATGGTAAGCCCTCCCGTATCGTAGTTATCTACACGACGGGGAGTCAGGCAACTATGGATGAACGAAATAGACAGATCGCTGAGATAGGTGCCTCACTGATTAAGCATTGGTAACTGTCAGACCAAGTTTACTCATATATACTTTAGATTGATTTAAAACTTCATTTTTAATTTAAAAGGATCTAGGTGAAGATCCTTTTTGATAATCTCATGACCAAAATCCCTTAACGTGAGTTTTCGTTCCACTGAGCGTCAGACCCCGTAGAAAAGATCAAAGGATCTTCTTGAGATCCTTTTTTTCTGCGCGTAATCTGCTGCTTGCAAACAAAAAAACCACCGCTACCAGCGGTGGTTTGTTTGCCGGATCAAGAGCTACCAACTCTTTTTCCGAAGGTAACTGGCTTCAGCAGAGCGCAGATACCAAATACTGTTCTTCTAGTGTAGCCGTAGTTAGGCCACCACTTCAAGAACTCTGTAGCACCGCCTACATACCTCGCTCTGCTAATCCTGTTACCAGTGGCTGCTGCCAGTGGCGATAAGTCGTGTCTTACCGGGTTGGACTCAAGACGATAGTTACCGGATAAGGCGCAGCGGTCGGGCTGAACGGGGGGTTCGTGCACACAGCCCAGCTTGGAGCGAACGACCTACACCGAACTGAGATACCTACAGCGTGAGCTATGAGAAAGCGCCACGCTTCCCGAAGGGAGAAAGGCGGACAGGTATCCGGTAAGCGGCAGGGTCGGAACAGGAGAGCGCACGAGGGAGCTTCCAGGGGGAAACGCCTGGTATCTTTATAGTCCTGTCGGGTTTCGCCACCTCTGACTTGAGCGTCGATTTTTGTGATGCTCGTCAGGGGGGCGGAGCCTATGGAAAAACGCCAGCAACGCGGCCTTTTTACGGTTCCTGGCCTTTTGCTGGCCTTTTGCTCACATGTTCTTTCCTGCGTTATCCCCTGATTCTGTGGATAACCGTATTACCGCCTTTGAGTGAGCTGATACCGCTCGCCGCAGCCGAACGACCGAGCGCAGCGAGTCAGTGAGCGAGGAAGCGGAAGAGCGCCCAATACGCAAACCGCCTCTCCCCGCGCGTTGGCCGATTCATTAATGCAGCTGGCACGACAGGTTTCCCGACTGGAAAGCGGGCAGTGAGCGCAACGCAATTAATGTGAGTTAGCTCACTCATTAGGCACCCCAGGCTTTACACTTTATGCTTCCGGCTCGTATGTTGTGTGGAATTGTGAGCGGATAACAATTTCACACAGGAAACAGCTATGACCATGATTACGAATTGCCTGCAGGCAG
```

<br />
<br />

```
# The FASTA file is divided into particular elements of the designed vector
project['vector']['fasta']
```

Example return:


```
# test_RNAi_ssAAV_rnai_6790nc

>5`ITR_start:1_stop:130_length:130 visible=True
CTGCGCGCTCGCTCGCTCACTGAGGCCGCCCGGGCAAAGCCCGGGCGTCGGGCGACCTTTGGTCGCCCGGCCTCAGTGAGCGAGCGAGCGCGCAGAGAGGGAGTGGCCAACTCCATCACTAGGGGTTCCT
>backbone_element_start:131_stop:136_length:6 visible=False
ATCGAT
>Promoter_ncRNA : U6_start:137_stop:385_length:249 visible=True
GAGGGCCTATTTCCCATGATTCCTTCATATTTGCATATACGATACAAGGCTGTTAGAGAGATAATTGGAATTAATTTGACTGTAAACACAAAGATATTAGTACAAAATACGTGACGTAGAAAGTAATAATTTCTTGGGTAGTTTGCAGTTTTAAAATTATGTTTTAAAATGGACTATCATATGCTTACCGTAACTTGAAAGTATTTCGATTTCTTGGCTTTATATATCTTGTGGAAAGGACGAAACACC
>backbone_element_start:386_stop:387_length:2 visible=False
GG
>RNAi : PAX3_RNAi_35_hs_start:388_stop:455_length:68 visible=True
GCCTTTCCGTTTCGCCTTCACCTTAGTGAAGCCACAGATGTACAGGTGAAGGCGAAACGGAAAGGCTT
>Terminator_start:456_stop:460_length:5 visible=True
TTTTT
>backbone_element_start:461_stop:487_length:27 visible=False
GAATTCCAACTTTGTATAGAAAAGTTG
>Promoter : TBG_start:488_stop:947_length:460 visible=True
GGGCTGGAAGCTACCTTTGACATCATTTCCTCTGCGAATGCATGTATAATTTCTACAGAACCTATTAGAAAGGATCACCCAGCCTCTGCTTTTGTACAACTTTCCCTTAAAAAACTGCCAATTCCACTGCTGTTTGGCCCAATAGTGAGAACTTTTTCCTGCTGCCTCTTGGTGCTTTTGCCTATGGCCCCTATTCTGCCTGCTGAAGACACTCTTGCCAGCATGGACTTAAACCCCTCCAGCTCTGACAATCCTCTTTCTCTTTTGTTTTACATGAAGGGTCTGGCAGCCAAAGCAATCACTCAAAGTTCAAACCTTATCATTTTTTGCTTTGTTCCTCTTGGCCTTGGTTTTGTACATCAGCTTTGAAAATACCATCCCAGGGTTAATGCTGGGGTTAATTTATAACTAAGAGTGCTCTAGTTTTGCAATACAGGACATGCTATAAAAATGGAAAGAT
>backbone_element_start:948_stop:977_length:30 visible=False
CAAGTTTGTACAAAAAAGCAGGCTGCCACC
>SEQ1 : SMN1_start:978_stop:1862_length:885 visible=True
ATGGCTATGTCTAGCGGAGGCTCTGGAGGAGGAGTTCCTGAACAGGAGGACTCTGTGCTGTTCCGGAGGGGCACAGGACAAAGCGATGACAGCGACATCTGGGACGACACAGCTCTGATTAAGGCCTACGACAAGGCCGTGGCCAGCTTCAAGCACGCCCTGAAGAACGGCGACATCTGCGAGACCAGCGGAAAGCCTAAAACCACCCCTAAGAGAAAGCCTGCTAAAAAGAACAAGAGCCAGAAGAAGAACACCGCTGCCAGCCTGCAGCAGTGGAAGGTGGGCGACAAGTGCAGCGCCATTTGGAGCGAGGACGGATGTATCTACCCTGCCACAATCGCCAGCATCGACTTCAAGCGGGAGACCTGCGTGGTGGTGTATACCGGCTACGGCAACAGGGAAGAGCAGAACCTGAGCGACCTGCTGAGCCCTATTTGCGAGGTGGCCAATAACATCGAGCAGAACGCCCAGGAGAACGAGAACGAGAGCCAGGTGAGCACCGACGAGAGCGAGAACAGCCGGAGCCCCGGCAATAAGAGCGACAACATCAAGCCCAAGAGCGCCCCCTGGAACTCTTTCCTGCCCCCCCCCCCCCCCATGCCTGGACCTAGATTGGGACCTGGAAAACCTGGACTGAAATTCAACGGCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCATTTGCTGTCTTGTTGGCTGCCCCCCTTCCCTTCTGGACCCCCCATTATCCCCCCCCCCCCCCCCATCTGTCCTGATTCTCTGGACGACGCCGATGCTTTGGGCTCTATGCTGATCTCTTGGTATATGAGCGGCTACCACACCGGCTACTACATGTTCCCCGAGGCCAGCCTGAAGGCCGAGCAGATGCCCGCTCCTTGTTTTCTG
>Fluorescent_tag_linker : T2A_start:1863_stop:1925_length:63 visible=True
GGAAGCGGAGAGGGCAGGGGAAGTCTTCTAACATGCGGGGACGTGGAGGAAAATCCCGGCCCC
>Fluorescent_tag : EGFP_start:1926_stop:2645_length:720 visible=True
ATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCTGGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGAGGGCGATGCCACCTACGGCAAGCTGACCCTGAAGTTCATCTGCACCACCGGCAAGCTGCCCGTGCCCTGGCCCACCCTCGTGACCACCCTGACCTACGGCGTGCAGTGCTTCAGCCGCTACCCCGACCACATGAAGCAGCACGACTTCTTCAAGTCCGCCATGCCCGAAGGCTACGTCCAGGAGCGCACCATCTTCTTCAAGGACGACGGCAACTACAAGACCCGCGCCGAGGTGAAGTTCGAGGGCGACACCCTGGTGAACCGCATCGAGCTGAAGGGCATCGACTTCAAGGAGGACGGCAACATCCTGGGGCACAAGCTGGAGTACAACTACAACAGCCACAACGTCTATATCATGGCCGACAAGCAGAAGAACGGCATCAAGGTGAACTTCAAGATCCGCCACAACATCGAGGACGGCAGCGTGCAGCTCGCCGACCACTACCAGCAGAACACCCCCATCGGCGACGGCCCCGTGCTGCTGCCCGACAACCACTACCTGAGCACCCAGTCCGCCCTGAGCAAAGACCCCAACGAGAAGCGCGATCACATGGTCCTGCTGGAGTTCGTGACCGCCGCCGGGATCACTCTCGGCATGGACGAGCTGTACAAGTAA
>Enhancer : WPRE_start:2646_stop:3243_length:598 visible=True
CGATAATCAACCTCTGGATTACAAAATTTGTGAAAGATTGACTGGTATTCTTAACTATGTTGCTCCTTTTACGCTATGTGGATACGCTGCTTTAATGCCTTTGTATCATGCTATTGCTTCCCGTATGGCTTTCATTTTCTCCTCCTTGTATAAATCCTGGTTGCTGTCTCTTTATGAGGAGTTGTGGCCCGTTGTCAGGCAACGTGGCGTGGTGTGCACTGTGTTTGCTGACGCAACCCCCACTGGTTGGGGCATTGCCACCACCTGTCAGCTCCTTTCCGGGACTTTCGCTTTCCCCCTCCCTATTGCCACGGCGGAACTCATCGCCGCCTGCCTTGCCCGCTGCTGGACAGGGGCTCGGCTGTTGGGCACTGACAATTCCGTGGTGTTGTCGGGGAAGCTGACGTCCTTTCCATGGCTGCTCGCCTGTGTTGCCACCTGGATTCTGCGCGGGACGTCCTTCTGCTACGTCCCTTCGGCCCTCAATCCAGCGGACCTTCCTTCCCGCGGCCTGCTGCCGGCTCTGCGGCCTCTTCCGCGTCTTCGCCTTCGCCCTCAGACGAGTCGGATCTCCCTTTGGGCCGCCTCCCCGCATCGG
>backbone_element_start:3244_stop:3287_length:44 visible=False
ACCCAGCTTTCTTGTACAAAGTGGTGATGGCCGGCCGCTTCGAG
>PolyA_signal : SV40_late_start:3288_stop:3509_length:222 visible=True
CAGACATGATAAGATACATTGATGAGTTTGGACAAACCACAACTAGAATGCAGTGAAAAAAATGCTTTATTTGTGAAATTTGTGATGCTATTGCTTTATTTGTAACCATTATAAGCTGCAATAAACAAGTTAACAACAACAATTGCATTCATTTTATGTTTCAGGTTCAGGGGGAGGTGTGGGAGGTTTTTTAAAGCAAGTAAAACCTCTACAAATGTGGTA
>backbone_element_start:3510_stop:3521_length:12 visible=False
ATCGATAGATCT
>3`ITR_start:3522_stop:3651_length:130 visible=True
AGGAACCCCTAGTGATGGAGTTGGCCACTCCCTCTCTGCGCGCTCGCTCGCTCACTGAGGCCGGGCGACCAAAGGTCGCCCGACGCCCGGGCTTTGCCCGGGCGGCCTCAGTGAGCGAGCGAGCGCGCAG
>backbone_element_start:3652_stop:4742_length:1091 visible=False
CTGCCTGCAGGCAGCTTGGCACTGGCCGTCGTTTTACAACGTCGTGACTGGGAAAACCCTGGCGTTACCCAACTTAATCGCCTTGCAGCACATCCCCCTTTCGCCAGCTGGCGTAATAGCGAAGAGGCCCGCACCGATCGCCCTTCCCAACAGTTGCGCAGCCTGAATGGCGAATGGCGCCTGATGCGGTATTTTCTCCTTACGCATCTGTGCGGTATTTCACACCGCATACGTCAAAGCAACCATAGTACGCGCCCTGTAGCGGCGCATTAAGCGCGGCGGGTGTGGTGGTTACGCGCAGCGTGACCGCTACACTTGCCAGCGCCCTAGCGCCCGCTCCTTTCGCTTTCTTCCCTTCCTTTCTCGCCACGTTCGCCGGCTTTCCCCGTCAAGCTCTAAATCGGGGGCTCCCTTTAGGGTTCCGATTTAGTGCTTTACGGCACCTCGACCCCAAAAAACTTGATTTGGGTGATGGTTCACGTAGTGGGCCATCGCCCTGATAGACGGTTTTTCGCCCTTTGACGTTGGAGTCCACGTTCTTTAATAGTGGACTCTTGTTCCAAACTGGAACAACACTCAACCCTATCTCGGGCTATTCTTTTGATTTATAAGGGATTTTGCCGATTTCGGCCTATTGGTTAAAAAATGAGCTGATTTAACAAAAATTTAACGCGAATTTTAACAAAATATTAACGTTTACAATTTTATGGTGCACTCTCAGTACAATCTGCTCTGATGCCGCATAGTTAAGCCAGCCCCGACACCCGCCAACACCCGCTGACGCGCCCTGACGGGCTTGTCTGCTCCCGGCATCCGCTTACAGACAAGCTGTGACCGTCTCCGGGAGCTGCATGTGTCAGAGGTTTTCACCGTCATCACCGAAACGCGCGAGACGAAAGGGCCTCGTGATACGCCTATTTTTATAGGTTAATGTCATGATAATAATGGTTTCTTAGACGTCAGGTGGCACTTTTCGGGGAAATGTGCGCGGAACCCCTATTTGTTTATTTTTCTAAATACATTCAAATATGTATCCGCTCATGAGACAATAACCCTGATAAATGCTTCAATAATATTGAAAAAGGAAGAGT
>Resistance : Ampicillin_start:4743_stop:5603_length:861 visible=True
ATGAGTATTCAACATTTCCGTGTCGCCCTTATTCCCTTTTTTGCGGCATTTTGCCTTCCTGTTTTTGCTCACCCAGAAACGCTGGTGAAAGTAAAAGATGCTGAAGATCAGTTGGGTGCACGAGTGGGTTACATCGAACTGGATCTCAACAGCGGTAAGATCCTTGAGAGTTTTCGCCCCGAAGAACGTTTTCCAATGATGAGCACTTTTAAAGTTCTGCTATGTGGCGCGGTATTATCCCGTATTGACGCCGGGCAAGAGCAACTCGGTCGCCGCATACACTATTCTCAGAATGACTTGGTTGAGTACTCACCAGTCACAGAAAAGCATCTTACGGATGGCATGACAGTAAGAGAATTATGCAGTGCTGCCATAACCATGAGTGATAACACTGCGGCCAACTTACTTCTGACAACGATCGGAGGACCGAAGGAGCTAACCGCTTTTTTGCACAACATGGGGGATCATGTAACTCGCCTTGATCGTTGGGAACCGGAGCTGAATGAAGCCATACCAAACGACGAGCGTGACACCACGATGCCTGTAGCAATGGCAACAACGTTGCGCAAACTATTAACTGGCGAACTACTTACTCTAGCTTCCCGGCAACAATTAATAGACTGGATGGAGGCGGATAAAGTTGCAGGACCACTTCTGCGCTCGGCCCTTCCGGCTGGCTGGTTTATTGCTGATAAATCTGGAGCCGGTGAGCGTGGAAGCCGCGGTATCATTGCAGCACTGGGGCCAGATGGTAAGCCCTCCCGTATCGTAGTTATCTACACGACGGGGAGTCAGGCAACTATGGATGAACGAAATAGACAGATCGCTGAGATAGGTGCCTCACTGATTAAGCATTGGTAA
>backbone_element_start:5604_stop:5773_length:170 visible=False
CTGTCAGACCAAGTTTACTCATATATACTTTAGATTGATTTAAAACTTCATTTTTAATTTAAAAGGATCTAGGTGAAGATCCTTTTTGATAATCTCATGACCAAAATCCCTTAACGTGAGTTTTCGTTCCACTGAGCGTCAGACCCCGTAGAAAAGATCAAAGGATCTTC
>pUC_ori_start:5774_stop:6362_length:589 visible=True
TTGAGATCCTTTTTTTCTGCGCGTAATCTGCTGCTTGCAAACAAAAAAACCACCGCTACCAGCGGTGGTTTGTTTGCCGGATCAAGAGCTACCAACTCTTTTTCCGAAGGTAACTGGCTTCAGCAGAGCGCAGATACCAAATACTGTTCTTCTAGTGTAGCCGTAGTTAGGCCACCACTTCAAGAACTCTGTAGCACCGCCTACATACCTCGCTCTGCTAATCCTGTTACCAGTGGCTGCTGCCAGTGGCGATAAGTCGTGTCTTACCGGGTTGGACTCAAGACGATAGTTACCGGATAAGGCGCAGCGGTCGGGCTGAACGGGGGGTTCGTGCACACAGCCCAGCTTGGAGCGAACGACCTACACCGAACTGAGATACCTACAGCGTGAGCTATGAGAAAGCGCCACGCTTCCCGAAGGGAGAAAGGCGGACAGGTATCCGGTAAGCGGCAGGGTCGGAACAGGAGAGCGCACGAGGGAGCTTCCAGGGGGAAACGCCTGGTATCTTTATAGTCCTGTCGGGTTTCGCCACCTCTGACTTGAGCGTCGATTTTTGTGATGCTCGTCAGGGGGGCGGAGCCTATGGAAA
>backbone_element_start:6363_stop:6790_length:428 visible=False
AACGCCAGCAACGCGGCCTTTTTACGGTTCCTGGCCTTTTGCTGGCCTTTTGCTCACATGTTCTTTCCTGCGTTATCCCCTGATTCTGTGGATAACCGTATTACCGCCTTTGAGTGAGCTGATACCGCTCGCCGCAGCCGAACGACCGAGCGCAGCGAGTCAGTGAGCGAGGAAGCGGAAGAGCGCCCAATACGCAAACCGCCTCTCCCCGCGCGTTGGCCGATTCATTAATGCAGCTGGCACGACAGGTTTCCCGACTGGAAAGCGGGCAGTGAGCGCAACGCAATTAATGTGAGTTAGCTCACTCATTAGGCACCCCAGGCTTTACACTTTATGCTTCCGGCTCGTATGTTGTGTGGAATTGTGAGCGGATAACAATTTCACACAGGAAACAGCTATGACCATGATTACGAATTGCCTGCAGGCAG
```

<br />
<br />

```
# Top 1 designed RNAi in shRNA form information
# RNAi name
project['rnai']['name']

# RNAi sequence
project['rnai']['sequence']

# RNAi prediction structure
rnai_prediction = project['rnai']['figure']
rnai_prediction.savefig('rnai_predicted_structure.svg')
```

Example return:

<p align="center">
<img  src="https://raw.githubusercontent.com/jkubis96/JBioSeqTools/3fb8a369a9c893d65589a92680fcb1e0cbcefa87/fig/rnai_predicted_structure.svg" alt="drawing" width="600" />
</p>

<br />

```
# other selected RNAi

pd.DataFrame(project['rnai']['full_data'])
```

##### Examples with structure description presented in:
 - 1.23. [Prediction of RNAi on the provided sequence](#rnai-prediction) 
 - 1.24. [Correcting of RNAi_data for complementarity to the loop sequence](#correcting-loop) 
 - 1.25. [Correcting of RNAi_data for complementarity to the additional external sequence](#correcting-sequence) 


<br />
<br />

```
## *if occur user-defined sequences for additional expression in the plasmid vector
## genes names
project['transcripts']['sequences']['name']

## proteins sequences
project['transcripts']['sequences']['sequence_aa']

## average codon frequency in the input sequence
project['transcripts']['sequences']['vector_sequence_frequence']

## GC% content in the input sequence
project['transcripts']['sequences']['vector_sequence_GC']

############################################################################

## average codon frequency in the output sequence
project['transcripts']['sequences']['optimized_vector_sequence_frequence']

## GC% content in the output sequence
project['transcripts']['sequences']['optimized_vector_sequence_GC']
```




<br />


#### 2.2.3 Creating plasmid vector of in-vitro transcription of mRNA <a id="transcript-mrna"></a>

##### Empty input dictionary schema:


```
input_dict = {
    
    # REQUIRED!
    # name of current project (defined by user)
    'project_name':'',
    
    # REQUIRED!
    # avaiable of vector types (transcription)
    'vector_type':'transcription',
    
    # REQUIRED!
    # in this case 'vector_function':'mrna'
    'vector_function':'mrna',
    
    # REQUIRED!
    # avaiable options (human / mouse / rat / both (mouse + human) / both2 (rat + human) / multi (mouse + rat + human))
    # 'both / both2 / multi' - creating vector function adjusted for all species taking into consideration most adjustments for Homo sapiens
    'species':'human',
    
    # REQUIRED!
    # list of coding sequences (CDS) provided to make expression from the vector
    # amount of sequences is not restricted as the user must remember that the length of whole vector is limited
    # excide the relevant vector size can decrease vector working
    # sequences orientation 5' ---> 3' - sense
    'sequences':[''],
    # REQUIRED!
    # list of names of coding sequences
    # amount of names should be equal with amount of sequences
    # if provided no sequences, provide ['']
    'sequences_names':[''],
    
    # REQUIRED if more than one sequence of transcripts!
    # sequences of provided linkers
    # number of linkers_sequences should be equal number of sequences (transcripts) - 1. One linker for each pair of sequences.
    # if the number of transcript sequences is equal 1 then provide empty list []
    # if the user wants to not provide any linkers between the transcript sequences, provide an empty string '' for each pair of transcripts where the user wants to avoid linker; empty strings '' provide inside the list ['']
    # sequence orientation 5' ---> 3' - sense
    'linkers_sequences':[''],
    # REQUIRED if transcript sequence occures, if not empty string ''!
    # names of provided linkers
    # if the number of transcript sequences is equal 1 then provide empty list []
    # if the user wants to not provide any linkers between the transcript sequences, provide an empty string '' for each pair of transcripts where the user wants to avoid linker; empty strings '' provide inside the list ['']
    'linkers_names':[''],
    
    # REQUIRED!
    # sequence of provided 5`UTR
    # sequence orientation 5' ---> 3' - sense
    'utr5_sequence':'',
    # REQUIRED!
    # name of provided 5`UTR
    'utr5_name':'',
    
    # REQUIRED!
    # sequence of provided 3`UTR
    # sequence orientation 5' ---> 3' - sense
    'utr3_sequence':'',
    # REQUIRED!
    # name of provided 3`UTR
    'utr3_name':'',
    
    # REQUIRED!
    # number (integer) of A repeat in the polyA tail
    'polya_tail_x':00,
    
    # REQUIRED!
    # sequence of provided selection marker
    # sequence orientation 5' ---> 3' - sense
    'selection_marker_sequence':'',
    # REQUIRED!
    # name of provided selection marker
    'selection_marker_name':'',
    
    # POSSIBLE!
    # restriction enzymes protection of transcript sequences
    # if the user does not need any restriction places protection, provide empty list []
    'restriction_list':[],
    
    # REQUIRED!
    # available options (True / False)
    # decision; if the user wants the transcription sequences optimized based on the provided species
    'optimize':True

}
```


<br />


##### Example dictionary:



```
input_dict = {
    
    'project_name':'test_invitro_transcription_mRNA',
    'vector_type':'transcription',
    'vector_function':'mrna',
    'species':'human',
    'sequences':['ATGGCGATGAGCAGCGGCGGCAGTGGTGGCGGCGTCCCGGAGCAGGAGGATTCCGTGCTGTTCCGGCGCGGCACAGGCCAGAGCGATGATTCTGACATTTGGGATGATACAGCACTGATAAAAGCATATGATAAAGCTGTGGCTTCATTTAAGCATGCTCTAAAGAATGGTGACATTTGTGAAACTTCGGGTAAACCAAAAACCACACCTAAAAGAAAACCTGCTAAGAAGAATAAAAGCCAAAAGAAGAATACTGCAGCTTCCTTACAACAGTGGAAAGTTGGGGACAAATGTTCTGCCATTTGGTCAGAAGACGGTTGCATTTACCCAGCTACCATTGCTTCAATTGATTTTAAGAGAGAAACCTGTGTTGTGGTTTACACTGGATATGGAAATAGAGAGGAGCAAAATCTGTCCGATCTACTTTCCCCAATCTGTGAAGTAGCTAATAATATAGAACAAAATGCTCAAGAGAATGAAAATGAAAGCCAAGTTTCAACAGATGAAAGTGAGAACTCCAGGTCTCCTGGAAATAAATCAGATAACATCAAGCCCAAATCTGCTCCATGGAACTCTTTTCTCCCTCCACCACCCCCCATGCCAGGGCCAAGACTGGGACCAGGAAAGCCAGGTCTAAAATTCAATGGCCCACCACCGCCACCGCCACCACCACCACCCCACTTACTATCATGCTGGCTGCCTCCATTTCCTTCTGGACCACCAATAATTCCCCCACCACCTCCCATATGTCCAGATTCTCTTGATGATGCTGATGCTTTGGGAAGTATGTTAATTTCATGGTACATGAGTGGCTATCATACTGGCTATTATATGTTTCCTGAGGCCTCCCTAAAAGCCGAGCAGATGCCAGCACCATGCTTCCTGTAA'],
    'sequences_names':['SMN1'],
    'linkers_sequences':[''],
    'linkers_names':[''],
    'utr5_sequence':'GGGCTGGAAGCTACCTTTGACATCATTTCCTCTGCGAATGCATGTATAATTTCTACAGAACCTATTAGAAAGGATCACCCAGCCTCTGCTTTTGTACAACTTTCCCTTAAAAAACTGCCAATTCCACTGCTGTTTGGCCCAATAGTGAGAACTTTTTCCTGCTGCCTCTTGGTGCTTTTGCCTATGGCCCCTATTCTGCCTGCTGAAGACACTCTTGCCAGCATGGACTTAAACCCCTCCAGCTCTGACAATCCTCTTTCTCTTTTGTTTTACATGAAGGGTCTGGCAGCCAAAGCAATCACTCAAAGTTCAAACCTTATCATTTTTTGCTTTGTTCCTCTTGGCCTTGGTTTTGTACATCAGCTTTGAAAATACCATCCCAGGGTTAATGCTGGGGTTAATTTATAACTAAGAGTGCTCTAGTTTTGCAATACAGGACATGCTATAAAAATGGAAAGAT',
    'utr5_name':'SMN1',
    'utr3_sequence':'CAGACATGATAAGATACATTGATGAGTTTGGACAAACCACAACTAGAATGCAGTGAAAAAAATGCTTTATTTGTGAAATTTGTGATGCTATTGCTTTATTTGTAACCATTATAAGCTGCAATAAACAAGTTAACAACAACAATTGCATTCATTTTATGTTTCAGGTTCAGGGGGAGGTGTGGGAGGTTTTTTAAAGCAAGTAAAACCTCTACAAATGTGGTA',
    'utr3_name':'KIT',
    'polya_tail_x':50,
    'selection_marker_sequence':'ATGAGTATTCAACATTTCCGTGTCGCCCTTATTCCCTTTTTTGCGGCATTTTGCCTTCCTGTTTTTGCTCACCCAGAAACGCTGGTGAAAGTAAAAGATGCTGAAGATCAGTTGGGTGCACGAGTGGGTTACATCGAACTGGATCTCAACAGCGGTAAGATCCTTGAGAGTTTTCGCCCCGAAGAACGTTTTCCAATGATGAGCACTTTTAAAGTTCTGCTATGTGGCGCGGTATTATCCCGTATTGACGCCGGGCAAGAGCAACTCGGTCGCCGCATACACTATTCTCAGAATGACTTGGTTGAGTACTCACCAGTCACAGAAAAGCATCTTACGGATGGCATGACAGTAAGAGAATTATGCAGTGCTGCCATAACCATGAGTGATAACACTGCGGCCAACTTACTTCTGACAACGATCGGAGGACCGAAGGAGCTAACCGCTTTTTTGCACAACATGGGGGATCATGTAACTCGCCTTGATCGTTGGGAACCGGAGCTGAATGAAGCCATACCAAACGACGAGCGTGACACCACGATGCCTGTAGCAATGGCAACAACGTTGCGCAAACTATTAACTGGCGAACTACTTACTCTAGCTTCCCGGCAACAATTAATAGACTGGATGGAGGCGGATAAAGTTGCAGGACCACTTCTGCGCTCGGCCCTTCCGGCTGGCTGGTTTATTGCTGATAAATCTGGAGCCGGTGAGCGTGGAAGCCGCGGTATCATTGCAGCACTGGGGCCAGATGGTAAGCCCTCCCGTATCGTAGTTATCTACACGACGGGGAGTCAGGCAACTATGGATGAACGAAATAGACAGATCGCTGAGATAGGTGCCTCACTGATTAAGCATTGGTAA',
    'selection_marker_name':'Ampicillin',
    'restriction_list':['RsaI', 'MnlI', 'AciI', 'AluI', 'BmrI'],
    'optimize':True
}
```

<br />

##### Output:

```
# Name of project
project['project']
```

``` 
# Graph of the designed vector
vector_plot = project['vector']['graph']
vector_plot.savefig('expression_vector.svg')
```
<br />

Example return:

<p align="center">
<img  src="https://raw.githubusercontent.com/jkubis96/JBioSeqTools/3fb8a369a9c893d65589a92680fcb1e0cbcefa87/fig/transcription_mrna_vector.svg" alt="drawing" width="600" />
</p>

<br />

```
# Complete FASTA file of the designed vecotr
project['vector']['full_fasta']
```

Example return:

```
>test_invitro_transcription_mRNA_Regular_plasmid_mrna_3676nc
TAATACGACTCACTATAGGGGGCTGGAAGCTACCTTTGACATCATTTCCTCTGCGAATGCATGTATAATTTCTACAGAACCTATTAGAAAGGATCACCCAGCCTCTGCTTTTGTACAACTTTCCCTTAAAAAACTGCCAATTCCACTGCTGTTTGGCCCAATAGTGAGAACTTTTTCCTGCTGCCTCTTGGTGCTTTTGCCTATGGCCCCTATTCTGCCTGCTGAAGACACTCTTGCCAGCATGGACTTAAACCCCTCCAGCTCTGACAATCCTCTTTCTCTTTTGTTTTACATGAAGGGTCTGGCAGCCAAAGCAATCACTCAAAGTTCAAACCTTATCATTTTTTGCTTTGTTCCTCTTGGCCTTGGTTTTGTACATCAGCTTTGAAAATACCATCCCAGGGTTAATGCTGGGGTTAATTTATAACTAAGAGTGCTCTAGTTTTGCAATACAGGACATGCTATAAAAATGGAAAGATGCCACCATGGCTATGTCTAGCGGAGGCTCTGGAGGAGGAGTTCCTGAACAGGAGGACTCTGTGCTGTTCCGGAGGGGCACAGGACAAAGCGATGACAGCGACATCTGGGACGACACAGCTCTGATTAAGGCCTACGACAAGGCCGTGGCCAGCTTCAAGCACGCCCTGAAGAACGGCGACATCTGCGAGACCAGCGGAAAGCCTAAAACCACCCCTAAGAGAAAGCCTGCTAAAAAGAACAAGAGCCAGAAGAAGAACACCGCTGCCAGCCTGCAGCAGTGGAAGGTGGGCGACAAGTGCAGCGCCATTTGGAGCGAGGACGGATGTATCTACCCTGCCACAATCGCCAGCATCGACTTCAAGCGGGAGACCTGCGTGGTGGTGTATACCGGCTACGGCAACAGGGAAGAGCAGAACCTGAGCGACCTGCTGAGCCCTATTTGCGAGGTGGCCAATAACATCGAGCAGAACGCCCAGGAGAACGAGAACGAGAGCCAGGTGAGCACCGACGAGAGCGAGAACAGCCGGAGCCCCGGCAATAAGAGCGACAACATCAAGCCCAAGAGCGCCCCCTGGAACTCTTTCCTGCCCCCCCCCCCCCCCATGCCTGGACCTAGATTGGGACCTGGAAAACCTGGACTGAAATTCAACGGCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCATTTGCTGTCTTGTTGGCTGCCCCCCTTCCCTTCTGGACCCCCCATTATCCCCCCCCCCCCCCCCATCTGTCCTGATTCTCTGGACGACGCCGATGCTTTGGGCTCTATGCTGATCTCTTGGTATATGAGCGGCTACCACACCGGCTACTACATGTTCCCCGAGGCCAGCCTGAAGGCCGAGCAGATGCCCGCTCCTTGTTTTCTGTGACAGACATGATAAGATACATTGATGAGTTTGGACAAACCACAACTAGAATGCAGTGAAAAAAATGCTTTATTTGTGAAATTTGTGATGCTATTGCTTTATTTGTAACCATTATAAGCTGCAATAAACAAGTTAACAACAACAATTGCATTCATTTTATGTTTCAGGTTCAGGGGGAGGTGTGGGAGGTTTTTTAAAGCAAGTAAAACCTCTACAAATGTGGTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATGAAGAGCCGTACGGGCGCGCCTAGGCGCGATTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGCGGCGAGCGGTATCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGAGCAAAAGGCCAGCAAAAGGCCAGGAACCGTAAAAAGGCCGCGTTGCTGGCGTTTTTCCATAGGCTCCGCCCCCCTGACGAGCATCACAAAAATCGACGCTCAAGTCAGAGGTGGCGAAACCCGACAGGACTATAAAGATACCAGGCGTTTCCCCCTGGAAGCTCCCTCGTGCGCTCTCCTGTTCCGACCCTGCCGCTTACCGGATACCTGTCCGCCTTTCTCCCTTCGGGAAGCGTGGCGCTTTCTCATAGCTCACGCTGTAGGTATCTCAGTTCGGTGTAGGTCGTTCGCTCCAAGCTGGGCTGTGTGCACGAACCCCCCGTTCAGCCCGACCGCTGCGCCTTATCCGGTAACTATCGTCTTGAGTCCAACCCGGTAAGACACGACTTATCGCCACTGGCAGCAGCCACTGGTAACAGGATTAGCAGAGCGAGGTATGTAGGCGGTGCTACAGAGTTCTTGAAGTGGTGGCCTAACTACGGCTACACTAGAAGAACAGTATTTGGTATCTGCGCTCTGCTGAAGCCAGTTACCTTCGGAAAAAGAGTTGGTAGCTCTTGATCCGGCAAACAAACCACCGCTGGTAGCGGTGGTTTTTTTGTTTGCAAGCAGCAGATTACGCGCAGAAAAAAAGGATCTCAAGAAGATCCTTTGATCTTTTCTACGGGGTCTGACGCTCAGTGGAACGAAAACTCACGTTAAGGGATTTTGGTCATGAGATTATCAAAAAGGATCTTCACCTAGATCCTTTTAAATTAAAAATGAAGTTTTAAATCAATCTAAAGTATATATGAGTAAACTTGGTCTGACAGAATGGTTACGAATTAGTCACTCCGTGGATAGAGTCGCTAGACAGATAAAGCAAGTAGGTATCAACGGACTGAGGGGCAGCACATCTATTGATGCTATGCCCTCCCGAATGGTAGACCGGGGTCACGACGTTACTATGGCGCCGAAGGTGCGAGTGGCCGAGGTCTAAATAGTCGTTATTTGGTCGGTCGGCCTTCCCGGCTCGCGTCTTCACCAGGACGTTGAAATAGGCGGAGGTAGGTCAGATAATTAACAACGGCCCTTCGATCTCATTCATCAAGCGGTCAATTATCAAACGCGTTGCAACAACGGTAACGATGTCCGTAGCACCACAGTGCGAGCAGCAAACCATACCGAAGTAAGTCGAGGCCAAGGGTTGCTAGTTCCGCTCAATGTACTAGGGGGTACAACACGTTTTTTCGCCAATCGAGGAAGCCAGGAGGCTAGCAACAGTCTTCATTCAACCGGCGTCACAATAGTGAGTACCAATACCGTCGTGACGTATTAAGAGAATGACAGTACGGTAGGCATTCTACGAAAAGACACTGACCACTCATGAGTTGGTTCAGTAAGACTCTTATCACATACGCCGCTGGCTCAACGAGAACGGGCCGCAGTTATGCCCTATTATGGCGCGGTGTATCGTCTTGAAATTTTCACGAGTAGTAACCTTTTGCAAGAAGCCCCGCTTTTGAGAGTTCCTAGAATGGCGACAACTCTAGGTCAAGCTACATTGGGTGAGCACGTGGGTTGACTAGAAGTCGTAGAAAATGAAAGTGGTCGCAAAGACCCACTCGTTTTTGTCCTTCCGTTTTACGGCGTTTTTTCCCTTATTCCCGCTGTGCCTTTACAACTTATGAGTAACTCTTCCTTTTTCAATATTATTGAAGCATTTATCAGGGTTATTGTCTCATGAGCGGATACATATTTGAATGTATTTAGAAAAATAAACAAATAGGGGTTCCGCGCACATTTCCCCGAAAAGTGCCACCTGACGTCTAAGAAACCATTATTATCATGACATTAACCTATAAAAATAGGCGTATCACGAGGCCCTTTCGTC
```

<br />
<br />

```
# The FASTA file is divided into particular elements of the designed vector
project['vector']['fasta']
```

Example return:


```
#test_invitro_transcription_mRNA_Regular_plasmid_mrna_3676nc

>T7_start:1_stop:19_length:19 visible=True
TAATACGACTCACTATAGG
>5`UTR : SMN1_start:20_stop:479_length:460 visible=True
GGGCTGGAAGCTACCTTTGACATCATTTCCTCTGCGAATGCATGTATAATTTCTACAGAACCTATTAGAAAGGATCACCCAGCCTCTGCTTTTGTACAACTTTCCCTTAAAAAACTGCCAATTCCACTGCTGTTTGGCCCAATAGTGAGAACTTTTTCCTGCTGCCTCTTGGTGCTTTTGCCTATGGCCCCTATTCTGCCTGCTGAAGACACTCTTGCCAGCATGGACTTAAACCCCTCCAGCTCTGACAATCCTCTTTCTCTTTTGTTTTACATGAAGGGTCTGGCAGCCAAAGCAATCACTCAAAGTTCAAACCTTATCATTTTTTGCTTTGTTCCTCTTGGCCTTGGTTTTGTACATCAGCTTTGAAAATACCATCCCAGGGTTAATGCTGGGGTTAATTTATAACTAAGAGTGCTCTAGTTTTGCAATACAGGACATGCTATAAAAATGGAAAGAT
>Kozak_sequence_start:480_stop:485_length:6 visible=True
GCCACC
>SEQ1 : SMN1_start:486_stop:1373_length:888 visible=True
ATGGCTATGTCTAGCGGAGGCTCTGGAGGAGGAGTTCCTGAACAGGAGGACTCTGTGCTGTTCCGGAGGGGCACAGGACAAAGCGATGACAGCGACATCTGGGACGACACAGCTCTGATTAAGGCCTACGACAAGGCCGTGGCCAGCTTCAAGCACGCCCTGAAGAACGGCGACATCTGCGAGACCAGCGGAAAGCCTAAAACCACCCCTAAGAGAAAGCCTGCTAAAAAGAACAAGAGCCAGAAGAAGAACACCGCTGCCAGCCTGCAGCAGTGGAAGGTGGGCGACAAGTGCAGCGCCATTTGGAGCGAGGACGGATGTATCTACCCTGCCACAATCGCCAGCATCGACTTCAAGCGGGAGACCTGCGTGGTGGTGTATACCGGCTACGGCAACAGGGAAGAGCAGAACCTGAGCGACCTGCTGAGCCCTATTTGCGAGGTGGCCAATAACATCGAGCAGAACGCCCAGGAGAACGAGAACGAGAGCCAGGTGAGCACCGACGAGAGCGAGAACAGCCGGAGCCCCGGCAATAAGAGCGACAACATCAAGCCCAAGAGCGCCCCCTGGAACTCTTTCCTGCCCCCCCCCCCCCCCATGCCTGGACCTAGATTGGGACCTGGAAAACCTGGACTGAAATTCAACGGCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCATTTGCTGTCTTGTTGGCTGCCCCCCTTCCCTTCTGGACCCCCCATTATCCCCCCCCCCCCCCCCATCTGTCCTGATTCTCTGGACGACGCCGATGCTTTGGGCTCTATGCTGATCTCTTGGTATATGAGCGGCTACCACACCGGCTACTACATGTTCCCCGAGGCCAGCCTGAAGGCCGAGCAGATGCCCGCTCCTTGTTTTCTGTGA
>3`UTR : KIT_start:1374_stop:1595_length:222 visible=True
CAGACATGATAAGATACATTGATGAGTTTGGACAAACCACAACTAGAATGCAGTGAAAAAAATGCTTTATTTGTGAAATTTGTGATGCTATTGCTTTATTTGTAACCATTATAAGCTGCAATAAACAAGTTAACAACAACAATTGCATTCATTTTATGTTTCAGGTTCAGGGGGAGGTGTGGGAGGTTTTTTAAAGCAAGTAAAACCTCTACAAATGTGGTA
>PolyA_tail : x 50_start:1596_stop:1645_length:50 visible=True
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
>backbone_element_start:1646_stop:1646_length:1 visible=False
T
>SapI_start:1647_stop:1653_length:7 visible=True
GAAGAGC
>BsiWI_start:1654_stop:1659_length:6 visible=True
CGTACG
>AscI_start:1660_stop:1667_length:8 visible=True
GGCGCGCC
>backbone_element_start:1668_stop:1856_length:189 visible=False
TAGGCGCGATTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGCGGCGAGCGGTATCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGAGCAAAAGGCCAGCAAAAGGCCAGGAACCGTAAAAAGGCCGCGTTGCTGGCGTT
>pUC_ori_start:1857_stop:2445_length:589 visible=True
TTTCCATAGGCTCCGCCCCCCTGACGAGCATCACAAAAATCGACGCTCAAGTCAGAGGTGGCGAAACCCGACAGGACTATAAAGATACCAGGCGTTTCCCCCTGGAAGCTCCCTCGTGCGCTCTCCTGTTCCGACCCTGCCGCTTACCGGATACCTGTCCGCCTTTCTCCCTTCGGGAAGCGTGGCGCTTTCTCATAGCTCACGCTGTAGGTATCTCAGTTCGGTGTAGGTCGTTCGCTCCAAGCTGGGCTGTGTGCACGAACCCCCCGTTCAGCCCGACCGCTGCGCCTTATCCGGTAACTATCGTCTTGAGTCCAACCCGGTAAGACACGACTTATCGCCACTGGCAGCAGCCACTGGTAACAGGATTAGCAGAGCGAGGTATGTAGGCGGTGCTACAGAGTTCTTGAAGTGGTGGCCTAACTACGGCTACACTAGAAGAACAGTATTTGGTATCTGCGCTCTGCTGAAGCCAGTTACCTTCGGAAAAAGAGTTGGTAGCTCTTGATCCGGCAAACAAACCACCGCTGGTAGCGGTGGTTTTTTTGTTTGCAAGCAGCAGATTACGCGCAGAAAAAAAGGATCTCAA
>backbone_element_start:2446_stop:2615_length:170 visible=False
GAAGATCCTTTGATCTTTTCTACGGGGTCTGACGCTCAGTGGAACGAAAACTCACGTTAAGGGATTTTGGTCATGAGATTATCAAAAAGGATCTTCACCTAGATCCTTTTAAATTAAAAATGAAGTTTTAAATCAATCTAAAGTATATATGAGTAAACTTGGTCTGACAG
>Resistance : Ampicillin_start:2616_stop:3476_length:861 visible=True
AATGGTTACGAATTAGTCACTCCGTGGATAGAGTCGCTAGACAGATAAAGCAAGTAGGTATCAACGGACTGAGGGGCAGCACATCTATTGATGCTATGCCCTCCCGAATGGTAGACCGGGGTCACGACGTTACTATGGCGCCGAAGGTGCGAGTGGCCGAGGTCTAAATAGTCGTTATTTGGTCGGTCGGCCTTCCCGGCTCGCGTCTTCACCAGGACGTTGAAATAGGCGGAGGTAGGTCAGATAATTAACAACGGCCCTTCGATCTCATTCATCAAGCGGTCAATTATCAAACGCGTTGCAACAACGGTAACGATGTCCGTAGCACCACAGTGCGAGCAGCAAACCATACCGAAGTAAGTCGAGGCCAAGGGTTGCTAGTTCCGCTCAATGTACTAGGGGGTACAACACGTTTTTTCGCCAATCGAGGAAGCCAGGAGGCTAGCAACAGTCTTCATTCAACCGGCGTCACAATAGTGAGTACCAATACCGTCGTGACGTATTAAGAGAATGACAGTACGGTAGGCATTCTACGAAAAGACACTGACCACTCATGAGTTGGTTCAGTAAGACTCTTATCACATACGCCGCTGGCTCAACGAGAACGGGCCGCAGTTATGCCCTATTATGGCGCGGTGTATCGTCTTGAAATTTTCACGAGTAGTAACCTTTTGCAAGAAGCCCCGCTTTTGAGAGTTCCTAGAATGGCGACAACTCTAGGTCAAGCTACATTGGGTGAGCACGTGGGTTGACTAGAAGTCGTAGAAAATGAAAGTGGTCGCAAAGACCCACTCGTTTTTGTCCTTCCGTTTTACGGCGTTTTTTCCCTTATTCCCGCTGTGCCTTTACAACTTATGAGTA
>backbone_element_start:3477_stop:3676_length:200 visible=False
ACTCTTCCTTTTTCAATATTATTGAAGCATTTATCAGGGTTATTGTCTCATGAGCGGATACATATTTGAATGTATTTAGAAAAATAAACAAATAGGGGTTCCGCGCACATTTCCCCGAAAAGTGCCACCTGACGTCTAAGAAACCATTATTATCATGACATTAACCTATAAAAATAGGCGTATCACGAGGCCCTTTCGTC
```

<br />
<br />

```
## genes names
project['transcripts']['sequences']['name']

## proteins sequences
project['transcripts']['sequences']['sequence_aa']

## average codon frequency in the input sequence
project['transcripts']['sequences']['vector_sequence_frequence']

## GC% content in the input sequence
project['transcripts']['sequences']['vector_sequence_GC']

############################################################################

## average codon frequency in the output sequence
project['transcripts']['sequences']['optimized_vector_sequence_frequence']

## GC% content in the output sequence
project['transcripts']['sequences']['optimized_vector_sequence_GC']
```


<br />


#### 2.2.4 Creating plasmid vector of in-vitro transcription of RNAi <a id="transcription-rnai"></a>

##### Empty input dictionary schema:


```
input_dict = {
    
    # REQUIRED!
    # name of current project (defined by user)
    'project_name':'',
    
    # REQUIRED!
    # avaiable of vector types (transcription)
    'vector_type':'transcription',
    
    # REQUIRED!
    # in this case 'vector_function':'rnai'
    'vector_function':'rnai',
    
    # REQUIRED!
    # avaiable options (human / mouse / rat / both (mouse + human) / both2 (rat + human) / multi (mouse + rat + human))
    # 'both / both2 / multi' - creating vector function adjusted for all species taking into consideration most adjustments for Homo sapiens
    'species':'human',
    
    # POSSIBLE!
    # sequence of custom RNAi, which can be provided by user
    # if provided, then the algorithm of RNAi estimation is off
    # if empt '' the algorithm share the best possible RNAi based on 'rnai_gene_name'
    # sequence orientation 5' ---> 3' - sense
    'rnai_sequence':'',
    
    # REQUIRED!
    # name of the target gene for the RNAi searching algorithm (gene name for Homo sapien or Mus musculus)
    # algorithm is working when the rnai_sequence is empty ''
    # if the user defines 'rnai_sequence' this 'rnai_gene_name' is just a name for a user-supplied sequence
    'rnai_gene_name':'',
    
    # REQUIRED!
    # sequence of the loop to create the structure of the hairpin of shRNA or siRNA depending on the loop sequence
    # algorithm is working when the rnai_sequence is empty ''
    # if the user defines 'rnai_sequence' this 'rnai_gene_name' is just a name for a user-supplied sequence
    # sequence orientation 5' ---> 3' - sense
    'loop_sequence':'',
    
    # REQUIRED!
    # sequence of provided selection marker
    # sequence orientation 5' ---> 3' - sense
    'selection_marker_sequence':'',
    # REQUIRED!
    # name of provided selection marker
    'selection_marker_name':''
}
```


<br />


##### Example dictionary:



```
input_dict = {

    'project_name':'test_invitro_transcription_RNAi',
    'vector_type':'transcription',
    'vector_function':'rnai',
    'species':'human',
    'rnai_sequence':'',
    'rnai_gene_name':'KIT',
    'loop_sequence':'TAGTGAAGCCACAGATGTAC',
    'selection_marker_sequence':'ATGAGTATTCAACATTTCCGTGTCGCCCTTATTCCCTTTTTTGCGGCATTTTGCCTTCCTGTTTTTGCTCACCCAGAAACGCTGGTGAAAGTAAAAGATGCTGAAGATCAGTTGGGTGCACGAGTGGGTTACATCGAACTGGATCTCAACAGCGGTAAGATCCTTGAGAGTTTTCGCCCCGAAGAACGTTTTCCAATGATGAGCACTTTTAAAGTTCTGCTATGTGGCGCGGTATTATCCCGTATTGACGCCGGGCAAGAGCAACTCGGTCGCCGCATACACTATTCTCAGAATGACTTGGTTGAGTACTCACCAGTCACAGAAAAGCATCTTACGGATGGCATGACAGTAAGAGAATTATGCAGTGCTGCCATAACCATGAGTGATAACACTGCGGCCAACTTACTTCTGACAACGATCGGAGGACCGAAGGAGCTAACCGCTTTTTTGCACAACATGGGGGATCATGTAACTCGCCTTGATCGTTGGGAACCGGAGCTGAATGAAGCCATACCAAACGACGAGCGTGACACCACGATGCCTGTAGCAATGGCAACAACGTTGCGCAAACTATTAACTGGCGAACTACTTACTCTAGCTTCCCGGCAACAATTAATAGACTGGATGGAGGCGGATAAAGTTGCAGGACCACTTCTGCGCTCGGCCCTTCCGGCTGGCTGGTTTATTGCTGATAAATCTGGAGCCGGTGAGCGTGGAAGCCGCGGTATCATTGCAGCACTGGGGCCAGATGGTAAGCCCTCCCGTATCGTAGTTATCTACACGACGGGGAGTCAGGCAACTATGGATGAACGAAATAGACAGATCGCTGAGATAGGTGCCTCACTGATTAAGCATTGGTAA',
    'selection_marker_name':'Ampicillin'
}
```
<br />

##### Output:

```
# Name of project
project['project']
```

``` 
# Graph of the designed vector
vector_plot = project['vector']['graph']
vector_plot.savefig('expression_vector.svg')
```
<br />

Example return:

<p align="center">
<img  src="https://raw.githubusercontent.com/jkubis96/JBioSeqTools/3fb8a369a9c893d65589a92680fcb1e0cbcefa87/fig/transcription_rnai_vector.svg" alt="drawing" width="600" />
</p>

<br />

```
# Complete FASTA file of the designed vecotr
project['vector']['full_fasta']
```

Example return:

```
>test_invitro_transcription_mRNA_Regular_plasmid_mrna_3676nc
TAATACGACTCACTATAGGGGGCTGGAAGCTACCTTTGACATCATTTCCTCTGCGAATGCATGTATAATTTCTACAGAACCTATTAGAAAGGATCACCCAGCCTCTGCTTTTGTACAACTTTCCCTTAAAAAACTGCCAATTCCACTGCTGTTTGGCCCAATAGTGAGAACTTTTTCCTGCTGCCTCTTGGTGCTTTTGCCTATGGCCCCTATTCTGCCTGCTGAAGACACTCTTGCCAGCATGGACTTAAACCCCTCCAGCTCTGACAATCCTCTTTCTCTTTTGTTTTACATGAAGGGTCTGGCAGCCAAAGCAATCACTCAAAGTTCAAACCTTATCATTTTTTGCTTTGTTCCTCTTGGCCTTGGTTTTGTACATCAGCTTTGAAAATACCATCCCAGGGTTAATGCTGGGGTTAATTTATAACTAAGAGTGCTCTAGTTTTGCAATACAGGACATGCTATAAAAATGGAAAGATGCCACCATGGCTATGTCTAGCGGAGGCTCTGGAGGAGGAGTTCCTGAACAGGAGGACTCTGTGCTGTTCCGGAGGGGCACAGGACAAAGCGATGACAGCGACATCTGGGACGACACAGCTCTGATTAAGGCCTACGACAAGGCCGTGGCCAGCTTCAAGCACGCCCTGAAGAACGGCGACATCTGCGAGACCAGCGGAAAGCCTAAAACCACCCCTAAGAGAAAGCCTGCTAAAAAGAACAAGAGCCAGAAGAAGAACACCGCTGCCAGCCTGCAGCAGTGGAAGGTGGGCGACAAGTGCAGCGCCATTTGGAGCGAGGACGGATGTATCTACCCTGCCACAATCGCCAGCATCGACTTCAAGCGGGAGACCTGCGTGGTGGTGTATACCGGCTACGGCAACAGGGAAGAGCAGAACCTGAGCGACCTGCTGAGCCCTATTTGCGAGGTGGCCAATAACATCGAGCAGAACGCCCAGGAGAACGAGAACGAGAGCCAGGTGAGCACCGACGAGAGCGAGAACAGCCGGAGCCCCGGCAATAAGAGCGACAACATCAAGCCCAAGAGCGCCCCCTGGAACTCTTTCCTGCCCCCCCCCCCCCCCATGCCTGGACCTAGATTGGGACCTGGAAAACCTGGACTGAAATTCAACGGCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCATTTGCTGTCTTGTTGGCTGCCCCCCTTCCCTTCTGGACCCCCCATTATCCCCCCCCCCCCCCCCATCTGTCCTGATTCTCTGGACGACGCCGATGCTTTGGGCTCTATGCTGATCTCTTGGTATATGAGCGGCTACCACACCGGCTACTACATGTTCCCCGAGGCCAGCCTGAAGGCCGAGCAGATGCCCGCTCCTTGTTTTCTGTGACAGACATGATAAGATACATTGATGAGTTTGGACAAACCACAACTAGAATGCAGTGAAAAAAATGCTTTATTTGTGAAATTTGTGATGCTATTGCTTTATTTGTAACCATTATAAGCTGCAATAAACAAGTTAACAACAACAATTGCATTCATTTTATGTTTCAGGTTCAGGGGGAGGTGTGGGAGGTTTTTTAAAGCAAGTAAAACCTCTACAAATGTGGTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATGAAGAGCCGTACGGGCGCGCCTAGGCGCGATTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGCGGCGAGCGGTATCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGAGCAAAAGGCCAGCAAAAGGCCAGGAACCGTAAAAAGGCCGCGTTGCTGGCGTTTTTCCATAGGCTCCGCCCCCCTGACGAGCATCACAAAAATCGACGCTCAAGTCAGAGGTGGCGAAACCCGACAGGACTATAAAGATACCAGGCGTTTCCCCCTGGAAGCTCCCTCGTGCGCTCTCCTGTTCCGACCCTGCCGCTTACCGGATACCTGTCCGCCTTTCTCCCTTCGGGAAGCGTGGCGCTTTCTCATAGCTCACGCTGTAGGTATCTCAGTTCGGTGTAGGTCGTTCGCTCCAAGCTGGGCTGTGTGCACGAACCCCCCGTTCAGCCCGACCGCTGCGCCTTATCCGGTAACTATCGTCTTGAGTCCAACCCGGTAAGACACGACTTATCGCCACTGGCAGCAGCCACTGGTAACAGGATTAGCAGAGCGAGGTATGTAGGCGGTGCTACAGAGTTCTTGAAGTGGTGGCCTAACTACGGCTACACTAGAAGAACAGTATTTGGTATCTGCGCTCTGCTGAAGCCAGTTACCTTCGGAAAAAGAGTTGGTAGCTCTTGATCCGGCAAACAAACCACCGCTGGTAGCGGTGGTTTTTTTGTTTGCAAGCAGCAGATTACGCGCAGAAAAAAAGGATCTCAAGAAGATCCTTTGATCTTTTCTACGGGGTCTGACGCTCAGTGGAACGAAAACTCACGTTAAGGGATTTTGGTCATGAGATTATCAAAAAGGATCTTCACCTAGATCCTTTTAAATTAAAAATGAAGTTTTAAATCAATCTAAAGTATATATGAGTAAACTTGGTCTGACAGAATGGTTACGAATTAGTCACTCCGTGGATAGAGTCGCTAGACAGATAAAGCAAGTAGGTATCAACGGACTGAGGGGCAGCACATCTATTGATGCTATGCCCTCCCGAATGGTAGACCGGGGTCACGACGTTACTATGGCGCCGAAGGTGCGAGTGGCCGAGGTCTAAATAGTCGTTATTTGGTCGGTCGGCCTTCCCGGCTCGCGTCTTCACCAGGACGTTGAAATAGGCGGAGGTAGGTCAGATAATTAACAACGGCCCTTCGATCTCATTCATCAAGCGGTCAATTATCAAACGCGTTGCAACAACGGTAACGATGTCCGTAGCACCACAGTGCGAGCAGCAAACCATACCGAAGTAAGTCGAGGCCAAGGGTTGCTAGTTCCGCTCAATGTACTAGGGGGTACAACACGTTTTTTCGCCAATCGAGGAAGCCAGGAGGCTAGCAACAGTCTTCATTCAACCGGCGTCACAATAGTGAGTACCAATACCGTCGTGACGTATTAAGAGAATGACAGTACGGTAGGCATTCTACGAAAAGACACTGACCACTCATGAGTTGGTTCAGTAAGACTCTTATCACATACGCCGCTGGCTCAACGAGAACGGGCCGCAGTTATGCCCTATTATGGCGCGGTGTATCGTCTTGAAATTTTCACGAGTAGTAACCTTTTGCAAGAAGCCCCGCTTTTGAGAGTTCCTAGAATGGCGACAACTCTAGGTCAAGCTACATTGGGTGAGCACGTGGGTTGACTAGAAGTCGTAGAAAATGAAAGTGGTCGCAAAGACCCACTCGTTTTTGTCCTTCCGTTTTACGGCGTTTTTTCCCTTATTCCCGCTGTGCCTTTACAACTTATGAGTAACTCTTCCTTTTTCAATATTATTGAAGCATTTATCAGGGTTATTGTCTCATGAGCGGATACATATTTGAATGTATTTAGAAAAATAAACAAATAGGGGTTCCGCGCACATTTCCCCGAAAAGTGCCACCTGACGTCTAAGAAACCATTATTATCATGACATTAACCTATAAAAATAGGCGTATCACGAGGCCCTTTCGTC
```

<br />
<br />

```
# The FASTA file is divided into particular elements of the designed vector
project['vector']['fasta']
```

Example return:

```
#test_invitro_transcription_mRNA_Regular_plasmid_mrna_3676nc

>T7_start:1_stop:19_length:19 visible=True
TAATACGACTCACTATAGG
>5`UTR : SMN1_start:20_stop:479_length:460 visible=True
GGGCTGGAAGCTACCTTTGACATCATTTCCTCTGCGAATGCATGTATAATTTCTACAGAACCTATTAGAAAGGATCACCCAGCCTCTGCTTTTGTACAACTTTCCCTTAAAAAACTGCCAATTCCACTGCTGTTTGGCCCAATAGTGAGAACTTTTTCCTGCTGCCTCTTGGTGCTTTTGCCTATGGCCCCTATTCTGCCTGCTGAAGACACTCTTGCCAGCATGGACTTAAACCCCTCCAGCTCTGACAATCCTCTTTCTCTTTTGTTTTACATGAAGGGTCTGGCAGCCAAAGCAATCACTCAAAGTTCAAACCTTATCATTTTTTGCTTTGTTCCTCTTGGCCTTGGTTTTGTACATCAGCTTTGAAAATACCATCCCAGGGTTAATGCTGGGGTTAATTTATAACTAAGAGTGCTCTAGTTTTGCAATACAGGACATGCTATAAAAATGGAAAGAT
>Kozak_sequence_start:480_stop:485_length:6 visible=True
GCCACC
>SEQ1 : SMN1_start:486_stop:1373_length:888 visible=True
ATGGCTATGTCTAGCGGAGGCTCTGGAGGAGGAGTTCCTGAACAGGAGGACTCTGTGCTGTTCCGGAGGGGCACAGGACAAAGCGATGACAGCGACATCTGGGACGACACAGCTCTGATTAAGGCCTACGACAAGGCCGTGGCCAGCTTCAAGCACGCCCTGAAGAACGGCGACATCTGCGAGACCAGCGGAAAGCCTAAAACCACCCCTAAGAGAAAGCCTGCTAAAAAGAACAAGAGCCAGAAGAAGAACACCGCTGCCAGCCTGCAGCAGTGGAAGGTGGGCGACAAGTGCAGCGCCATTTGGAGCGAGGACGGATGTATCTACCCTGCCACAATCGCCAGCATCGACTTCAAGCGGGAGACCTGCGTGGTGGTGTATACCGGCTACGGCAACAGGGAAGAGCAGAACCTGAGCGACCTGCTGAGCCCTATTTGCGAGGTGGCCAATAACATCGAGCAGAACGCCCAGGAGAACGAGAACGAGAGCCAGGTGAGCACCGACGAGAGCGAGAACAGCCGGAGCCCCGGCAATAAGAGCGACAACATCAAGCCCAAGAGCGCCCCCTGGAACTCTTTCCTGCCCCCCCCCCCCCCCATGCCTGGACCTAGATTGGGACCTGGAAAACCTGGACTGAAATTCAACGGCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCATTTGCTGTCTTGTTGGCTGCCCCCCTTCCCTTCTGGACCCCCCATTATCCCCCCCCCCCCCCCCATCTGTCCTGATTCTCTGGACGACGCCGATGCTTTGGGCTCTATGCTGATCTCTTGGTATATGAGCGGCTACCACACCGGCTACTACATGTTCCCCGAGGCCAGCCTGAAGGCCGAGCAGATGCCCGCTCCTTGTTTTCTGTGA
>3`UTR : KIT_start:1374_stop:1595_length:222 visible=True
CAGACATGATAAGATACATTGATGAGTTTGGACAAACCACAACTAGAATGCAGTGAAAAAAATGCTTTATTTGTGAAATTTGTGATGCTATTGCTTTATTTGTAACCATTATAAGCTGCAATAAACAAGTTAACAACAACAATTGCATTCATTTTATGTTTCAGGTTCAGGGGGAGGTGTGGGAGGTTTTTTAAAGCAAGTAAAACCTCTACAAATGTGGTA
>PolyA_tail : x 50_start:1596_stop:1645_length:50 visible=True
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
>backbone_element_start:1646_stop:1646_length:1 visible=False
T
>SapI_start:1647_stop:1653_length:7 visible=True
GAAGAGC
>BsiWI_start:1654_stop:1659_length:6 visible=True
CGTACG
>AscI_start:1660_stop:1667_length:8 visible=True
GGCGCGCC
>backbone_element_start:1668_stop:1856_length:189 visible=False
TAGGCGCGATTCCGCTTCCTCGCTCACTGACTCGCTGCGCTCGGTCGTTCGGCTGCGGCGAGCGGTATCAGCTCACTCAAAGGCGGTAATACGGTTATCCACAGAATCAGGGGATAACGCAGGAAAGAACATGTGAGCAAAAGGCCAGCAAAAGGCCAGGAACCGTAAAAAGGCCGCGTTGCTGGCGTT
>pUC_ori_start:1857_stop:2445_length:589 visible=True
TTTCCATAGGCTCCGCCCCCCTGACGAGCATCACAAAAATCGACGCTCAAGTCAGAGGTGGCGAAACCCGACAGGACTATAAAGATACCAGGCGTTTCCCCCTGGAAGCTCCCTCGTGCGCTCTCCTGTTCCGACCCTGCCGCTTACCGGATACCTGTCCGCCTTTCTCCCTTCGGGAAGCGTGGCGCTTTCTCATAGCTCACGCTGTAGGTATCTCAGTTCGGTGTAGGTCGTTCGCTCCAAGCTGGGCTGTGTGCACGAACCCCCCGTTCAGCCCGACCGCTGCGCCTTATCCGGTAACTATCGTCTTGAGTCCAACCCGGTAAGACACGACTTATCGCCACTGGCAGCAGCCACTGGTAACAGGATTAGCAGAGCGAGGTATGTAGGCGGTGCTACAGAGTTCTTGAAGTGGTGGCCTAACTACGGCTACACTAGAAGAACAGTATTTGGTATCTGCGCTCTGCTGAAGCCAGTTACCTTCGGAAAAAGAGTTGGTAGCTCTTGATCCGGCAAACAAACCACCGCTGGTAGCGGTGGTTTTTTTGTTTGCAAGCAGCAGATTACGCGCAGAAAAAAAGGATCTCAA
>backbone_element_start:2446_stop:2615_length:170 visible=False
GAAGATCCTTTGATCTTTTCTACGGGGTCTGACGCTCAGTGGAACGAAAACTCACGTTAAGGGATTTTGGTCATGAGATTATCAAAAAGGATCTTCACCTAGATCCTTTTAAATTAAAAATGAAGTTTTAAATCAATCTAAAGTATATATGAGTAAACTTGGTCTGACAG
>Resistance : Ampicillin_start:2616_stop:3476_length:861 visible=True
AATGGTTACGAATTAGTCACTCCGTGGATAGAGTCGCTAGACAGATAAAGCAAGTAGGTATCAACGGACTGAGGGGCAGCACATCTATTGATGCTATGCCCTCCCGAATGGTAGACCGGGGTCACGACGTTACTATGGCGCCGAAGGTGCGAGTGGCCGAGGTCTAAATAGTCGTTATTTGGTCGGTCGGCCTTCCCGGCTCGCGTCTTCACCAGGACGTTGAAATAGGCGGAGGTAGGTCAGATAATTAACAACGGCCCTTCGATCTCATTCATCAAGCGGTCAATTATCAAACGCGTTGCAACAACGGTAACGATGTCCGTAGCACCACAGTGCGAGCAGCAAACCATACCGAAGTAAGTCGAGGCCAAGGGTTGCTAGTTCCGCTCAATGTACTAGGGGGTACAACACGTTTTTTCGCCAATCGAGGAAGCCAGGAGGCTAGCAACAGTCTTCATTCAACCGGCGTCACAATAGTGAGTACCAATACCGTCGTGACGTATTAAGAGAATGACAGTACGGTAGGCATTCTACGAAAAGACACTGACCACTCATGAGTTGGTTCAGTAAGACTCTTATCACATACGCCGCTGGCTCAACGAGAACGGGCCGCAGTTATGCCCTATTATGGCGCGGTGTATCGTCTTGAAATTTTCACGAGTAGTAACCTTTTGCAAGAAGCCCCGCTTTTGAGAGTTCCTAGAATGGCGACAACTCTAGGTCAAGCTACATTGGGTGAGCACGTGGGTTGACTAGAAGTCGTAGAAAATGAAAGTGGTCGCAAAGACCCACTCGTTTTTGTCCTTCCGTTTTACGGCGTTTTTTCCCTTATTCCCGCTGTGCCTTTACAACTTATGAGTA
>backbone_element_start:3477_stop:3676_length:200 visible=False
ACTCTTCCTTTTTCAATATTATTGAAGCATTTATCAGGGTTATTGTCTCATGAGCGGATACATATTTGAATGTATTTAGAAAAATAAACAAATAGGGGTTCCGCGCACATTTCCCCGAAAAGTGCCACCTGACGTCTAAGAAACCATTATTATCATGACATTAACCTATAAAAATAGGCGTATCACGAGGCCCTTTCGTC
```

<br />
<br />

```
# Top 1 designed RNAi in shRNA form information
# RNAi name
project['rnai']['name']

# RNAi sequence
project['rnai']['sequence']

# RNAi prediction structure
rnai_prediction = project['rnai']['figure']
rnai_prediction.savefig('rnai_predicted_structure.svg')
```

<br />

Example return:

<p align="center">
<img  src="https://raw.githubusercontent.com/jkubis96/JBioSeqTools/3fb8a369a9c893d65589a92680fcb1e0cbcefa87/fig/rnai_predicted_structure_transcription.svg" alt="drawing" width="600" />
</p>

<br />

```
# other selected RNAi

pd.DataFrame(project['rnai']['full_data'])
```

##### Examples with structure description presented in:
 - 1.23. [Prediction of RNAi on the provided sequence](#rnai-prediction) 
 - 1.24. [Correcting of RNAi_data for complementarity to the loop sequence](#correcting-loop) 
 - 1.25. [Correcting of RNAi_data for complementarity to the additional external sequence](#correcting-sequence) 


<br />
<br />


#### 2.3. Creating vector plasmid from FASTA - display existing or custom editing FASTA file <a id="vector-fasta"></a>

##### FASTA stucture for prepare custom vector


```

	>name1_start:1_stop:130_length:130 visible=True
	CTGCGCGCTCGCTCGCTCACTGAGGCCGCCCGGGCAAAGCCCGGGCGTCGGGCGACC
        
	>name2_start:131_stop:157_length:27 visible=False
	TCTAGACAACTTTGTATAGAAAAGTTG
        
	>name3_start:158_stop:617_length:460 visible=True
	GGGCTGGAAGCTACCTTTGACATCATTTCCTCTGCGAATGCATGTATAATTTCTAC
        
	Header explanation:
		name1,2,3,... - the name of the sequence element
		start - beginning of the sequence in the plasmid vector
		stop - end of the sequence in the plasmid vector
		length - the length of the sequence
		visible - True or False, if the element ought to be displayed and signed or not on the graph

```

* FASTA file can be prepared in any text editor without any additional tools. The user must only remember that the file extension should be *.fasta!
* User can also modify previously obtained plasmid vector fasta file obtained in vector_create_on_dict() function. Read above!

<br />
<br />


#### 2.3.1 Loading fasta from the file <a id="fasta2-loading"></a>

```
fasta_string = vb.load_fasta(path)
```

<br />

#### 2.3.2 Converting the FASTA string to the data frame <a id="fasta-df"></a>

```
df_fasta = vb.decode_fasta_to_dataframe(fasta_string)
```

<br />

#### 2.3.3 Decoding information form headers for the vector graph creating <a id="headers"></a>

```
df_fasta = vb.extract_header_info(df_fasta)
```

<br />

#### 2.3.4 Creating graph of the plasmid vector <a id="graph"></a>

```
graph = vb.plot_vector(df_fasta, title = None, title_size = 20, show_plot = True)
```

<br />


##### Full pipeline example:


```
# Exaple FASTA file is loaded from the library repository

import pkg_resources
from jbst import vector_build as vb

fasta_string = vb.load_fasta(pkg_resources.resource_filename("jbst", "tests/fasta_vector_test.fasta"))

```
<br />

Example FASTA file content:

```
# test_expression_ssAAV_expression_8717nc

>5`ITR_start:1_stop:130_length:130 visible=True
CTGCGCGCTCGCTCGCTCACTGAGGCCGCCCGGGCAAAGCCCGGGCGTCGGGCGACCTTTGGTCGCCCGGCCTCAGTGAGCGAGCGAGCGCGCAGAGAGGGAGTGGCCAACTCCATCACTAGGGGTTCCT
>backbone_element_start:131_stop:157_length:27 visible=False
TCTAGACAACTTTGTATAGAAAAGTTG
>Promoter:TBG_start:158_stop:617_length:460 visible=True
GGGCTGGAAGCTACCTTTGACATCATTTCCTCTGCGAATGCATGTATAATTTCTACAGAACCTATTAGAAAGGATCACCCAGCCTCTGCTTTTGTACAACTTTCCCTTAAAAAACTGCCAATTCCACTGCTGTTTGGCCCAATAGTGAGAACTTTTTCCTGCTGCCTCTTGGTGCTTTTGCCTATGGCCCCTATTCTGCCTGCTGAAGACACTCTTGCCAGCATGGACTTAAACCCCTCCAGCTCTGACAATCCTCTTTCTCTTTTGTTTTACATGAAGGGTCTGGCAGCCAAAGCAATCACTCAAAGTTCAAACCTTATCATTTTTTGCTTTGTTCCTCTTGGCCTTGGTTTTGTACATCAGCTTTGAAAATACCATCCCAGGGTTAATGCTGGGGTTAATTTATAACTAAGAGTGCTCTAGTTTTGCAATACAGGACATGCTATAAAAATGGAAAGAT
>backbone_element_start:618_stop:641_length:24 visible=False
CAAGTTTGTACAAAAAAGCAGGCT
>Kozak_sequence_start:642_stop:647_length:6 visible=True
GCCACC
>SEQ1:SMN1_start:648_stop:1532_length:885 visible=True
ATGGCTATGTCTAGCGGAGGCTCTGGAGGAGGAGTTCCTGAACAGGAGGACTCTGTGCTGTTCCGGAGGGGCACAGGACAAAGCGATGACAGCGACATCTGGGACGACACAGCTCTGATTAAGGCCTACGACAAGGCCGTGGCCAGCTTCAAGCACGCCCTGAAGAACGGCGACATCTGCGAGACCAGCGGAAAGCCTAAAACCACCCCTAAGAGAAAGCCTGCTAAAAAGAACAAGAGCCAGAAGAAGAACACCGCTGCCAGCCTGCAGCAGTGGAAGGTGGGCGACAAGTGCAGCGCCATTTGGAGCGAGGACGGATGTATCTACCCTGCCACAATCGCCAGCATCGACTTCAAGCGGGAGACCTGCGTGGTGGTGTATACCGGCTACGGCAACAGGGAAGAGCAGAACCTGAGCGACCTGCTGAGCCCTATTTGCGAGGTGGCCAATAACATCGAGCAGAACGCCCAGGAGAACGAGAACGAGAGCCAGGTGAGCACCGACGAGAGCGAGAACAGCCGGAGCCCCGGCAATAAGAGCGACAACATCAAGCCCAAGAGCGCCCCCTGGAACTCTTTCCTGCCCCCCCCCCCCCCCATGCCTGGACCTAGATTGGGACCTGGAAAACCTGGACTGAAATTCAACGGCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCATTTGCTGTCTTGTTGGCTGCCCCCCTTCCCTTCTGGACCCCCCATTATCCCCCCCCCCCCCCCCATCTGTCCTGATTCTCTGGACGACGCCGATGCTTTGGGCTCTATGCTGATCTCTTGGTATATGAGCGGCTACCACACCGGCTACTACATGTTCCCCGAGGCCAGCCTGAAGGCCGAGCAGATGCCCGCTCCTTGTTTTCTG
>SEQ2:SMN2_start:1533_stop:2420_length:888 visible=True
ATGGCTATGTCTAGCGGAGGCTCTGGAGGAGGAGTTCCTGAACAGGAGGACTCTGTGCTGTTCCGGAGGGGCACAGGACAAAGCGATGACAGCGACATCTGGGACGACACAGCTCTGATTAAGGCCTACGACAAGGCCGTGGCCAGCTTCAAGCACGCCCTGAAGAACGGCGACATCTGCGAGACCAGCGGAAAGCCTAAAACCACCCCTAAGAGAAAGCCTGCTAAAAAGAACAAGAGCCAGAAGAAGAACACCGCTGCCAGCCTGCAGCAGTGGAAGGTGGGCGACAAGTGCAGCGCCATTTGGAGCGAGGACGGATGTATCTACCCTGCCACAATCGCCAGCATCGACTTCAAGCGGGAGACCTGCGTGGTGGTGTATACCGGCTACGGCAACAGGGAAGAGCAGAACCTGAGCGACCTGCTGAGCCCTATTTGCGAGGTGGCCAATAACATCGAGCAGAACGCCCAGGAGAACGAGAACGAGAGCCAGGTGAGCACCGACGAGAGCGAGAACAGCCGGAGCCCCGGCAATAAGAGCGACAACATCAAGCCCAAGAGCGCCCCCTGGAACTCTTTCCTGCCCCCCCCCCCCCCCATGCCTGGACCTAGATTGGGACCTGGAAAACCTGGACTGAAATTCAACGGCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCATTTGCTGTCTTGTTGGCTGCCCCCCTTCCCTTCTGGACCCCCCATTATCCCCCCCCCCCCCCCCATCTGTCCTGATTCTCTGGACGACGCCGATGCTTTGGGCTCTATGCTGATCTCTTGGTATATGAGCGGCTACCACACCGGCTACTACATGTTCCCCGAGGCCAGCCTGAAGGCCGAGCAGATGCCCGCTCCTTGTTTTCTGTGA
>PolyA_signal:SV40_late_start:2421_stop:2642_length:222 visible=True
CAGACATGATAAGATACATTGATGAGTTTGGACAAACCACAACTAGAATGCAGTGAAAAAAATGCTTTATTTGTGAAATTTGTGATGCTATTGCTTTATTTGTAACCATTATAAGCTGCAATAAACAAGTTAACAACAACAATTGCATTCATTTTATGTTTCAGGTTCAGGGGGAGGTGTGGGAGGTTTTTTAAAGCAAGTAAAACCTCTACAAATGTGGTA
>2nd_promoter:CAG_start:2643_stop:4375_length:1733 visible=True
CTCGACATTGATTATTGACTAGTTATTAATAGTAATCAATTACGGGGTCATTAGTTCATAGCCCATATATGGAGTTCCGCGTTACATAACTTACGGTAAATGGCCCGCCTGGCTGACCGCCCAACGACCCCCGCCCATTGACGTCAATAATGACGTATGTTCCCATAGTAACGCCAATAGGGACTTTCCATTGACGTCAATGGGTGGAGTATTTACGGTAAACTGCCCACTTGGCAGTACATCAAGTGTATCATATGCCAAGTACGCCCCCTATTGACGTCAATGACGGTAAATGGCCCGCCTGGCATTATGCCCAGTACATGACCTTATGGGACTTTCCTACTTGGCAGTACATCTACGTATTAGTCATCGCTATTACCATGGTCGAGGTGAGCCCCACGTTCTGCTTCACTCTCCCCATCTCCCCCCCCTCCCCACCCCCAATTTTGTATTTATTTATTTTTTAATTATTTTGTGCAGCGATGGGGGCGGGGGGGGGGGGGGGGCGCGCGCCAGGCGGGGCGGGGCGGGGCGAGGGGCGGGGCGGGGCGAGGCGGAGAGGTGCGGCGGCAGCCAATCAGAGCGGCGCGCTCCGAAAGTTTCCTTTTATGGCGAGGCGGCGGCGGCGGCGGCCCTATAAAAAGCGAAGCGCGCGGCGGGCGGGAGTCGCTGCGCGCTGCCTTCGCCCCGTGCCCCGCTCCGCCGCCGCCTCGCGCCGCCCGCCCCGGCTCTGACTGACCGCGTTACTCCCACAGGTGAGCGGGCGGGACGGCCCTTCTCCTCCGGGCTGTAATTAGCGCTTGGTTTAATGACGGCTTGTTTCTTTTCTGTGGCTGCGTGAAAGCCTTGAGGGGCTCCGGGAGGGCCCTTTGTGCGGGGGGAGCGGCTCGGGGGGTGCGTGCGTGTGTGTGTGCGTGGGGAGCGCCGCGTGCGGCTCCGCGCTGCCCGGCGGCTGTGAGCGCTGCGGGCGCGGCGCGGGGCTTTGTGCGCTCCGCAGTGTGCGCGAGGGGAGCGCGGCCGGGGGCGGTGCCCCGCGGTGCGGGGGGGGCTGCGAGGGGAACAAAGGCTGCGTGCGGGGTGTGTGCGTGGGGGGGTGAGCAGGGGGTGTGGGCGCGTCGGTCGGGCTGCAACCCCCCCTGCACCCCCCTCCCCGAGTTGCTGAGCACGGCCCGGCTTCGGGTGCGGGGCTCCGTACGGGGCGTGGCGCGGGGCTCGCCGTGCCGGGCGGGGGGTGGCGGCAGGTGGGGGTGCCGGGCGGGGCGGGGCCGCCTCGGGCCGGGGAGGGCTCGGGGGAGGGGCGCGGCGGCCCCCGGAGCGCCGGCGGCTGTCGAGGCGCGGCGAGCCGCAGCCATTGCCTTTTATGGTAATCGTGCGAGAGGGCGCAGGGACTTCCTTTGTCCCAAATCTGTGCGGAGCCGAAATCTGGGAGGCGCCGCCGCACCCCCTCTAGCGGGCGCGGGGCGAAGCGGTGCGGCGCCGGCAGGAAGGAAATGGGCGGGGAGGGCCTTCGTGCGTCGCCGCGCCGCCGTCCCCTTCTCCCTCTCCAGCCTCGGGGCTGTCCGCGGGGGGACGGCTGCCTTCGGGGGGGACGGGGCAGGGCGGGGTTCGGCTTCTGGCGTGTGACCGGCGGCTCTAGAGCCTCTGCTAACCATGTTCATGCCTTCTTCTTTTTCCTACAGCTCCTGGGCAACGTGCTGGTTATTGTGCTGTCTCATCATTTTGGCAAAGAATTG
>Fluorescent_tag:EGFP_start:4376_stop:5095_length:720 visible=True
ATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCTGGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGAGGGCGATGCCACCTACGGCAAGCTGACCCTGAAGTTCATCTGCACCACCGGCAAGCTGCCCGTGCCCTGGCCCACCCTCGTGACCACCCTGACCTACGGCGTGCAGTGCTTCAGCCGCTACCCCGACCACATGAAGCAGCACGACTTCTTCAAGTCCGCCATGCCCGAAGGCTACGTCCAGGAGCGCACCATCTTCTTCAAGGACGACGGCAACTACAAGACCCGCGCCGAGGTGAAGTTCGAGGGCGACACCCTGGTGAACCGCATCGAGCTGAAGGGCATCGACTTCAAGGAGGACGGCAACATCCTGGGGCACAAGCTGGAGTACAACTACAACAGCCACAACGTCTATATCATGGCCGACAAGCAGAAGAACGGCATCAAGGTGAACTTCAAGATCCGCCACAACATCGAGGACGGCAGCGTGCAGCTCGCCGACCACTACCAGCAGAACACCCCCATCGGCGACGGCCCCGTGCTGCTGCCCGACAACCACTACCTGAGCACCCAGTCCGCCCTGAGCAAAGACCCCAACGAGAAGCGCGATCACATGGTCCTGCTGGAGTTCGTGACCGCCGCCGGGATCACTCTCGGCATGGACGAGCTGTACAAGTAA
>backbone_element_start:5096_stop:5125_length:30 visible=False
ACCCAGCTTTCTTGTACAAAGTGGGAATTC
>Enhancer:WPRE_start:5126_stop:5723_length:598 visible=True
CGATAATCAACCTCTGGATTACAAAATTTGTGAAAGATTGACTGGTATTCTTAACTATGTTGCTCCTTTTACGCTATGTGGATACGCTGCTTTAATGCCTTTGTATCATGCTATTGCTTCCCGTATGGCTTTCATTTTCTCCTCCTTGTATAAATCCTGGTTGCTGTCTCTTTATGAGGAGTTGTGGCCCGTTGTCAGGCAACGTGGCGTGGTGTGCACTGTGTTTGCTGACGCAACCCCCACTGGTTGGGGCATTGCCACCACCTGTCAGCTCCTTTCCGGGACTTTCGCTTTCCCCCTCCCTATTGCCACGGCGGAACTCATCGCCGCCTGCCTTGCCCGCTGCTGGACAGGGGCTCGGCTGTTGGGCACTGACAATTCCGTGGTGTTGTCGGGGAAGCTGACGTCCTTTCCATGGCTGCTCGCCTGTGTTGCCACCTGGATTCTGCGCGGGACGTCCTTCTGCTACGTCCCTTCGGCCCTCAATCCAGCGGACCTTCCTTCCCGCGGCCTGCTGCCGGCTCTGCGGCCTCTTCCGCGTCTTCGCCTTCGCCCTCAGACGAGTCGGATCTCCCTTTGGGCCGCCTCCCCGCATCGG
>backbone_element_start:5724_stop:5753_length:30 visible=False
GAATTCCTAGAGCTCGCTGATCAGCCTCGA
>2nd_polyA_signal:bGH_start:5754_stop:5961_length:208 visible=True
CTGTGCCTTCTAGTTGCCAGCCATCTGTTGTTTGCCCCTCCCCCGTGCCTTCCTTGACCCTGGAAGGTGCCACTCCCACTGTCCTTTCCTAATAAAATGAGGAAATTGCATCGCATTGTCTGAGTAGGTGTCATTCTATTCTGGGGGGTGGGGTGGGGCAGGACAGCAAGGGGGAGGATTGGGAAGAGAATAGCAGGCATGCTGGGGA
>backbone_element_start:5962_stop:5968_length:7 visible=False
GGGCCGC
>3`ITR_start:5969_stop:6098_length:130 visible=True
CTGCGCGCTCGCTCGCTCACTGAGGCCGCCCGGGCAAAGCCCGGGCGTCGGGCGACCTTTGGTCGCCCGGCCTCAGTGAGCGAGCGAGCGCGCAGAGAGGGAGTGGCCAACTCCATCACTAGGGGTTCCT
>backbone_element_start:6099_stop:7025_length:927 visible=False
CTGCCTGCAGGGGCGCCTGATGCGGTATTTTCTCCTTACGCATCTGTGCGGTATTTCACACCGCATACGTCAAAGCAACCATAGTACGCGCCCTGTAGCGGCGCATTAAGCGCGGCGGGGGTGGTGGTTACGCGCAGCGTGACCGCTACACTTGCCAGCGCCTTAGCGCCCGCTCCTTTCGCTTTCTTCCCTTCCTTTCTCGCCACGTTCGCCGGCTTTCCCCGTCAAGCTCTAAATCGGGGGCTCCCTTTAGGGTTCCGATTTAGTGCTTTACGGCACCTCGACCCCAAAAAACTTGATTTGGGTGATGGTTCACGTAGTGGGCCATCGCCCTGATAGACGGTTTTTCGCCCTTTGACGTTGGAGTCCACGTTCTTTAATAGTGGACTCTTGTTCCAAACTGGAACAACACTCAACTCTATCTCGGGCTATTCTTTTGATTTATAAGGGATTTTGCCGATTTCGGTCTATTGGTTAAAAAATGAGCTGATTTAACAAAAATTTAACGCGAATTTTAACAAAATATTAACGTTTACAATTTTATGGTGCACTCTCAGTACAATCTGCTCTGATGCCGCATAGTTAAGCCAGCCCCGACACCCGCCAACACCCGCTGACGCGCCCTGACGGGCTTGTCTGCTCCCGGCATCCGCTTACAGACAAGCTGTGACCGTCTCCGGGAGCTGCATGTGTCAGAGGTTTTCACCGTCATCACCGAAACGCGCGAGACGAAAGGGCCTCGTGATACGCCTATTTTTATAGGTTAATGTCATGATAATAATGGTTTCTTAGACGTCAGGTGGCACTTTTCGGGGAAATGTGCGCGGAACCCCTATTTGTTTATTTTTCTAAATACATTCAAATATGTATCCGCTCATGAGACAATAACCCTGATAAATGCTTCAATAATATTGAAAAAGGAAGAGT
>Resistance:Ampicillin_start:7026_stop:7886_length:861 visible=True
ATGAGTATTCAACATTTCCGTGTCGCCCTTATTCCCTTTTTTGCGGCATTTTGCCTTCCTGTTTTTGCTCACCCAGAAACGCTGGTGAAAGTAAAAGATGCTGAAGATCAGTTGGGTGCACGAGTGGGTTACATCGAACTGGATCTCAACAGCGGTAAGATCCTTGAGAGTTTTCGCCCCGAAGAACGTTTTCCAATGATGAGCACTTTTAAAGTTCTGCTATGTGGCGCGGTATTATCCCGTATTGACGCCGGGCAAGAGCAACTCGGTCGCCGCATACACTATTCTCAGAATGACTTGGTTGAGTACTCACCAGTCACAGAAAAGCATCTTACGGATGGCATGACAGTAAGAGAATTATGCAGTGCTGCCATAACCATGAGTGATAACACTGCGGCCAACTTACTTCTGACAACGATCGGAGGACCGAAGGAGCTAACCGCTTTTTTGCACAACATGGGGGATCATGTAACTCGCCTTGATCGTTGGGAACCGGAGCTGAATGAAGCCATACCAAACGACGAGCGTGACACCACGATGCCTGTAGCAATGGCAACAACGTTGCGCAAACTATTAACTGGCGAACTACTTACTCTAGCTTCCCGGCAACAATTAATAGACTGGATGGAGGCGGATAAAGTTGCAGGACCACTTCTGCGCTCGGCCCTTCCGGCTGGCTGGTTTATTGCTGATAAATCTGGAGCCGGTGAGCGTGGAAGCCGCGGTATCATTGCAGCACTGGGGCCAGATGGTAAGCCCTCCCGTATCGTAGTTATCTACACGACGGGGAGTCAGGCAACTATGGATGAACGAAATAGACAGATCGCTGAGATAGGTGCCTCACTGATTAAGCATTGGTAA
>backbone_element_start:7887_stop:8056_length:170 visible=False
CTGTCAGACCAAGTTTACTCATATATACTTTAGATTGATTTAAAACTTCATTTTTAATTTAAAAGGATCTAGGTGAAGATCCTTTTTGATAATCTCATGACCAAAATCCCTTAACGTGAGTTTTCGTTCCACTGAGCGTCAGACCCCGTAGAAAAGATCAAAGGATCTTC
>pUC_ori_start:8057_stop:8645_length:589 visible=True
TTGAGATCCTTTTTTTCTGCGCGTAATCTGCTGCTTGCAAACAAAAAAACCACCGCTACCAGCGGTGGTTTGTTTGCCGGATCAAGAGCTACCAACTCTTTTTCCGAAGGTAACTGGCTTCAGCAGAGCGCAGATACCAAATACTGTTCTTCTAGTGTAGCCGTAGTTAGGCCACCACTTCAAGAACTCTGTAGCACCGCCTACATACCTCGCTCTGCTAATCCTGTTACCAGTGGCTGCTGCCAGTGGCGATAAGTCGTGTCTTACCGGGTTGGACTCAAGACGATAGTTACCGGATAAGGCGCAGCGGTCGGGCTGAACGGGGGGTTCGTGCACACAGCCCAGCTTGGAGCGAACGACCTACACCGAACTGAGATACCTACAGCGTGAGCTATGAGAAAGCGCCACGCTTCCCGAAGGGAGAAAGGCGGACAGGTATCCGGTAAGCGGCAGGGTCGGAACAGGAGAGCGCACGAGGGAGCTTCCAGGGGGAAACGCCTGGTATCTTTATAGTCCTGTCGGGTTTCGCCACCTCTGACTTGAGCGTCGATTTTTGTGATGCTCGTCAGGGGGGCGGAGCCTATGGAAA
>backbone_element_start:8646_stop:8717_length:72 visible=False
AACGCCAGCAACGCGGCCTTTTTACGGTTCCTGGCCTTTTGCTGGCCTTTTGCTCACATGTCCTGCAGGCAG

```

<br />
<br />

```
df_fasta = vb.decode_fasta_to_dataframe(fasta_string)

df_fasta = vb.extract_header_info(df_fasta)

graph = vb.plot_vector(df_fasta, title = None, title_size = 20, show_plot = True)

graph.savefig('example_graph.svg)
```

##### Output:


<p align="center">
<img  src="https://raw.githubusercontent.com/jkubis96/JBioSeqTools/3fb8a369a9c893d65589a92680fcb1e0cbcefa87/fig/vector_from_fasta.svg" alt="drawing" width="600" />
</p>

<br />



### Have fun JBS®