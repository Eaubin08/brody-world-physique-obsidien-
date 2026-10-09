"""P2.10b: source-supervised visual error atlas, by protected/object/background regions.
No semantic attribution or learned vision is claimed.
"""
from __future__ import annotations
from PIL import Image,ImageChops
from .p210a_visual_loop_contract_v0 import open_rgba
ERROR_TYPES=("POSITION","SHAPE","PROPORTION","ORIENTATION","COLOR","TEXTURE","BACKGROUND","PART_RELATION","OCCLUSION","UNKNOWN")

def _mask(mask,size):
    m=mask.convert("L")
    if m.size!=size:raise ValueError("mask dimensions differ")
    return m.point(lambda v:255 if v>=128 else 0)

def diagnose(source,generated,object_mask,protected_mask=None):
    if source.size!=generated.size:raise ValueError("image size mismatch")
    a,b=source.convert("RGBA"),generated.convert("RGBA")
    object_mask=_mask(object_mask,a.size)
    protected=_mask(protected_mask,a.size) if protected_mask is not None else Image.new("L",a.size,0)
    overlap=ImageChops.multiply(object_mask,protected)
    if overlap.getbbox():raise ValueError("object and protected regions overlap")
    diff=ImageChops.difference(a,b).convert("RGB")
    changed=diff.convert("L").point(lambda _:0) # will be replaced with exact per-pixel differences
    d=Image.new("L",a.size,0)
    dm=d.load(); pix=diff.load()
    for y in range(a.height):
        for x in range(a.width):
            dm[x,y]=255 if any(pix[x,y]) else 0
    changed=d
    total=a.width*a.height
    obj=object_mask.histogram()[255]
    prot=protected.histogram()[255]
    obj_err=ImageChops.multiply(changed,object_mask).histogram()[255]
    prot_err=ImageChops.multiply(changed,protected).histogram()[255]
    all_err=changed.histogram()[255]
    bg_err=all_err-obj_err-prot_err
    return {"schema":"BRODY_P210B_VISUAL_ERROR_ATLAS_V0",
            "error_type":"UNKNOWN", # classification requires independent object semantics
            "total_pixels":total,"object_pixels":obj,"protected_pixels":prot,
            "object_changed_pixels":obj_err,"protected_changed_pixels":prot_err,
            "background_changed_pixels":bg_err,"changed_pixels":all_err,
            "object_error_rate":obj_err/obj if obj else None,
            "background_error_rate":bg_err/(total-obj-prot) if total>obj+prot else None,
            "semantic_cause_proven":False,"source_supervised":True}

def from_paths(source,generated,mask,protected=None):
    with Image.open(mask) as m:
        if protected is None:return diagnose(open_rgba(source),open_rgba(generated),m)
        with Image.open(protected) as p:return diagnose(open_rgba(source),open_rgba(generated),m,p)
