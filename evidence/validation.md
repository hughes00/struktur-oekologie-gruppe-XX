# Validation record — 19 October 2026

- Ten automated numerical/data tests passed in tests.py: member reconciliation, taper hand calculation, rod/tube areas, unresolved decisions, declared steel quantity conversion, exclusive scenarios, missing concrete C4, rebar calculation, all five UUIDs and alternative steel sensitivity.
- JavaScript syntax check passed; Python application files compiled successfully.
- All five public dataset requests succeeded. The launcher-started app reported all five as live, independently checked through the local API and visible browser badge.
- Chrome displayed the 3D pavilion, default A1–A3 known subtotal 6,442 kg CO₂e, coverage 718/736, and the explicit 18-member exclusion notice.
- Switching steel to heavy plate displayed 19,518 kg CO₂e; member 1 changed 11.15 to 50.34 kg CO₂e with the same displayed geometry quantities.
- Default C displayed 47 assigned members with missing module values, complete coverage 671/736. Alternative concrete restored complete selected-module coverage to 718/736. D was shown separately, including negative values.
- Unresolved audit filter returned exactly 18 table rows and 18 visible members. Member 78 retained its original concrete label and user-requested unresolved decision.
- The browser download-event observer timed out, but the CSV was downloaded. The actual file was independently parsed: 736 rows, 18 unresolved, all unresolved carbon fields blank, and known A1–A3 subtotal 6441.7837104588725 kg CO₂e. Copy preserved as carbon-default-export.csv.
- HTTP checks returned 200 for UI assets and APIs; direct requests for the .3dm, .env and parent-directory source returned 404.
- Launcher server detection/startup was tested with browser opening mocked; it returned http://127.0.0.1:8765. The resulting app was then opened and visibly verified in Chrome. Temporary preview servers were stopped; the launcher-started local app remains available.
- Original Rhino geometry was never edited or saved. The public course-template repository was read only; no GitHub upload, tag push or OLAT submission occurred.

Limitations: no claim of human hand-check completion, final material coverage, exact as-built volumes or a full whole-life carbon assessment. Eighteen materials intentionally remain unresolved. The Python runtime is already available on this laptop; another presentation laptop needs Python 3.10+.
