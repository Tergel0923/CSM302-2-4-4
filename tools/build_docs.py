#!/usr/bin/env python3
"""Rebuild Mongolian PDFs from versioned Markdown (ReportLab + DejaVu Sans)."""
import re
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
from reportlab.lib.pagesizes import A4

ROOT=Path(__file__).resolve().parents[1]
FONT=Path('/usr/share/fonts/truetype/dejavu')
pdfmetrics.registerFont(TTFont('DejaVu',str(FONT/'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuBold',str(FONT/'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuMono',str(FONT/'DejaVuSansMono.ttf')))
BLUE=colors.HexColor('#12324c');TEAL=colors.HexColor('#167d89')
styles={
 'body':ParagraphStyle('body',fontName='DejaVu',fontSize=9.2,leading=14,spaceAfter=9,textColor=BLUE),
 'h1':ParagraphStyle('h1',fontName='DejaVuBold',fontSize=22,leading=28,spaceAfter=18,textColor=BLUE),
 'h2':ParagraphStyle('h2',fontName='DejaVuBold',fontSize=12,leading=17,spaceBefore=8,spaceAfter=9,textColor=TEAL),
 'cell':ParagraphStyle('cell',fontName='DejaVu',fontSize=8.2,leading=12,textColor=BLUE),
 'code':ParagraphStyle('code',fontName='DejaVuMono',fontSize=7.2,leading=11,backColor=colors.HexColor('#eef3f7'),borderPadding=8,spaceBefore=4,spaceAfter=12)
}
def p(text,style='body'):
    return Paragraph(escape(text),styles[style])
def footer(canvas,doc):
    w,h=A4;canvas.setStrokeColor(TEAL);canvas.setLineWidth(2);canvas.line(44,h-35,w-44,h-35)
    canvas.setFont('DejaVu',8);canvas.setFillColor(TEAL)
    canvas.drawString(44,h-25,'F.CSM302  /  II-4-4  /  ЦӨМИЙН ӨГӨГДЛИЙН БҮТЭЦ')
    canvas.setFillColor(BLUE);canvas.drawString(44,27,'2026-11-01  ·  Хэрэгжилт ба баталгаажуулалтын тэмдэглэл')
    canvas.drawRightString(w-44,27,str(doc.page))
def render(source,target):
    lines=source.read_text().splitlines();flow=[];i=0
    while i<len(lines):
        line=lines[i];i+=1
        if not line.strip():continue
        if line=='---PAGE---':flow.append(PageBreak());continue
        if line.startswith('```'):
            code=[]
            while i<len(lines) and not lines[i].startswith('```'):code.append(lines[i]);i+=1
            i+=1;flow.append(Preformatted('\n'.join(code),styles['code']));continue
        if line.startswith('|'):
            rows=[]
            while True:
                rows.append([p(t.strip(),'cell') for t in line.strip('|').split('|')])
                if i>=len(lines) or not lines[i].startswith('|'):break
                line=lines[i];i+=1
            widths=[(A4[0]-88)/len(rows[0])]*len(rows[0]);table=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT')
            table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#d7edf0')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#d3dde5'))]))
            flow.extend([table,Spacer(1,12)]);continue
        if line.startswith('# '):flow.append(p(line[2:],'h1'))
        elif line.startswith('## '):flow.append(p(line[3:],'h2'))
        else:flow.append(p(line))
    doc=SimpleDocTemplate(str(target),pagesize=A4,rightMargin=44,leftMargin=44,topMargin=55,bottomMargin=49,title=source.stem+' — II-4-4',author='II-4-4 / AI тусламжтай боловсруулсан төсөл')
    doc.build(flow,onFirstPage=footer,onLaterPages=footer)
    print(target)

if __name__=='__main__':
    for src,dst in [('Report.md','II-4-4_BD1_Report.pdf'),('Manual.md','II-4-4_Manual.pdf'),('Review_TEMPLATE.md','II-4-4_Review_IV-2-7_TEMPLATE.pdf')]:
        render(ROOT/'docs'/src,ROOT/'docs'/dst)
