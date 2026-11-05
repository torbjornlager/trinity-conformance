# Initial public qualification

This attempt built and deployed consumer `a1cbfe4`, passed its 36 CI groups,
and passed all 1,568 real-browser library assertions. The public native batch
probe recorded 664 passes and eight failed batch members on N5. Isolated checks
then passed all eight cases; nesting `forall/2` inside `findall/3` exposed early
validation of an unused test callback. This was a real nested-execution gap.

The parent release record contains the pinned repair and final repeated gates.
The initial images and rollback tags remain available. These files retain the
first attempt and must not be read as a successful final library qualification.
