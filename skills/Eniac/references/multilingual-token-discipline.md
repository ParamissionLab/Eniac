# Multilingual Token Discipline

Use this reference when the request, source material, or required output is in Thai or another language that tends to consume more tokens than English.

## Language Policy

- Reply in the user's language by default.
- Keep code, commands, API names, file paths, identifiers, stack traces, and quoted source text unchanged.
- Use English internally for compact planning when it reduces tokens, but do not expose unnecessary English reasoning to the user.
- If the final answer must be bilingual, keep one language primary and use short parenthetical translations only where they add value.

## Compact Working Brief

For long non-English prompts, create a short private brief:

```text
User language:
Desired output language:
Goal:
Must preserve exactly:
Constraints:
Done criteria:
Open risks:
```

Avoid translating the whole prompt. Translate intent, not bulk content.

## Thai Compression

- Preserve user-specific Thai terms when wording matters.
- Use compact English internally for planning only when it saves tokens.
- Prefer paths, commands, file/line references, and concrete outcomes over prose.
- Keep exact Thai quotes only when the wording is part of the task.
- Infer "do it" vs "explain it" from workspace context; ask only when the wrong assumption would be costly.

## Glossary

Maintain a tiny glossary only for terms that affect correctness:

```text
"งานวนซ้ำ" = iterative loop work
"เครดิต" = paid usage/compute budget
"สำเร็จลุล่วง" = complete according to stop criteria
```

Do not create a glossary for obvious words or terms that appear once.

## Compression Rules

- Summarize repeated user requirements once and refer back to the compact brief.
- For long Thai or multilingual documents, extract headings, decisions, obligations, and exact quoted clauses only when needed.
- For logs or errors in any language, keep exact failing lines and summarize surrounding prose.
- For code review or engineering tasks, prefer file paths and line references over prose explanations.

## User-Facing Reports

Use concise Thai or the user's language:

```text
ทำแล้ว:
ตรวจสอบ:
ยังเหลือความเสี่ยง:
ไฟล์สำคัญ:
```

Skip sections that are empty. Do not include hidden chain-of-thought or verbose loop traces.
