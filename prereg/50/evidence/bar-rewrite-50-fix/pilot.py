import collections,json,math
P=2**61-1; B=1815673109382999696; CHECK={1000,10000,100000,1000000}
MACHINES=[] # populated below after source-row selection

def ent(s):
 n=len(s); return -sum((v/n)*math.log2(v/n) for v in collections.Counter(s).values())
def epreds(hist,h):
 d=list(hist); full=len(d)>=10
 flip=sum(a*b<0 and abs(a)>.001 and abs(b)>.001 for a,b in zip(d,d[1:]))
 mean=sum(d)/len(d) if d else 0; var=sum((x-mean)**2 for x in d)/len(d) if d else 0
 return {'converged':full and all(abs(x)<.001 for x in d) and h<.1,'stable':full and h>=.1 and all(abs(x)<.01 for x in d) and flip==0,'improving':len(d)>=3 and sum(d)<0 and sum(x<-.01 for x in d)*5>=len(d)*3,'oscillating':len(d)>=3 and flip>=4,'diverging':len(d)>=3 and sum(d)>0 and sum(x>.01 for x in d)*5>=len(d)*3,'equilibrium':full and abs(mean)<.001 and var<.000001}
def npreds(vals,raw,last):
 d=list(vals); r=list(raw); full=len(d)>=10; az=all(abs(x)<.001 for x in d); small=all(abs(x)<.01 for x in d)
 flips=sum(a*b<0 and abs(a)>.001 and abs(b)>.001 for a,b in zip(d,d[1:])); rev=sum(a*b<0 for a,b in zip(r,r[1:])); path=sum(map(abs,r)); net=sum(r)
 oscill=flips>=4 or (full and not az and rev>=2 and path>0 and abs(net)<=.3*path)
 divergent=len(r)>=4 and all(x>0 for x in r) or len(r)>=4 and all(x<0 for x in r)
 improving=False
 if len(r)>=4 and not az and not oscill and all(x*r[0]>0 for x in r[1:]):
  half=len(r)//2; recent=r[:half]; older=r[half:]
  improving=sum(map(abs,recent))/len(recent)<=.7*sum(map(abs,older))/len(older) and max(map(abs,recent))<=.7*max(map(abs,older))
 mean=sum(d)/len(d) if d else 0; var=sum((x-mean)**2 for x in d)/len(d) if d else 0
 return {'converged':full and az and not divergent,'stable':full and small and not divergent and flips==0,'improving':improving,'oscillating':oscill,'diverging':divergent,'equilibrium':full and not divergent and abs(mean)<.001 and var<1e-6}
def run(name,kind,machine):
 rules={}
 for si,pair in enumerate(machine.split('_')):
  for sym in range(2):
   x=pair[sym*3:sym*3+3]; rules[(si,sym)]=None if x=='---' else (int(x[0]),1 if x[1]=='R' else -1,5 if x[2]=='Z' else ord(x[2])-65)
 tape={}; state=head=left=right=h=0; powers=[1]; eh=collections.deque(maxlen=10); vals=collections.deque(maxlen=10); raw=collections.deque(maxlen=10); prev_e=prev_off=0; out=[]; halted=None
 for step in range(1,1000001):
  rule=rules.get((state,tape.get(head,0)))
  if rule is None: halted=step-1; break
  old=tape.get(head,0); new,d,state=rule
  if new!=old:
   off=head-left
   while len(powers)<=off:powers.append(powers[-1]*B%P)
   h=(h+(new-old)*powers[off])%P
   if new:tape[head]=1
   else:tape.pop(head,None)
  head+=d
  if head<left: left=head; h=h*B%P
  if head>right: right=head
  sig=f'{h:016x}'; e=ent(sig); eh.appendleft(e-prev_e); prev_e=e
  off=head-left; rv=off-prev_off; vals.appendleft(rv/(1+abs(off))); raw.appendleft(rv); prev_off=off
  if step in CHECK: out.append({'checkpoint':step,'signature_hash':epreds(eh,e),'head_offset':npreds(vals,raw,off)})
 if halted is not None:
  for cp in sorted(CHECK):
   if cp>halted: out.append({'checkpoint':cp,'halted_at':halted,'signature_hash':None,'head_offset':None})
 return {'name':name,'class':kind,'machine':machine,'checkpoints':sorted(out,key=lambda x:x['checkpoint'])}
if __name__=='__main__':
 import sys
 MACHINES=json.load(open(sys.argv[1])); print(json.dumps([run(**m) for m in MACHINES],indent=2))
