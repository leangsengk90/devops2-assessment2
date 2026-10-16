"""Tiny XML builders that reproduce the UP dissertation template's direct formatting exactly.

Inline markup in text:  _italic_   **bold**   (underscores inside words are left alone)
"""
import re
from xml.sax.saxutils import escape

W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'

_tok = re.compile(r"(\*\*.+?\*\*|(?<![\w/])_(?!\s).+?(?<!\s)_(?![\w/]))")


def runs(text, base_rpr=""):
    out = []
    for part in _tok.split(text):
        if not part:
            continue
        rpr = base_rpr
        if part.startswith("**") and part.endswith("**"):
            part, rpr = part[2:-2], rpr + "<w:b/><w:bCs/>"
        elif part.startswith("_") and part.endswith("_") and len(part) > 2:
            part, rpr = part[1:-1], rpr + "<w:i/><w:iCs/>"
        r = f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
        out.append(f'<w:r>{r}<w:t xml:space="preserve">{escape(part)}</w:t></w:r>')
    return "".join(out)


def p(text, after=160, before=0, line=360, jc="both", ind="", rpr="", extra_ppr=""):
    i = f"<w:ind {ind}/>" if ind else ""
    return (f'<w:p {W}><w:pPr>{extra_ppr}<w:spacing w:after="{after}" w:before="{before}" w:line="{line}"/>'
            f'{i}<w:jc w:val="{jc}"/></w:pPr>{runs(text, rpr)}</w:p>')


def h1(text):
    return (f'<w:p {W}><w:pPr><w:pStyle w:val="Heading1"/><w:pageBreakBefore/><w:spacing w:after="240" w:before="240"/>'
            f'<w:jc w:val="left"/></w:pPr>{runs(text)}</w:p>')


def h2(text):
    return (f'<w:p {W}><w:pPr><w:pStyle w:val="Heading2"/><w:keepNext/><w:spacing w:after="140" w:before="280"/></w:pPr>'
            f'{runs(text)}</w:p>')


def h3(text):
    return (f'<w:p {W}><w:pPr><w:pStyle w:val="Heading3"/><w:keepNext/><w:spacing w:after="120" w:before="220"/></w:pPr>'
            f'{runs(text)}</w:p>')


def li(text):
    return p(text, after=80, ind='w:left="360"')


def caption(kind_num, title):
    return (f'<w:p {W}><w:pPr><w:keepNext/><w:spacing w:after="100" w:before="200" w:line="240"/><w:jc w:val="left"/></w:pPr>'
            f'<w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:t xml:space="preserve">{escape(kind_num)} </w:t></w:r>'
            f'{runs(title, "<w:i/><w:iCs/>")}</w:p>')


def note(text):
    return (f'<w:p {W}><w:pPr><w:spacing w:after="200" w:before="60" w:line="240"/><w:jc w:val="left"/></w:pPr>'
            f'<w:r><w:rPr><w:i/><w:iCs/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:t xml:space="preserve">Note. </w:t></w:r>'
            f'{runs(text, "<w:sz w:val=\"20\"/><w:szCs w:val=\"20\"/>")}</w:p>')


def figcap(text):
    return (f'<w:p {W}><w:pPr><w:spacing w:after="220" w:line="240"/><w:jc w:val="left"/></w:pPr>'
            f'{runs(text, "<w:sz w:val=\"20\"/><w:szCs w:val=\"20\"/>")}</w:p>')


def ref(text):
    return (f'<w:p {W}><w:pPr><w:spacing w:after="120" w:line="360"/><w:ind w:left="720" w:hanging="720"/>'
            f'<w:jc w:val="left"/></w:pPr>{runs(text)}</w:p>')


def pagebreak():
    return f'<w:p {W}><w:r><w:br w:type="page"/></w:r></w:p>'


_MAR = ('<w:tcMar><w:top w:type="dxa" w:w="80"/><w:left w:type="dxa" w:w="110"/>'
        '<w:bottom w:type="dxa" w:w="80"/><w:right w:type="dxa" w:w="110"/></w:tcMar>')


def _cell(text, w, header, sz):
    shd = '<w:shd w:fill="EDEFF3" w:color="auto" w:val="clear"/>' if header else ""
    b = "<w:b/><w:bCs/>" if header else '<w:b w:val="false"/><w:bCs w:val="false"/>'
    rpr = f'{b}<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
    paras = "".join(
        f'<w:p><w:pPr><w:spacing w:after="40" w:line="240"/><w:jc w:val="left"/></w:pPr>{runs(line, rpr)}</w:p>'
        for line in str(text).split("\n"))
    return (f'<w:tc><w:tcPr><w:tcW w:type="dxa" w:w="{w}"/>{shd}{_MAR}<w:vAlign w:val="center"/></w:tcPr>'
            f'{paras}</w:tc>')


def table(headers, rows, widths, sz=20):
    """widths in DXA; the template's tables are 8640 wide."""
    tw = sum(widths)
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    hdr = '<w:tr><w:trPr><w:tblHeader/></w:trPr>' + "".join(_cell(h, w, True, sz) for h, w in zip(headers, widths)) + "</w:tr>"
    body = "".join("<w:tr><w:trPr><w:cantSplit/></w:trPr>" + "".join(_cell(c, w, False, sz) for c, w in zip(r, widths)) + "</w:tr>" for r in rows)
    return (f'<w:tbl {W}><w:tblPr><w:tblW w:type="dxa" w:w="{tw}"/><w:tblBorders>'
            '<w:top w:val="single" w:color="000000" w:sz="6"/><w:left w:val="none" w:color="FFFFFF" w:sz="0"/>'
            '<w:bottom w:val="single" w:color="000000" w:sz="6"/><w:right w:val="none" w:color="FFFFFF" w:sz="0"/>'
            '<w:insideH w:val="single" w:color="BFBFBF" w:sz="2"/><w:insideV w:val="none" w:color="FFFFFF" w:sz="0"/>'
            f'</w:tblBorders></w:tblPr><w:tblGrid>{grid}</w:tblGrid>{hdr}{body}</w:tbl>')
