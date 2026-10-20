#!/usr/bin/env python3
"""Freeze issue-50 samples in exactly two streaming ``zstd -dc`` passes."""
import argparse, array, hashlib, json, pathlib, subprocess
import numpy as np
EXPECTED = "2be2101b18b80a458bf85814ee361aa4f4e8d0d45a719cccda9756a65cd0685a"
def rows(path):
    proc=subprocess.Popen(["zstd","-dc",str(path)],stdout=subprocess.PIPE)
    assert proc.stdout is not None
    next(proc.stdout)
    try:
        for line in proc.stdout:
            fields=line.rstrip(b"\n").split(b",")
            yield fields[0],fields[1],fields[2],fields[5]
    finally:
        proc.stdout.close()
        if proc.wait()!=0: raise SystemExit("zstd -dc failed")
def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda:stream.read(1<<20),b""): h.update(block)
    return h.hexdigest()
def distribution(values):
    q=np.quantile(values,[0,.25,.5,.75,.9,.99,1],method="linear")
    return dict(zip(("min","p25","median","p75","p90","p99","max"),map(float,q)))
def main():
    p=argparse.ArgumentParser(); p.add_argument("csv",type=pathlib.Path); p.add_argument("--out",type=pathlib.Path,default=pathlib.Path("prereg/50")); a=p.parse_args()
    actual=digest(a.csv)
    if actual!=EXPECTED: raise SystemExit(f"sha256 mismatch: {actual}")
    long_halt_ordinals=array.array("I")
    counts={"halting":0,"halting_steps_ge_1000":0,"loop1_nonhalting":0,"ngram_cps_nonhalting":0}
    for machine,status,decider,steps in rows(a.csv): # streaming pass 1
        if status==b"halt":
            counts["halting"]+=1
            if int(steps)>=1000:
                long_halt_ordinals.append(counts["halting"]-1)
                counts["halting_steps_ge_1000"]+=1
        elif status==b"nonhalt" and decider.startswith(b"LOOP1_"): counts["loop1_nonhalting"]+=1
        elif status==b"nonhalt" and decider.startswith(b"NGRAM_CPS_"): counts["ngram_cps_nonhalting"]+=1
    rng=np.random.default_rng(50)
    hui=sorted(map(int,rng.choice(counts["halting"],5000,replace=False))); hus=set(hui)
    # Translate the long-stratum index to its halting ordinal, excluding draw 1.
    eligible_long=[x for x in long_halt_ordinals if x not in hus]
    hli=sorted(map(int,rng.choice(len(eligible_long),min(5000,len(eligible_long)),replace=False)))
    hl_halt_ordinals={eligible_long[i] for i in hli}
    li=sorted(map(int,rng.choice(counts["loop1_nonhalting"],10000,replace=False)))
    ni=sorted(map(int,rng.choice(counts["ngram_cps_nonhalting"],1000,replace=False)))
    lis,nis=set(li),set(ni)
    hu=[]; hl=[]; loops=[]; ngrams=[]; hi=lj=nj=0
    for machine,status,decider,steps in rows(a.csv): # streaming pass 2
        if status==b"halt":
            if hi in hus: hu.append((hi,machine.decode("ascii"),int(steps)))
            if hi in hl_halt_ordinals: hl.append((hi,machine.decode("ascii"),int(steps)))
            hi+=1
        elif status==b"nonhalt" and decider.startswith(b"LOOP1_"):
            if lj in lis: loops.append((lj,machine.decode("ascii")))
            lj+=1
        elif status==b"nonhalt" and decider.startswith(b"NGRAM_CPS_"):
            if nj in nis: ngrams.append((nj,machine.decode("ascii")))
            nj+=1
    outputs={"halting-uniform.txt":[x[1] for x in hu],"halting-ge-1000.txt":[x[1] for x in hl],"loop1-nonhalt.txt":[x[1] for x in loops],"ngram-cps-nonhalt.txt":[x[1] for x in ngrams]}
    a.out.mkdir(parents=True,exist_ok=True); digests={}
    for name,machines in outputs.items():
        path=a.out/name; path.write_text("".join(f"{m}\n" for m in machines),encoding="ascii",newline="\n"); digests[name]=digest(path)
    indices={"halting_uniform":hui,"halting_ge_1000":hli,"loop1_nonhalt":li,"ngram_cps_nonhalt":ni}
    result={"source_sha256":actual,"pass_1_eligible_counts":counts,"disjoint_long_eligible_count":len(eligible_long),"selected_counts":{k:len(v) for k,v in outputs.items()},"draw_indices_sha256":{k:hashlib.sha256(json.dumps(v).encode()).hexdigest() for k,v in indices.items()},"id_file_sha256":digests,"halting_uniform_time_distribution":distribution([x[2] for x in hu]),"halting_ge_1000_time_distribution":distribution([x[2] for x in hl])}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
