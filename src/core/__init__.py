"""
Standardized Modules Framework

A production-ready framework for generating containerized microservices
with AI-assisted development and infrastructure templates.
"""

__version__ = "1.1.0"
__author__ = "Standardized Modules Framework"

# Main public API
from .generators.module_generator import ModuleGenerator
from .models.generation_result import GenerationResult

__all__ = [
    "ModuleGenerator", 
    "GenerationResult",
    "__version__"
]
