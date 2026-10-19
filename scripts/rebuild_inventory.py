import Rhino, scriptcontext as sc, json, os
from System import Enum
out=os.path.join(os.path.dirname(__file__),'model_audit.json')
def pt(p): return [p.X,p.Y,p.Z]
def us(x):
    n=x.GetUserStrings()
    return dict((k,n[k]) for k in n.AllKeys) if n else {}
data={'path':sc.doc.Path,'units':str(sc.doc.ModelUnitSystem),'tolerance':sc.doc.ModelAbsoluteTolerance,'layers':[],'objects':[]}
for l in sc.doc.Layers:
    data['layers'].append({'index':l.Index,'path':l.FullPath,'id':str(l.Id),'visible':l.IsVisible,'locked':l.IsLocked,'deleted':l.IsDeleted,'userstrings':us(l)})
s=Rhino.DocObjects.ObjectEnumeratorSettings()
s.NormalObjects=True
s.HiddenObjects=True
s.LockedObjects=True
s.ReferenceObjects=True
for o in sc.doc.Objects.GetObjectList(s):
    g=o.Geometry; a=o.Attributes; b=g.GetBoundingBox(True)
    r={'id':str(o.Id),'type':str(o.ObjectType),'geometry_type':g.GetType().FullName,'layer':a.LayerIndex,'name':a.Name,'hidden':o.IsHidden,'locked':o.IsLocked,'attributes_userstrings':us(a),'geometry_userstrings':us(g),'bbox':[pt(b.Min),pt(b.Max)],'groups':list(a.GetGroupList() or []),'material_index':a.MaterialIndex,'standard_attributes':dict((p.Name,str(p.GetValue(a,None))) for p in a.GetType().GetProperties() if p.CanRead and p.GetIndexParameters().Length==0)}
    if isinstance(g,Rhino.Geometry.Curve):
        r.update({'start':pt(g.PointAtStart),'end':pt(g.PointAtEnd),'length':g.GetLength(),'closed':g.IsClosed,'linear':g.IsLinear(sc.doc.ModelAbsoluteTolerance)})
    if isinstance(g,Rhino.Geometry.Brep):
        r.update({'solid':g.IsSolid,'faces':g.Faces.Count,'edges':g.Edges.Count})
        v=Rhino.Geometry.VolumeMassProperties.Compute(g)
        if v: r.update({'volume':v.Volume,'centroid':pt(v.Centroid)})
    data['objects'].append(r)
with open(out,'w') as f: json.dump(data,f,indent=2)
print('READ-ONLY AUDIT: {} objects, {} layers; {}'.format(len(data['objects']),len(data['layers']),out))
# Reproducible inventory and verification. Read-only: no Add/Modify/Delete/Save calls.
import csv, collections, math
outdir=os.path.dirname(__file__)
key='BG_RFEM_Exchange_BeamId_bg0246'
byid=collections.defaultdict(list)
for o in data['objects']:
    mid=o['attributes_userstrings'].get(key)
    if mid: byid[mid].append(o)
