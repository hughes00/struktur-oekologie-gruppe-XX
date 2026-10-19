import math, unittest
from carbon import quantities, section, cached_dataset, module_factors, carbon_for

class AssignmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.members=quantities(); cls.byid={m['id']:m for m in cls.members}
    def test_inventory_and_representation_reconciliation(self):
        self.assertEqual(len(self.members),736);self.assertEqual(len(self.byid),736)
        self.assertEqual(sum(m['representation']=='axis_only' for m in self.members),175)
        self.assertEqual(sum(m['tapered'] for m in self.members),386)
    def test_taper_hand_calculation_member_1(self):
        # Independent endpoint distance, dimensions in mm -> m², trapezoidal integral.
        length=math.sqrt((2.5-1.666666666666667)**2+(4-4.141)**2)
        v=length*((275*12+225*12)/2)/1_000_000
        self.assertAlmostEqual(self.byid['1']['volume_m3'],v,places=12)
    def test_round_and_hollow_sections(self):
        self.assertAlmostEqual(section('RD 12')['area'],math.pi*0.012**2/4)
        self.assertAlmostEqual(section('RO 139.7x8.0 | EN 10210-2:2006')['area'],math.pi*(.1397**2-.1237**2)/4)
        self.assertLess(section('RO 139.7x8.0')['area'],math.pi*.1397**2/4)
    def test_user_requested_unresolved_materials(self):
        unresolved=[m for m in self.members if m['material_group']=='unresolved']
        self.assertEqual(len(unresolved),18)
        self.assertTrue(all(m['material']=='Concrete C25/30' for m in unresolved))
        self.assertTrue(all(m['steel_mass_kg']==0 for m in unresolved))
        self.assertEqual(carbon_for(unresolved[0],cached_dataset('steel_default')), {})
    def test_declared_tonne_conversion_and_hand_carbon(self):
        d=cached_dataset('steel_default');self.assertEqual(d['declared_unit'],'kg');self.assertEqual(d['declared_amount'],1000)
        m=self.byid['1'];expected=m['volume_m3']*7850/1000*560.287415289044
        self.assertAlmostEqual(carbon_for(m,d)['A1-A3'],expected,places=10)
    def test_scenarios_are_exclusive(self):
        d=cached_dataset('steel_default');a=module_factors(d,'S1');b=module_factors(d,'S2')
        self.assertAlmostEqual(a['D'],284.967329927546)
        self.assertAlmostEqual(b['D'],-557.360309337828)
        self.assertNotEqual(a['D'],sum(e['value'] for e in d['entries'] if e['module']=='D'))
    def test_missing_concrete_module_not_zero(self):
        self.assertIsNone(module_factors(cached_dataset('concrete_default'))['C4'])
    def test_rebar_separate_a_modules_and_mass(self):
        m=next(m for m in self.members if m['material_group']=='concrete')
        d=cached_dataset('rebar_default');v=carbon_for(m,d,rebar=True)
        self.assertAlmostEqual(m['rebar_mass_kg'],85*m['volume_m3'])
        self.assertAlmostEqual(sum(v[k] for k in ['A1','A2','A3']),m['rebar_mass_kg']*(.0558+.0182+.519))
    def test_all_five_required_datasets(self):
        for k in ['steel_default','steel_alternative','concrete_default','concrete_alternative','rebar_default']:
            d=cached_dataset(k);self.assertEqual(d['indicator'],'GWP-total');self.assertGreater(d['declared_amount'],0)
    def test_switch_steel_changes_carbon_not_quantities(self):
        m=self.byid['1'];v=m['volume_m3']
        a=carbon_for(m,cached_dataset('steel_default'))['A1-A3'];b=carbon_for(m,cached_dataset('steel_alternative'))['A1-A3']
        self.assertGreater(b,a);self.assertEqual(m['volume_m3'],v)
        self.assertAlmostEqual(b/a,2528.98448544598/560.287415289044)

if __name__=='__main__': unittest.main(verbosity=2)
