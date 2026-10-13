"""P2 experimental raster-only predictor on past video frames.

No call to world_transfer_probe_v1.iter_video_points or its tracked XY state.
The video is synthetic. Segmentation thresholds are engineered; pixel-source
independence and learned image understanding are NOT claimed.
"""
from __future__ import annotations

from math import isfinite
from pathlib import Path


def raster_history_only(video: Path, source_sha256: str, indices: tuple[int, int, int],
                        *, anchored: bool = True):
    """Decode no frame after the final allowed observation index."""
    import cv2
    from .video_observation_v0 import video_sha256
    if video_sha256(video) != source_sha256:
        raise ValueError("raster source hash mismatch")
    if len(indices) != 3 or tuple(sorted(set(indices))) != indices:
        raise ValueError("three strictly increasing past frame indices required")
    if indices[0] < 0 or indices[2] >= 72 or any(i % 6 for i in indices):
        raise ValueError("unsupported frame window")
    cap = cv2.VideoCapture(str(video))
    results = {}
    try:
        if not cap.isOpened():
            raise ValueError("cannot open raster video")
        for idx in range(indices[-1]+1):
            ok, frame = cap.read()
            if not ok or frame is None:
                raise ValueError("missing past raster frame")
            if idx not in indices:
                continue
            if frame.shape[:2] != (320,480):
                raise ValueError("raster frame size mismatch")
            hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            saturated=cv2.inRange(hsv,(0,120,115),(179,255,255))
            cyan=cv2.inRange(hsv,(83,105,105),(104,255,255))
            foreground=cv2.bitwise_and(saturated,cv2.bitwise_not(cyan))
            count, labels, stats, centers=cv2.connectedComponentsWithStats(foreground,8)
            objects=[]
            for k in range(1,count):
                area=int(stats[k,cv2.CC_STAT_AREA])
                w=int(stats[k,cv2.CC_STAT_WIDTH])
                h=int(stats[k,cv2.CC_STAT_HEIGHT])
                if 140 <= area <= 1200 and 0.6 <= w/max(h,1) <= 1.52 and min(w,h)>=12:
                    objects.append(tuple(map(float,centers[k])))
            if len(objects)!=1:
                return None
            x,y=objects[0]
            if anchored:
                _, _, a_stats, a_centers=cv2.connectedComponentsWithStats(cyan,8)
                anchors=[tuple(map(float,a_centers[k])) for k in range(1,len(a_stats))
                         if 120 <= int(a_stats[k,cv2.CC_STAT_AREA]) <= 400
                         and 30 < a_centers[k][0] < 195
                         and 200 < a_centers[k][1] < 312]
                if len(anchors)!=1:
                    return None
                x,y=x-anchors[0][0]+70,y-anchors[0][1]+270
            if not all(isfinite(v) for v in (x,y)):
                return None
            results[idx]=(x,y)
    finally:
        cap.release()
    if len(results)!=3:
        return None
    return [results[i] for i in indices]


def raster_linear_forecast(past, indices, future_index):
    if past is None:
        return None
    if not (len(past)==len(indices)==3 and indices[0]<indices[1]<indices[2]<future_index):
        raise ValueError("invalid raster chronology")
    dt=indices[2]-indices[1]
    horizon=future_index-indices[2]
    return [past[2][k]+(past[2][k]-past[1][k])*horizon/dt for k in range(2)]


def raster_spatial_agreement(raster_xy, spatial_xy, tolerance_px=3.0):
    """Conservative compatibility gate; never magically repair disagreement."""
    from math import hypot
    if raster_xy is None or spatial_xy is None:
        return False
    return hypot(raster_xy[0]-spatial_xy[0],raster_xy[1]-spatial_xy[1]) <= tolerance_px
