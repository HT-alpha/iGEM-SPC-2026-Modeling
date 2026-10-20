# ScyE computational redesign — code, constraint files and analysis data

BioAegis / BioScyde, St. Paul's College, Hong Kong. iGEM 2026.

This repository holds the material behind the Modeling pages of our wiki: the molecular
dynamics analysis outputs, the design-constraint files, the Cycle 2 (C2-52) design and docking
artefacts, the scripts that draw every figure, and the figures themselves. It exists so that
anyone reading the page can open the file a number came from instead of taking the number on
trust, and so the next team can re-run what we ran.

**What the project is.** ScyE carries out the final oxidative dimerisation step in scytonemin
biosynthesis, in the cyanobacterial periplasm. We simulated the enzyme in two redox states to
decide whether the compartment is a real design variable, used the per-residue flexibility from
those simulations to decide which residues a redesign may not touch, and then redesigned the
rest with ProteinMPNN, folded the best candidates with ESMFold and docked them against the
scytonemin monomer.

**What this is not.** There is no wet-lab validation here, of anything. The ScyE expression arm
never produced a confirmed band, and none of the designed sequences was ever synthesised. What
the work validates is the pipeline — a method that recovers a known fold to 1.37 Å and rejects
two wrong fold families at 7-8 Å — not the designs. Every docking score, pLDDT and RMSD in this
repository is a computational prediction.

-----

## The two simulated systems

Everything in `data/`, and most of the figures, refers to one of two molecular dynamics runs.
They were built from the same prepared structure, `scyE_clean.pdb`, the 403-residue construct
we cloned, signal peptide at 1-22 and His6 tag at 398-403. The only intended difference between
them is one bond.

**System A — oxidizing, periplasm-like.** The Cys62-Cys74 disulfide is present for the whole
run; `pdb2gmx` detected it automatically from an SG-SG separation of 0.195 nm. Cubic cell,
213,010 atoms, 90 ns production, analysed over the 70-90 ns window. This is ScyE as it would be
after export to the periplasm.

**System B — reducing, cytoplasm-like.** The same structure built with disulfide detection
switched off after moving the two SG atoms to 3.5 Å apart, so the protein carries two free
thiols. Rhombic dodecahedral cell, 150,984 atoms, 100 ns production, analysed over 70-100 ns.
This is ScyE as it would sit in the cytoplasm.

Because the two cells differ in shape and size, only protein-centred quantities are ever
compared between A and B — never cell-dependent ones.

-----

## Layout

```
.
├── README.md
├── LICENSE                      MIT
├── .gitignore
├── docs/
│   └── RETRACTIONS.md           the withdrawn numbers, where they came from, why
├── data/
│   ├── README.md
│   ├── system_B/                production .xvg analysis outputs, 70-100 ns
│   └── system_B_check_run_RETRACTED/   100 ps check run; retracted material only
├── design/
│   ├── README.md
│   ├── frozen_core_21_cycle1.txt
│   ├── frozen_core_52.txt
│   └── fixed_positions_52_plus_tags397.regenerated.jsonl
├── cycle1/
│   ├── README.md
│   └── proteinmpnn_cycle1_scyE_clean_60seqs.fa
├── c2_52/
│   ├── RESULTS_2026-10-19.md    every Cycle 2 number, as transcribed from the runs
│   ├── C2_52_shortlist_top10.fa
│   ├── contact_sets.json
│   ├── models/                  three ESMFold predictions
│   ├── receptors/               parent structure and the .pdbqt receptors docked
│   └── docking_logs/            Vina runs, including the discarded first attempt
├── figures/
│   ├── README.md
│   └── Figure_01..20            300 dpi PNG, six also as PDF
└── scripts/
    ├── make_figs.py             draws Figures 2-12, 14, 17
    ├── fig1_v2.py               draws Figure 1, the pipeline schematic
    ├── analyze_c2_52.py         pocket RMSD, pocket extent, 4.5 Å contact sets
    └── c2_52_setup.sh           writes the frozen-core files and runs the numbering gates
```

### Which run each data file came from

Every file in `data/system_B/` is from the System B 100 ns production trajectory, computed over
the 70-100 ns window unless the GROMACS command line in its own header says otherwise; those
headers are preserved in each `.xvg`, with machine paths replaced by placeholders.
`B_prod_rmsf.xvg` is the full 403-value per-residue Cα RMSF file the Supplementary Materials
inventory promises. `sgsg_70_100.xvg` is the Cys62-Cys74 SG-SG distance series that Figures 5
and 7 are drawn from; `hbond_70_100.xvg` and `dssp_num_70_100.xvg` are the hydrogen-bond and
secondary-structure counts over the same window; `reduced_bb_rmsd.xvg` is the correct,
`.tpr`-referenced, PBC-corrected backbone RMSD for the whole run.

Everything in `data/system_B_check_run_RETRACTED/` is from the 100 ps check run that preceded
production. None of it is a result. It is kept, labelled, because the corrections the wiki page
makes have to be traceable to actual files.

