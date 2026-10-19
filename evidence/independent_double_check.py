import csv,json,math,collections
from pathlib import Path
p=Path(__file__).resolve().parents[1];r=list(csv.DictReader((p/'data/member_inventory.csv').open(encoding='utf-8-sig')))
raw={f.stem:json.loads(f.read_text(encoding='utf-8'))['raw'] for f in (p/'data/epd').glob('*.json')}
def area(s):
 s=s.split('|')[0].strip()
 if s.startswith('Flat Bar '): a,b=map(float,s[9:].split('/'));return a*b*1e-6
 if s.startswith('Rectangle '): a,b=map(float,s[10:].split('/'));return a*b*1e-6
 if s.startswith('RD '): return math.pi*(float(s[3:])/1000)**2/4
 if s.startswith('RO '): d,t=map(float,s[3:].split('x'));return math.pi*(d*d-(d-2*t)**2)/4*1e-6
 raise Exception(s)
factors={}
for k,d in raw.items():
 ex=next(x for x in d['exchanges']['exchange'] if x.get('referenceFlow'))
 prop=next(x for x in ex['flowProperties'] if x.get('referenceFlowProperty'))
 gwp=next(x for x in d['LCIAResults']['LCIAResult'] if any('GWP-total' in t.get('value','') for t in x['referenceToLCIAMethodDataSet']['shortDescription']))
 vals=[x for x in gwp['other']['anies'] if 'module' in x]
 a=next((float(x['value']) for x in vals if x['module']=='A1-A3'),None)
 if a is None:a=sum(float(x['value']) for x in vals if x['module'] in ['A1','A2','A3'])
 factors[k]={'A1A3':a,'amount':ex['resultingflowAmount'],'unit':prop['referenceUnit'],'per_unit':a/float(ex['resultingflowAmount'])}
sums=collections.defaultdict(lambda:dict(n=0,volume=0,mass=0,carbon=0,solid=0))
errors=[];volumes={}
for x in r:
 L=math.dist([float(x['start_'+t+'_m']) for t in 'xyz'],[float(x['end_'+t+'_m']) for t in 'xyz'])
 if abs(L-float(x['length_m']))>1e-8:errors.append(x['rfem_member_id'])
 a=area(x['section_start']);b=area(x['section_end']) if x['section_end'] not in ('','-') else a
 V=L*(a+b)/2;volumes[x['rfem_member_id']]=V
 group='unresolved' if x['material']=='Concrete C25/30' else 'concrete' if x['section_start'].startswith('Rectangle') else 'steel'
 q=sums[group];q['n']+=1;q['volume']+=V;q['solid']+=float(x['solid_volume_m3'] or 0)
 if group=='steel':q['mass']+=V*7850;q['carbon']+=V*7850*factors['steel_default']['per_unit']
 if group=='concrete':q['mass']+=V*2400;q['carbon']+=V*factors['concrete_default']['per_unit']
 if group=='unresolved':q['mass']+=V*7850;q['carbon']+=V*7850*factors['steel_default']['per_unit']
concrete=sums['concrete']['volume'];rebar=concrete*85;rebar_c=rebar*factors['rebar_default']['per_unit'];total=sums['steel']['carbon']+sums['concrete']['carbon']+rebar_c
app=json.loads((p/'data/members.json').read_text(encoding='utf-8'))
diffs=[(x['id'],volumes[x['id']]-x['volume_m3']) for x in app if abs(volumes[x['id']]-x['volume_m3'])>1e-10]
report={'groups':dict(sums),'rebar_mass_kg':rebar,'rebar_A1A3_kgCO2e':rebar_c,'known_A1A3_subtotal':total,'conditional_total_if_18_are_steel':total+sums['unresolved']['carbon'],'unresolved_steel_sensitivity_percent':sums['unresolved']['carbon']/total*100,'factors':factors,'axis_length_mismatches':errors,'quantity_mismatches':diffs,'bounds':[[min(float(x['start_'+t+'_m']) for x in r),max(float(x['end_'+t+'_m']) for x in r)] for t in 'xyz']}
(p/'evidence/independent-double-check.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))

