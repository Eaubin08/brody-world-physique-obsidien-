"""Observable structural visual facts: components, arrangement and invariants.

Descriptive candidate facts only. No semantic object identity or 3D claim.
"""
from __future__ import annotations
import hashlib
from collections import deque
from PIL import Image,ImageOps

def describe(image):
    im=image.convert("L").resize((64,64))
    pixels=im.tobytes()
    dark=[v<128 for v in pixels]
    visited=set();components=[]
    for origin in range(4096):
        if not dark[origin] or origin in visited:continue
        queue=deque([origin]);visited.add(origin);pts=[]
        while queue:
            k=queue.popleft();x,y=k%64,k//64;pts.append((x,y))
            for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                j=ny*64+nx
                if 0<=nx<64 and 0<=ny<64 and j not in visited and dark[j]:
                    visited.add(j);queue.append(j)
        if len(pts)>=4:
            xs=[x for x,y in pts];ys=[y for x,y in pts]
            components.append({"size":len(pts),"bbox":[min(xs),min(ys),max(xs),max(ys)],
                "center":[round(sum(xs)/len(pts),2),round(sum(ys)/len(pts),2)]})
    components.sort(key=lambda x:(-x["size"],x["bbox"]))
    centers=[c["center"] for c in components[:8]]
    relations=[]
    for i in range(len(centers)):
        for j in range(i+1,len(centers)):
            dx=centers[j][0]-centers[i][0]
            dy=centers[j][1]-centers[i][1]
            dist=(dx*dx+dy*dy)**.5
            relations.append({"parts":[i,j],"proximity":"near" if dist<20 else "far",
                "orientation":"horizontal" if abs(dx)>abs(dy)*1.5 else
                ("vertical" if abs(dy)>abs(dx)*1.5 else "diagonal")})
    occupied=sum(dark)
    density="sparse" if occupied<300 else "medium" if occupied<1500 else "dense"
    tonal="flat" if max(pixels)-min(pixels)<20 else "varied"
    orientation="none"
    if components:
        b=components[0]["bbox"];w=b[2]-b[0]+1;h=b[3]-b[1]+1
        orientation="horizontal" if w>h*1.5 else "vertical" if h>w*1.5 else "balanced"
    # context is structural, not filename or "object category"
    context=f"tone:{tonal}|density:{density}|parts:{min(len(components),4)}|axis:{orientation}"
    return {"context":context,"properties":{"tone":tonal,"density":density,
        "orientation":orientation,"dark_pixels":occupied},
        "parts":components[:8],"relations":relations,
        "observable_only":True,"object_identity_known":False,
        "pixel_sha256":hashlib.sha256(pixels).hexdigest()}
