# Trajectory-derived data

Trajectories themselves are not in this repository — the System B production `.xtc` alone is
about 11 GB. What is here are the analysis outputs computed from them, in GROMACS `.xvg` form,
with each file's original command line preserved in its header. Machine-specific paths in those
headers have been replaced with `<CONDA_PREFIX>` and `<WORKDIR>` placeholders; nothing else in
the headers was altered.

## `system_B/` — reducing, cytoplasm-like state

Two free cysteines instead of the Cys62–Cys74 disulfide. Rhombic dodecahedral cell, 150,984
atoms, 100 ns production, analysis window 70–100 ns.

| File | Contents |
| :- | :- |
| `B_prod_rmsf.xvg` | Per-residue Cα RMSF, all 403 residues, 70–100 ns. This is the full 403-value file the Supplementary Materials inventory promises. |
| `B_prod_rmsd.xvg` | Protein-group RMSD, whole run. |
| `reduced_bb_rmsd.xvg` | Backbone-group RMSD, whole run. The correct, `.tpr`-referenced, PBC-corrected series. |
| `B_prod_rg.xvg` | Radius of gyration. |
| `sgsg_70_100.xvg` | Cys62–Cys74 SG–SG distance over 70–100 ns; the series Figure 5 and Figure 7 are drawn from. |
| `hbond_70_100.xvg` | Intra-protein hydrogen bond count, 70–100 ns. |
| `dssp_num_70_100.xvg` | DSSP secondary-structure counts, 70–100 ns. |

## `system_B_check_run_RETRACTED/` — do not quote

The 100 ps check run that preceded production. Retracted and superseded material only, kept
labelled rather than deleted. See the README in that directory and `../docs/RETRACTIONS.md`.

## System A — oxidizing, periplasm-like state

Cys62–Cys74 disulfide present throughout, detected automatically by `pdb2gmx` from an SG–SG
separation of 0.195 nm. Cubic cell, 213,010 atoms, 90 ns production, analysis window 70–90 ns.

**No System A data files are in this repository.** Its production per-residue RMSF file was not
retained and no longer exists; its 90 ns production log and run input remain on the team
machines and have not reached this repository. The System A numbers quoted on the wiki page and
hard-coded in `scripts/make_figs.py` are from those runs, but the files behind them are not
here to check against. See the "Files that no longer exist" section of the top-level README.

Because the two cells differ in shape and size, only protein-centred quantities are ever
compared between System A and System B, never cell-dependent ones.
