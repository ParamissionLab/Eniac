# Multilingual Token Discipline

Use when the request, source, or required output is Thai or another token-expensive language.

## Policy

- Reply in the user's language by default.
- Keep code, commands, API names, file paths, identifiers, stack traces, and quoted source text unchanged.
- Plan in compact English only when it saves tokens; do not expose unnecessary English reasoning.
- For bilingual output, keep one primary language and use short parenthetical translations only where useful.

## Brief

For long non-English prompts:

```text
Lang:
Output:
Goal:
Preserve:
Constraints:
Done:
Risk:
```

Translate intent, not bulk text.

## Thai Compression

- Preserve user-specific Thai terms.
- Keep exact Thai quotes when wording matters.
- Prefer paths, commands, and concrete outcomes over prose.
- Use project-native technical nouns naturally: `build`, `lint`, `typecheck`, API names, file paths.
- If "ยังไง" appears in an open repo, infer whether advice or implementation is intended from context; implement only when the workspace and request imply it.

## Glossary

Maintain a tiny glossary only for correctness-critical repeated terms. Do not define obvious or one-off words.

## Extraction

- Summarize repeated requirements once.
- For long documents, extract headings, decisions, obligations, and exact clauses only when needed.
- For logs/errors, keep exact failing lines and summarize surrounding prose.
- For code/review, prefer file paths and line references.

## Reports

Implementation:

```text
ทำแล้ว:
ตรวจสอบ:
ความเสี่ยง:
ไฟล์:
```

Recommendation:

```text
ควรปรับ:
เหตุผล:
ทำก่อน:
ระวัง:
```

Skip empty fields. Do not expose hidden chain-of-thought or verbose loop traces.
