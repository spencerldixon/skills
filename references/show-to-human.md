# Show to human 

Show a saved plan, proposal, or document to the user for approval.

Use its absolute path in this command to open a focused rex pane:

```sh
rex run -s "$REX_SESSION" -b "$REX_BLOCK" --split=right --label review -- nvim -- "/absolute/path/to/plan.md"
```

Notify the user that you need their attention.

Ask for the decision in chat and wait for an explicit answer; opening a document does not count as approval.
