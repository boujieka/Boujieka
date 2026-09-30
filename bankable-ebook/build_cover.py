"""KDP paperback full-wrap cover (6 x 9 in trim, 0.125 in bleed) for Bankable Is Not Enough.

usage: build_cover.py front.png pages fonts_dir out.pdf [paper=white|cream]
Spine width = pages x 0.002252 in (white) or 0.0025 in (cream), KDP black-and-white interiors.
"""
import os
import sys

from PIL import Image, ImageFilter
from weasyprint import HTML

front_src, pages, fonts, out = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
paper = sys.argv[5] if len(sys.argv) > 5 else "white"
BLEED, TW, TH = 0.125, 6.0, 9.0
spine = pages * (0.002252 if paper == "white" else 0.0025)
W, H = BLEED + TW + spine + TW + BLEED, BLEED + TH + BLEED
DPI = 300
px = lambda inch: int(round(inch * DPI))

# ---------- raster background at 300 dpi (no PDF transparency)
bg = Image.new("RGB", (px(W), px(H)), (26, 18, 12))
src = Image.open(front_src).convert("RGB")
fx0 = px(BLEED + TW + spine)
fw, fh = px(W) - fx0, px(H)
scale = max(fw / src.width, fh / src.height)
big = src.resize((round(src.width * scale), round(src.height * scale)), Image.LANCZOS)
cx = (big.width - fw) // 2
front = big.crop((cx, 0, cx + fw, fh))
bg.paste(front, (fx0, 0))
# back: mirrored, blurred and darkened front
back_w = px(BLEED + TW)
back = big.transpose(Image.FLIP_LEFT_RIGHT).crop((0, 0, back_w, fh)).filter(ImageFilter.GaussianBlur(28))
back = Image.blend(back, Image.new("RGB", back.size, (26, 18, 12)), 0.74)
bg.paste(back, (0, 0))
bg_path = os.path.splitext(out)[0] + "_bg.jpg"
bg.save(bg_path, quality=95, dpi=(DPI, DPI))

F = lambda n: "file://" + os.path.abspath(os.path.join(fonts, n))
gold, cream = "#d9b25f", "#f3e6cf"
spine_x = BLEED + TW
back_l, back_r = BLEED + 0.55, BLEED + TW - 0.55   # text box inside the back trim with 0.55 in margin

html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"/><style>
@font-face {{ font-family: Charis; src: url({F('CharisSIL-Regular.ttf')}); }}
@font-face {{ font-family: Charis; src: url({F('CharisSIL-Bold.ttf')}); font-weight: bold; }}
@font-face {{ font-family: Charis; src: url({F('CharisSIL-Italic.ttf')}); font-style: italic; }}
@page {{ size: {W:.4f}in {H:.4f}in; margin: 0; }}
html, body {{ margin: 0; padding: 0; }}
.bg {{ position: absolute; left: 0; top: 0; width: {W:.4f}in; height: {H:.4f}in; }}
.spine {{ position: absolute; left: {spine_x:.4f}in; top: {BLEED}in; width: {spine:.4f}in; height: {TH}in; }}
.spine .rot {{ position: absolute; left: 50%; top: 50%; width: {TH - 0.9:.3f}in; height: {spine:.4f}in;
  transform: translate(-50%, -50%) rotate(90deg); display: flex; align-items: center; justify-content: space-between;
  font-family: Charis; color: {gold}; }}
.spine .t {{ font-weight: bold; font-size: 13pt; letter-spacing: 1.6pt; white-space: nowrap; }}
.spine .a {{ font-size: 8.5pt; letter-spacing: 1.4pt; color: {cream}; white-space: nowrap; }}
.back {{ position: absolute; left: {back_l:.4f}in; top: {BLEED + 0.75:.4f}in; width: {back_r - back_l:.4f}in;
  font-family: Charis; color: {cream}; }}
.back .kicker {{ font-size: 8.5pt; letter-spacing: 2pt; color: {gold}; margin: 0 0 0.16in 0; }}
.back h1 {{ font-size: 18.5pt; line-height: 1.22; font-weight: bold; color: #ffffff; margin: 0 0 0.24in 0; }}
.back p {{ font-size: 10.2pt; line-height: 1.45; margin: 0 0 0.13in 0; text-align: left; }}
.back .rule {{ width: 1.1in; border-top: 1pt solid {gold}; margin: 0.22in 0 0.2in 0; }}
.back .tag {{ font-size: 9.5pt; letter-spacing: 1.6pt; color: {gold}; font-weight: bold; margin-bottom: 0.2in; }}
.back .bio {{ font-size: 8.8pt; font-style: italic; line-height: 1.4; width: 3.1in; }}
</style></head><body>
<img class="bg" src="file://{os.path.abspath(bg_path)}"/>
<div class="spine"><div class="rot"><span class="t">BANKABLE IS NOT ENOUGH</span><span class="a">EMMANUEL BOUJIEKA KAMGA</span></div></div>
<div class="back">
  <div class="kicker">THE SUSTAINABLE FINANCIAL CLOSE FRAMEWORK</div>
  <h1>A power project that lenders will finance has passed only half of its examination.</h1>
  <p>A power purchase agreement can satisfy every lender and still become a public liability. Contracts are signed
  quickly, often in response to shortages, through direct negotiation, with fixed payments in hard currency and state
  support behind a financially weak buyer. Each contract is bankable. The sum of them is not always affordable.</p>
  <p>This book turns the state's question into a framework that a government can apply before signature: seven tests,
  forty-five questions, three gates at which to ask them, three institutions that answer for them, and four decisions
  that they can lead to. A power deal should close only when both tests, the lender's and the state's, have been passed
  and the state's answer has been published.</p>
  <div class="rule"></div>
  <div class="tag">7 TESTS · 45 QUESTIONS · 3 GATES · 1 DECISION</div>
  <p class="bio">Emmanuel Boujieka Kamga is an energy investment specialist with more than twenty years of professional
  experience, including seventeen years in the power and energy access sector across 22 African countries.</p>
</div>
</body></html>"""
HTML(string=html, base_url=os.getcwd()).write_pdf(out)
print(f"wrote {out}: {W:.4f} x {H:.4f} in, spine {spine:.4f} in ({pages} pages, {paper} paper)")
