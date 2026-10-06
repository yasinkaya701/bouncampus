# PMR Source Entry Template

Use this template when adding a new external/public/academic/method/vendor/procurement source to the cumulative PMR hub.

## Dedupe first

Before adding anything, search [SOURCE_REGISTRY.json](./SOURCE_REGISTRY.json) by:

1. DOI;
2. canonical URL;
3. publisher + report title + edition/date.

Do not create a second source ID for the same artifact just because a mirror URL exists.

## Required record

\`\`\`json
{
  "id": "SRC-<CLASS>-<NNN>",
  "title": "Exact source title",
  "source_class": "PUBLIC_OFFICIAL | ACADEMIC | METHOD_REFERENCE | VENDOR_CLAIM | PUBLIC_PROCUREMENT",
  "authority": "Publisher / institution",
  "canonical_url": "https://...",
  "formats": ["HTML", "PDF"],
  "accessed_at": "YYYY-MM-DD",
  "verification": "VERIFIED_WEB | VERIFIED_BIBLIOGRAPHY | ...",
  "narrow_use": "One or two sentences describing exactly what this source is useful for.",
  "does_not_prove": "Explicit non-inference / claim boundary.",
  "pmr_question_tags": ["H1", "H4"]
}
\`\`\`

Optional fields:

- \`doi\`;
- \`asset_urls\`;
- \`repo_snapshot\`;
- \`bibliographic_note\`;
- \`supersedes\`;
- \`status: stale | conflicted | superseded\`.

## Human-readable synthesis rule

If the source changes a PMR question or falsifier, update [SECONDARY_RESEARCH_INDEX.md](./SECONDARY_RESEARCH_INDEX.md) with:

- the \`SRC-*\` ID;
- the narrow finding;
- the interview question it changes;
- the hypothesis it pressures;
- the non-inference boundary.

Do **not** paste long source summaries for volume.

## PDF / visual rule

If the source exposes a useful PDF, raw dataset, image, table or standard, add a row to [PDF_VISUAL_REFERENCE_MANIFEST.md](./PDF_VISUAL_REFERENCE_MANIFEST.md).

Prefer a canonical link. Before vendoring a binary, record:

- source URL;
- retrieval date;
- license/permission;
- SHA-256;
- whether the file is immutable;
- why repository storage is necessary.

## Data transcription rule

For a small official public table, a structured snapshot may be added only when:

- every row carries the source ID/URL;
- units and labels are preserved;
- source inconsistencies are preserved/flagged rather than “fixed”;
- no missing field is inferred;
- the dataset is explicitly prevented from masquerading as service truth.

## Interview promotion rule

A source entry never creates \`E-INT-*\`.

After a **real completed interview**:

1. create/update the interview artifact from [INTERVIEW_TEMPLATE.md](./INTERVIEW_TEMPLATE.md);
2. record the real completion in [INTERVIEW_TRACKER.md](./INTERVIEW_TRACKER.md);
3. promote only narrow supported/contradicted claims to \`../EVIDENCE.md\`;
4. link the actual interview artifact;
5. preserve contradictory evidence and \`NONE — no promotable claim\` when appropriate.

## Cross-role routing

- **IE:** interview target, workflow, buyer, persona, incentives.
- **CS1:** source semantics, timing, feature admission, benchmark use.
- **CS2:** application claim/evidence boundary and market synthesis.
- **EE:** measurement boundary and physical truth.
- **EHB:** device feasibility only after an approved measurement gap exists.

If a source cannot change a question, decision, claim boundary, measurement plan or acquisition route, do not add it just to grow the bibliography.
