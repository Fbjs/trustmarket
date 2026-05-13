import os

filepath = r'c:\yess\Trust-MK-prueba\Trustmarket2\templates\core\stitch_landing.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

button_html = """</ul>
                  <div class="mt-8">
                    <a href="#contacto" class="inline-flex items-center gap-2 bg-primary/10 text-primary px-5 py-2.5 rounded-xl font-bold text-sm hover:bg-primary hover:text-white transition-all">
                      Ver más <span class="material-symbols-outlined !text-sm">arrow_forward</span>
                    </a>
                  </div>"""

grid_start = content.find('<!-- SERVICES GRID -->')
if grid_start != -1:
    grid_end = content.find('<!-- PROPUESTA DE VALOR -->', grid_start)
    if grid_end != -1:
        grid_content = content[grid_start:grid_end]
        new_grid_content = grid_content.replace('</ul>', button_html)
        content = content[:grid_start] + new_grid_content + content[grid_end:]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Buttons added successfully.')
    else:
        print('Could not find end of grid.')
else:
    print('Could not find start of grid.')
