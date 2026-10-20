# Figures

The twenty figures of the Modeling page, at the numbering the page uses, as 300 dpi PNG; six of
them also as vector PDF where one was produced. `Figure_NN_title` is the same naming used in
the team's Drive folder, so a figure can be matched between the two without opening it.

`scripts/make_figs.py` and `scripts/fig1_v2.py` regenerate them. Several panels are drawn from
values hard-coded in those scripts rather than from a data file, because the file they were
computed from is not in this repository; the script says so at each such block.

## One figure carries retracted values

`Figure_06_sgsg_occupancy_checkrun_superseded.png` is **superseded for System B**. The System B
occupancy values drawn on it — 7.9 / 24.8 / 31.7 / 74.3% of frames within 3.5 / 4.0 / 4.5 /
5.0 A, mean 4.55 A, median 4.75 A, range 3.23-5.48 A — came from a 100 ps check run, not from a
production trajectory. They are retracted and must not be quoted.
`Figure_07_sgsg_occupancy_production.png` recomputes every one of them on the System B
70-100 ns production trajectory and replaces them. The System A line on Figure 6 (100.00% of
frames within 3.0 A, mean 2.04 A) is production data and stands. The figure is kept rather than
deleted so that the correction stays visible. See `../docs/RETRACTIONS.md`.

`Figure_04_rmsd_summaries.png` deliberately omits the withdrawn 10.11 A and 14.30 A RMSD
values; they are not missing by accident.

Nothing in these figures is a wet-lab measurement.
