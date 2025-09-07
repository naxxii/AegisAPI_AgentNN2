from ..telemetry import load_events
from jinja2 import Template
from pathlib import Path

def render_dashboard(use_enhanced=True):
    ev = load_events()
    template_path = 'aegisapi/reporting/templates/enhanced_dashboard.html' if use_enhanced else 'aegisapi/reporting/templates/report.html'
    tpl = Path(template_path).read_text(encoding='utf-8')
    html = Template(tpl).render(recent=ev[-100:])
    Path('reports').mkdir(parents=True, exist_ok=True)
    (Path('reports')/'index.html').write_text(html, encoding='utf-8')
    return str(Path('reports').absolute() / 'index.html')

def render_basic_dashboard():
    """Render the basic dashboard (legacy)"""
    return render_dashboard(use_enhanced=False)
