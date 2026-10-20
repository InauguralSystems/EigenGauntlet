#!/usr/bin/env python3
"""Freeze issue-50 samples from the Coq-BB5 augmented CSV (no network access)."""
import argparse,csv,hashlib,io,json,pathlib
import numpy as np
import zstandard
EXPECTED='2be2101b18b80a458bf85814ee361aa4f4e8d0d45a719cccda9756a65cd0685a'

def main():
 p=argparse.ArgumentParser(); p.add_argument('csv',type=pathlib.Path); p.add_argument('--out',type=pathlib.Path,default=pathlib.Path('prereg/50'))
 a=p.parse_args(); h=hashlib.sha256()
 with a.csv.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 if h.hexdigest()!=EXPECTED: raise SystemExit(f'sha256 mismatch: {h.hexdigest()}')
 halt=[]; long=[]; loops=[]; ng=[]
 with a.csv.open('rb') as raw:
  with zstandard.ZstdDecompressor().stream_reader(raw) as decoded:
   f=io.TextIOWrapper(decoded,encoding='ascii',newline='')
   for row in csv.DictReader(f):
    m,s,d=row['machine'],row['status'],row['decider']
    if s=='halt':
     halt.append((m,int(row['steps'])))
     if int(row['steps'])>=1000: long.append((m,int(row['steps'])))
    elif d.startswith('LOOP1_'): loops.append(m)
    elif d.startswith('NGRAM_CPS_'): ng.append(m)
 rng=np.random.default_rng(50)
 hu=rng.choice(len(halt),5000,replace=False)
 used={halt[i][0] for i in hu}; eligible=[x for x in long if x[0] not in used]
 hl=rng.choice(len(eligible),5000,replace=False); li=rng.choice(len(loops),10000,replace=False); ni=rng.choice(len(ng),1000,replace=False)
 samples={'halting.txt':[halt[i][0] for i in hu]+[eligible[i][0] for i in hl], 'loops.txt':[loops[i] for i in li], 'ngramcps.txt':[ng[i] for i in ni]}
 a.out.mkdir(parents=True,exist_ok=True)
 for name,rows in samples.items(): (a.out/name).write_text(''.join(x+'\n' for x in rows),encoding='ascii',newline='\n')
 def dist(xs):
  q=np.quantile(xs,[0,.25,.5,.75,.9,.99,1],method='linear')
  return dict(zip(('min','p25','median','p75','p90','p99','max'),map(float,q)))
 print(json.dumps({'counts':{k:len(v) for k,v in samples.items()},'uniform_halting_time':dist([halt[i][1] for i in hu]),'long_halting_time':dist([eligible[i][1] for i in hl]),'sha256':{k:hashlib.sha256((''.join(x+'\n' for x in v)).encode('ascii')).hexdigest() for k,v in samples.items()}},sort_keys=True,indent=2))
if __name__=='__main__': main()
