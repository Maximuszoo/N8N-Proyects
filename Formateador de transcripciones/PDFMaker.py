import sys
import markdown2
from weasyprint import HTML

# Parámetros
input_arg   = sys.argv[1]     # /tmp/resumen.md
output_pdf  = sys.argv[2]     # Resumen_final.pdf

# Leemos el markdown en UTF-8
with open(input_arg, 'r', encoding='utf-8') as f:
    texto_md = f.read()

# Convertimos a HTML
html_body = markdown2.markdown(texto_md)

# Cabecera completa con meta charset y CSS
html = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <style>
      body {{ font-family: Arial, sans-serif; padding: 20px; }}
      h1, h2, h3 {{ color: #333366; }}
      p {{ line-height: 1.5; margin-bottom: 10px; }}
    </style>
  </head>
  <body>
    {html_body}
  </body>
</html>"""

# Genera el PDF
HTML(string=html).write_pdf(output_pdf)

print(f"PDF generado en {output_pdf}")
