"""Glue the Module 9 body parts to afd/_template_dark.html.

After the first autolink/splice run, afd/module09.html becomes the source of
truth and this script must not be run again -- the same rule Module 8 followed.
"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
AFD = os.path.dirname(HERE)

tpl = io.open(os.path.join(AFD, "_template_dark.html"), encoding="utf-8").read()

parts = []
for n in range(1, 7):
    p = os.path.join(HERE, f"m09_body{n}.html")
    parts.append(io.open(p, encoding="utf-8").read().rstrip() + "\n")
body = "\n".join(parts)

# The template carries a placeholder h1/sub/toc block between <body> and the
# <hr>; body1 supplies its own, so drop the template's.
start = tpl.index("<body>") + len("<body>")
end = tpl.index("<hr>") + len("<hr>")
head = tpl[:start]
tail = tpl[end:]

head = head.replace("<title>TITLE — Astrophysical Fluid Dynamics</title>",
                    "<title>9. Bondi accretion and the Parker wind — "
                    "Astrophysical Fluid Dynamics</title>")

out = head + "\n\n" + body + "\n" + tail
io.open(os.path.join(AFD, "module09.html"), "w", encoding="utf-8").write(out)
print("wrote module09.html (%d bytes, %d lines)" % (len(out), out.count("\n") + 1))
