// Run this body inside Pi codemode; optional `options`: { backlog: true }.
const backlog = typeof options !== "undefined" && options.backlog === true;
const scope = backlog
  ? 'project = HMRC AND status = "Backlog"'
  : '((project = AI AND status IN ("TO DO", "Blocked", "On hold")) OR (project = HMRC AND status IN ("Ready to Start", "To Do", "Blocked", "On hold")))';
const result = { complete: false, matched: {}, skippedEmpty: 0, excludedBlocked: [], issues: [] };
const seen = new Set();
const cursors = new Set();
let cursor = "";
function plain(value) {
  if (typeof value === "string") return value;
  if (!value || typeof value !== "object") return "";
  return [value.text || "", ...(value.content || []).map(plain)].filter(Boolean).join("\n");
}
function excerpt(value) {
  const text = plain(value).replace(/!\[[^\]]*\]\([^)]*\)/g, "").trim();
  if (text.length <= 1200) return { text, clipped: false };
  const criteria = text.search(/acceptance criteria|definition of done/i);
  const dependencies = text.split("\n").filter(line => /blocked|depends on|waiting|awaiting|pending|prerequisite|cannot.*until/i.test(line)).join("\n");
  return { text: [text.slice(0, 400), criteria < 0 ? text.slice(-550) : text.slice(criteria, criteria + 550), dependencies.slice(0, 200)].join("\n[excerpt]\n"), clipped: true };
}
function unpack(response) {
  if (response.isError) throw new Error("Jira search failed");
  if (Array.isArray(response.structuredContent?.issues)) return response.structuredContent;
  for (const item of response.content || []) {
    if (item.type !== "text") continue;
    try { const data = JSON.parse(item.text); if (Array.isArray(data.issues)) return data; } catch {}
  }
  throw new Error("Jira returned no structured issue page");
}
try {
  do {
    if (cursors.has(cursor)) throw new Error("Jira repeated a pagination cursor");
    cursors.add(cursor);
    const page = unpack(await tools.mcp__atlassian__searchJiraIssuesUsingJql({
      cloudId: "https://transformuk.atlassian.net",
      jql: `assignee IS EMPTY AND description IS NOT EMPTY AND ${scope} ORDER BY priority DESC, updated DESC`,
      maxResults: 100, fields: ["summary", "description", "priority", "status", "issuelinks"],
      nextPageToken: cursor, responseContentFormat: "markdown", searchResultMode: "issues", actionSource: "model_tool_call",
    }));
    for (const issue of page.issues) {
      if (seen.has(issue.key)) continue;
      seen.add(issue.key);
      const fields = issue.fields;
      const project = issue.key.split("-")[0];
      result.matched[project] = (result.matched[project] || 0) + 1;
      if (!plain(fields.description).trim()) { result.skippedEmpty++; continue; }
      const blockers = (fields.issuelinks || []).filter(link => link.inwardIssue && link.type?.inward === "is blocked by").map(link => ({
        key: link.inwardIssue.key, status: link.inwardIssue.fields?.status?.name,
        category: link.inwardIssue.fields?.status?.statusCategory?.key,
      }));
      if (blockers.some(blocker => blocker.category && blocker.category !== "done")) {
        result.excludedBlocked.push({ key: issue.key, blockers });
        continue;
      }
      const description = excerpt(fields.description);
      result.issues.push({ key: issue.key, title: fields.summary, priority: fields.priority?.name, status: fields.status?.name,
        description: description.text, clipped: description.clipped, ...(blockers.length ? { blockers } : {}) });
    }
    cursor = page.nextPageToken || "";
    if (page.isLast === false && !cursor) throw new Error("Jira omitted the next pagination cursor");
  } while (cursor);
  result.complete = true;
} catch (error) {
  result.error = "Jira search incomplete; do not treat these results as exhaustive.";
}
return result;
