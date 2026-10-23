#!/usr/bin/env python3
"""Build ATS-safe resume + cover letter PDFs from a job folder's package.yaml."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

ROOT_HELP = "Windows: build.bat ..\\jobs\\<slug>   macOS/Linux: ./build.sh ../jobs/<slug>"


def xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


_WIN_RESERVED = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def slug(text: str) -> str:
    text = re.sub(r"[^\w]+", "_", text.strip(), flags=re.ASCII)
    text = re.sub(r"_+", "_", text).strip("._ ") or "output"
    if text.upper() in _WIN_RESERVED:
        text = f"_{text}"
    return text



def add_style(styles, name, **kwargs):
    if name not in styles.byName:
        styles.add(ParagraphStyle(name=name, **kwargs))
    return styles[name]


def styles():
    s = getSampleStyleSheet()
    add_style(
        s, "Name", parent=s["Heading1"], fontName="Times-Bold",
        fontSize=16, leading=18, spaceAfter=2, alignment=TA_LEFT,
    )
    add_style(
        s, "Sub", parent=s["Normal"], fontName="Times-Roman",
        fontSize=10, leading=12, spaceAfter=8,
    )
    add_style(
        s, "H", parent=s["Heading2"], fontName="Times-Bold",
        fontSize=11, leading=14, spaceBefore=10, spaceAfter=4,
    )
    add_style(
        s, "Body", parent=s["Normal"], fontName="Times-Roman",
        fontSize=10, leading=13, spaceAfter=6, alignment=TA_LEFT,
    )
    add_style(
        s, "Bullet", parent=s["Normal"], fontName="Times-Roman",
        fontSize=10, leading=13, leftIndent=14, bulletIndent=0,
        spaceAfter=3,
    )
    add_style(
        s, "JobLine", parent=s["Normal"], fontName="Times-Bold",
        fontSize=10, leading=13, spaceBefore=6, spaceAfter=1,
    )
    add_style(
        s, "JobMeta", parent=s["Normal"], fontName="Times-Italic",
        fontSize=9.5, leading=12, spaceAfter=3,
    )
    return s


def load_package(job_dir: Path) -> dict:
    path = job_dir / "package.yaml"
    if not path.is_file():
        sys.exit(f"No package.yaml in {job_dir}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        sys.exit("package.yaml did not parse as a mapping")
    return data


def contact_line(c: dict) -> str:
    parts = [c.get("location"), c.get("phone"), c.get("email")]
    parts += list(c.get("links") or [])
    return " | ".join(p for p in parts if p)


def resume_story(pkg: dict, s) -> list:
    c = pkg.get("contact") or {}
    story = []
    name = xml_escape(c.get("name") or "Name")
    story.append(Paragraph(name, s["Name"]))
    if c.get("headline"):
        story.append(Paragraph(xml_escape(c["headline"]), s["Sub"]))
    cl = contact_line(c)
    if cl:
        story.append(Paragraph(xml_escape(cl), s["Sub"]))

    summary = (pkg.get("summary") or "").strip()
    if summary:
        story.append(Paragraph("SUMMARY", s["H"]))
        story.append(Paragraph(xml_escape(summary), s["Body"]))

    skills = pkg.get("skills") or []
    skills = [sk for sk in skills if sk and (sk.get("label") or sk.get("items"))]
    if skills:
        story.append(Paragraph("SKILLS", s["H"]))
        for sk in skills:
            label = xml_escape((sk.get("label") or "").strip())
            items = xml_escape((sk.get("items") or "").strip())
            if label and items:
                story.append(Paragraph(f"<b>{label}:</b> {items}", s["Body"]))
            elif items:
                story.append(Paragraph(items, s["Body"]))

    exp = pkg.get("experience") or []
    if exp:
        story.append(Paragraph("EXPERIENCE", s["H"]))
        for job in exp:
            title = xml_escape(job.get("title") or "")
            company = xml_escape(job.get("company") or "")
            dates = xml_escape(job.get("dates") or "")
            loc = xml_escape(job.get("location") or "")
            head = " · ".join(p for p in (title, company) if p)
            meta = " · ".join(p for p in (dates, loc) if p)
            if head:
                story.append(Paragraph(head, s["JobLine"]))
            if meta:
                story.append(Paragraph(meta, s["JobMeta"]))
            for b in job.get("bullets") or []:
                if b and str(b).strip():
                    story.append(Paragraph(f"• {xml_escape(str(b).strip())}", s["Bullet"]))

    edu = [e for e in (pkg.get("education") or []) if e and str(e).strip()]
    if edu:
        story.append(Paragraph("EDUCATION", s["H"]))
        for e in edu:
            story.append(Paragraph(xml_escape(str(e).strip()), s["Body"]))

    for sec in pkg.get("extra_sections") or []:
        heading = (sec.get("heading") or "").strip()
        if heading:
            story.append(Paragraph(xml_escape(heading.upper()), s["H"]))
        for b in sec.get("bullets") or []:
            if b and str(b).strip():
                story.append(Paragraph(f"• {xml_escape(str(b).strip())}", s["Bullet"]))

    return story


def letter_story(pkg: dict, s) -> list:
    c = pkg.get("contact") or {}
    t = pkg.get("target") or {}
    cl = pkg.get("cover_letter") or {}
    story = []
    name = xml_escape(c.get("name") or "Name")
    story.append(Paragraph(name, s["Name"]))
    meta = contact_line(c)
    if meta:
        story.append(Paragraph(xml_escape(meta), s["Sub"]))
    role = t.get("role") or "the role"
    company = t.get("company") or ""
    story.append(Paragraph(
        xml_escape(f"Re: {role}" + (f" — {company}" if company else "")),
        s["Sub"],
    ))
    greet = xml_escape(cl.get("greeting") or "Hiring Manager")
    story.append(Paragraph(f"Dear {greet},", s["Body"]))
    for p in cl.get("paragraphs") or []:
        if p and str(p).strip():
            story.append(Paragraph(xml_escape(str(p).strip()), s["Body"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Sincerely,", s["Body"]))
    story.append(Paragraph(name, s["Body"]))
    return story


def write_pdf(path: Path, flowables) -> None:
    doc = SimpleDocTemplate(
        str(path),
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
        title=path.stem,
    )
    doc.build(flowables)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build resume + cover letter PDFs.")
    parser.add_argument("job_dir", help="Path to jobs/<slug> containing package.yaml")
    args = parser.parse_args()
    job_dir = Path(args.job_dir).resolve()
    if not job_dir.is_dir():
        sys.exit(f"Not a directory: {job_dir}\n{ROOT_HELP}")

    pkg = load_package(job_dir)
    s = styles()
    c = pkg.get("contact") or {}
    t = pkg.get("target") or {}
    who = slug(c.get("name") or "Candidate")
    role = slug(t.get("role") or "Resume")
    resume_path = job_dir / f"{who}_{role}_Resume.pdf"
    letter_path = job_dir / f"{who}_{role}_Cover_Letter.pdf"
    write_pdf(resume_path, resume_story(pkg, s))
    write_pdf(letter_path, letter_story(pkg, s))
    print(resume_path)
    print(letter_path)


if __name__ == "__main__":
    main()
