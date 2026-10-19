# Log Sprint 1: Carbon inventory Stockerau pavilion

Prepared with ChatGPT desktop, 19 October 2026. The calculations and software checks below were carried out with the agent. Independent review by the pair remains to be recorded; no personal hand-check is claimed here.

## Stage 1: Read the model

**Test:** The Rhino audit found **736 unique RFEM members**: 561 members represented by both an axis line and a solid Brep, plus 175 RD 12 tension members represented only by an axis. The 1,297 structural representation objects were grouped using the RFEM member ID, so each member was counted once. All paired attributes matched, and no coincident axes with different IDs were found. The entire document contained 2,986 objects across 330 layers; 1,689 page-space objects were excluded from the member inventory.

**Learning or peculiarity:** Counting solids alone would miss 175 members. Counting axes and solids together would double-count 561 members. The original geometry was inspected without modification.

## Stage 2: Understand the cross-sections

**Test:** An independent arithmetic calculation was prepared for member 1, which tapers from Flat Bar 275/12 to Flat Bar 225/12. Its axis endpoints give L = 0.845177759 m. The areas are A₀ = 275 × 12 = 3,300 mm² = 0.0033 m² and A₁ = 225 × 12 = 2,700 mm² = 0.0027 m². Assuming a linear width change and constant thickness:

V = L × (A₀ + A₁) / 2 = **0.002535533277 m³**.

This agrees with the program. The Rhino display solid has a volume of 0.002527926677 m³, approximately 0.30% smaller than the nominal-section calculation.

**Learning or peculiarity:** There are 386 tapered members. Display solids are not always suitable for material quantities: the 12 hollow-section columns appear as filled cylinders. Their steel volumes were therefore calculated from diameter and wall thickness, subtracting the hollow core. Nominal quantities and Rhino solid volumes remain available for comparison.

## Stage 3: Assign materials

**Test:** Member 78 is a thin flat bar tapering from 162.5/20 to 125/20, but its exported material label is Concrete C25/30. The course's section-family rule suggests structural steel, and the agent flagged the label as implausible. Following the user's decision, this member and the other 17 conflicting flat bars were **kept unresolved**, with their original labels preserved. The remaining assignments comprise 671 steel members and 47 foundation members assigned concrete C25/30 by rule.

**Learning or peculiarity:** Material labels in an export should not be accepted automatically. Rules, agent reasoning and human decisions need separate provenance. Foundation concrete grade C25/30 is an assumption requiring confirmation. Stage 3 remains incomplete while the 18 conflicts are unresolved; those members are excluded from carbon subtotals.

## Stage 4: Embodied carbon from ÖKOBAUDAT

**Test:** Using member 1's Stage 2 volume and a steel density of 7,850 kg/m³:

- Mass = 0.002535533277 m³ × 7,850 kg/m³ = **19.903936226 kg**.
- The specified default steel dataset, UUID `20c29cbd-f9a2-4518-a1ce-c681246c29c8`, gives GWP-total A1–A3 = **560.287415289 kg CO₂e per 1,000 kg steel**.
- A1–A3 = 19.903936226 / 1,000 × 560.287415289 = **11.151924982 kg CO₂e**.

The independent calculation agrees with the program. All five required dataset endpoints were retrieved successfully, and a second retrieval confirmed their factors and declared units. With default datasets, the known A1–A3 subtotal is **6,441.78 kg CO₂e**, excluding the 18 unresolved members.

**Learning or peculiarity:** Declared quantities differ: structural steel is per 1,000 kg, concrete per 1 m³ and reinforcement per 1 kg. Foundation reinforcement is added separately at the required 85 kg/m³ concrete. Rebar A1, A2 and A3 must be summed, while other datasets declare A1–A3 together. Default concrete C4 is undeclared, so the C subtotal is marked incomplete. Module D is reported separately.

## Stage 5: Web app

**Test:** Before switching, the expectation was that the alternative heavy-plate dataset would increase A1–A3 carbon while member lengths, volumes, concrete and reinforcement quantities stayed unchanged. The browser test confirmed that the known subtotal increased from **6,441.78 to 19,517.83 kg CO₂e**, an increase of **13,076.05 kg CO₂e**. Member 1 changed from 11.15 to 50.34 kg CO₂e with unchanged quantities. Coverage remained 718 of 736 members.

**Learning or peculiarity:** The default steel dataset describes scrap-based steel and has a much lower production factor than the heavy-plate alternative. The switch is a dataset sensitivity comparison, not evidence of the pavilion's actual procurement. Our additional idea is an **audit lens** linking the 3D model to unresolved materials, tapered sections, volume discrepancies and a member calculation passport. CSV export preserves the current results and their provenance; saved factors are labelled as cached when a live refresh fails.

## Finally

We used ChatGPT desktop instead of Cline to inspect Rhino, prepare the member inventory, calculate quantities, connect the specified ÖKOBAUDAT datasets and build the local web app. The agent also prepared independent arithmetic checks and tested the browser behaviour. Ten automated numerical/data tests passed. The original Rhino geometry was left unchanged.

For the next group: check duplicate representations first, verify section and dataset units before trusting totals, and investigate implausible material labels. Keep raw model data separate from assumptions and make missing information visible. Review the hand-calculation examples yourselves before presenting them as personal checks. Eighteen material decisions, private-repository milestone tags/pushes and OLAT submission remain outstanding; the existing public course template must not receive the model file.
