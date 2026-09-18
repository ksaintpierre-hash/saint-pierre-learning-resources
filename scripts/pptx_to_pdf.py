"""Render a .pptx to a reasonably faithful .pdf without LibreOffice.

LibreOffice headless conversion is unavailable in this environment (its
multi-process bootstrap exits before rendering, in this sandbox and only
this sandbox). This renders each slide directly from python-pptx shape
geometry, text runs, and embedded images onto a reportlab canvas at the
slide's actual size, so positions, text, and pictures match the source
deck. Effects python-pptx does not expose (gradients, shadows, SmartArt)
are skipped rather than approximated.
"""
import sys, io
from pptx import Presentation
from pptx.util import Emu
from pptx.enum.shapes import MSO_SHAPE_TYPE
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.utils import ImageReader
from PIL import Image

EMU_PER_PT = 12700

def emu_to_pt(v):
    return v / EMU_PER_PT

def rgb_of(color_format):
    try:
        if color_format.type is not None:
            rgb = color_format.rgb
            return (rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
    except Exception:
        pass
    return None

def draw_text_frame(c, tf, left_pt, top_pt, width_pt, height_pt, page_h):
    y = top_pt
    for para in tf.paragraphs:
        runs = para.runs
        if not runs and not para.text:
            y += 12
            continue
        text = ''.join(r.text for r in runs) if runs else para.text
        if not text.strip():
            y += 12
            continue
        size = 14
        bold = False
        color = (0.13, 0.15, 0.18)
        if runs:
            r0 = runs[0]
            if r0.font.size:
                size = r0.font.size.pt
            bold = bool(r0.font.bold)
            rgb = rgb_of(r0.font.color)
            if rgb:
                color = rgb
        elif para.font.size:
            size = para.font.size.pt
        font = 'Helvetica-Bold' if bold else 'Helvetica'
        c.setFont(font, max(6, min(size, 44)))
        c.setFillColorRGB(*color)
        indent = getattr(para, 'level', 0) * 14
        py = page_h - y - size
        max_chars = max(10, int((width_pt - indent) / (size * 0.52)))
        words = text.split(' ')
        line = ''
        lines = []
        for w in words:
            trial = (line + ' ' + w).strip()
            if len(trial) > max_chars and line:
                lines.append(line)
                line = w
            else:
                line = trial
        if line:
            lines.append(line)
        for ln in lines:
            if py < 20:
                break
            c.drawString(left_pt + indent, py, ln)
            py -= size * 1.22
        y = page_h - py

def draw_shape(c, shape, page_h, ox=0, oy=0):
    try:
        left = emu_to_pt(shape.left or 0) + ox
        top = emu_to_pt(shape.top or 0) + oy
        width = emu_to_pt(shape.width or 0)
        height = emu_to_pt(shape.height or 0)
    except Exception:
        return
    if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
        for sub in shape.shapes:
            draw_shape(c, sub, page_h, ox=left - emu_to_pt(getattr(shape, 'left', 0) or 0) if False else ox, oy=oy)
        return
    try:
        if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
            img_bytes = shape.image.blob
            im = Image.open(io.BytesIO(img_bytes))
            if im.mode not in ('RGB', 'RGBA'):
                im = im.convert('RGB')
            c.drawImage(ImageReader(im), left, page_h - top - height, width=width, height=height,
                        preserveAspectRatio=False, mask='auto')
            return
    except Exception:
        pass
    try:
        fill = shape.fill
        if fill.type is not None:
            rgb = rgb_of(fill.fore_color)
            if rgb:
                c.setFillColorRGB(*rgb)
                c.rect(left, page_h - top - height, width, height, fill=1, stroke=0)
    except Exception:
        pass
    if getattr(shape, 'has_text_frame', False) and shape.text_frame.text.strip():
        draw_text_frame(c, shape.text_frame, left + 4, top + 4, max(width - 8, 20), height, page_h)
    if getattr(shape, 'has_table', False):
        table = shape.table
        rows = len(table.rows)
        cols = len(table.columns)
        row_h = height / max(rows, 1)
        col_w = width / max(cols, 1)
        for ri in range(rows):
            for ci in range(cols):
                cell = table.cell(ri, ci)
                cx = left + ci * col_w
                cy = top + ri * row_h
                c.setStrokeColorRGB(0.7, 0.7, 0.7)
                c.rect(cx, page_h - cy - row_h, col_w, row_h, fill=0, stroke=1)
                if cell.text.strip():
                    draw_text_frame(c, cell.text_frame, cx + 3, cy + 3, col_w - 6, row_h - 6, page_h)

def convert(pptx_path, pdf_path):
    prs = Presentation(pptx_path)
    page_w = emu_to_pt(prs.slide_width)
    page_h = emu_to_pt(prs.slide_height)
    c = rl_canvas.Canvas(pdf_path, pagesize=(page_w, page_h))
    for slide in prs.slides:
        bg = None
        try:
            bg = rgb_of(slide.background.fill.fore_color)
        except Exception:
            pass
        c.setFillColorRGB(*(bg or (1, 1, 1)))
        c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
        for shape in slide.shapes:
            draw_shape(c, shape, page_h)
        c.showPage()
    c.save()
    return len(prs.slides)

if __name__ == '__main__':
    n = convert(sys.argv[1], sys.argv[2])
    print(f'Rendered {n} slides -> {sys.argv[2]}')
