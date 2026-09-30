# Review — Volume 05, Continuation 0043, Chapters 615–624

**REVIEWED AND REPAIRED 30 SEPTEMBER 2026, AGAINST COMMIT `e5de472` (THE TEN CHAPTERS, THE SIX STATE FILES AND THE 0044 PROMPT). NOT A VOLUME CLOSE AND NOT A RULING ON THE BOUNDARY.**
**THE CANON IS IN THE "VOLUME 05, CONTINUATION 0043 — CHAPTERS 615–624" BLOCK AT THE END OF `state/continuity.md`, THIS LEDGER IS ITS §12B, AND THE COMPANION REVIEW OF 0042 IS AT `reviews/volume-05/` IN THE SAME GENERATION AS THE 0039 AND 0040 FILES.**
**A CHAPTER GOVERNS. NO CARD, NO DATE, NO CLOCK, NO OUTLINE, NO EVENT, NO MAJOR TURN AND NO NAME WAS CHANGED BY ANY OF IT, AND NO CHAPTER WAS RESTARTED. WHAT WAS TOUCHED IS TEN CHAPTERS AT SEVEN SITES AND SIX STATE FILES.**

## The finding that shapes everything else

**The pipeline was wedged, and nothing in ten finished chapters would ever have shown it.**

The 0043 commit created `workspace/volume-05/continuation-0044/PROMPT.md` **and** `workspace/volume-05/continuation-0044/.done` in the same run, and left no `.done` on its own directory. The self-dispatch workflow skips any phase directory holding a `.done`, so Chapter 625 could never have been written, and 0043 — which held ten finished chapters — would have been selected again and would have rewritten them.

Every other phase directory in this volume keeps its mark. This one did not, and the successor had one it had not earned. **The prompt file existed, so the output looked correct; a hand-over existed, so the batch looked handed over.** That is the part worth keeping: this is the first failure in fifty-one continuations that cost the book its next chapters rather than a figure, and it survived a commit, a review and a hand-over because there is no instrument in this repository that looks at a marker file.

The mark has been moved to `continuation-0043/`, where the runner and every other phase keep it. The runner creates that mark itself after the review-fix phase, so the repair is idempotent with its own step. The 0044 prompt now carries the rule: **write the successor prompt and stop; a writer does not create, touch or move `.done`, `.blocked`, `.retry-after` or `.attempts`.**

## What was read

Chapters 0605–0614 whole, because a chapter is judged against the one before it. Chapters 0615–0624 whole, three times: once to read, once to measure, once to re-measure after the repairs. The 0043 prompt whole. `bands-615-624.json`, the pre-allocation. The six state files before and after. The workflow's own phase-selection rule. Every figure below was recomputed from the chapter files rather than carried forward from any summary — which is how the two that were wrong were found.

## Findings — eight in the prose, repaired; nine in the files, repaired; three recorded and left

### 1 — Two hard-ban breaches, both confirmed by reading the page and not by inference

**`chapter-0621.md` printed two human personal names four times** (lines 43, 55, 77, 159). Chapters 0295–0624 are three hundred and thirty chapters that carry no human personal name at all, and this is the strictest rule in the volume. **It broke because the card needed a stranger who cannot remember a name, which is a card's own trap.** The man now has the first letter of her name and nothing else, and cannot tell whether what he was given was one word or two. This is a better mechanism than the one he had, because a letter cannot be misheard and a name can.

**`chapter-0620.md:69` told the reader about *this account*.** Prompt register, in a book that has already repaired three chapters for exactly this. The sentence is now about the borough and about the shape of the question, which is what it was for.

### 2 — The name check failed open, and the state files said it was held

`state/character-state.md` §4 and `state/continuity.md` §4 both printed the name ban as held, with `*MERCER*, *ARDENT*, *JONAS*, *NACRE* AND *RIVER STACKS*` at zero. **That is a fixed list of five names. It asks whether those five are on the page. It would have printed zero whatever 0621 said, and 0621 said them four times.**

