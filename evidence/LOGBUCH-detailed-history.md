# Logbuch — Sprint 1: Carbon-Inventur Pavillon Stockerau

Prepared with ChatGPT desktop on 19 October 2026. Tests below describe work actually performed by the agent; the pair should review the calculation examples before presenting them as their own checks. Cline and an OpenAI API key are not required for this implementation.

## Etappe 0

- **Was wir gemacht haben:** Switched from Cline to ChatGPT desktop. Located the old Desktop template folder; built a separate local app under this chat's outputs folder. The old Git remote is the public course template, not a verified private group repository. No upload was made.
- **Wichtigste Prompts:** “Use Computer Use to interact with Rhino 8 on my Windows desktop.” / “Do not modify or delete the original geometry.” / “since this task was originally to do with cline, but now i decide to use chatgpt desktop … can you keep continue to finish the task?”
- **Was schiefging und woran wir es gemerkt haben:** A direct network request was blocked by the execution environment; the allowed public-dataset fetch was repeated with network access. The concrete response contains a module with no value, so the parser was changed to retain missing status. A browser download-event wait timed out, but the CSV was downloaded successfully and then checked from disk.
- **Was wir selbst geprüft haben:** Agent checks are documented below and in evidence/stage-tests.md. Human/pair review is still to be recorded honestly.

## Etappe 1: Modell lesen

**Test:** 736 distinct RFEM member IDs. 561 IDs have one solid Brep plus one axis; 175 RD 12 tension IDs have only an axis. 1,297 model-space representations reconcile to 736 members. The live Rhino audit enumerated 2,986 objects across 330 layers, compared paired metadata, found no coincident axes under different IDs, and rechecked the live object-table total. All remaining 1,689 objects are in page space. See data/verification.json and the per-object audit.

**Learning oder Besonderheit:** Counting solids alone misses 175 tension members. Member 1473 has an approximately 179 mm offset between its solid and axis. No original geometry was modified or saved.

**Status:** Technical test passed. Git commit/tag/push not performed.

## Etappe 2: Querschnitte verstehen

**Test:** Member 1 changes from Flat Bar 275/12 to Flat Bar 225/12. Endpoint distance L=0.845177759081 m. A0=0.0033 m², A1=0.0027 m²; V=L(A0+A1)/2=0.002535533277 m³. An independent arithmetic test agrees with the quantity program. The Rhino solid is 0.002527926677 m³, 0.300903% smaller than the nominal-axis calculation. Full arithmetic in evidence/stage-tests.md.

**Learning oder Besonderheit:** 386 members have changing sections. Hollow tube volume must subtract the hollow core; the 12 exported tube Breps appear filled. Nominal and solid quantities remain separate; 116 small flat bars also have >2% volume discrepancies.

**Status:** Technical test passed with documented quantity assumptions and geometry discrepancies. Human hand-check review and Git milestone still pending.

## Etappe 3: Material zuordnen

**Test:** Member 78 is a tapered 162.5/20 to 125/20 thin flat bar, but its exported label is Concrete C25/30. A section-family rule suggests steel; language-model review flags the contradiction. User response: **“Keep them unresolved.”** All 18 conflicting flat bars therefore remain unresolved and are excluded from carbon subtotals. The other 671 steel members and 47 assumed C25/30 foundation members have visible rule provenance. Existing S355 labels on 12 tube columns are consistent with their section family.

**Learning oder Besonderheit:** Original material metadata can be implausible. Preserve it, separate assignments from raw data, and make human decisions traceable. The concrete foundation grade is an assumption, not recovered metadata.

**Status:** Incomplete by explicit user choice: 18 material decisions remain open. Do not claim the “every member assigned” requirement or an etappe-3 completion tag.

## Etappe 4: Embodied Carbon aus der ÖKOBAUDAT

**Test:** Member 1: V=0.002535533277 m³ × 7,850 kg/m³ = 19.903936226 kg steel. Default steel GWP-total A1–A3=560.287415289044 kg CO₂e / 1,000 kg steel. Result=11.151924982 kg CO₂e; program agrees. All five specified UUIDs fetched live successfully. See raw timestamped responses in data/epd/ and evidence/test-values.json.

**Learning oder Besonderheit:** Steel is declared per 1,000 kg, rebar per 1 kg and concrete per 1 m³. Rebar A1/A2/A3 are separate. Concrete default C4 is undeclared. End-of-life scenarios must not be added together, and D is displayed separately. Each foundation includes 85 kg rebar per m³ concrete.

**Status:** Live integration and example test pass. The pavilion result remains a subtotal while 18 materials are unresolved; no completion tag/push claimed.

## Etappe 5: Web-App

**Test:** Before switching, the expected result was a higher A1–A3 subtotal with the heavy-plate steel dataset and unchanged geometry/quantities. Browser test confirmed approximately 6,442 → 19,518 kg CO₂e, using default concrete and rebar, with 718/736 assigned members. Exact saved-factor values: 6,441.783710 → 19,517.832590 kg CO₂e. Member 1 changed 11.15 → 50.34 kg CO₂e; length and volume stayed unchanged. The default C view correctly flags 47 members with incomplete module coverage; EcoPact restores declared C1–C4 coverage for the assigned members. D is separate. Unresolved filter displays exactly 18 members. The downloaded CSV has 736 data rows and empty carbon values for all 18 unresolved members.

**Learning oder Besonderheit:** The plate/profile comparison is a dataset sensitivity test, not proof that materials can be substituted without redesign. Own idea: an audit lens joins the 3D model to material conflicts, changing sections, volume discrepancies and a calculation passport. Cached data is labelled honestly for offline presentation.

**Status:** Local app implemented and browser-tested. Submission, private-repository milestones and material decisions remain outstanding.

## Zum Schluss

The agent carried out a read-only Rhino audit, wrote the quantity and EPD calculation code, built the local app and prepared reproducible tests and evidence. Ten numerical/data tests passed. Original Rhino geometry and the original Desktop course template were left unchanged. No source model was uploaded. Review the 18 unresolved materials with the partner/instructor; then create/use a private group repository and complete genuine milestone commits/tags before OLAT submission.
