# AutoDock Vina runs for the C2-52 models

Vina's own `.log` files were written on the machine the docking ran on and did not reach this
repository. What is here are the values transcribed from those logs at the time, in
`vina_results.md`, together with the full run configuration, so the numbers on the wiki page
can be traced to the run that produced them and a reproduction can use the same box.

The first docking attempt is included and is marked DISCARDED. It is kept because the mistake
it contains — a docking box inherited from a different model's coordinate frame — is one of the
self-corrections the Modeling page reports, and a reader should be able to see what the wrong
numbers were rather than take the correction on trust.