checks={'objects':len(data['objects']),'layers':len(data['layers']),'unique_member_ids':len(byid),'units':data['units'],'tolerance':data['tolerance'],'source':data['path'],'errors':[],'geometry_warnings':[],'coincident_axes_different_ids':[]}
rows=[]; axes=[]
for mid,objs in sorted(byid.items(),key=lambda kv:int(kv[0])):
    aa=[o for o in objs if o['type']=='Curve']; bb=[o for o in objs if o['type']=='Brep']
    if len(aa)!=1 or len(bb)>1: checks['errors'].append('Unexpected representation counts for '+mid)
    if not aa: continue
    a=aa[0]; u=a['attributes_userstrings']; axes.append((mid,a))
    if bb:
        b=bb[0]
        if u!=b['attributes_userstrings']: checks['errors'].append('Attribute mismatch '+mid)
        if not b['solid']: checks['errors'].append('Nonclosed Brep '+mid)
        center=[(a['start'][j]+a['end'][j])/2 for j in range(3)]
        if not all(b['bbox'][0][j]-data['tolerance']<=center[j]<=b['bbox'][1][j]+data['tolerance'] for j in range(3)): checks['geometry_warnings'].append('Axis midpoint outside solid bounds '+mid)
    r={'rfem_member_id':mid,'member_type':u.get('BG_RFEM_Exchange_Type_bg0247',''),'section_start':u.get('BG_RFEM_Exchange_CrosSec_S_bg0252',''),'section_end':u.get('BG_RFEM_Exchange_CrosSec_E_bg0251',''),'material':u.get('BG_Dlubal-Name (Material)_bg0211','').strip(),'axis_guid':a['id'],'solid_guid':bb[0]['id'] if bb else '', 'axis_layer':sc.doc.Layers[a['layer']].FullPath,'solid_layer':sc.doc.Layers[bb[0]['layer']].FullPath if bb else '', 'length_m':a['length'],'solid_volume_m3':bb[0].get('volume','') if bb else '', 'representation':'axis+solid' if bb else 'axis_only','rotation':u.get('BG_RFEM_Exchange_RotAngle_bg0248',''),'start_hinge':u.get('BG_RFEM_Exchange_SHinge_bg0249',''),'end_hinge':u.get('BG_RFEM_Exchange_RHinge_bg0250','')}
    for j,k in enumerate(['x','y','z']): r['start_'+k+'_m']=a['start'][j]; r['end_'+k+'_m']=a['end'][j]
    rows.append(r)
def distance(a,b): return math.sqrt(sum((a[j]-b[j])**2 for j in range(3)))
for i,(mi,a) in enumerate(axes):
    for mj,b in axes[:i]:
        t=data['tolerance']
        if (distance(a['start'],b['start'])<=t and distance(a['end'],b['end'])<=t) or (distance(a['start'],b['end'])<=t and distance(a['end'],b['start'])<=t): checks['coincident_axes_different_ids'].append([mi,mj])
checks['axis_count']=len(axes)
checks['solid_count']=sum(1 for o in data['objects'] if o['type']=='Brep')
checks['axis_only_count']=sum(r['representation']=='axis_only' for r in rows)
checks['section_counts']=dict(collections.Counter(r['section_start'] for r in rows))
checks['geometry_counts']=dict(collections.Counter(o['geometry_type'] for o in data['objects']))
checks['populated_layers']=len(set(o['layer'] for o in data['objects']))
checks['member_objects_without_id']=[o['id'] for o in data['objects'] if ('::Members::' in sc.doc.Layers[o['layer']].FullPath or '::MemberAxes::' in sc.doc.Layers[o['layer']].FullPath) and not o['attributes_userstrings'].get(key)]
checks['missing_material_members']=sum(not r['material'] for r in rows)
checks['all_axes_linear']=all(a['linear'] for mid,a in axes)
# Compare current live object-table totals with the first enumeration.
checks['live_object_count_recheck']=len(list(sc.doc.Objects.GetObjectList(s)))
checks['geometric_check_pass']=not checks['geometry_warnings']
checks['pass']=not checks['errors'] and not checks['coincident_axes_different_ids'] and not checks['member_objects_without_id'] and checks['live_object_count_recheck']==checks['objects']
with open(os.path.join(outdir,'member_inventory.csv'),'wb') as f:
    w=csv.DictWriter(f,fieldnames=sorted(rows[0].keys())); w.writeheader(); w.writerows(rows)
with open(os.path.join(outdir,'verification.json'),'w') as f: json.dump(checks,f,indent=2)
with open(os.path.join(outdir,'model_audit.json'),'w') as f: json.dump(data,f,indent=2)
with open(os.path.join(outdir,'layer_inventory.csv'),'wb') as f:
    w=csv.writer(f); w.writerow(['layer_index','full_path','visible','locked','deleted','object_count'])
    for l in data['layers']: w.writerow([l['index'],l['path'],l['visible'],l['locked'],l['deleted'],sum(o['layer']==l['index'] for o in data['objects'])])
print('VERIFIED: {} unique RFEM members = {} axis+solid + {} axis-only. Checks passed: {}.'.format(len(rows),checks['solid_count'],checks['axis_only_count'],checks['pass']))

