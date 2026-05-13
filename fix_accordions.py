import os

filepath = r"c:\yess\Trust-MK-prueba\Trustmarket2\templates\core\stitch_landing.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Restore button headers
content = content.replace('<div class="w-full p-8 text-left">', '<button class="sub-accordion-header w-full p-8 text-left group">')

# Restore ver detalles and closing button, and the max-h-0 for content
old_transition = """</p>
              </div>
              <div class="bg-white">"""
new_transition = """</p>
                <span class="text-primary font-bold text-xs uppercase tracking-wider flex items-center gap-2">
                  Ver detalles <span class="material-symbols-outlined !text-sm">add</span>
                </span>
              </button>
              <div class="sub-accordion-content max-h-0 overflow-hidden transition-all duration-300 bg-white">"""
content = content.replace(old_transition, new_transition)

# Remove the ver mas link block I added
button_html = """</ul>
                  <div class="mt-8">
                    <a href="#contacto" class="inline-flex items-center gap-2 bg-primary/10 text-primary px-5 py-2.5 rounded-xl font-bold text-sm hover:bg-primary hover:text-white transition-all">
                      Ver más <span class="material-symbols-outlined !text-sm">arrow_forward</span>
                    </a>
                  </div>"""
content = content.replace(button_html, '</ul>')

# Add back script
script_html = """<script>
        document.querySelectorAll('.sub-accordion-header').forEach(header => {
          header.addEventListener('click', () => {
            const content = header.nextElementSibling;
            const icon = header.querySelector('span:last-child span');
            
            if (content.style.maxHeight && content.style.maxHeight !== '0px') {
              content.style.maxHeight = '0px';
              icon.textContent = 'add';
            } else {
              content.style.maxHeight = content.scrollHeight + "px";
              icon.textContent = 'remove';
            }
          });
        });
      </script>"""
      
# Find `<!-- Script removed -->` and replace it
content = content.replace('<!-- Script removed -->', script_html)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Restored accordions successfully")
