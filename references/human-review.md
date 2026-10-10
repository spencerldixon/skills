# Human review

Before asking for approval or a required human check, save the plan, proposal, or walkthrough and open it in Neovim in a new Ghostty tab. Reuse the existing document.

Use its absolute path in this command:

```sh
osascript - "/absolute/path/to/plan.md" "$(command -v nvim)" <<'APPLESCRIPT'
on run argv
    tell application "/Applications/Ghostty.app"
        set reviewConfig to new surface configuration
        set command of reviewConfig to (quoted form of (item 2 of argv)) & " -- " & (quoted form of (item 1 of argv))
        activate
        if (count of windows) > 0 then
            new tab in front window with configuration reviewConfig
        else
            new window with configuration reviewConfig
        end if
    end tell
end run
APPLESCRIPT
```

If opening fails, say why and provide the file link. Do not claim it opened. Ask for the decision in chat and wait for an explicit answer; opening a document does not count as approval. This procedure adds no approval gates.
