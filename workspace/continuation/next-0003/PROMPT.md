Continue the novel after the completed phase continuation-0062. This phase does ONE job.

Read NOVEL_SPEC.md, the series outline and ending, the relevant volume outline, state/current.md, the rolling
summaries, and the previous 20 chapters before doing anything.

If the current volume is NOT complete, write the next planned batch and nothing else.

If the current volume IS complete, this phase is a VOLUME-PLANNING phase and it writes only:
  - the volume outline for the next volume, and
  - its batch cards, and
  - exactly one next phase prompt, which is that volume's FIRST BATCH.
It must NOT write any chapter prose in this phase. The first batch is a separate run.

If that planning turn is itself too large to do well, split it further across another run: plan the
movements in one phase and the batch cards in the next. Judge it by whether the work actually got
written, not by an estimate. A phase that returns without writing anything has asked for more than one
call can deliver, so narrow it and continue rather than retrying it unchanged.

Update manuscript state files, create exactly one next phase prompt, and do not edit controller, workflow,
agent, or dispatcher files.
