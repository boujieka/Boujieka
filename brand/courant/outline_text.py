"""Outline text from a variable font instance into SVG path data. Usage: outline.py font.ttf wdth wght "text" """
import sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
font = TTFont(sys.argv[1])
font = instantiateVariableFont(font, {"wdth": float(sys.argv[2]), "wght": float(sys.argv[3])})
gs, cmap = font.getGlyphSet(), font.getBestCmap()
upm = font['head'].unitsPerEm
kern_pairs = {}
x = 0; parts = []
text = sys.argv[4]
for ch in text:
    g = cmap[ord(ch)]
    pen = SVGPathPen(gs)
    gs[g].draw(TransformPen(pen, (1, 0, 0, -1, x, 0)))
    parts.append(pen.getCommands())
    x += gs[g].width
asc = font['OS/2'].sCapHeight; xh = font['OS/2'].sxHeight
print(f"UPM={upm} WIDTH={x} CAP={asc} XH={xh}")
print(" ".join(parts))
