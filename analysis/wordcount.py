"""Word-count check for manuscript sections."""
import re
from pathlib import Path

t = (Path(__file__).resolve().parents[1] / "manuscript" / "main.tex").read_text()

def count(body: str) -> int:
    body = re.sub(r"\\textbf{[^}]*}", " ", body)
    body = re.sub(r"\\citep\{[^}]*\}", " ", body)
    body = re.sub(r"\\cite\{[^}]*\}", " ", body)
    body = re.sub(r"\\label\{[^}]*\}", " ", body)
    body = re.sub(r"\\ref\{[^}]*\}", " X ", body)
    body = re.sub(r"\\input\{[^}]*\}", " ", body)
    body = re.sub(r"\\includegraphics(\[[^\]]*\])?\{[^}]*\}", " ", body)
    body = re.sub(r"\\caption\{[^}]*\}", " ", body)
    body = re.sub(r"\$[^$]*\$", "X", body)
    body = re.sub(r"\\\\[a-zA-Z]+\*?", " ", body)
    body = re.sub(r"[{}\\]", " ", body)
    body = re.sub(r"%.*", "", body)
    return len(body.split())

for label, pat in [
    ("Abstract",   r"\\begin{abstract}(.*?)\\end{abstract}"),
    ("KO box",     r"\\begin{mdframed}(.*?)\\end{mdframed}"),
    ("Introduction", r"\\section{Introduction}.*?\\label{sec:intro}(.*?)\\section{Methods}"),
    ("Methods",    r"\\section{Methods}.*?\\label{sec:methods}(.*?)\\section{Results}"),
    ("Results",    r"\\section{Results}.*?\\label{sec:results}(.*?)\\section{Discussion}"),
]:
    m = re.search(pat, t, re.DOTALL)
    if m:
        print(f"{label:>14s}: {count(m.group(1)):>4d} words")

# discussion is in its own file
disc = (Path(__file__).resolve().parents[1] / "manuscript" / "discussion.tex").read_text()
print(f"{'Discussion':>14s}: {count(disc):>4d} words")
