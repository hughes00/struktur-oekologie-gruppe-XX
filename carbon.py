"""Auditable quantities and ILCD+EPD GWP-total calculations; standard library only."""
import csv, json, math, re, urllib.request
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
DATASETS = {
 'steel_default': ('20c29cbd-f9a2-4518-a1ce-c681246c29c8', 'Structural steel — sections and bars'),
 'steel_alternative': ('04d1311a-ae38-4bfb-8e11-8992f1ddb14f', 'Structural steel — heavy plate'),
 'concrete_default': ('8347f9a7-f4ec-4a36-a266-a0281f5fd16d', 'Concrete C25/30'),
 'concrete_alternative': ('69dc12cf-ce4d-4251-8ea3-330ed72f2f79', 'Concrete C25/30 EcoPact'),
 'rebar_default': ('a8ebf8f2-2fcc-4431-b730-93bf5efd8111', 'Reinforcing steel — bars'),
}

def section(name):
    """Area m², width/height m; input section dimensions are mm."""
    s = name.split('|')[0].strip()
    if s.startswith(('Flat Bar ', 'Rectangle ')):
        w,h = map(float, s.split(' ', 2)[2].split('/') if s.startswith('Flat Bar') else s.split(' ',1)[1].split('/'))
        return {'area':w*h/1e6, 'w':w/1000, 'h':h/1000, 'shape':'rectangle'}
    if s.startswith('RD '):
        d = float(s[3:])/1000
        return {'area':math.pi*d*d/4, 'w':d, 'h':d, 'shape':'round'}
    if s.startswith('RO '):
        d,t = [float(x)/1000 for x in re.split('[xX]',s[3:])]
        if not 0 < 2*t < d: raise ValueError('Invalid tube: '+name)
        return {'area':math.pi*(d*d-(d-2*t)**2)/4, 'w':d, 'h':d, 'shape':'tube'}
    raise ValueError('Unsupported section: '+name)

def quantities():
    members=[]
    with (ROOT/'data/member_inventory.csv').open(encoding='utf-8-sig', newline='') as f:
        for row in csv.DictReader(f):
            a=section(row['section_start']); end=row['section_end']
            b=section(end) if end not in ('','-') else a
            length=float(row['length_m'])
            if a['shape']!=b['shape']: raise ValueError('Incompatible taper')
            if a['shape']=='rectangle':
                # Integral of (w0+dw*t)(h0+dh*t) from 0 to 1.
                dw=b['w']-a['w']; dh=b['h']-a['h']
                area_mean=a['w']*a['h']+(a['w']*dh+a['h']*dw)/2+dw*dh/3
            elif a!=b: raise ValueError('Unimplemented circular taper')
            else: area_mean=a['area']
            volume=length*area_mean
            original=row['material']; concrete=row['section_start'].startswith('Rectangle ')
            # Foundation rule uses both section and low elevation, not section alone.
            low=max(float(row['start_z_m']),float(row['end_z_m'])) < 1.1
            if concrete and not low: raise ValueError('Rectangle requires human review')
            group='concrete' if concrete else 'steel'
            conflict=bool(original and ('Concrete' in original)!=(group=='concrete'))
            reason=('500×500 rectangular member below 1.1 m: foundation concrete C25/30 (rule assumption).'
                    if concrete else 'Flat bar, circular hollow section or RD tension rod: structural steel (course material-group rule).')
            if conflict: reason+=' Exported Concrete C25/30 contradicts thin flat-bar geometry. User explicitly requested keeping this unresolved; excluded from carbon totals.'
            solid=float(row['solid_volume_m3']) if row['solid_volume_m3'] else None
            delta=(volume/solid-1)*100 if solid else None
            warnings=[]
            if conflict: warnings.append('Material label conflict — human review')
            if row['rfem_member_id']=='1473': warnings.append('Solid offset from analytical axis ≈179 mm')
            if delta is not None and abs(delta)>2: warnings.append('Analytical/solid volume difference >2%')
            members.append({**row,'id':row['rfem_member_id'],'start':[float(row['start_'+x+'_m']) for x in 'xyz'],
                'end':[float(row['end_'+x+'_m']) for x in 'xyz'],'length':length,'start_section':a,'end_section':b,
                'area_start_m2':a['area'],'area_end_m2':b['area'],'volume_m3':volume,
                'volume_method':'linear section-dimension integration' if a!=b else 'constant area × axis length',
                'tapered':a!=b,'solid_volume':solid,'volume_difference_percent':delta,
                'material_group':'unresolved' if conflict else group,'assigned_material':'Unresolved' if conflict else ('Concrete C25/30' if concrete else 'Structural steel'),
                'assignment_source':'human: keep unresolved; rule/LLM suggests steel' if conflict else 'rule',
                'assignment_reason':reason,'human_review_required':conflict,
                'density_kg_m3':None if concrete else 7850,
                'steel_mass_kg':volume*7850 if not concrete and not conflict else 0,
                'rebar_mass_kg':volume*85 if concrete else 0,'warnings':warnings})
    if len(members)!=736 or len({m['id'] for m in members})!=736: raise ValueError('Member count changed; re-audit required')
    return members

def text(value):
    if isinstance(value,list): return ' / '.join(text(x) for x in value)
    if isinstance(value,dict): return str(value.get('value',''))
    return str(value)

