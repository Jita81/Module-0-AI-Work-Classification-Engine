"""
Generation result model for module creation operations.
"""

class GenerationResult:
    """Result of module generation operation"""
    
    def __init__(self, success: bool, module_path: str = None, ai_completion_file: str = None, 
                 error: str = None, containerized: bool = False, deployment_target: str = None):
        self.success = success
        self.module_path = module_path
        self.ai_completion_file = ai_completion_file
        self.error = error
        self.containerized = containerized
        self.deployment_target = deployment_target
    
    def __repr__(self):
        return f"GenerationResult(success={self.success}, module_path='{self.module_path}')"
    
    def __str__(self):
        if self.success:
            return f"✅ Module generated successfully at {self.module_path}"
        else:
            return f"❌ Generation failed: {self.error}"
