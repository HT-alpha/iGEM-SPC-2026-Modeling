import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size":9,"axes.titlesize":10,"axes.labelsize":9,
 "figure.dpi":300,"savefig.dpi":300,"axes.spines.top":False,"axes.spines.right":False,
 "font.family":"DejaVu Sans"})
C1,C2,C3,CG="#1f4e79","#c0392b","#2e7d32","#7f8c8d"
OUT="/workspace/figures/"

# F27 Rg per 10 ns, system A (md_100ns, 0-90 ns, Protein)
w=["0–10","10–20","20–30","30–40","40–50","50–60","60–70","70–80","80–90"]
m=[2.3032,2.1963,2.1301,2.1070,2.1365,2.1275,2.1407,2.1194,2.1288]
s=[0.0547,0.0197,0.0244,0.0153,0.0124,0.0159,0.0094,0.0121,0.0105]
f,a=plt.subplots(figsize=(5.5,3.2))
a.errorbar(range(9),m,yerr=s,fmt="o-",color=C1,capsize=3,ms=4,lw=1.4)
a.axvspan(6.5,8.5,color=C3,alpha=.10)
a.text(7.5,2.29,"analysis window",ha="center",color=C3,fontsize=8)
a.set_xticks(range(9)); a.set_xticklabels(w,rotation=45,ha="right")
a.set_xlabel("simulation window (ns)"); a.set_ylabel(r"radius of gyration $R_g$ (nm)")
a.set_title("Fig. 27  Compaction settles within 30 ns and stays flat (system A, disulfide-intact)")
f.tight_layout(); f.savefig(OUT+"fig27_rg_blocks_systemA.png"); plt.close(f)

# F28 SG-SG occupancy vs cutoff
cut=[3.5,4.0,4.5,5.0]; occB=[7.9,24.8,31.7,74.3]
f,a=plt.subplots(figsize=(5.0,3.2))
a.plot(cut,occB,"o-",color=C2,lw=1.6,ms=5,label="disulfide-free (system B)")
a.axhline(100,color=C1,lw=1.6,ls="--",label="disulfide-intact (system A): 100.0% at 3.0 Å")
for x,y in zip(cut,occB): a.annotate(f"{y:.1f}%",(x,y),textcoords="offset points",xytext=(0,7),ha="center",fontsize=8,color=C2)
a.set_xlabel("SG–SG distance cutoff (Å)"); a.set_ylabel("frames satisfying cutoff (%)")
a.set_ylim(-5,112); a.legend(frameon=False,loc="lower right",fontsize=8)
a.set_title("Fig. 28  The disulfide is binary: held at 2.04 Å, or never re-formed")
f.tight_layout(); f.savefig(OUT+"fig28_sgsg_occupancy.png"); plt.close(f)

# F29 RMSD comparison
labels=["System A\n0–90 ns\n(Backbone fit+calc)","System A\n70–90 ns\nlate window","System B\n0–100 ns\n(gmx analyze)"]
mean=[0.8395,0.9346,0.9991]; sd=[0.1959,0.0155,0.2005]
lo=[0.0005,0.8542,np.nan]; hi=[1.0920,0.9777,np.nan]
f,a=plt.subplots(figsize=(5.4,3.4))
x=np.arange(3)
for i in range(3):
    if not np.isnan(lo[i]): a.vlines(x[i],lo[i],hi[i],color=CG,lw=6,alpha=.35)
a.errorbar(x,mean,yerr=sd,fmt="o",color=C1,capsize=4,ms=7,lw=1.5)
for i,v in enumerate(mean): a.annotate(f"{v:.3f} ± {sd[i]:.3f} nm",(x[i],v),textcoords="offset points",xytext=(0,12),ha="center",fontsize=8)
a.annotate("min–max\nnot archived\n(T4/T5)",(2,0.999),textcoords="offset points",xytext=(0,-38),ha="center",fontsize=7.5,color=C2)
a.set_xticks(x); a.set_xticklabels(labels,fontsize=8); a.set_ylabel("backbone RMSD (nm)")
a.set_ylim(0,1.25)
a.set_title("Fig. 29  Both states plateau; the late window is flat to ±0.016 nm")
f.tight_layout(); f.savefig(OUT+"fig29_rmsd_summary.png"); plt.close(f)

# F30 top-10 flexible residues, system A 70-90 ns (Protein group)
res=[403,402,16,12,18,17,11,15,401,400]; val=[0.5923,0.5682,0.5546,0.4765,0.4762,0.4674,0.4391,0.4347,0.4313,0.4110]
col=[C2 if r>=398 else (C3 if r<=22 else C1) for r in res]
f,a=plt.subplots(figsize=(5.6,3.2))
a.bar([str(r) for r in res],val,color=col)
a.axhline(0.15,color="k",ls=":",lw=1)
a.text(9.4,0.165,"0.15 nm rigidity cutoff",ha="right",fontsize=8)
a.set_xlabel("residue"); a.set_ylabel("RMSF (nm), 70–90 ns")
import matplotlib.patches as mp
a.legend(handles=[mp.Patch(color=C2,label="His-tag region (398–403)"),
                  mp.Patch(color=C3,label="signal-peptide region (1–22)"),
                  mp.Patch(color=C1,label="native ScyE body")],frameon=False,fontsize=8)
a.set_title("Fig. 30  Every one of the ten most mobile residues is something we added")
f.tight_layout(); f.savefig(OUT+"fig30_rmsf_top10.png"); plt.close(f)