def parse_dataset(raw, key, fetched_at):
    uuid,label=DATASETS[key]
    info=raw['processInformation']['dataSetInformation']
    if info['UUID']!=uuid: raise ValueError('Dataset UUID mismatch')
    refs=raw['processInformation']['quantitativeReference']['referenceToReferenceFlow']
    exchanges=[x for x in raw['exchanges']['exchange'] if x.get('referenceFlow') or x.get('dataSetInternalID') in refs]
    if len(exchanges)!=1: raise ValueError('Expected one declared reference flow')
    ex=exchanges[0]
    props=[x for x in ex['flowProperties'] if x.get('referenceFlowProperty')]
    if len(props)!=1: raise ValueError('Ambiguous declared unit')
    p=props[0]; unit=p['referenceUnit']; amount=float(ex['resultingflowAmount'])
    if amount<=0 or unit not in ('kg','m3','m^3','m³','t'): raise ValueError('Unsupported declared unit '+unit)
    results=[x for x in raw['LCIAResults']['LCIAResult'] if 'GWP-total' in text(x['referenceToLCIAMethodDataSet']['shortDescription'])]
    if len(results)!=1: raise ValueError('Exactly one GWP-total indicator required')
    entries=[{'module':x['module'],'scenario':x.get('scenario'),'value':float(x['value']) if x.get('value') is not None else None}
             for x in results[0]['other']['anies'] if 'module' in x]
    if any(x['value'] is not None and not math.isfinite(x['value']) for x in entries): raise ValueError('Nonfinite factor')
    others=raw['processInformation'].get('other',{})
    return {'key':key,'uuid':uuid,'label':label,'name':text(info['name']['baseName']),
      'version':raw['administrativeInformation']['publicationAndOwnership'].get('dataSetVersion'), 'declared_unit':unit,'declared_amount':amount,
      'indicator':'GWP-total','indicator_unit':'kg CO2e','fetched_at':fetched_at,
      'source_url':f'https://oekobaudat.de/OEKOBAU.DAT/resource/processes/{uuid}?format=json&view=extended',
      'entries':entries,'scenarios':sorted({x['scenario'] for x in entries if x['scenario']}),
      'material_properties':ex.get('materialProperties',[]),
      'scenario_metadata':info.get('other',{}),
      'general_comment':text(info.get('generalComment',[]))}

def fetch_dataset(key):
    uuid,_=DATASETS[key]
    url=f'https://oekobaudat.de/OEKOBAU.DAT/resource/processes/{uuid}?format=json&view=extended'
    req=urllib.request.Request(url,headers={'Accept':'application/json','User-Agent':'Stockerau-Carbon-Inventory/1.0'})
    with urllib.request.urlopen(req,timeout=45) as r: raw=json.load(r)
    timestamp=datetime.now(timezone.utc).isoformat()
    parsed=parse_dataset(raw,key,timestamp)
    folder=ROOT/'data/epd'; folder.mkdir(exist_ok=True)
    (folder/(key+'.json')).write_text(json.dumps({'fetched_at':timestamp,'raw':raw},ensure_ascii=False,indent=2),encoding='utf-8')
    return parsed

def cached_dataset(key):
    saved=json.loads((ROOT/'data/epd'/f'{key}.json').read_text(encoding='utf-8'))
    return parse_dataset(saved['raw'],key,saved['fetched_at'])

def module_factors(dataset, scenario='S1'):
    """Never sum mutually exclusive scenarios; absent modules remain absent."""
    if len(dataset['scenarios'])==1: scenario=dataset['scenarios'][0]
    elif dataset['scenarios'] and scenario not in dataset['scenarios']: raise ValueError('Select a declared scenario')
    result={}
    for e in dataset['entries']:
        if e['scenario'] not in (None,scenario): continue
        if e['module'] in result: raise ValueError('Duplicate applicable module '+e['module'])
        result[e['module']]=e['value']
    return result

def carbon_for(member, dataset, scenario='S1', rebar=False):
    if member['material_group']=='unresolved': return {}
    unit=dataset['declared_unit']
    if rebar: quantity=member['rebar_mass_kg']
    elif member['material_group']=='steel': quantity=member['steel_mass_kg']
    else: quantity=member['volume_m3']
    if unit=='t': quantity/=1000
    elif member['material_group']=='concrete' and not rebar and unit=='kg':
        density=next((float(x['value']) for x in dataset['material_properties'] if x['name']=='gross density'),None)
        if density is None: raise ValueError('Concrete mass conversion requires dataset density')
        quantity*=density
    elif (member['material_group']=='steel' or rebar) and unit not in ('kg','t'):
        raise ValueError('Steel requires mass-declared dataset')
    return {k:v*quantity/dataset['declared_amount'] if v is not None else None for k,v in module_factors(dataset,scenario).items()}

if __name__=='__main__':
    members=quantities()
    (ROOT/'data/members.json').write_text(json.dumps(members,ensure_ascii=False,indent=2),encoding='utf-8')
    fields=['id','section_start','section_end','length','area_start_m2','area_end_m2','volume_m3','volume_method','solid_volume','volume_difference_percent','material','assigned_material','assignment_source','assignment_reason','human_review_required','steel_mass_kg','rebar_mass_kg']
    with (ROOT/'data/member_quantities.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(members)
    print(json.dumps({'members':len(members),'tapered':sum(m['tapered'] for m in members),'concrete':sum(m['material_group']=='concrete' for m in members),'human_review':sum(m['human_review_required'] for m in members),'volume_warnings':sum(any('volume' in w for w in m['warnings']) for m in members)},indent=2))
