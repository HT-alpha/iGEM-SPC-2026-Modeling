# System B 100 ps check run — retracted and superseded material

Nothing in this directory is a result. It is the short 100 ps check run that was done
before the System B production simulation, kept so the corrections made on the wiki page
can be traced back to the actual files.

| File | What it is | Status |
| :- | :- | :- |
| `B_check_rmsd_gro.xvg` | Backbone RMSD referenced to `reduced_solv_minimized.gro` | **RETRACTED.** Source of the withdrawn 14.30 Å figure (its maximum is 1.4304 nm). PBC artefact. |
| `B_check_rmsd_nptref.xvg` | Backbone RMSD referenced to `reduced_npt.gro` | **RETRACTED.** Same fault, different reference file; this is the comparison that exposed it. |
| `B_check_ca_rmsd.xvg` | Cα RMSD referenced to `reduced_npt.gro` | **RETRACTED.** Same fault. |
| `B_check_ca_rmsd_fixed.xvg` | Cα RMSD on the PBC-centred check trajectory | Not retracted, but still the 100 ps check run, not production. Shown only as the control that demonstrates the artefact: the same trajectory measured properly peaks at 0.139 nm, not 1.43 nm. |
| `B_check_temp.xvg`, `B_check_PDpV.xvg` | Thermostat / pressure diagnostics for the check run | Diagnostics only, never reported as results. |

The withdrawn **10.11 Å** and **14.30 Å** RMSD numbers both came from this family of
`.gro`-referenced check-run measurements. They must not be quoted. The production System B
backbone RMSD is in `../system_B/reduced_bb_rmsd.xvg`.

The SG–SG occupancy values that were computed from this check run — 7.9 / 24.8 / 31.7 / 74.3%
within 3.5 / 4.0 / 4.5 / 5.0 Å, mean 4.55 Å, median 4.75 Å, range 3.23–5.48 Å — are also
retracted. They appear in `figures/Figure_06_sgsg_occupancy_checkrun_superseded.png` and are
replaced by Figure 7, recomputed on the 70–100 ns production trajectory.

The per-residue RMSF file that the frozen core was originally defined from also belongs to
this check run. It was not retained and is not in this repository.