`c2_52/` is the Cycle 2 design round of 2026-10-18 to 2026-10-19: ProteinMPNN with 81 positions
fixed, ESMFold on the top three, AutoDock Vina against the scytonemin monomer. `cycle1/` is the
earlier Cycle 1 generator output, which fixed only 21 residues.

-----

## Retracted material — read before quoting any number

Two sets of numbers were published and then withdrawn. Both are labelled in place rather than
deleted, so the correction stays visible; `docs/RETRACTIONS.md` has the full account.

1. **The 10.11 Å and 14.30 Å backbone RMSD values are withdrawn.** They came from `gmx rms`
   referenced to a `.gro` file instead of a run input, on the check run, with no periodic
   boundary handling, so they measure periodic-image displacement and not conformational
   change. Re-measuring the same trajectory properly peaks at 0.139 nm. The affected `.xvg`
   files each carry a RETRACTED header; `figures/Figure_04_rmsd_summaries.png` omits the values
   deliberately. The rule that came out of it: never reference `gmx rms` to a `.gro`, use the
   `.tpr`, and centre the trajectory first.

2. **The Figure 6 System B SG-SG occupancy values are retracted.** 7.9 / 24.8 / 31.7 / 74.3% of
   frames within 3.5 / 4.0 / 4.5 / 5.0 Å, mean 4.55 Å, median 4.75 Å, range 3.23-5.48 Å — all
   computed on the 100 ps check run and mistaken for production numbers.
   `Figure_07_sgsg_occupancy_production.png` recomputes them on the 70-100 ns production
   trajectory and supersedes every one. The System A line on Figure 6 is production data and
   stands. `scripts/make_figs.py` carries a RETRACTED comment directly above the block that
   hard-codes the values.

Separately: the first AutoDock Vina run on the C2-52 models is marked DISCARDED in
`c2_52/docking_logs/vina_results.md`. Its box was centred on a different model's coordinate
frame, so its scores are meaningless. They are kept visible rather than quietly dropped.

-----

## Files that were not retained

The wiki's Supplementary Materials section names several files it cannot supply, and the same
gaps apply here. Nothing below has been reconstructed or estimated.

- **System A's production per-residue Cα RMSF file was not retained and no longer exists.**
  This is why there is no `data/system_A/` directory. The System A values quoted on the page
  and hard-coded in `scripts/make_figs.py` come from that run, but the file behind them cannot
  be checked.
- **System A's 90 ns production log and its run input** remain on the team machines and have
  not reached this repository.
- **The two backed-up `.mdp` files** likewise remain on the team machines and are not here.
- **The check-run per-residue RMSF file** — the one the frozen core was originally defined
  from — was not retained either.
- **The 60-sequence ProteinMPNN output for the accepted C2-52 run**
  (`proteinmpnn_output_C2_52_final/seqs/scyE_clean.fa`) is not here; what survives of that run
  is the top-10 shortlist and the recorded statistics. The 60 sequences in `cycle1/` are from
  Cycle 1, a different and earlier run, and are labelled as such.
- **Vina's own `.log` files** were not retained; the scores and configurations transcribed from
  them at the time are in `c2_52/docking_logs/vina_results.md`.

Two optional values were absent from the output we received and are not estimated here: the
standard deviations on System B's production temperature and density, and the whole-run
backbone RMSD minimum and maximum for System B.

Trajectories are not in this repository at all, and never will be — the System B production
`.xtc` alone is about 11 GB. They stay on the lab machine and a backup drive.

-----

## Environment

| | |
| :- | :- |
| MD engine | GROMACS 2026.3, conda-forge CUDA build, AVX2_256 binary |
| Force field / water | AMBER99SB-ILDN / SPC/E |
| Analysis | `gmx rms, rmsf, gyrate, hbond, dssp, covar, anaeig, trjconv, distance`; MDAnalysis; NumPy; Matplotlib; DSSP 4.2.2 |
| Design | ProteinMPNN `v_48_020`, git `8907e6671bfbfc92303b5f79c4b5e6ce47cdef57`, seed 37 |
| Structure prediction | ESMFold, `esmfold_v1` weights, torch 2.8.0+cu128 |
| Docking | AutoDock Vina 1.2.7; receptors prepared with MGLTools 1.5.7 `prepare_receptor4.py -A hydrogens` |

Absolute paths, usernames and machine names have been removed from every file in this
repository; GROMACS headers show `<CONDA_PREFIX>` and `<WORKDIR>` placeholders where the
original path was.

-----

## Licence and citation

Code is under the MIT licence (see `LICENSE`). Figures and documentation are under CC BY 4.0.
Cite as: BioAegis / BioScyde (St. Paul's College), iGEM 2026, *Redesigning ScyE:
two-environment molecular dynamics and a wet-lab-independent validation design*. If you run any
of the experiments the page proposes, please tell us what happened — including if it failed.
