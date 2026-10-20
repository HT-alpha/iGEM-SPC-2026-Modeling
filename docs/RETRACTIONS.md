# Retracted and withdrawn numbers

Two groups of numbers from this project were published, then withdrawn. They are listed here
so that nobody picks them out of a raw file and quotes them in good faith. Both the files and
the figures that carry them are kept rather than deleted, each one labelled in place.

## 1. The 10.11 Å and 14.30 Å backbone RMSD figures — WITHDRAWN

Where they came from: `gmx rms` run against a `.gro` file instead of a run input (`.tpr`), on
the 100 ps check run, with no periodic-boundary handling and masses guessed from residue names.

Why they are wrong: re-measuring the same trajectory against a different `.gro` moved the
"result" from about 10 Å to 23.87 Å. Changing only the reference file moved the number by
roughly 14 Å, which identifies the quantity as periodic-image displacement rather than
conformational change. A protein that had genuinely travelled 24 Å would be unfolded, and the
hydrogen-bond, DSSP and radius-of-gyration data say plainly that it was not. Measured properly
on the PBC-centred trajectory, the same check run peaks at 0.139 nm.

Where they are labelled: `data/system_B_check_run_RETRACTED/` — a RETRACTED header is prepended
to each affected `.xvg`, and the directory README gives the file-by-file status.

The rule that came out of this and is enforced in every script here: **never reference
`gmx rms` to a `.gro` file. Use the `.tpr`, and centre the trajectory first.**

The figure that replaces them is `figures/Figure_04_rmsd_summaries.png`, which uses the
production System A and System B series and deliberately omits the withdrawn values.

## 2. The Figure 6 System B SG–SG occupancy values — RETRACTED

The values: 7.9 / 24.8 / 31.7 / 74.3% of frames within 3.5 / 4.0 / 4.5 / 5.0 Å, mean 4.55 Å,
median 4.75 Å, range 3.23–5.48 Å.

Why they are withdrawn: they were computed on the 100 ps check run, not on a production
trajectory, and were mistaken for production numbers. Figure 7 recomputes every one of them on
the System B 70–100 ns production trajectory and replaces them.

What survives: the System A line in the same figure — 100.00% of frames within 3.0 Å, mean
2.04 Å — is from the production trajectory and stands. So does the conclusion the figure was
drawn to make, which is cutoff-insensitive in both versions: the disulfide is binary, either
held or permanently lost.

Where they are labelled: `figures/README.md`, and in `scripts/make_figs.py` directly above the
block that hard-codes them.

## Scope note

Nothing in this repository is a wet-lab measurement. The ScyE expression arm never produced a
confirmed band and none of the designed sequences were synthesised, so no claim here is
experimentally validated. What is validated is the pipeline, not the designs.
