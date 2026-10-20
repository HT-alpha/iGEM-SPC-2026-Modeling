# Design constraint files

These are the files that told the sequence generators which residues they were not allowed to
change. They are in the repository because the Modeling page's own argument is that losing one
small constraint file cost us the ability to say what our candidates were allowed to vary, and
the fix for that is to publish the constraint files rather than describe them.

| File | Bytes | What it is |
| :- | :- | :- |
| `frozen_core_21_cycle1.txt` | 80 | The 21 residues actually held fixed in Cycle 1, comma-separated, no trailing newline. |
| `frozen_core_52.txt` | 196 | All 52 Pocket 1 residues the MD returned as rigid; the Cycle 2 (C2-52) core. Comma-separated, no trailing newline. |
| `fixed_positions_52_plus_tags397.regenerated.jsonl` | 387 | The 81 positions handed to ProteinMPNN for the accepted C2-52 run: the 52 pocket residues, plus 1–22 (signal peptide), plus 397, plus 398–403 (His6 tag). |

## Read this about the JSONL

The 81-position JSONL in this directory is **regenerated from its recorded definition**, not a
copy of the original file. The original was written on the team machine and is not on the
machine this repository was assembled from. It is reconstructed here from the two things that
were recorded: the 52-residue pocket list above, and the stated composition
`52 pocket + 1-22 + 397 + 398-403 = 81 positions`. The regenerated file is 387 bytes, which is
the byte count recorded for the original, and it asserts 81 positions on write — but it is a
reconstruction and is named so, and anyone reproducing the run should regenerate it through
ProteinMPNN's own `helper_scripts/make_fixed_positions_dict.py` against their own
`parsed_pdbs.jsonl` rather than trusting this copy's key name.

Position 397 is in the list for a reason worth keeping: in the run where only 80 positions were
fixed, the designs put a seventh histidine at the C-terminus, because native position 397 is a
serine and the model preferred H next to the tag. Fixing 397 stopped it.

`scripts/c2_52_setup.sh` writes `frozen_core_52.txt` and `frozen_core_21.txt` from scratch and
runs the numbering gates that must pass before any sequence is generated; the script refuses to
proceed on a FAIL.
