
import re
import nbformat
from pathlib import Path

# Bestandsnamen
input_file = Path(
   r"C:\Users\ducvi\Documents\TN\IP_2\IP_2-thermo\simulations\NB1_deeltjesmodel.md"
)

output_file = input_file.with_suffix(".ipynb")

# Lees het volledige Markdown-bestand
text = input_file.read_text(encoding="utf-8")

# Zoek uitsluitend Python-codeblokken
pattern = re.compile(
    r"^```python[ \t]*\n(.*?)^```[ \t]*$",
    re.MULTILINE | re.DOTALL
)

nb = nbformat.v4.new_notebook()
cells = []

last_position = 0

for match in pattern.finditer(text):

    # Alle tekst vóór het Python-codeblok behouden
    markdown = text[last_position:match.start()]

    if markdown.strip():
        cells.append(
            nbformat.v4.new_markdown_cell(markdown.strip())
        )

    # Python-codeblok omzetten naar uitvoerbare codecel
    code = match.group(1)

    cells.append(
        nbformat.v4.new_code_cell(code.rstrip())
    )

    last_position = match.end()

# Resterende tekst na het laatste codeblok
markdown = text[last_position:]

if markdown.strip():
    cells.append(
        nbformat.v4.new_markdown_cell(markdown.strip())
    )

# Notebook opslaan
nb.cells = cells

nbformat.write(nb, output_file)

print("Conversie voltooid!")
print(f"Aantal Markdown-cellen: {sum(c.cell_type == 'markdown' for c in cells)}")
print(f"Aantal codecellen: {sum(c.cell_type == 'code' for c in cells)}")
print(f"Bestand: {output_file}")
