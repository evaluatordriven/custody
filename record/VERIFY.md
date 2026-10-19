# Checking the v0.9.3 record

Check it against the release, not the latest version: `git checkout v0.9.3`, then

    python3 checker/check.py record/custody-v0.9.3.json --files . --bar record/BAR-AMENDMENT-1.md

Without more, it reads `NOT-CHECKABLE` on one requirement, CL1-15: the files that show what the four
reader models and the cold implementer actually returned. Those files hold answers to test cases that
later versions reuse, so they are not public. The Owner keeps them and can produce them on request; a
verifier who has them passes `--evidence DIR` as well.

The CI run at the v0.9.3 tag failed because its quickstart step left out `--bar`. The fix came in the
next commit on `main` and changes nothing the record covers except that CI file.
