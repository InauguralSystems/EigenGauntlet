import math,time
M='1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA'; P=2**61-1; B=1815673109382999696
rules={};
for si,pair in enumerate(M.split('_')):
 for sym in range(2):
  x=pair[sym*3:sym*3+3]; rules[(si,sym)]=(int(x[0]),1 if x[1]=='R' else -1,5 if x[2]=='Z' else ord(x[2])-65)
tape={}; state=head=left=right=0; powers=[1]; h=0; last_entropy=0.0
def entropy(s):
 f={c:s.count(c) for c in set(s)}; n=len(s)
 return -sum((v/n)*math.log2(v/n) for v in f.values())
t0=time.perf_counter()
for step in range(1,1_000_001):
 old=tape.get(head,0); new,d,state=rules[(state,old)]
 if new!=old:
  off=head-left
  while len(powers)<=off: powers.append((powers[-1]*B)%P)
  h=(h+(new-old)*powers[off])%P
  if new:tape[head]=1
  else:tape.pop(head,None)
 head+=d
 if head<left:
  left=head; h=(h*B)%P
  if tape.get(head,0):h=(h+1)%P
 if head>right:
  right=head
  while len(powers)<=right-left:powers.append((powers[-1]*B)%P)
 sig=f'{h:016x}'; last_entropy=entropy(sig) # exact string-channel assignment work
 head_offset=head-left # numeric observer assignment work (raw/value capture)
elapsed=time.perf_counter()-t0
print(f'machine={M}')
print('transitions=1000000 signature_updates=1000000 observer_assignments=2000000')
print(f'base={B} modulus={P} final_hash={h} final_head_offset={head_offset} final_entropy={last_entropy}')
print(f'elapsed_seconds={elapsed:.9f} transitions_per_second={1_000_000/elapsed:.3f}')
for name,n in [('champion',47176870),('antihydra',100000000),('one_sample_machine',1050000),('all_21000_samples',22050000000)]: print(f'{name}_seconds={n*elapsed/1_000_000:.6f}')
# Separate plain-simulator lane required for the champion graded run.
tape={}; state=head=0; t0=time.perf_counter()
for step in range(1,1_000_001):
 old=tape.get(head,0); new,d,state=rules[(state,old)]
 if new:tape[head]=1
 else:tape.pop(head,None)
 head+=d
plain=time.perf_counter()-t0
print(f'plain_elapsed_seconds={plain:.9f} plain_transitions_per_second={1_000_000/plain:.3f}')
print(f'champion_plain_seconds={47176870*plain/1_000_000:.6f}')
