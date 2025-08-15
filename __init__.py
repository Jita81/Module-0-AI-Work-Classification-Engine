"""
Standardized Modules Framework

AI-optimized module scaffolding framework for rapid development.
"""

from .module_scaffolding_system import (
    ModuleGenerator,
    ModuleTemplates,
    GenerationResult,
    cli
)

__version__ = "1.0.0"
__author__ = "Standardized Modules Framework Contributors"
__email__ = "contact@standardized-modules.dev"
__license__ = "MIT"

# Public API
__all__ = [
    "ModuleGenerator",
    "ModuleTemplates", 
    "GenerationResult",
    "cli"
]
