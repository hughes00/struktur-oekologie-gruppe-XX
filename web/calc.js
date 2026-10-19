export function factors(d,scenario){
 if(d.scenarios.length===1)scenario=d.scenarios[0];
 if(d.scenarios.length>1&&!d.scenarios.includes(scenario))throw Error('Scenario not declared');
 const out={};for(const e of d.entries){if(e.scenario!==null&&e.scenario!==scenario)continue;if(e.module in out)throw Error('Duplicate module');out[e.module]=e.value;}return out;
}
export function contribution(m,d,stage,scenario,rebar=false){
 if(!d)return {value:0,missing:['dataset unavailable'],modules:{}};
 const f=factors(d,scenario);let quantity=rebar?m.rebar_mass_kg:m.material_group==='steel'?m.steel_mass_kg:m.volume_m3;
 if(d.declared_unit==='t')quantity/=1000;
 else if(m.material_group==='concrete'&&!rebar&&d.declared_unit==='kg'){
  const p=d.material_properties.find(x=>x.name==='gross density');if(!p)throw Error('Density missing');quantity*=Number(p.value);
 }else if((rebar||m.material_group==='steel')&&!['kg','t'].includes(d.declared_unit))throw Error('Unsupported steel unit');
 const wanted=stage==='A'?('A1-A3' in f?['A1-A3']:['A1','A2','A3']):stage==='C'?['C1','C2','C3','C4']:['D'];
 let value=0;const missing=[],modules={};for(const mod of wanted){if(f[mod]==null){missing.push(mod);modules[mod]=null;}else{modules[mod]=f[mod]*quantity/d.declared_amount;value+=modules[mod];}}
 return {value,missing,modules,quantity,declared_amount:d.declared_amount,declared_unit:d.declared_unit,dataset:d};
}
export function calculate(m,datasets,stage,steelKey,concreteKey,scenario){
 if(m.material_group==='unresolved')return {value:null,missing:['unresolved material'],parts:[]};
 const d=datasets[m.material_group==='steel'?steelKey:concreteKey]?.dataset;
 const parts=[contribution(m,d,stage,scenario)];
 if(m.material_group==='concrete')parts.push(contribution(m,datasets.rebar_default?.dataset,stage,scenario,true));
 return {value:parts.reduce((s,x)=>s+x.value,0),missing:parts.flatMap(x=>x.missing.map(y=>`${x.dataset?.label||'Dataset'}: ${y}`)),parts};
}