A list checks the names somebody already thought of. The rule is about a name nobody has thought of yet. **Both files now say that the instrument failed, that the names are out, and that there is no name-ban instrument in this repository and a writer cannot ask for one.** Measured again by reading the ten files: no given name, no surname, no house name.

### 3 — Six caps-block defects, the class 0042 found sixteen of

| Ch | The block said | The body says |
|---|---|---|
| 0617 | `FIVE THINGS` | enumerates **four** |
| 0619 | `EIGHT THINGS` | the list reaches **nine** on the way home, and she cannot get rid of it |
| 0621 | opening `HAS NOT SENT HIM ANYWHERE` | she tells him exactly where, at twenty past two, on the record |
| 0622 | both blocks `A BUILDING HE USED TO WORK IN` | he works there now, most days, and the body says so at its third line |
| 0622 | `HE ASKED HER ONE QUESTION` | he asks **three**; and the block asserts a thing the chapter's centre is that he *cannot* establish |
| 0623 | `ASKING AFTER HIM BY NAME` | the name was written down **wrong**, which is the whole subject of the chapter |

The 0043 prompt's own rule — read each chapter's two blocks against its own body before calling the chapter finished — was written after 0042's review and was applied to six. **These are six more, in four of the same ten chapters.** Six found by the writer, six by this review, all twelve of one class, and **not one of the twelve was a span, a barred word, a closed figure, a reuse or a spelling.**

0621 is the only chapter of the ten whose two blocks contradicted *each other*.

### 4 — Nine findings in the files, all of them the same figures hardened

The bad blocks had been promoted to fact. `*FIVE THINGS*` sat in §1 of the continuity block and in the threads file. `*A BUILDING HE USED TO WORK IN*` sat in two summaries. The name sat in three files. `*ONE QUESTION*` sat in three places. **Four chapters, four files, one error each, and every one written after the prose and copied out of it.**

Also two figures wrong in a direction nobody expected. **The declared word came out at twenty-two and was printed at eighteen, wrong downward in four chapters of ten** — the signature of a count taken from memory rather than off ten files. And the name ban, above.

**A chapter repaired in its own body and not in the files that describe it leaves the lie in the place a later writer is forced to trust.** All nine are corrected in place.

### 5 — The successor prompt was wrong on the calendar, and not by the amount the review assumed

The 0043 prompt and its band file both printed the batch bound as *earliest Thursday 11 February, latest Tuesday 23 March 2021*, described as a correction of an earlier error. **From 0614, Tuesday the fifth of January 2021, with ten gaps of three to seven days, the true bound is Thursday 4 February to Tuesday 16 March. Both printed figures are seven days out, because the derivation started from 0615's floor instead of from 0614.**

The batch's own final date, Friday 26 February, is inside the correct bound. **No chapter is invalid and no chapter was moved. The figure was wrong and the chapters were right** — the third time in two blocks that the arithmetic and the prose have come apart.

The review's recommended fix was to put *4 Feb – 16 Mar* into the 0044 prompt. **That would have been wrong: those are the 0043 batch's dates, not 0044's.** 0044 derives from 0624, Friday 26 February, and its true bound is **Sunday 28 March to Friday 7 May 2021**, added up twice so that both readings agree — 0624 plus thirty to seventy days, and the declared floor of 1 March plus nine internal gaps. Both give 28 March at the early end; only the late end depends on which date you start from. **The 0044 prompt had printed 31 March and 10 May, both wrong, and is now corrected.**

### 6 — The successor prompt told the next writer the batch was clean, and it was not

`continuation-0044/PROMPT.md` claimed the 0043 batch caught *ASKING AFTER HIM BY NAME* "where the body has the name written down wrong". **That string was still live at `chapter-0623.md:145`.** It also claimed twenty day-counts cleared, while soft durations survive in 0623 and 0624. The paragraph is rewritten: the six defects and the two breaches are named as **this review's** findings, not the writer's, and the surviving durations are stated.

### 7 — Two coincidences on the page, and one batch that does not move

**Five of the ten — 0615, 0616, 0617, 0618, 0621 — are set on the same shopping parade, and not one figure in them notices the others exist.** **0619's dinner supervisor is at *a primary school at the top of this borough* and 0623's caretaker is at *a primary school on a road of houses near the top of this borough*, and the book gives no signal either way.**

