"""Splice generated SVGs into a module's HTML at named placeholders.

Usage:  python splice.py ../module01.html

Each placeholder is an HTML comment of the form <!--FIG_NAME--> and is
replaced by the contents of mNN_fig_name.svg, where NN comes from the
module filename. Running it twice is safe: the placeholder is preserved
above the spliced block so the next run finds it again.
"""
import re
import sys
import os

BEGIN = "<!--FIG_{name}-->"
END = "<!--/FIG_{name}-->"


def splice(html_path):
    base = os.path.basename(html_path)
    num = re.search(r"(\d+)", base).group(1)
    here = os.path.dirname(os.path.abspath(__file__))
    src = open(html_path, encoding="utf-8").read()
    names = set(re.findall(r"<!--FIG_([A-Z]+)-->", src))
    if not names:
        print("no placeholders found")
        return
    for name in sorted(names):
        svg_file = os.path.join(here, f"m{num}_fig_{name.lower()}.svg")
        svg = open(svg_file, encoding="utf-8").read()
        b, e = BEGIN.format(name=name), END.format(name=name)
        pat = re.compile(re.escape(b) + r".*?" + re.escape(e), re.S)
        block = b + "\n" + svg + "\n" + e
        if pat.search(src):
            src = pat.sub(lambda _: block, src)
            print(f"  replaced FIG_{name} ({len(svg)} bytes)")
        else:
            src = src.replace(b, block)
            print(f"  inserted FIG_{name} ({len(svg)} bytes)")
    open(html_path, "w", encoding="utf-8").write(src)
    print("wrote", html_path)


if __name__ == "__main__":
    splice(sys.argv[1])
