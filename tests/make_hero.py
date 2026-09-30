"""
Draws wfm-demand-forecasting-hero.png from the notebook's own Tuesday interval data.
Run from the repo root:  python tests/make_hero.py
"""
import json, contextlib, io, os, sys
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.show=lambda *a,**k:None
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
nb=json.load(open('WFM_Demand_Forecasting.ipynb')); g={}
for c in nb['cells'][:32]:
    if c['cell_type']=='code':
        with contextlib.redirect_stdout(io.StringIO()): exec(''.join(c['source']),g)
np=g['np']; d=g['d']; o=d[d.scheduled_actual>0].reset_index(drop=True)
req=o.scheduled_fte.values; sch=o.scheduled_actual.values; t=o.interval_30.values/60
assert len(o)==34 and req.sum()==494 and sch.sum()==486
under=(sch<req).sum(); over=(sch>req).sum()
sl=np.average(o.delivered_sl,weights=o.forecast_calls)*100
print(under,over,round(sl,1), req.max(), sch.max())

BG='#0B1220'; INK='#F1F5F9'; INK2='#AAB4C3'; MUTED='#6B7688'; GRID='#1E2A3C'
BLUE='#3987e5'; AQUA='#199e70'; RED='#e66767'
plt.rcParams['font.family']='DejaVu Sans'
fig=plt.figure(figsize=(17.9,8.8),dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.024,0.935,'WFM Demand Forecasting Model',fontsize=40,fontweight='bold',color=INK,va='center')
t1=fig.text(0.024,0.862,'Near-right total staffing.',fontsize=25,fontweight='bold',color=INK,va='center')
bb=t1.get_window_extent(renderer=fig.canvas.get_renderer()).transformed(fig.transFigure.inverted())
fig.text(bb.x1+0.008,0.862,'Wrong distribution.',fontsize=25,color='#9DB2CF',va='center')
fig.text(0.024,0.805,f'{sch.sum()} scheduled vs. {req.sum()} required FTE-intervals (−1.6%)',fontsize=17,color=INK,va='center')
fig.text(0.024,0.760,'Real call arrivals  ·  Synthetic shift schedule  ·  Tuesday, staffed hours 07:00–24:00',fontsize=13.5,color=INK2,va='center')

ax=fig.add_axes([0.06,0.33,0.915,0.39]); ax.set_facecolor(BG)
x=np.append(t,t[-1]+0.5); R=np.append(req,req[-1]); Sx=np.append(sch,sch[-1])
from matplotlib.patches import Rectangle, Patch
for ti,r_,s_ in zip(t,req,sch):
    if s_!=r_: ax.add_patch(Rectangle((ti,min(r_,s_)),0.5,abs(r_-s_),color=RED if s_<r_ else AQUA,alpha=0.30,lw=0))
extra=[Patch(color=RED,alpha=0.30,label='Understaffed'),Patch(color=AQUA,alpha=0.30,label='Overstaffed')]
ax.step(x,R,where='post',color=BLUE,lw=2.6,label='Required')
ax.step(x,Sx,where='post',color=AQUA,lw=2.6,ls=(0,(5,3)),label='Scheduled')
ax.set_xlim(7,24); ax.set_ylim(0,30)
ax.set_xticks(range(7,25,2)); ax.set_xticklabels(['7am','9am','11am','1pm','3pm','5pm','7pm','9pm','11pm'],color=INK2,fontsize=13)
ax.set_yticks([0,5,10,15,20,25,30]); ax.tick_params(axis='y',colors=INK2,labelsize=12,length=0); ax.tick_params(axis='x',length=0,pad=8)
ax.grid(False); ax.grid(axis='y',color=GRID,lw=1); ax.set_axisbelow(True)
for s in ['top','right','left']: ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color('#33415A')
ax.set_ylabel('FTEs per 30-min interval',color=INK2,fontsize=12.5,labelpad=10)
h,l=ax.get_legend_handles_labels()
leg=ax.legend(handles=extra+h,loc='upper right',ncol=4,frameon=False,fontsize=12.5,labelcolor=INK,bbox_to_anchor=(1,1.13),handlelength=2.4)

def card(x0,color,big,line1,line2):
    a=fig.add_axes([x0,0.075,0.305,0.175]); a.axis('off'); a.set_xlim(0,1); a.set_ylim(0,1)
    a.add_patch(FancyBboxPatch((0.005,0.02),0.99,0.96,boxstyle='round,pad=0,rounding_size=0.06',fc=BG,ec=color,lw=1.6,transform=a.transAxes,mutation_aspect=0.3))
    a.text(0.06,0.68,big,fontsize=34,fontweight='bold',color=color,va='center')
    a.text(0.06,0.38,line1,fontsize=16,color=INK,va='center')
    a.text(0.06,0.16,line2,fontsize=12.5,color=INK2,va='center')
card(0.024,RED,f'{under/34:.0%}','intervals understaffed',f'{under} of 34 staffed intervals')
card(0.347,AQUA,f'{over/34:.0%}','intervals overstaffed',f'{over} of 34 staffed intervals')
card(0.670,'#E0A33A',f'{sl:.1f}%','service level vs 80% target','call-weighted, staffed hours')
fig.text(0.024,0.028,'Interval forecasting  ·  Erlang C  ·  Shrinkage  ·  FTE gap analysis   |   Python',fontsize=13,color=MUTED,va='center')
fig.savefig('wfm-demand-forecasting-hero.png',facecolor=BG,dpi=100)