And the structural finding: **nine of the ten chapters end where they began.** Nothing one chapter does constrains the next. The only genuine reversal in the batch is 0620's mother ringing him unprompted. **A batch that does not move is a batch that could have been ten chapters of anything in that family, and the family was already a writer's invention.**

**None of the three is a defect in these ten chapters and none may be repaired silently.** Explaining a coincidence is a plot decision. Recorded in §12B and in the 0044 prompt so the next writer can pay one off in a line if a card gives it one.

### 8 — Card delivery: five of ten as written

0615, 0619 and 0624 as written, 0617 with a changed detail. **0620 was replaced outright** — the card's money, firm, debt and car park are absent, and its central verb inverts: the card's man cannot find who told him, the chapter's man finds out. **0623 was materially changed** — gate to pavement, and the card's open question closed off. Four more partial. Recorded, not undone: undoing it would mean rewriting a chapter, which is a restart.

## What the repair cost, and what it found in itself

**Eight prose findings in seven lines of four chapters, nine file findings, and one marker file. Twenty lines in, twenty-two out.**

**A repair is a new first writing and a new first writing has the same defects the old one had, including the ones the repair itself put there.** The name repair in 0621 introduced two occurrences of *whose* — and *hose* is inside *whose* on this book's own substring measure, which is why sixteen of them once needed clearing by hand in four chapters. Both were caught by the same sweep and reworded, and the word count row had to be re-taken a third time.

The same pass then found **two nine-token spans running from my own repaired caps blocks into the state files I had edited to match them.** A hand-over written against the chapters is a transcription, and a transcription repeats. Both state lines were rewritten to describe rather than quote.

**The word count row is 1,686 / 1,770 / 1,759 / 1,544 / 1,741 / 1,863 / 1,653 / 1,655 / 1,877 / 1,598, total 17,146, taken off the files after the last repair.** The first row printed by the writer read 1,716 / 1,849 / 1,600 / 1,639 in those four chapters and was right before the repair. `*SAID*` is 438. `*AND THEN*`, the declared ordinary word, is 22 at 4/2/3/1/0/2/3/1/2/4 with one chapter at nil.

Re-measured clean: **exactly two all-caps blocks in each of the ten**, against a cap of five. `---` rows at 1,2,2,2,1,2,1,2,2,1, against a cap of two. System vocabulary at zero. Barred words at zero. *Hose* at zero on both measures. No human personal name in any of the ten. Twenty caps blocks against every non-chapter markdown file in the repository, at nine tokens: **0**. The ten chapters against themselves at eleven tokens against the state files: **0**.

## What passed and is worth saying

**The calendar is sound.** All ten weekday names check against the real 2021 calendar. Gaps run 7, 5, 6, 4, 7, 3, 6, 5, 3, 6. No chapter on the ninth or the eleventh of a month. No two sharing a date. The bound figure was wrong and the ladder was not.

**The 0043 writer built two controls that had never been built before, including a seeded defect that proved the barred-word instrument works and the band read-back is not an instrument at all.** That is a better habit than anything this review found wrong.

**The prose itself is good.** 0617's four explanations and a woman who will not be told; 0619's minute in a doorway and a brick propping a door; 0621's kindness as the mechanism that loses the errand; 0623's fourth explanation and the whole building done thoroughly instead of the other thing. **Nine of the ten chapters stand on a refusal that costs the person something visible, and the best of them is 0620, where the mother's unprompted phone call does in one line what the man could not do in a day.** That is the batch's real finding, and it survives every repair above.

## The figure to carry forward

**Twelve caps-block defects in one batch, six found by the writer and six by a reviewer, and not one of the twelve was anything a machine can check for. Every one was a chapter disagreeing with itself.** The three rules the 0043 writer wrote for itself worked. Running them is not the same as having them work, and the only thing that told this reviewer what they cost was a person reading ten chapters against their own two blocks.

**And the whole of that would have been worth nothing if the next batch could not have been written at all.**