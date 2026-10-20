# Cycle 1 ProteinMPNN output

`proteinmpnn_cycle1_scyE_clean_60seqs.fa` is the full generator output from Cycle 1: the native
sequence as entry 1, then 60 designs of 403 residues, twenty each at sampling temperatures 0.1,
0.2 and 0.3. Headers carry ProteinMPNN's own score, global score and sequence recovery. Model
`v_48_020`, git hash 8907e6671bfbfc92303b5f79c4b5e6ce47cdef57, seed 37; 60 sequences generated
in 99.6575 s.

Two of these are the candidates the wiki page names: C2_39 is `T=0.2, sample=18` and C2_50 is
`T=0.3, sample=9`, counting the native header as entry 1.

This is the Cycle 1 run, which held only the 21-residue frozen core fixed, not the 81 positions
of Cycle 2. It is included because it is the generator output that actually survives in a
readable form. **The equivalent 60-sequence file for the accepted C2-52 run
(`proteinmpnn_output_C2_52_final/seqs/scyE_clean.fa`) is not in this repository** — see the
"Files that were not retained" section of the top-level README. What survives from that run is
the top-10 shortlist in `../c2_52/C2_52_shortlist_top10.fa` and the run statistics in
`../c2_52/RESULTS_2026-10-19.md`.

The sequences were recovered from a terminal transcript, so the file is a transcription rather
than the original output file, and the leading proline-rich stretches in the designs are real:
Cycle 1 did not fix the signal peptide or the tag, which is exactly the failure that led to the
81-position constraint used in Cycle 2.