# F31 DCCM strongest long-range pairs (disulfide-free, 70-100 ns, unfitted)
pairs=[("149–160",0.9020),("16–401",0.8964),("124–150",0.8876),("148–161",0.8860),
("149–159",0.8854),("149–161",0.8797),("77–98",0.8784),("81–94",0.8749),("125–149",0.8748),
("77–97",0.8740),("148–162",0.8735),("148–160",0.8714),("150–160",0.8710),("125–150",0.8628),
("15–401",0.8459)]
names=[p[0] for p in pairs][::-1]; vals=[p[1] for p in pairs][::-1]
col=[C2 if ("401" in n) else C1 for n in names]
f,a=plt.subplots(figsize=(5.2,4.0))
a.hlines(range(len(names)),0.80,vals,color=col,lw=2)
a.plot(vals,range(len(names)),"o",color="none",markeredgecolor="none")
for i,(n,v) in enumerate(zip(names,vals)): a.plot(v,i,"o",color=col[i],ms=5)
a.set_yticks(range(len(names))); a.set_yticklabels(names,fontsize=8)
a.set_xlim(0.80,0.92); a.set_xlabel("Cα–Cα dynamic cross-correlation")
a.set_ylabel("residue pair (|i − j| > 10)")
a.set_title("Fig. 31  Two of the strongest long-range\ncouplings involve the His-tag",fontsize=9.5)
a.text(0.918,13.0,"construct\nartefact",color=C2,fontsize=8,ha="right")
f.tight_layout(); f.savefig(OUT+"fig31_dccm_pairs.png"); plt.close(f)

# F32 pipeline benchmark, cealign
lab=["Node 8\n(ancestor,\npositive control)","Node 12\n(candidate)","Strategy A\ntop-10 range","Strategy D\n(RFdiffusion)","5FXE\n(wrong family)","1VAO\n(wrong family)"]
v=[1.37,2.15,None,7.44,7.07,8.26]
f,a=plt.subplots(figsize=(5.8,3.4))
xs=np.arange(6)
for i,val in enumerate(v):
    if val is not None:
        a.bar(xs[i],val,color=C3 if val<2 else (C1 if val<3 else C2))
a.vlines(xs[2],2.39,6.97,color=C2,lw=10,alpha=.45)
a.annotate("2.39–6.97 Å\n(none passed)",(xs[2],6.97),textcoords="offset points",xytext=(0,6),ha="center",fontsize=7.5)
a.axhline(2.0,color="k",ls=":",lw=1); a.text(5.45,2.12,"2 Å acceptance threshold",ha="right",fontsize=8)
a.set_xticks(xs); a.set_xticklabels(lab,fontsize=7.5)
a.set_ylabel("Cα RMSD to native ScyE, PyMOL cealign (Å)")
a.set_title("Fig. 32  The structural check recovers a known answer and rejects wrong ones")
f.tight_layout(); f.savefig(OUT+"fig32_cealign_benchmark.png"); plt.close(f)

# F33 docking reproducibility
f,a=plt.subplots(figsize=(5.2,3.2))
seeds=[-9.713,-9.701,-9.734]
a.plot([1,1,1],seeds,"o",color=C1,ms=6,label="Pocket 1, three random seeds")
a.plot([2],[-7.61],"s",color=CG,ms=7,label="Pocket 2 (best alternative cavity)")
a.plot([3,3],[-10.68,-10.73],"^",color=C3,ms=7,label="C2_39 re-dock, two top poses")
a.annotate(f"mean −9.716\nrange 0.033 kcal/mol",(1,-9.716),textcoords="offset points",xytext=(14,0),fontsize=8,va="center")
a.annotate("Δ ≈ 2.1 kcal/mol",(1.5,-8.66),ha="center",fontsize=8,color=CG)
a.set_xlim(0.5,3.8); a.set_xticks([]); a.set_ylabel("AutoDock Vina affinity (kcal/mol)")
a.legend(frameon=False,fontsize=8,loc="lower left")
a.set_title("Fig. 33  Pocket ranking is a real separation, not search noise")
f.tight_layout(); f.savefig(OUT+"fig33_docking_reproducibility.png"); plt.close(f)

# F34 RMSF five-number summary (rmsf.xvg used for the frozen core)
f,a=plt.subplots(figsize=(5.2,3.0))
stats=[{"med":0.0576,"q1":0.0457,"q3":0.0753,"whislo":0.0315,"whishi":0.3154,"mean":0.0707,"fliers":[]}]
bp=a.bxp(stats,showmeans=True,vert=False,widths=.45,patch_artist=True)
bp["boxes"][0].set_facecolor("#dce6f1")
a.axvline(0.15,color=C2,ls="--",lw=1.4)
a.text(0.152,1.28,"0.15 nm cutoff — selected 52 of 52\npocket residues, i.e. filtered nothing",color=C2,fontsize=8)
a.set_yticks([1]); a.set_yticklabels(["whole protein\n(403 residues)"],fontsize=8)
a.set_xlabel("per-residue RMSF (nm), rmsf.xvg — the file used\nto define the frozen core")
a.set_title("Fig. 34  Why the rigidity cutoff did not discriminate",fontsize=9.5)
f.tight_layout(); f.savefig(OUT+"fig34_rmsf_distribution.png"); plt.close(f)
print("done")
