import sys,json,math,shutil
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from carbon import *
m=quantities();byid={x['id']:x for x in m};example=byid['1'];ds={k:cached_dataset(k) for k in DATASETS}
snapshot=ROOT/'evidence/epd-test-snapshot';snapshot.mkdir(exist_ok=True)
for key in DATASETS:shutil.copyfile(ROOT/'data/epd'/f'{key}.json',snapshot/f'{key}.json')
def a13(values): return values.get('A1-A3',sum(values.get(k,0) or 0 for k in ['A1','A2','A3']))
def total(steel):
    result=0
    for x in m:
        if x['material_group']=='unresolved':continue
        result+=a13(carbon_for(x,ds[steel if x['material_group']=='steel' else 'concrete_default'],'S3'))
        if x['material_group']=='concrete':result+=a13(carbon_for(x,ds['rebar_default'],'S3',True))
    return result
default=total('steel_default');alt=total('steel_alternative')
conflict=next(x for x in m if x['material_group']=='unresolved')
hand_length=math.sqrt((2.5-1.666666666666667)**2+(4-4.141)**2)
hand_volume=hand_length*(275*12+225*12)/2/1e6
hand_mass=hand_volume*7850
hand_carbon=hand_mass/1000*560.287415289044
notes=f'''# Stage tests — Stockerau Pavilion

## Stage 1 — member count
Read-only Rhino enumeration: 2,986 objects, 330 layers, 56 populated. All 1,297 model-space objects are structural representations; 1,689 page-space objects are drawing/layout content. RFEM ID grouping: 561 axis+solid pairs + 175 axis-only tension members = **736 unique member entities**. No coincident axes under different IDs. Original geometry unchanged.

## Stage 2 — independent hand calculation, member 1
Start (8.48, 2.5, 4.0) m; end (8.48, 1.666666666666667, 4.141) m.

- L = sqrt((2.5 − 1.666666666666667)² + (4.141 − 4.0)²) = {hand_length:.12f} m.
- Start section 275 × 12 mm: A0 = 0.003300 m².
- End section 225 × 12 mm: A1 = 0.002700 m².
- Constant thickness and linear width change: V = L × (A0 + A1)/2 = **{hand_volume:.12f} m³**.
- Program: {example['volume_m3']:.12f} m³. Difference: {abs(hand_volume-example['volume_m3']):.3g} m³.
- Rhino display Brep: {example['solid_volume']:.12f} m³, a {example['volume_difference_percent']:.6f}% difference from nominal axis calculation. Do not hide this discrepancy.

There are 386 changing sections, all flat bars with constant thickness. The general implementation integrates both rectangular dimensions linearly (including the cross-term), rather than assuming averaging endpoint areas is valid for every taper. RD rods use πd²/4. Hollow tubes use π(D²−(D−2t)²)/4. The 12 tube Breps appear filled and overstate steel volume if used directly. 116 Flat Bar 33.3/20 members differ from Brep volumes by >2%; nominal labels and the discrepancy are retained. Analytical quantities are the app's declared basis, not exact as-built quantities.

## Stage 3 — material plausibility test
Example member **{conflict['id']}**, section {conflict['section_start']} to {conflict['section_end']}, is labelled Concrete C25/30. Its thin flat-bar form and the course material grouping suggest steel, so blindly copying the exported material is implausible. Rules proposed steel; language-model review flagged the contradiction. The user explicitly chose **keep unresolved**, so all 18 conflicting members remain unresolved and are excluded from carbon subtotals. This is a documented open decision, not a completed full material assignment.

The other 671 steel members use a section-family rule; 47 low-level Rectangle 500/500 members use a foundation rule (assumed C25/30). The 12 exported S355 tube labels agree with their section family. Original labels remain unchanged. UI human reviews record reason and timestamp locally and export with provenance.

## Stage 4 — hand A1–A3 calculation, member 1
Using the Stage 2 volume:

- Steel mass = {hand_volume:.12f} m³ × 7,850 kg/m³ = {hand_mass:.9f} kg.
- Dataset {DATASETS['steel_default'][0]}, version {ds['steel_default']['version']}.
- Live response fetched at {ds['steel_default']['fetched_at']}.
- GWP-total A1–A3 = 560.287415289044 kg CO₂e per **1,000 kg** steel.
- Result = {hand_mass:.9f}/1,000 × 560.287415289044 = **{hand_carbon:.9f} kg CO₂e**.
- Program = {carbon_for(example,ds['steel_default'])['A1-A3']:.9f} kg CO₂e.

All five assignment UUIDs are fetched through the required extended JSON endpoint. Concrete is per 1 m³; steel defaults/alternative are per 1,000 kg; rebar is per 1 kg. Foundation contribution includes 85 kg rebar per m³ concrete. Rebar declares A1, A2 and A3 separately, so they are summed once. Other EPDs declare A1–A3 together. Concrete default C4 is undeclared, so C totals are marked partial; missing values are not silently zero. Steel scenarios are mutually exclusive; default S3 is the EPD European-average scenario. Sole scenarios in EcoPact/rebar are selected explicitly by the parser. D remains separate.

## Stage 5 — dataset switch prediction and result
Prediction before switching: the heavy-plate dataset has a higher A1–A3 factor than profiles/bars; steel carbon should increase while geometry, volumes, concrete and rebar quantities remain unchanged. This is a dataset sensitivity comparison, not proof that heavy plate is an interchangeable specification for every section.

Saved live-factor test, excluding the 18 unresolved members:

- Profiles/bars + default concrete + rebar: **{default:.6f} kg CO₂e** A1–A3.
- Heavy plate + default concrete + rebar: **{alt:.6f} kg CO₂e** A1–A3.
- Increase: **{alt-default:.6f} kg CO₂e**, or {(alt/default-1)*100:.3f}% of the known pavilion subtotal.
- Factors: {module_factors(ds['steel_default'])['A1-A3']:.9f} vs {module_factors(ds['steel_alternative'])['A1-A3']:.9f} per 1,000 kg. Steel-only factor ratio: {module_factors(ds['steel_alternative'])['A1-A3']/module_factors(ds['steel_default'])['A1-A3']:.6f}.

Own idea: audit lens links material conflicts, taper geometry and volume/axis discrepancies directly to the 3D member and its calculation passport. CSV export includes current module, dataset UUIDs, factor-fetch timestamps, material provenance and incomplete-status markers.

## Remaining assignment work
18 human material decisions intentionally remain open. Git commits/tags/pushes and OLAT submission are separate from implementation and must not be claimed as completed without evidence. The private source .3dm must never be pushed to a public repository. Present these documented tests as agent-prepared calculations, and independently review them with your partner before claiming personal verification.
'''
(ROOT/'evidence/stage-tests.md').write_text(notes,encoding='utf-8')
(ROOT/'evidence/test-values.json').write_text(json.dumps({'hand_member':example['id'],'hand_volume':hand_volume,'hand_mass':hand_mass,'hand_carbon_A1A3':hand_carbon,'default_A1A3_known_subtotal':default,'alternative_A1A3_known_subtotal':alt,'unresolved_members':18,'live_dataset_snapshots':{k:{'version':d['version'],'fetched_at':d['fetched_at'],'unit':d['declared_unit'],'quantity':d['declared_amount']} for k,d in ds.items()}},indent=2),encoding='utf-8')
print(notes)
