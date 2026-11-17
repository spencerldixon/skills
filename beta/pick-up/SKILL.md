---
name: pick-up
description: Take one Jira ticket from reading to open, CI-checked pull requests - questions, proof plan, worktrees, implement, verify, review and ship.
disable-model-invocation: true
---

# Pick up

Take the ticket the user names from Jira to open pull requests. Invoking this skill hands over the whole run: carry on without check-ins, and stop only where a step says so.

1. **Read and claim.** Read the ticket, its comments and linked tickets with the Jira tools. Assign the ticket to Spencer Dixon; if someone else owns it, stop and ask before reassigning. Read the ticket back and verify Spencer is the assignee before proceeding. Read the code it touches on each repo's default branch, and each repo's `AGENTS.md`.
2. **Questions.** List anything that would change what you build, then stop and ask. When the ticket waits on someone else, such as a decision or a measurement, stop and say who and what. Done when no open question would change the build.
3. **Proof.** Before writing code, state how you will prove the change works: one check per acceptance criterion, such as a spec, a command or a measurement. For a performance change, plan before and after numbers as the workspace `AGENTS.md` describes. Done when every criterion has a check.
4. **Worktrees.** For each repo the change touches, run `git fetch origin`, then `git worktree add ../<key>-<repo> -b <KEY>-<short-name> origin/<default branch>`, with `<key>` in lower case and `<repo>` as the repo name without the `trade-tariff-` prefix. Use the same branch name in every repo. Leave the main checkouts unchanged.
5. **Implement.** Make the change the ticket asks for. Note other problems you find for the report, and leave them unfixed.
6. **Verify.** Run every check from step 3, following the repo and workspace `AGENTS.md`. Done when each check passes and you have its output. Put the proof in the pull request description.
7. **Review.** Run the [code-review](../code-review/SKILL.md) skill on each worktree's diff. Fix every changes-needed finding, then run step 6 again.
8. **Clean up.** Stop containers and services you started, and drop test databases you created. Keep the worktrees for review fixes.
9. **Ship.** Run the [ship-it](../../skills/ship-it/SKILL.md) skill from the worktrees. It ends by babysitting the pull requests in this session.

End with the babysit report, then one line for each problem noted in step 5.
