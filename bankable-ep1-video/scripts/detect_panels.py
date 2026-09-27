"""Detect comic panel boxes (x, y, w, h in page pixels) on the extracted book pages."""
from PIL import Image; import numpy as np, json, sys
from scipy import ndimage
out={}
for idx in range(3, 24):  # book pages 4-24
    f=f"assets/pages/pg-{idx:03d}.jpg"
    im=np.asarray(Image.open(f).convert('RGB')).astype(int)
    d=np.abs(im-np.array([254,253,248])).sum(2)>40
    d=ndimage.binary_fill_holes(ndimage.binary_closing(d,iterations=3))
    lab,n=ndimage.label(d)
    boxes=[]
    for sl in ndimage.find_objects(lab):
        y0,y1,x0,x1=sl[0].start,sl[0].stop,sl[1].start,sl[1].stop
        if (y1-y0)>150 and (x1-x0)>300:
            boxes.append([x0,y0,x1-x0,y1-y0])
    boxes.sort(key=lambda b:(b[1]//60,b[0]))
    out[idx]=boxes
    print(idx,boxes)
json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "scripts/panels.json", "w"))
