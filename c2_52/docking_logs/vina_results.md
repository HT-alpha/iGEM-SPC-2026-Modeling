# AutoDock Vina — C2-52 re-docking, transcribed results

Ligand: scytonemin monomer, `monomer.pdbqt`, 23 atoms.
Receptor preparation: MGLTools 1.5.7 `prepare_receptor4.py -A hydrogens`.
Vina: Windows build 1.2.7, invoked from WSL.
Box in every run below: 22 x 22 x 22 A, exhaustiveness 16, num_modes 20, energy_range 4 —
identical to the Cycle 1 `config_C2_39.txt`, so the two cycles stay comparable.

-----

## Run 1 — DISCARDED. Box in the wrong place. DO NOT QUOTE THESE NUMBERS.

This run reused Cycle 1's box centre, (7.452961543910214, 1.3470321535975596,
-11.22630990652119), which was defined on C2_39's coordinate frame. The pocket centres of the
C2-52 models sit near x = -6.9 to -4.7, so the box was not over the pocket at all. The scores
below are an artefact of that misplacement and are recorded only so the correction is visible.

| Model | Score (kcal/mol) | Status |
| :- | :- | :- |
| C2_52_1 | -4.866 | DISCARDED |
| C2_52_2 | -7.444 | DISCARDED |
| C2_52_3 | -8.236 | DISCARDED |

-----

## Run 2 — corrected. Each model docked in a box centred on its own pocket centroid.

| Model | Top score (kcal/mol) | Box centre (A) | Next-best modes |
| :- | :- | :- | :- |
| C2_52_1 | -7.89 | -6.857, 0.271, -13.910 | -7.64 / -7.11 / -6.999 |
| C2_52_2 | -8.182 | -6.376, -1.503, -14.786 | -8.111 / -7.905 / -7.805 |
| C2_52_3 | -7.861 | -4.697, 0.086, -15.036 | -7.641 / -7.578 / -7.438 |

Caveat that belongs with these numbers: the 52 pocket residues span 32-35 A, which is wider
than the 22 A box, so the pocket centroid is not a tight cavity. The 22 A box was kept anyway,
for comparability with Cycle 1, and that choice has to be stated wherever the scores are.

## Native control, on equal footing — same ligand, same box size, own pocket centre

| Receptor | Top score (kcal/mol) | Box centre (A) | Next-best modes |
| :- | :- | :- | :- |
| scyE_clean (parent) | -9.55 | 6.007, -1.311, 12.644 | -9.253 / -9.217 / -9.079 |

The parent scores -9.55 and the designs -7.86 to -8.18, so all three dock 1.4-1.7 kcal/mol
more weakly than the native enzyme. Nothing here supports a claim that the designs bind
scytonemin as well as ScyE does. Cycle 1's C2_39 (-10.68 against a native pose of -9.71) is
not a clean comparison with these numbers: different receptor frame, recomputed box centre.

## Pocket-contact check on the top pose — the decisive step

Pocket residues (of the 52) with any atom within 4.5 A of any atom of the top docked pose:

| Receptor | Contacts | Residues |
| :- | :- | :- |
| C2_52_1 | 15 of 52 | 65, 67, 68, 71, 102, 108, 130, 179, 181, 183, 197, 198, +3 more |
| C2_52_2 | 5 of 52 | 71, 319, 323, 328, 376 |
| C2_52_3 | 11 of 52 | 36, 108, 130, 183, 251, 266, 268, 271, 299, 314, 359 |
| scyE_clean | 14 of 52 | 65, 66, 67, 73, 108, 130, 183, 249, 251, 266, 299, 314, +2 more |

C2_52_2 has the best-looking raw score and only five pocket contacts, in a different region of
the protein: it is a surface pose and must not be ranked first. Ranked by pocket engagement the
order is C2_52_1 > C2_52_3 > C2_52_2, the reverse of the raw-score order. The per-receptor
contact sets are in `../contact_sets.json`.
