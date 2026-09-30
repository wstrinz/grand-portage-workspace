import pathlib,json,subprocess,time,os
r=pathlib.Path('.').resolve();p=r/'spikes/lean-core'
env=os.environ.copy();env['PATH']='C:/Users/wstri/.elan/toolchains/leanprover--lean4---v4.32.1/bin;'+env['PATH'];env['TEMP']=str(r/'tmp');env['TMP']=env['TEMP']
lake='C:/Users/wstri/.elan/toolchains/leanprover--lean4---v4.32.1/bin/lake.exe'
assert p==pathlib.Path('F:/repos/grandportage-0.50/spikes/lean-core')
out=[]
for label,args in [('clean-generated-build',['clean']),('clean-package-build',['build']),('warm-no-change',['build']),('kernel-replay-toy',['env','leanchecker','-v','Spike']),('kernel-replay-LRAT-native',['env','leanchecker','-v','Spike.Lrat'])]:
    start=time.perf_counter();q=subprocess.run([lake,*args],cwd=p,env=env,encoding='utf-8',capture_output=True,timeout=180);elapsed=time.perf_counter()-start
    out.append(dict(label=label,seconds=elapsed,exit=q.returncode,stdout=q.stdout,stderr=q.stderr))
    if q.returncode:break
(r/'reports/PHASE-0C-CORE-BUILD.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps([{k:v for k,v in row.items() if k not in ('stdout','stderr')} for row in out]))
if out[-1]['exit']:raise SystemExit(1)
