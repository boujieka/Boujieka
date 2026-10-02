"""QA: evaluate every formula of a workbook with the Python 'formulas' engine (no Excel/LibreOffice needed).

Run: pip install formulas && python tools/qa_evaluate.py <file.xlsx>
Reports formula errors and pickles computed values to <file.xlsx>.pkl for comparison with tools/shadow_shs.py.
"""
import sys, time, pickle, formulas, numpy as np
p=sys.argv[1]
t=time.time()
xl=formulas.ExcelModel().loads(p).finish()
sol=xl.calculate()
print('calc',round(time.time()-t),flush=True)
out={}; errs=[]
for k,v in sol.items():
    try: val=v.value
    except Exception: continue
    arr=np.asarray(val)
    if arr.size!=1: continue
    x=arr.ravel()[0]
    if isinstance(x, formulas.functions.XlError) or (isinstance(x,str) and x.startswith('#')):
        errs.append((k,str(x)))
    try: x=float(x)
    except Exception: x=str(x)
    out[k.upper()]=x
pickle.dump(out,open(p+'.pkl','wb'))
print('cells',len(out),'errors',len(errs))
for e in errs[:40]: print(e)
