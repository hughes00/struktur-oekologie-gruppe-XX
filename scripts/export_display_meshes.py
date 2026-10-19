# Run in Rhino 8. Reads Breps and creates meshes in memory only.
import Rhino, scriptcontext as sc, json, os
folder=os.path.join(os.path.dirname(os.path.dirname(__file__)),'web')
result={}
settings=Rhino.DocObjects.ObjectEnumeratorSettings()
settings.NormalObjects=True;settings.HiddenObjects=True;settings.LockedObjects=True;settings.ReferenceObjects=True
for o in sc.doc.Objects.GetObjectList(settings):
    mid=o.Attributes.GetUserString('BG_RFEM_Exchange_BeamId_bg0246')
    if not mid or not isinstance(o.Geometry,Rhino.Geometry.Brep): continue
    verts=[];faces=[]
    for mesh in Rhino.Geometry.Mesh.CreateFromBrep(o.Geometry,Rhino.Geometry.MeshingParameters.FastRenderMesh):
        offset=len(verts)//3
        for v in mesh.Vertices: verts.extend([round(v.X,6),round(v.Y,6),round(v.Z,6)])
        for f in mesh.Faces:
            faces.extend([offset+f.A,offset+f.B,offset+f.C])
            if f.IsQuad: faces.extend([offset+f.A,offset+f.C,offset+f.D])
    result[mid]={'vertices':verts,'indices':faces}
with open(os.path.join(folder,'meshes.json'),'w') as f:json.dump(result,f,separators=(',',':'))
print('READ-ONLY display export: {} member meshes; source geometry unchanged.'.format(len(result)))
