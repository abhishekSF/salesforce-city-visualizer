import os
import re

base_dir = '/Users/asmgkr/.gemini/antigravity/scratch/salesforce-city-visualizer'
artifact_path = '/Users/asmgkr/.gemini/antigravity/brain/70c5c001-c5d6-45ac-acd0-3a33f17eabe3/salesforce_pixel_city.html'
standalone_path = os.path.join(base_dir, 'standalone.html')

def read_file(rel_path):
    with open(os.path.join(base_dir, rel_path), 'r') as f:
        return f.read()

# Read CSS
css_content = read_file('src/styles/pixel-city.css')

# Read JS modules and strip imports/exports
def clean_js(content):
    content = re.sub(r'import\s+.*?from\s+[\'"].*?[\'"];?', '', content)
    content = re.sub(r'export\s+(const|let|var|function|class)\s+', r'\1 ', content)
    content = re.sub(r'export\s*\{[^}]*\};?', '', content)
    return content

js_metadata = clean_js(read_file('src/data/metadataCatalog.js'))
js_layout = clean_js(read_file('src/data/cityLayout.js'))
js_guides = clean_js(read_file('src/data/conceptGuides.js'))
js_sound = clean_js(read_file('src/engine/SoundFx.js'))
js_particles = clean_js(read_file('src/engine/ParticleSystem.js'))
js_canvas = clean_js(read_file('src/engine/IsometricCanvas.js'))
js_world = clean_js(read_file('src/engine/TopDownWorld.js'))
js_player = clean_js(read_file('src/engine/PlayerCharacter.js'))
js_inspector = clean_js(read_file('src/components/BuildingInspector.js'))
js_modal = clean_js(read_file('src/components/ConceptModal.js'))
js_palette = clean_js(read_file('src/components/CommandPalette.js'))
js_tour = clean_js(read_file('src/components/GuidedTour.js'))
js_guide = clean_js(read_file('src/components/FieldGuide.js'))
js_atlas = clean_js(read_file('src/components/Atlas.js'))
js_sim = clean_js(read_file('src/components/SimulationController.js'))
js_main = clean_js(read_file('src/main.js'))

combined_js = f"""
(function() {{
  {js_sound}
  {js_layout}
  {js_metadata}
  {js_guides}
  {js_particles}
  {js_canvas}
  {js_world}
  {js_player}
  {js_inspector}
  {js_modal}
  {js_guide}
  {js_atlas}
  {js_palette}
  {js_tour}
  {js_sim}
  {js_main}
}})();
"""

index_html_raw = read_file('index.html')
# Replace <link rel="stylesheet" href="./src/styles/pixel-city.css" /> with inline style
# Replace <script type="module" src="./src/main.js"></script> with inline script
standalone_html = re.sub(
    r'<link rel="stylesheet" href="\./src/styles/pixel-city\.css"\s*/>',
    f'<style>\n{css_content}\n</style>',
    index_html_raw
)
standalone_html = re.sub(
    r'<script type="module" src="\./src/main\.js"></script>',
    f'<script>\n{combined_js}\n</script>',
    standalone_html
)

with open(artifact_path, 'w') as f:
    f.write(standalone_html)

with open(standalone_path, 'w') as f:
    f.write(standalone_html)

print("Rebuilt standalone.html and salesforce_pixel_city.html successfully!")
