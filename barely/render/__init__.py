"""
The render sub-package deals with
rendering markdown files to html-
documents with the use of jinja
Templates. It also handles ressource
(images/css/js) minimization.
"""

from .renderer import Renderer
from .minimizer import Minimizer

RENDERER = Renderer.instance()
MINIMIZER = Minimizer.instance()
