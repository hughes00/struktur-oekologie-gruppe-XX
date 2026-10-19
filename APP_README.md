# Stockerau · Carbon Atlas

Local web app for Vibe Coding Studio · SE Structure and Ecology · Sprint 1.

## Open the app

On this Windows laptop, double-click **START_APP.vbs**. It starts a hidden local Python server and opens the app in your browser. No OpenAI key, Cline, npm or paid service is needed. Python's standard library is sufficient.

On another laptop with Python 3.10 or later:

```text
python launch.pyw
```

Or run `python server.py` and open `http://127.0.0.1:8765` manually. Keep that server running during the presentation. Stop a manually started server with Ctrl+C. Internet access is required for fresh ÖKOBAUDAT responses; timestamped saved responses keep the app usable offline and are labelled as cached. Three.js is bundled locally under its MIT licence.

## What is implemented

- 736 unique RFEM member IDs; solids and axes reconciled without double-counting.
- All member areas and volumes, including 386 linear flat-bar tapers, 175 axis-only rods and hollow tube sections.
- Material assignments with rule, model-label, language-model and human-decision provenance. Original labels preserved.
- Five required ÖKOBAUDAT UUIDs, fetched through extended JSON, GWP-total only, declared quantity/unit conversion, exclusive end-of-life scenarios, missing-module handling and 85 kg/m³ foundation rebar.
- 3D meshes from the unmodified Rhino Breps plus generated axis-only rods. Click to inspect; orbit, zoom, plan view, isolate and search.
- Dataset alternatives and separate A1–A3 / C1–C4 / D views, carbon CSV export and an audit lens for unresolved materials, volume discrepancies and tapers.

## Deliberately incomplete decisions

**18 thin flat bars labelled concrete remain unresolved at the user's explicit request.** They stay in the inventory and viewer but are excluded from carbon subtotals. Thus the assignment's requirement to assign every member a material is not yet fulfilled. The known A1–A3 subtotal is approximately 6,441.784 kg CO₂e using the saved default factors, not a complete pavilion total.

47 low-level rectangular members are assigned foundation concrete C25/30 by rule; this grade is an assumption. Human review can be recorded in the passport and exported; browser reviews do not change source data or Rhino.

The default concrete EPD has an undeclared C4 value. C is therefore a known partial sum with 47 members lacking complete C1–C4 coverage. D can be negative and is never subtracted from A1–A3. The course does not request A4/A5/B in the app; this is not a whole-life assessment.

Quantities use nominal section dimensions and analytical lengths. All 12 tube Breps appear filled, 116 small flat bars differ from nominal calculated volume by more than 2%, and member 1473's solid is offset from its axis. The comparison is exposed, not silently corrected. Volume assumptions and tests are in evidence/stage-tests.md.

## Test and reproduce

```text
python carbon.py
python tests.py
python scripts/fetch_epds.py
python -X utf8 scripts/make_evidence.py
```

Run `scripts/rebuild_inventory.py` in Rhino via RunPythonScript to repeat the read-only document audit, and `scripts/export_display_meshes.py` to rebuild the viewer meshes. The inventory script writes its outputs beside itself; copy the generated inventory/audit files into `data/` and run `python carbon.py`. Neither script saves or edits Rhino geometry.

`data/member_quantities.csv` contains quantities and default material decisions; the app's CSV export adds the active carbon results, chosen datasets, module, fetch timestamps and browser human reviews. `data/epd/` preserves raw timestamped live responses. These snapshots are evidence, not a claim of current factors on every later opening.

## Presentation and submission

Use `evidence/stage-tests.md`, `evidence/PRESENTATION.md` and the browser screenshots for stages 1–4; demonstrate the app live for stage 5. LOGBUCH.md records actual test results and open work. Do not claim the agent's hand-calculation example as a check you personally performed until you review it.

The existing Desktop folder points at **the public course template**, `AlinaSchuster/struktur-oekologie-gruppe-XX`. Do not push this model or this project there. Create your own **private** repository before uploading any files. Commit/push/tag milestones honestly: Stage 3 remains incomplete while the 18 material assignments are unresolved; later functionality is implemented but the full assignment is not yet finished. No GitHub upload or OLAT submission has been performed by this project.

Deadline: Friday 23 October 2026, 12:00 Europe/Vienna. Submit only the private repository link to the specified OLAT assignment, and ensure the instructor has the required access through the course's instructions.
