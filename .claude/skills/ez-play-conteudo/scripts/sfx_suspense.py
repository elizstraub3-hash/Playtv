# Trilha e efeitos de suspense, sintetizados do zero.
import numpy as np, wave, sys
SR=48000; DUR=34.5; N=int(SR*DUR); rng=np.random.default_rng(3)
def svf_bp(x,f0,f1,q=2.0):
    y=np.zeros_like(x); lo=bd=0.0; fr=np.geomspace(f0,f1,len(x))
    for i in range(len(x)):
        f=2*np.sin(np.pi*fr[i]/SR); hi=x[i]-lo-bd/q; bd+=f*hi; lo+=f*bd; y[i]=bd
    return y
def norm(x): return x/(np.abs(x).max()+1e-9)
out=np.zeros(N); mus=np.zeros(N)
def put(buf,s,at):
    i=int(at*SR); e=min(N,i+len(s))
    if i<N: buf[i:e]+=s[:e-i]
t=np.arange(N)/SR
# drone escuro (Lá menor com dissonância), respirando
drone=sum(np.sin(2*np.pi*f*t+np.sin(2*np.pi*0.07*t*k)*0.8)*a for k,(f,a) in enumerate([(55,1),(82.4,.6),(110,.5),(116.5,.25),(164.8,.2)],1))
drone*=0.5+0.5*np.sin(2*np.pi*0.11*t)**2
fade=np.minimum(1,t/2.0)*np.minimum(1,(DUR-t)/2.5)
mus+=norm(drone)*0.5*fade
# batida de coração 8.3 → 15.4 s, acelerando
tb=8.3; gap=1.0
while tb<15.4:
    for off,amp in [(0,1),(0.22,0.7)]:
        n=int(0.25*SR); tt=np.arange(n)/SR
        put(mus,np.sin(2*np.pi*(45+40*np.exp(-tt*30))*tt)*np.exp(-tt*14)*0.9*amp,tb+off)
    tb+=gap; gap=max(0.62,gap*0.93)
# rangido da porta (0.6 → 2.6 s)
n=int(2.0*SR); tt=np.arange(n)/SR
f=180+120*np.sin(2*np.pi*1.3*tt)+rng.standard_normal(n).cumsum()*0.02
saw=2*((np.cumsum(f)/SR)%1)-1
creak=svf_bp(saw*(0.6+0.4*rng.random(n)),900,1600,6)
creak=norm(creak)*np.sin(np.linspace(0,np.pi,n))**0.6*0.35
put(out,creak,0.6)
# brilho da luz (2.0 s)
n=int(2.5*SR); tt=np.arange(n)/SR
sh=sum(np.sin(2*np.pi*f*tt)*np.exp(-tt*2.2) for f in [1760,2217,2637]); put(out,norm(sh)*0.12,2.0)
# "Só que não": falha digital + impacto grave (6.97 s)
n=int(0.75*SR); g=rng.standard_normal(n); g=np.round(g*3)/3; g*=(rng.random(n)>0.5)
g=norm(g)*np.exp(-np.arange(n)/SR*3)*0.45; put(out,g,6.97)
n=int(2.0*SR); tt=np.arange(n)/SR
boom=np.sin(2*np.pi*(38+70*np.exp(-tt*12))*tt)*np.exp(-tt*2.2); put(out,boom*0.9,6.97)
# riser antes do título (14.4 → 16.0) e impacto (16.05)
n=int(1.6*SR); tt=np.arange(n)/SR
rs=norm(svf_bp(rng.standard_normal(n),300,6000,1.5))*(tt/1.6)**2.5*0.5
rs+=np.sin(2*np.pi*np.cumsum(np.geomspace(120,900,n))/SR)*(tt/1.6)**2*0.2
put(out,rs,14.45); put(out,boom*0.8,16.05)
# sorriso estranho: nota aguda dissonante (12.9 s)
n=int(2.2*SR); tt=np.arange(n)/SR
put(out,(np.sin(2*np.pi*1244*tt)+np.sin(2*np.pi*1318*tt))*np.exp(-tt*1.4)*0.08,12.9)
# carimbo "sem spoiler" (21.35 s)
n=int(0.4*SR); tt=np.arange(n)/SR
st=np.sin(2*np.pi*(90+200*np.exp(-tt*40))*tt)*np.exp(-tt*12)+norm(rng.standard_normal(n))*np.exp(-tt*40)*0.5
put(out,st*0.8,21.35)
# enquete: pops (25.7 e 26.8 s)
def pop(f0=950,f1=320,a=0.45):
    n=int(0.12*SR); tt=np.arange(n)/SR; f=f1+(f0-f1)*np.exp(-tt*45)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*28)*a
put(out,pop(),25.7); put(out,pop(1200,400,0.35),26.8)
# final: whoosh + sino (29.0 e 31.9 s)
n=int(0.8*SR); w=norm(svf_bp(rng.standard_normal(n),300,5000,2))*np.sin(np.linspace(0,np.pi,n))**1.5*0.45; put(out,w,28.75)
n=int(1.6*SR); tt=np.arange(n)/SR
bell=sum(np.sin(2*np.pi*f*k*tt)*w_*np.exp(-tt*(3+k*2)) for f in [1318.5] for k,w_ in [(1,1),(2.01,.4),(3.02,.2)])
put(out,bell*0.25,31.95); put(out,pop(1000,330,0.4),31.9)
def write(name,x):
    x=np.clip(x,-1,1); st=np.stack([x,x],1)
    with wave.open(name,'wb') as f:
        f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((st*32767).astype('<i2').tobytes())
d=sys.argv[1]
write(d+'/sfx.wav',out*0.8/max(1e-9,np.abs(out).max()))
write(d+'/musica.wav',mus*0.6/max(1e-9,np.abs(mus).max()))
print('ok')
