# Working In Systems Too Large To Read

Past a certain size the honest position is that you will never read the whole thing —
not this session, not ever. Competence stops being *how much you can hold* and becomes
*how well you choose the five percent that decides the answer.*

The failure this file prevents is the one that feels like diligence: reading breadth-first
until the context window fills, then acting on a shallow model of everything instead of a
deep model of the part that matters.

## Model From Partial Evidence

A useful model of a large system needs four things and nothing else at first:

1. **Entry points** — how work gets in. HTTP routes, CLI commands, queue consumers, cron
   entries, event handlers, scheduled jobs. Everything the system does starts at one of
   these, so this list bounds the whole behavior space.
2. **Persistence** — where state lives. Schemas, migrations, cache keys, buckets, external
   stores. Data outlives code; the shape of the data is the most durable description of
   what the system actually believes.
3. **Seams** — where it talks to something it does not control. Network calls, third-party
   SDKs, filesystem, clock, randomness. Bugs and blast radius concentrate here.
4. **Ownership** — who is responsible for each region. `CODEOWNERS`, directory conventions,
   commit history. This tells you which parts you may change, which you must coordinate on,
   and whose contract you are about to break.

With those four you can locate almost anything without having read almost anything.

**Ownership is also a structural predictor.** A system's shape mirrors the communication
structure of the organization that built it, so team boundaries forecast module
boundaries better than any design document does. This tells you where the awkward
couplings and the duplicated concepts will be, and it explains why an obviously correct
restructure keeps failing: the boundary being fought is organizational, and moving code
does not move it.

## The Three Locating Questions

For any specific question about a large system, ask in this order:

1. **Where does it enter?** — trace forward from the entry point that owns this behavior.
2. **Where does it land?** — trace backward from the table, file, or API that holds the result.
3. **Who owns the path between?** — the answer is usually one module, and now you can read it properly.

Tracing one real path end to end teaches more than skimming fifty files, and it costs less.

## Search Technique At Size

Broad search in a large repository returns noise, and noise invites a wider search. Narrow
first, always:

- **Narrow by directory before narrowing by pattern.** Find the owning region, then search
  inside it. `rg -g '!**/vendor/**' -g '!**/node_modules/**' -g '!**/dist/**'` or the
  repository's own ignore rules.
- **Definition and usage are different searches.** Finding where a symbol is *defined* is a
  tight pattern; finding every *caller* is a wide one. Do not run the wide one until you
  need the blast radius.
- **Symbol search misses dynamic references.** Reflection, dependency injection, route
  tables built by convention, template strings, configuration keys, serialized class names,
  and generated code do not appear. Search the *string form* of the name too, and check
  configuration and data.
- **Exclude generated output explicitly.** Generated files are the largest source of false
  matches in big repositories, and editing one is always wrong — change the generator.
- **Use history as an index.** `git log -S "<symbol>"` finds when behavior appeared or
  changed. `git log --format='%an' -- <path> | sort | uniq -c | sort -rn` finds who knows
  this code. Files that change together in history are coupled whether or not the structure
  says so.

When a search returns too much, the answer is a narrower question, never a wider read.

## Monorepos

- **The build graph is the dependency truth**, not the directory tree and not the imports
  you can see. Ask the build tool what depends on a target; it knows and you do not.
- **Test only what the change can affect.** Every monorepo tool has an affected-targets
  query. Running the whole suite on a 5,000-target repository is not thoroughness, it is a
  way to get no signal for forty minutes.
- **Package boundaries are the real boundaries.** A change inside one package with no
  reverse dependencies has a blast radius of one package, regardless of how large the
  repository is. Establish that first — it often collapses an intimidating task to a small one.
- **Shared packages are contracts.** A change to one is an API change with an unknown number
  of consumers. Enumerate them from the build graph before deciding anything.

## Reading A Service You Do Not Own

Prefer the contract to the implementation: the schema, the OpenAPI or protobuf definition,
the published types, the client library's signatures, the integration tests. These tell you
what you are allowed to depend on. The implementation tells you what happens to be true
today, which is a different and much more fragile fact.

Read the implementation only when the contract is silent on something you need, and record
that you depended on an undocumented behavior — it will change without warning.

## Blast Radius At Size

For anything non-local, the radius has five layers, and static callers are only the first:

| Layer | How to find it |
| --- | --- |
| Static callers | symbol search, build graph reverse dependencies |
| Dynamic callers | string search, DI registrations, route and event tables, config |
| Data | is a persisted shape, cache key, or serialized form affected? |
| Contracts | does any published API, event, or schema change shape? |
| Downstream systems | who consumes those contracts, and can they be deployed at the same time? |

Layers three through five are where large-scale changes actually break, because they fail
after deployment rather than at compile time.

## Knowing When You Have Read Enough

Stop when you can state, without hedging:

- what the change touches,
- what it must not break, and how you will know,
- what you are still assuming, and what would falsify it.

The last one is what makes partial knowledge safe. An explicit assumption is a manageable
risk; an unnoticed one is a defect waiting for a deploy. Reading further to feel prepared —
rather than to answer a named question — is the loading gate in `token-economy.md` being
violated with extra steps.

## Put The Map Somewhere Durable

A model of a large system that lives only in the context window is rebuilt from scratch next
session, at full price. When the model took real work to build, write it down — a short
architecture note, a comment at the seam, an entry in `CLAUDE.md`, or an ADR as described in
`campaigns.md`.

Record the four things above plus what surprised you. Surprise is the most valuable part,
because it is exactly what the next reader will also get wrong.
