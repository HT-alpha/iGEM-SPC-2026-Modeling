import numpy as np, json

FROZEN=[34,36,51,65,66,67,68,69,70,71,73,102,108,109,110,111,113,128,130,177,
        179,181,182,183,197,198,200,231,232,233,242,243,245,247,249,251,266,267,
        268,269,271,299,314,319,320,323,324,325,328,359,375,376]

def parse_receptor(fn):
    """return dict resnum -> list of (x,y,z) for all atoms"""
    res={}
    for line in open(fn):
        if line.startswith(("ATOM","HETATM")):
            try: rn=int(line[22:26])
            except: continue
            x=float(line[30:38]); y=float(line[38:46]); z=float(line[46:54])
            res.setdefault(rn,[]).append((x,y,z))
    return {k:np.array(v) for k,v in res.items()}

def parse_pose_model1(fn):
    coords=[]; started=False
    for line in open(fn):
        if line.startswith("MODEL"):
            if started: break   # we already collected MODEL 1
            started=True; continue
        if line.startswith("ENDMDL"):
            if started: break
        if started and line.startswith(("ATOM","HETATM")):
            x=float(line[30:38]); y=float(line[38:46]); z=float(line[46:54])
            coords.append((x,y,z))
    return np.array(coords)

def contacts(recfn, posefn, cutoff=4.5):
    rec=parse_receptor(recfn); L=parse_pose_model1(posefn)
    hit=[]
    for r in FROZEN:
        if r in rec:
            d=np.sqrt(((rec[r][:,None,:]-L[None,:,:])**2).sum(-1)).min()
            if d<cutoff: hit.append(r)
    return sorted(hit), len(L)

def ca_plddt(fn):
    """CA b-factor per residue in order"""
    vals={}
    for line in open(fn):
        if line.startswith("ATOM") and line[12:16].strip()=="CA":
            rn=int(line[22:26]); b=float(line[60:66])
            vals[rn]=b
    return vals

jobs=[("scyE_clean","scyE_clean.pdb","scyE_clean_mono.pdbqt"),
      ("C2_52_1","C2_52_1_esmfold.pdb","C2_52_1_mono2.pdbqt"),
      ("C2_52_2","C2_52_2_esmfold.pdb","C2_52_2_mono2.pdbqt"),
      ("C2_52_3","C2_52_3_esmfold.pdb","C2_52_3_mono2.pdbqt")]

print("="*70)
print("TASK 1a: COMPLETE pocket contact sets (4.5 A, MODEL 1 top pose)")
print("="*70)
csets={}
for name,rec,pose in jobs:
    hit,nlig=contacts(rec,pose)
    csets[name]=set(hit)
    print(f"{name:12s} ligand atoms {nlig:3d}  contacts {len(hit):2d}/52  -> {hit}")

recorded={"scyE_clean":14,"C2_52_1":15,"C2_52_2":5,"C2_52_3":11}
print("\nReproduction check vs recorded 15/5/11/14:")
for name in ["C2_52_1","C2_52_2","C2_52_3","scyE_clean"]:
    got=len(csets[name]); rec=recorded[name]
    print(f"  {name:12s} recorded {rec:2d}  computed {got:2d}  {'MATCH' if got==rec else '*** DIFFERS ***'}")

print("\n"+"="*70)
print("TASK 1b: TRUE intersection parent & C2_52_1 full contact sets")
print("="*70)
inter=sorted(csets["scyE_clean"] & csets["C2_52_1"])
print(f"  parent set   ({len(csets['scyE_clean'])}): {sorted(csets['scyE_clean'])}")
print(f"  C2_52_1 set  ({len(csets['C2_52_1'])}): {sorted(csets['C2_52_1'])}")
print(f"  INTERSECTION ({len(inter)}): {inter}")
print(f"  (earlier incorrect claim was 8: 65,67,68,108,130,183,197,198)")

print("\n"+"="*70)
print("TASK 1c: per-residue pLDDT (CA B-factor) for the 3 ESMFold models")
print("="*70)
sig=list(range(1,23)); his=list(range(398,404))
for name in ["C2_52_1","C2_52_2","C2_52_3"]:
    v=ca_plddt(f"{name}_esmfold.pdb")
    allv=np.array([v[r] for r in sorted(v)])
    pocket=np.array([v[r] for r in FROZEN if r in v])
    sigv=np.array([v[r] for r in sig if r in v])
    hisv=np.array([v[r] for r in his if r in v])
    print(f"{name}: n_res={len(allv)}  mean(all)={allv.mean():.2f}  "
          f"pocket(52)={pocket.mean():.2f}  signal(1-22)={sigv.mean():.2f}  His6(398-403)={hisv.mean():.2f}")

recorded_p={"C2_52_1":86.19,"C2_52_2":84.18,"C2_52_3":84.90}
print("\nReproduction check vs recorded mean pLDDT 86.19/84.18/84.90:")
for name in ["C2_52_1","C2_52_2","C2_52_3"]:
    v=ca_plddt(f"{name}_esmfold.pdb")
    m=np.mean([v[r] for r in sorted(v)])
    print(f"  {name}: recorded {recorded_p[name]}  computed {m:.2f}  {'MATCH' if abs(m-recorded_p[name])<0.05 else 'close/differs'}")

# dump csets for figure script
json.dump({k:sorted(v) for k,v in csets.items()}, open("/workspace/c2_52_results/contact_sets.json","w"))
print("\ncontact_sets.json written")
