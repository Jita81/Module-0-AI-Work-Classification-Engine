"""
Backward compatibility wrapper for the refactored Standardized Modules Framework.

This module provides the same interface as the original module_scaffolding_system.py
but uses the new refactored implementation under the hood.
"""

# Import from the new refactored modules
from src.standardized_modules.generators.module_generator import ModuleGenerator
from src.standardized_modules.models.generation_result import GenerationResult
from src.standardized_modules.cli.commands import create_cli

# Re-export for backward compatibility
__all__ = [
    'ModuleGenerator',
    'GenerationResult', 
    'create_cli'
]

# Create the CLI instance for backward compatibility
cli = create_cli()

# For direct script execution
if __name__ == "__main__":
    if cli:
        cli()
    else:
        print("CLI not available. Please install click: pip install click>=8.0.0")
