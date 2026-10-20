import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D
plt.rcParams.update({"font.family":"DejaVu Sans","axes.linewidth":0.8})
BLACK="#1a1a1a"; GREY="#6e6e6e"; LGREY="#d9d9d9"
BLUE="#2b5d8a"; GREEN="#2e6f4e"; VERM="#a8422b"
fig,a=plt.subplots(figsize=(8.4,6.6)); a.axis("off")
a.set_xlim(0,12.2); a.set_ylim(1.45,12.75)
steps=[
 (12.1,"ScyE structure\nAlphaFold-derived, prepared",BLUE),
 (10.75,"Two-state redox molecular dynamics\ndisulfide intact 90 ns / removed 100 ns",BLUE),
 (9.4,"Frozen-core definition\n52 Pocket-1 lining residues",BLUE),
 (8.05,"ProteinMPNN redesign\n81 fixed positions: 52 pocket + signal peptide + His\u2086",GREEN),
 (6.7,"ESMFold structure prediction\ntop 3 designs, mean pLDDT 84\u201386",GREEN),
 (5.35,"AutoDock Vina docking\n+ pocket-contact validation at 4.5 \u00c5",VERM),
 (4.0,"Shortlist\n10 designs; 3 folded and docked",VERM),
 (2.5,"Planned wet-lab tests\nexpression, export, activity assay \u2014 not performed",GREY),
]
# stage lanes
lanes=[("DESIGN",9.4,12.1,BLUE),("BUILD",6.7,8.05,GREEN),("TEST",4.0,5.35,VERM),("LEARN",2.5,2.5,GREY)]
for name,lo,hi,c in lanes:
    a.add_patch(Rectangle((0.35,lo-0.80),0.42,(hi-lo)+1.60,facecolor=c,alpha=0.13,edgecolor="none"))
    a.text(0.56,(lo+hi)/2,name,rotation=90,fontsize=8.5,color=c,fontweight="bold",ha="center",va="center")
cx=5.1
for y,t,c in steps:
    head,sub=t.split("\n",1)
    a.add_patch(FancyBboxPatch((cx-2.55,y-0.48),5.10,0.96,
        boxstyle="round,pad=0.04,rounding_size=0.12",lw=1.0,edgecolor=c,
        facecolor=c if c!=GREY else "#f2f2f2",alpha=1.0 if c!=GREY else 1.0))
    tc="white" if c!=GREY else BLACK
    a.text(cx,y+0.16,head,ha="center",va="center",fontsize=8.2,color=tc,fontweight="bold")
    a.text(cx,y-0.19,sub,ha="center",va="center",fontsize=6.9,color=tc)
for i in range(len(steps)-1):
    y1=steps[i][0]-0.48; y2=steps[i+1][0]+0.48
    a.add_patch(FancyArrowPatch((cx,y1),(cx,y2),arrowstyle="-|>",mutation_scale=12,lw=1.3,color=BLACK))
def loop(ylow,yhigh,label,xoff=0.70):
    xe=cx+2.55; x=xe+xoff
    a.add_patch(FancyArrowPatch((xe,ylow),(x,ylow),arrowstyle="-",lw=1.1,color=VERM,linestyle=(0,(4,2))))
    a.add_patch(FancyArrowPatch((x,ylow),(x,yhigh),arrowstyle="-",lw=1.1,color=VERM,linestyle=(0,(4,2))))
    a.add_patch(FancyArrowPatch((x,yhigh),(xe,yhigh),arrowstyle="-|>",mutation_scale=12,lw=1.1,color=VERM,linestyle=(0,(4,2))))
    a.text(x+0.14,(ylow+yhigh)/2,label,fontsize=6.5,color=VERM,ha="left",va="center")
loop(8.05,9.4,"runs A/B/C rejected:\nre-fix positions",0.55)
loop(5.35,6.7,"box on wrong frame:\nrecompute from\nESMFold pocket centroid",0.55)
loop(4.0,5.35,"contact count reverses\nthe score ranking",0.55)
a.add_patch(FancyArrowPatch((cx-2.55,1.72),(cx-2.00,1.72),arrowstyle="-|>",mutation_scale=12,lw=1.1,color=VERM,linestyle=(0,(4,2))))
a.text(cx-1.88,1.72,"self-correction feedback loop that actually occurred",fontsize=7.4,color=VERM,ha="left",va="center")
fig.tight_layout()
fig.savefig("figures_numbered/Figure_01_pipeline_schematic.png",dpi=400,bbox_inches="tight",facecolor="white")
fig.savefig("figures_numbered/Figure_01_pipeline_schematic.pdf",bbox_inches="tight",facecolor="white")
print("done")
