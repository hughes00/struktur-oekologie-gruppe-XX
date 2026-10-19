# Friday presentation — suggested speaking sequence

## 1. Read the model
Show the Rhino audit or model view and explain: 736 RFEM IDs = 561 axis+solid pairs + 175 axis-only tension rods. Layout content is excluded. Show the inventory and the ID grouping method.

## 2. Understand sections
Use member 1's passport. Read the taper example in stage-tests.md and reproduce the arithmetic on paper: 275×12 → 225×12 mm, L=0.845177759081 m, V=0.002535533277 m³. Explain why a hollow tube is not a solid cylinder. Acknowledge nominal/solid quantity differences.

## 3. Assign materials
Choose “Unresolved material” in the audit lens, then member 78. Show the original Concrete C25/30 label, thin flat-bar dimensions, proposed steel reasoning and the user's decision to keep it unresolved. State clearly that 18 materials are still open; do not present the assignment as finished.

## 4. Live carbon factors
Show the dataset source card and declared quantity. Member 1 is 19.903936226 kg steel; 560.287415289044 kg CO₂e per 1,000 kg gives 11.151924982 kg CO₂e. Show the timestamp and refresh control. Explain rebar 85 kg/m³, missing C4 and separate module D.

## 5. Live web app
Start with A1–A3, default steel and default concrete. Predict that heavy plate will increase the subtotal. Switch steel to the alternative: known subtotal approximately 6,442 → 19,518 kg CO₂e, with unchanged quantities. Orbit the model, click a member, show its passport, then switch C and D. Show the audit lens as the extra idea and export CSV.

## Before presenting
Double-click START_APP.vbs on the presentation laptop. Try the app once with internet and once offline to recognize the cached-data label. Keep the browser and local server running. Review the hand calculations with your partner. Save final human decisions to the project, not only browser storage, before claiming full material coverage. Create and push milestone tags only when their stages are truly complete, in your own private repository.

## Existing screenshots
- app-default.jpg — default A1–A3 view and 3D pavilion.
- app-steel-alternative.jpg — alternative steel result.
- app-unresolved.jpg — unresolved-material audit filter.

Screenshots are actual browser captures; numerical evidence is in stage-tests.md and test-values.json.
