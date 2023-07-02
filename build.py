import os
import markdown
import shutil

from staticjinja import Site
from pathlib import Path

#based on the example build script taken from the staticjinja documentation
#https://staticjinja.readthedocs.io/en/stable/user/advanced.html

output_path = Path(__file__).resolve().parent / "output"
shutil.rmtree(output_path)

md = markdown.Markdown(output_format="html5", extensions=["meta"])

def md_context(template):
  markdown_content = Path(template.filename).read_text()
  converted = md.convert(markdown_content)
  extracted_meta = md.Meta

  metadata = {}
  for key in extracted_meta:
    metadata[key] = extracted_meta[key][0]
  
  if converted.startswith("<hr>"):
    converted = converted.replace("<hr>", "", 1)
  converted = converted.strip()

  context = {**metadata, **{
    "post_content_html": converted
  }}
  return context


def render_md(site, template, **kwargs):
  # i.e. posts/post1.md -> build/posts/post1.html
  out = site.outpath / Path(template.name).with_suffix(".html")

  # Compile and stream the result
  os.makedirs(out.parent, exist_ok=True)
  site.get_template("blog/_post.html").stream(**kwargs).dump(str(out), encoding="utf-8")

site = Site.make_site(
  searchpath="src",
  outpath="output",
  contexts=[(r".*\.md", md_context)],
  rules=[(r".*\.md", render_md)],
  staticpaths=[
    "blog/assets"
  ]
)
site.render()