"""Find every drawn character in the story panels and identify who it is.

Eyes in this art style are white discs with a dark pupil, drawn in pairs on a
round brown face. For each eye pair we estimate the face circle, then identify
the character from the clothing colour under the chin and the headwear above.
Writes scripts/faces.json: {page: [{panel, cx, cy, r, who, score}, ...]}.
"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PANELS = {int(k): v for k, v in json.load(open(os.path.join(ROOT, "scripts", "panels.json"))).items()}

# Signature clothing colours in the book (RGB), sampled from the cast page.
CLOTHES = {
    "BELPAU": (240, 180, 50),     # yellow top
    "ENILEC": (33, 92, 156),      # royal blue
    "KERBU": (34, 40, 60),        # dark navy suit
    "EMSON": (152, 160, 178),     # grey suit
    "TIDIANIE": (140, 42, 66),    # maroon blazer
    "PAUL": (122, 84, 52),        # brown suit
}


def eye_blobs(img):
    white = (img.min(axis=2) > 235)
    lab, n = ndimage.label(white)
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
        if not (14 <= w <= 60 and 14 <= h <= 60 and 0.7 < w / h < 1.4):
            continue
        area = (lab[sl] == i).sum()
        if area < 0.45 * w * h:          # eyes are near-circular (pupil cut out)
            continue
        cy = (sl[0].start + sl[0].stop) / 2; cx = (sl[1].start + sl[1].stop) / 2
        # a dark pupil must sit inside the disc bounding box
        box = img[sl[0].start:sl[0].stop, sl[1].start:sl[1].stop]
        if (box.max(axis=2) < 70).sum() < 12:
            continue
        # surroundings must be skin (brownish), not a bubble or sky
        ring = img[max(0, int(cy - h)):int(cy + h), max(0, int(cx - 1.6 * w)):int(cx + 1.6 * w)]
        r, g, b = ring[..., 0].astype(int), ring[..., 1].astype(int), ring[..., 2].astype(int)
        skin = ((r > g + 10) & (g > b - 5) & (r < 215) & (r > 60)).mean()
        if skin < 0.18:
            continue
        out.append((cx, cy, (w + h) / 2))
    return out


def classify(img, cx, cy, r):
    H, W, _ = img.shape
    y0 = int(min(H - 2, cy + 2.35 * r)); y1 = int(min(H - 1, cy + 2.9 * r))
    x0 = int(max(0, cx - 0.9 * r)); x1 = int(min(W - 1, cx + 0.9 * r))
    patch = img[y0:y1, x0:x1].reshape(-1, 3).astype(int)
    if len(patch) == 0:
        return None, 0
    # median of the dominant (non-outline, non-white) pixels
    keep = patch[(patch.max(axis=1) > 45) & (patch.min(axis=1) < 235)]
    if len(keep) == 0:
        return None, 0
    col = np.median(keep, axis=0)
    best = min(CLOTHES, key=lambda k: np.sum((col - CLOTHES[k]) ** 2))
    return best, float(np.sqrt(np.sum((col - CLOTHES[best]) ** 2)))


def main():
    faces = {}
    for page, boxes in PANELS.items():
        if page < 3 or page > 22 or page == 4:
            continue
        img = np.asarray(Image.open(os.path.join(ROOT, "assets", "pages", f"pg-{page:03d}.jpg")).convert("RGB"))
        blobs = eye_blobs(img)
        used, found = set(), []
        for i, a in enumerate(blobs):
            if i in used:
                continue
            best = None
            for j, b in enumerate(blobs):
                if j == i or j in used:
                    continue
                d = abs(b[0] - a[0]); dy = abs(b[1] - a[1])
                if 1.6 * a[2] < d < 5.5 * a[2] and dy < 0.5 * a[2] and (best is None or d < best[1]):
                    best = (j, d)
            if not best:
                continue
            j, d = best; b = blobs[j]; used |= {i, j}
            cx, cy = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 0.05 * d
            r = 1.33 * d
            panel = next((k for k, (x, y, w, h) in enumerate(boxes) if x <= cx <= x + w and y <= cy <= y + h), None)
            who, dist = classify(img, cx, cy, r)
            found.append({"panel": panel, "cx": round(cx, 1), "cy": round(cy, 1), "r": round(r, 1), "who": who, "dist": round(dist, 1)})
        faces[page] = sorted(found, key=lambda f: (f["panel"] if f["panel"] is not None else 99, f["cx"]))
        print(page, [(f["panel"], f["who"], int(f["cx"]), int(f["cy"]), int(f["r"]), int(f["dist"])) for f in faces[page]])
    json.dump(faces, open(os.path.join(ROOT, "scripts", "faces.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
