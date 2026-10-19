# Independent number check — 19 October 2026

## Verdict
The current default A1–A3 display of **6,442 kg CO₂e** agrees with an independent calculation from the original exported member inventory and raw ÖKOBAUDAT responses: **6,441.783710 kg CO₂e**. No discrepancy was found in lengths, nominal volumes, factor selection, or declared-unit scaling. This is a consistent course-model subtotal, not a verified as-built or whole-life pavilion total.

## Independent route
The check did not import the app's quantity or carbon functions. It independently parsed section labels, recomputed all endpoint distances, applied section area formulas, integrated the flat-bar tapers and read GWP-total directly from the raw JSON. All 736 lengths and calculated volumes agreed with the app within numerical tolerance. All 386 tapered flat bars have constant thickness, so average endpoint area times length is valid here. Every one of the five public endpoints was re-fetched; its GWP-total module values and declared quantity/unit matched the saved app response. The visible app was checked in the user's in-app browser: A1–A3, default steel, default concrete, 718/736 coverage, 6,442 kg CO₂e.

## Default A1–A3 reconciliation

| Component | Quantity | Factor per quantity unit | kg CO₂e |
|---|---:|---:|---:|
| Assigned structural steel, 671 members | 6,641.981 kg | 0.560287415 kg CO₂e/kg | 3,721.418 |
| Foundation concrete, 47 members | 11.755862 m³ | 181 kg CO₂e/m³ | 2,127.811 |
| Foundation reinforcement | 999.248 kg | 0.593 kg CO₂e/kg | 592.554 |
| Known subtotal | | | **6,441.784** |

Rebar quantity = 11.755861997 m³ × 85 kg/m³. The concrete dataset describes unreinforced concrete, so adding reinforcement separately is appropriate. The steel EPD is per 1,000 kg (560.287415289 kg CO₂e), and the app correctly divides by 1,000. Rebar A1+A2+A3 = 0.0558+0.0182+0.519 = 0.593 kg CO₂e/kg.

Member 1 separately gives V=0.002535533277 m³, mass=19.903936226 kg, A1–A3=11.151924982 kg CO₂e.

## What the totals depend on

1. **18 material conflicts remain unresolved.** Their 0.019669683 m³ is excluded. If, and only if, all 18 were confirmed as steel, they would add 154.407 kg steel and 86.512 kg CO₂e with the default dataset; the total would be 6,528.296 kg CO₂e, 1.343% higher. This sensitivity is not a material decision; no assignments were changed.
2. **Foundation C25/30 is a rule assumption.** Geometry supports 47 low-level rectangular 500×500 mm foundation segments with total length 47.023448 m, giving 11.755862 m³. The grade/material should still be checked against course drawings or the instructor. The raw foundation material fields are blank.
3. **Nominal quantities differ from display geometry.** Twelve RO 139.7×8 tube Breps match filled cylinders to about 0.01%. Their nominal hollow volume is 0.135940962 m³ versus 0.629459518 m³ of filled display solids. Using those filled solids for steel would overstate default A1–A3 by about 2,170.621 kg CO₂e. The app correctly uses hollow areas. The 116 Flat Bar 33.3/20 volumes differ from their display solids by about 2.3%; their combined nominal mass is only 12.129 kg, so this discrepancy has little effect on the total. The remaining taper/solid differences and member 1473's offset are retained for review.
4. **The default steel factor represents a particular production route.** The required profiles/bars EPD describes steel produced from 100% scrap. Its lower factor is therefore meaningful for that dataset; it does not establish that the actual pavilion steel was procured that way. The course's alternative heavy-plate factor is 2.528984485 kg CO₂e/kg, about 4.514 times the default steel factor. Switching produces a known pavilion subtotal of 19,517.833 kg CO₂e, without changing geometry. This is a dataset sensitivity comparison, not a confirmed procurement comparison.
5. **Module scope matters.** A1–A3 is the production-stage result for the inventoried members. C and D are separate. Default concrete C4 is undeclared, so the C view is partial; negative D values are not subtracted from A1–A3. Other modules/components outside the selected inventory are not included.

## Sources and evidence

- Required default steel response: https://oekobaudat.de/OEKOBAU.DAT/resource/processes/20c29cbd-f9a2-4518-a1ce-c681246c29c8?format=json&view=extended
- Default concrete response: https://oekobaudat.de/OEKOBAU.DAT/resource/processes/8347f9a7-f4ec-4a36-a266-a0281f5fd16d?format=json&view=extended
- Rebar response: https://oekobaudat.de/OEKOBAU.DAT/resource/processes/a8ebf8f2-2fcc-4431-b730-93bf5efd8111?format=json&view=extended
- `independent-double-check.json`: detailed independently calculated quantities and factors.
- `live-factor-recheck.json`: fresh endpoint comparisons and dataset scope statements.
- `independent_double_check.py`: independent arithmetic implementation, runnable from any working directory.

No Rhino geometry, material assignments, app calculations or live UI settings were changed by this check.
