# Human review

Before asking for approval or a required human check, save the plan, proposal, or walkthrough and open it in Neovim in a new Rex pane beside your own, focused. Reuse the existing document.

Use its absolute path in this command:

```sh
rex run -s "$REX_SESSION" -b "$REX_BLOCK" --split=right --label review -- nvim -- "/absolute/path/to/plan.md"
```

If opening fails, say why and provide the file link. Do not claim it opened. Ask for the decision in chat and wait for an explicit answer; opening a document does not count as approval. This procedure adds no approval gates.
