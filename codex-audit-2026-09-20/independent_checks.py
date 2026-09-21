"""Independent audit checks. Reads the manuscript; writes only this audit folder."""
from pathlib import Path
import json, math, re, hashlib
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
checks = []
def record(name, explanation, values):
    checks.append(dict(name=name, explanation=explanation, values=values))

record('Reynolds number retains density dependence',
       'For neutral hard spheres, lambda=1/(sqrt(2)*n*sigma), so Re=3*U*L*sqrt(2)*n*sigma/v_th.',
       {'Re_after_doubling_n_over_before':2, 'Re_for_Ma_1e_6_Kn_1e_4_using_book_scaling':3e-6/1e-4})
record('Solar oscillation counterexample to a luminosity bound',
       'Illustrative sinusoidal displacement, not a measured solar amplitude. Oscillatory acceleration need not imply secular contraction power.',
       {'amplitude_cm':100, 'period_s':300, 'acceleration_over_surface_g':(2*math.pi/300)**2*100/2.742e4})
record('Buoyancy period consistency',
       'Table 1 labels its microhertz entries N/(2*pi). The Ledoux entry is larger than the Schwarzschild maximum used for the universal period claim.',
       {'Schwarzschild_period_minutes':1/(430.06e-6)/60,'Ledoux_table_entry_period_minutes':1/(453.84e-6)/60})
alpha, A, m, cd = .038, 1., .5, .77
record('Time-dependent Rayleigh-Taylor acceleration',
       'For R=C*t^m, g=m*(1-m)*C*t^(m-2). Applying the earlier chapter\'s Read-type integral h=alpha*A*(integral sqrt(g) dt)^2 from zero gives h/R=4*alpha*A*(1-m)/m. This is a counterexample to the claimed substitution/bound, not a validated supernova-shell model.',
       {'m':m,'alpha':alpha,'A':A,'Rcd_over_Rbw':cd,
        'instantaneous_substitution_h_over_Rbw':alpha*A*m*(1-m)*cd,
        'integral_scaling_h_over_Rbw':4*alpha*A*(1-m)/m*cd,
        'ratio':4/m**2})
record('Lower bound logic',
       'A predicted accretion rate above a lower limit satisfies that inequality.',
       {'prediction':8.02e-6,'lower_limit':2e-8,'ratio':8.02e-6/2e-8,'satisfies_lower_limit':8.02e-6>=2e-8})
record('Lognormal density mode',
       'For s=ln(x) Gaussian with mean -sigma_s^2/2 and variance sigma_s^2=ln(1+b^2*M^2), median(x)=exp(-sigma_s^2/2), mode(x)=exp(-3*sigma_s^2/2).',
       {'M':10,'b':1,'median':101**(-.5),'density_mode':101**(-1.5),'ratio_median_to_mode':101})
record('Circularisation is not a ballistic turning radius',
       'For a parabolic orbit E=0, l^2/(2*R_p^2)-GM/R_p=0, so R_p=l^2/(2*GM)=R_circ/2.',
       {'R_pericentre_over_R_circ':.5})
record('MRI viscosity parameter inequality',
       'If alpha_obs>=0.1 and 0<alpha_sim<=0.02, the ratio is >=5, not <=5.',
       {'minimum_ratio':.1/.02,'example_smaller_simulation_alpha':.005,'corresponding_ratio':.1/.005})
record('Plasma beta does not locate the Alfven surface',
       'M_A^2=(gamma*beta/2)*M_s^2. At M_A=1, beta=2/(gamma*M_s^2).',
       {'gamma':5/3,'sonic_Mach_number':10,'beta_at_Alfven_surface':2/((5/3)*100)})
record('A viscosity upper bound does not exclude a smaller coefficient',
       'A coefficient 1/5.941e25 is below 1e-3; the paper\'s one-sided constraint does not establish the manuscript\'s claimed lower bound.',
       {'classical_perpendicular_ratio':1/5.941e25,'satisfies_upper_bound_1e_3':1/5.941e25<=1e-3})
record('M11 radial decades',
       'Using Module 9\'s Bondi radius 197000 r_s and circularisation radius 100 r_s.',
       {'ratio':197000/100,'decades':math.log10(197000/100)})
record('Gyrophase versus orbit count',
       'When omega is an angular frequency, the complete-orbit count in time tau is omega*tau/(2*pi).',
       {'omega_tau':4.3087e12,'complete_orbits':4.3087e12/(2*math.pi)})

mechanical={'bare_carriage_returns':[], 'broken_local_links':[], 'rhetorical_counts':{}}
phrases=['refuted','confirmed','owes','owed','debt','paid','shipped','nothing else','by construction','not fetched']
for p in sorted((ROOT/'afd').glob('module[0-9][0-9].html')):
    raw=p.read_bytes()
    for match in re.finditer(rb'\r(?!\n)',raw):
        i=match.start()
        mechanical['bare_carriage_returns'].append({'file':p.name,'line':raw[:i].count(b'\n')+1,'context':repr(raw[max(0,i-35):i+45].decode('utf8'))})
    soup=BeautifulSoup(raw.decode('utf8'),'html.parser')
    for tag in soup(['script','style','svg']):tag.decompose()
    text=soup.get_text(' ',strip=True).lower()
    mechanical['rhetorical_counts'][p.name]={phrase:len(re.findall(r'\b'+re.escape(phrase)+r'\b',text)) for phrase in phrases}
    for a in soup.find_all('a',href=True):
        href=a['href']
        if re.match(r'^[a-z]+:',href) or href.startswith('//'):continue
        dest,_,fragment=href.partition('#')
        target=(p.parent/dest) if dest else p
        if not target.exists():mechanical['broken_local_links'].append({'file':p.name,'line':a.sourceline,'href':href,'reason':'file absent'})
        elif fragment and target.suffix=='.html':
            destsoup=BeautifulSoup(target.read_bytes().decode('utf8'),'html.parser')
            if not destsoup.find(id=fragment) and not destsoup.find('a',attrs={'name':fragment}):
                mechanical['broken_local_links'].append({'file':p.name,'line':a.sourceline,'href':href,'reason':'anchor absent'})
(OUT/'independent-checks.json').write_text(json.dumps(checks,indent=2),encoding='utf8')
(OUT/'mechanical-checks.json').write_text(json.dumps(mechanical,indent=2),encoding='utf8')
print(json.dumps({'independent_checks':len(checks),'bare_carriage_returns':mechanical['bare_carriage_returns'],'broken_local_links':mechanical['broken_local_links']},indent=2))
