# Carbon Inventory — Stockerau Pavilion: Stage 1

## Result
736 unique RFEM structural members in the open Rhino model. This is the count of exported RFEM member entities, not a claim about fabrication assemblies or continuous physical pieces spanning multiple RFEM elements.

Source: C:\Users\hughe\Downloads\Stockerau Rhino Export from RFEM.3dm
Units: meters. Absolute model tolerance: 0.00001 m.

## Entire-document audit
330 layers inspected, 56 populated. 2,986 objects enumerated, including normal, hidden, locked and reference objects. No enumerated objects were hidden or locked. Empty template layers were retained in the layer inventory.

| Geometry | Count |
|---|---:|
| LineCurve | 1462 |
| NurbsCurve | 39 |
| PolylineCurve | 13 |
| ArcCurve | 11 |
| PolyCurve | 3 |
| Brep | 561 |
| TextEntity | 642 |
| Hatch | 245 |
| DetailView | 10 |
| Total | 2986 |

The RFEM Members and MemberAxes branches contain all 1,297 member-representation objects. The remaining 1,689 objects occur in layout/title-block/drafting branches, including three detail views on the parent 2__B+G layer. They have no RFEM member ID and are excluded from the structural inventory.

Attributes inspected include object GUID, geometry class, layer, name, visibility, locking, groups, material index, standard public object-attribute properties, geometry user strings and all object user strings. The member metadata keys contain RFEM member ID, type, start/end section, material, rotation, start/end hinge and comments. The JSON audit preserves the extracted data for each object. Complex standard attribute properties are recorded as their string representations; this is not a lossless serialization of arbitrary plugin data.

## The two representations
Under 2__B+G::03_3D::RFEM_Export_260915:
- Members contains 561 closed Breps: the section/solid representations.
- MemberAxes contains 736 straight LineCurves: the analytical member axes.

561 IDs each have exactly one axis and one solid. Another 175 IDs have only one axis, with section RD 12 and RFEM type Tension. There are no solid-only IDs.

Therefore 1,297 geometric representations - 561 paired representations = **736 unique members**. Equivalently: 561 axis-plus-solid members + 175 axis-only members = 736.

## Identification and verification
The authoritative grouping key is the object user string BG_RFEM_Exchange_BeamId_bg0246. The script groups all objects by this ID, checks representation cardinalities, compares the complete user-string dictionaries of each axis/solid pair, and counts each ID once. Layer names corroborate the two representation classes; they are not used as a substitute for identity.

Verified in the active Rhino document:
- 736 IDs and exactly 736 member axes.
- 561 closed solid Breps; all paired user-string dictionaries match.
- No member-branch object lacks a member ID.
- No two axes of different IDs have the same endpoints in either direction within model tolerance.
- All member axes are linear.
- A second live object-table enumeration again returns 2,986 objects.
- CSV contains exactly 736 data rows, one per member ID.

Count/identity checks pass. A separate geometric screening flags one issue: member 1473 has axis x=16, y=0, z=0.85 to 4 m; the solid centroid is approximately x=15.829101, y=-0.051780, z=2.424981 m. The horizontal offset is approximately 0.17857 m. The matching RFEM ID and metadata support counting this as one member; its geometric discrepancy remains unresolved and has not been corrected.

## Section totals
| Section | Unique members |
|---|---:|
| Flat Bar 162.5/12 | 35 |
| Flat Bar 162.5/20 | 18 |
| Flat Bar 175/12 | 35 |
| Flat Bar 175/20 | 23 |
| Flat Bar 200/12 | 35 |
| Flat Bar 200/20 | 18 |
| Flat Bar 225/12 | 35 |
| Flat Bar 225/20 | 23 |
| Flat Bar 237.5/12 | 35 |
| Flat Bar 237.5/20 | 18 |
| Flat Bar 275/12 | 70 |
| Flat Bar 275/20 | 41 |
| Flat Bar 33.3/20 | 116 |
| RD 12 | 175 |
| RO 139.7x8.0, EN 10210-2:2006 | 12 |
| Rectangle 500/500 | 47 |
| Total | 736 |

## Carbon-inventory limitations
706 member IDs have blank material metadata. Twelve explicitly specify Steel S 355 and eighteen specify Concrete C25/30. Do not infer the remaining materials solely from shape. Axis length and solid volume are preserved where available; the 175 axis-only tension members have no solid volume. This stage does not calculate carbon factors, densities or embodied carbon.

## Reproduction and files
Run rebuild_inventory.py in Rhino 8 using RunPythonScript while this model is active. It reads the current document and writes member_inventory.csv, layer_inventory.csv, model_audit.json and verification.json beside the script. Rerunning overwrites those generated outputs. It contains no document geometry Add/Modify/Delete or Save calls.

No original geometry, attributes or layers were changed, and the source 3dm was not saved. Deliverables are in this chat's workspace outputs folder; the source model remains in Downloads.
