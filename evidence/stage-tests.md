# Stage tests — Stockerau Pavilion

## Stage 1 — member count
Read-only Rhino enumeration: 2,986 objects, 330 layers, 56 populated. All 1,297 model-space objects are structural representations; 1,689 page-space objects are drawing/layout content. RFEM ID grouping: 561 axis+solid pairs + 175 axis-only tension members = **736 unique member entities**. No coincident axes under different IDs. Original geometry unchanged.

## Stage 2 — independent hand calculation, member 1
Start (8.48, 2.5, 4.0) m; end (8.48, 1.666666666666667, 4.141) m.

- L = sqrt((2.5 − 1.666666666666667)² + (4.141 − 4.0)²) = 0.845177759081 m.
- Start section 275 × 12 mm: A0 = 0.003300 m².
- End section 225 × 12 mm: A1 = 0.002700 m².
- Constant thickness and linear width change: V = L × (A0 + A1)/2 = **0.002535533277 m³**.
- Program: 0.002535533277 m³. Difference: 0 m³.
- Rhino display Brep: 0.002527926677 m³, a 0.300903% difference from nominal axis calculation. Do not hide this discrepancy.

There are 386 changing sections, all flat bars with constant thickness. The general implementation integrates both rectangular dimensions linearly (including the cross-term), rather than assuming averaging endpoint areas is valid for every taper. RD rods use πd²/4. Hollow tubes use π(D²−(D−2t)²)/4. The 12 tube Breps appear filled and overstate steel volume if used directly. 116 Flat Bar 33.3/20 members differ from Brep volumes by >2%; nominal labels and the discrepancy are retained. Analytical quantities are the app's declared basis, not exact as-built quantities.

## Stage 3 — material plausibility test
Example member **78**, section Flat Bar 162.5/20 to Flat Bar 125/20, is labelled Concrete C25/30. Its thin flat-bar form and the course material grouping suggest steel, so blindly copying the exported material is implausible. Rules proposed steel; language-model review flagged the contradiction. The user explicitly chose **keep unresolved**, so all 18 conflicting members remain unresolved and are excluded from carbon subtotals. This is a documented open decision, not a completed full material assignment.

The other 671 steel members use a section-family rule; 47 low-level Rectangle 500/500 members use a foundation rule (assumed C25/30). The 12 exported S355 tube labels agree with their section family. Original labels remain unchanged. UI human reviews record reason and timestamp locally and export with provenance.

## Stage 4 — hand A1–A3 calculation, member 1
Using the Stage 2 volume:

- Steel mass = 0.002535533277 m³ × 7,850 kg/m³ = 19.903936226 kg.
- Dataset 20c29cbd-f9a2-4518-a1ce-c681246c29c8, version 00.03.000.
- Live response fetched at 2026-10-19T11:24:19.826834+00:00.
- GWP-total A1–A3 = 560.287415289044 kg CO₂e per **1,000 kg** steel.
- Result = 19.903936226/1,000 × 560.287415289044 = **11.151924982 kg CO₂e**.
- Program = 11.151924982 kg CO₂e.

All five assignment UUIDs are fetched through the required extended JSON endpoint. Concrete is per 1 m³; steel defaults/alternative are per 1,000 kg; rebar is per 1 kg. Foundation contribution includes 85 kg rebar per m³ concrete. Rebar declares A1, A2 and A3 separately, so they are summed once. Other EPDs declare A1–A3 together. Concrete default C4 is undeclared, so C totals are marked partial; missing values are not silently zero. Steel scenarios are mutually exclusive; default S3 is the EPD European-average scenario. Sole scenarios in EcoPact/rebar are selected explicitly by the parser. D remains separate.

## Stage 5 — dataset switch prediction and result
Prediction before switching: the heavy-plate dataset has a higher A1–A3 factor than profiles/bars; steel carbon should increase while geometry, volumes, concrete and rebar quantities remain unchanged. This is a dataset sensitivity comparison, not proof that heavy plate is an interchangeable specification for every section.

Saved live-factor test, excluding the 18 unresolved members:

- Profiles/bars + default concrete + rebar: **6441.783710 kg CO₂e** A1–A3.
- Heavy plate + default concrete + rebar: **19517.832590 kg CO₂e** A1–A3.
- Increase: **13076.048880 kg CO₂e**, or 202.988% of the known pavilion subtotal.
- Factors: 560.287415289 vs 2528.984485446 per 1,000 kg. Steel-only factor ratio: 4.513727.

Own idea: audit lens links material conflicts, taper geometry and volume/axis discrepancies directly to the 3D member and its calculation passport. CSV export includes current module, dataset UUIDs, factor-fetch timestamps, material provenance and incomplete-status markers.

## Remaining assignment work
18 human material decisions intentionally remain open. Git commits/tags/pushes and OLAT submission are separate from implementation and must not be claimed as completed without evidence. The private source .3dm must never be pushed to a public repository. Present these documented tests as agent-prepared calculations, and independently review them with your partner before claiming personal verification.
