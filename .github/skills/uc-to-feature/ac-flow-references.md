# AC flow references

Recognition rules for verbal flow references in human-authored UC acceptance
criteria. This is an interpretation aid, not a required UC syntax or an
executable parser. Read it during UC validation and oracle mapping.

## Accepted forms

Match case-insensitively. `X` below means the actual numeric flow identifier,
not a literal letter or a wildcard.

| Flow | Verbal forms | Acronym forms |
| --- | --- | --- |
| Main | `Flusso Principale` | `FP`, `F.P.`, `P.` |
| Alternative X | `Alternativo X`, `Alternativa X`, `Alternativi X`, `Alternative X`, `Flusso Alternativo X` | `AFX`, `A.F.X` |
| Exception X | `Eccezione X`, `Flusso di Eccezione X` | `EFX`, `E.F.X` |

`Alternativ*` denotes the meaningful Italian word forms above, not an arbitrary
suffix or a literal `*`. Allow whitespace around acronym letters, dots and the
numeric identifier: `AF02`, `AF 02`, `A. F. 02`, `A . F . 02` are equivalent.
Accept the existing UC identifier style with a separating hyphen as well:
`AF-02`, `EF-01`. Leading zeroes do not change the numeric identity.
Parentheses are convenient but not required; a reference may occur in prose
when it clearly identifies the criterion's target flow.

## Resolution procedure

1. Build the actual flow inventory from the UC: main flow, each AF and each
   EF. Normalize case, whitespace, acronym dots, separating hyphen and numeric
   padding for comparison only. Keep the original UC ids and wording in
   traceability; do not rewrite the source.
2. Identify a complete flow label in the AC, never a substring inside another
   word or identifier. `FP` and `P.` must be standalone labels referring to
   the main flow; `P.` in an unrelated abbreviation is not evidence. Longer
   forms such as `Flusso di Eccezione 2` identify one reference, not several
   nested matches. AF/EF references require a numeric identifier.
3. Resolve each label to the inventory by flow kind and numeric identity.
   `AF2` resolves to the actual `AF-02`, not to `EF-02` or FP. If two UC ids
   normalize to the same identity, report a duplicate/ambiguity; never choose
   the first. A nonexistent target is an explicit functional question, not
   permission to invent a flow or silently attach the AC to FP.
4. Preserve the criterion's meaning. A clear target scopes its verifications
   to that flow's supported data variants, unless the criterion explicitly
   limits them by condition or data properties. A reference does not define
   the number of variants, concrete data, new behaviours or missing oracles.
   Several compatible checks for the same case belong in one scenario.
   Separate cases/scenarios/outlines only when their functional context,
   behaviour or applicable verification sets differ.
5. Several explicit targets apply only as stated by the criterion. Resolve
   all of them and record each association; ask if their relationship or
   expected outcomes are unclear. A reference mentioned for comparison or
   exclusion is not a positive applicability label.
6. With no explicit reference, use the criterion's functional meaning and the
   UC flows as before. Do not default to FP, apply it to every flow, reject the
   UC, or ask merely for a formatting improvement. Ask only when applicability
   cannot be established or conflicts with the flow's stated behaviour.
7. Record the original reference, resolved target and any condition in the
   existing context Oracles/Functional evidence and final Coverage sections.
   Use their existing columns; unresolved references go to Questions and
   affected coverage remains incomplete. Do not impose new feature tags.

## AC cardinality and grouping

The AC-to-flow and AC-to-Gherkin-scenario relationships both allow **many to
one**. Multiple distinct ACs may reference FP, the same AF, or the same EF
and all be checked in one scenario, including a negative scenario. Repeated
references to the same flow in different ACs are not duplicate flow definitions
or an ambiguity.

Collect all applicable ACs for the case; do not overwrite an earlier criterion
when resolving another to the same flow, and do not create one scenario per AC.
With the same starting conditions and actions, compatible checks become
`Then`/`And` assertions in the same scenario. They can verify different
properties of that case's observable outcome. Retain each criterion and its
source/oracle separately in Coverage, allowing several rows to identify the
same scenario and Examples row.

The outline rule about different verification sets compares **different
cases**, not individual ACs: if every row needs AC01 and AC02, both checks
belong to their shared outline. If a different case requires a different or
additional set of checks, use a separate scenario/outline as prescribed by the
mapping rules. Conflicting criteria remain a functional question; do not split
them merely to hide the contradiction. Do not propagate one EF's criteria to
another EF without a requirement.

Illustrative associations only, not approved UC-to-feature examples:

| Criteria and target | Gherkin grouping |
| --- | --- |
| AC01 and AC02 both reference FP | One main-flow scenario/outline checking both |
| AC03 and AC04 both reference AF02 | One AF02 scenario/outline checking both |
| AC05 and AC06 both reference EF01 | One negative EF01 scenario/outline checking both |

These associations assume compatible criteria for the same case, not a rule
that every flow has exactly one scenario. One AC may also apply to several
supported cases or flows when its meaning establishes that scope.

## Recognition examples

These are label-recognition examples only, not approved UC-to-feature examples
or functional specifications. Assume an inventory with FP, `AF-02`, `EF-01`.

| AC reference fragment | Resolution |
| --- | --- |
| `(Flusso Principale)` | FP |
| `(fp)` | FP |
| `(F.P.)` | FP |
| `(f . p .)` | FP |
| `(P.)` | FP |
| `(Alternativo 2)` | AF-02 |
| `(alternativa 02)` | AF-02 |
| `(Alternativi 2)` | AF-02 |
| `(Alternative 02)` | AF-02 |
| `(Flusso Alternativo 02)` | AF-02 |
| `(AF02)` | AF-02 |
| `(af 2)` | AF-02 |
| `(A.F.02)` | AF-02 |
| `(a . f . 02)` | AF-02 |
| `(AF-02)` | AF-02 |
| `(Eccezione 1)` | EF-01 |
| `(Flusso di Eccezione 01)` | EF-01 |
| `(EF1)` | EF-01 |
| `(e.f. 01)` | EF-01 |
| `(E . F . 1)` | EF-01 |
| `(EF-01)` | EF-01 |
| `(AF 99)` | Unresolved: target absent |
| `(AF)` | Unresolved: numeric identifier missing |
| `(AF-2, AF-02)` with duplicate UC definitions | Unresolved: duplicate identity |
| `campoFP` or `codiceAF02` | Not a flow reference |
| `P. Rossi` | Not a flow reference: unrelated abbreviation |
| `non si applica ad AF02` | Excludes AF-02; not positive applicability |
| No reference | Determine applicability from functional meaning |

For example, a criterion scoped to FP can be checked in each supported row
of the main-flow outline without an AF naming those rows. A criterion scoped
to AF02 does not automatically add its checks to FP or EF01.
