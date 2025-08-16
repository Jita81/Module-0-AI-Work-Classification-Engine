"""
CLI command interface for the Standardized Modules Framework.
"""

try:
    import click
except ImportError:
    print("click not installed. Install with: pip install click>=8.0.0")
    click = None

from ..generators.module_generator import ModuleGenerator


def create_cli():
    """Create CLI interface when click is available"""
    if click is None:
        print("Error: click is required for CLI functionality")
        print("Install with: pip install click>=8.0.0")
        return None

    @click.group()
    def cli():
        """Standardized Modules Framework CLI"""
        pass

    @cli.command()
    @click.argument('module_name')
    @click.option('--type', 'module_type', 
                  type=click.Choice(['CORE', 'INTEGRATION', 'SUPPORTING', 'TECHNICAL']),
                  required=True, help='Type of module to create')
    @click.option('--domain', default='general', help='Business domain (e.g., ecommerce, finance)')
    @click.option('--output-dir', default='.', help='Output directory')
    @click.option('--ai-ready', is_flag=True, help='Generate with AI completion markers')
    @click.option('--with-docker', is_flag=True, help='Generate Docker and Kubernetes files')
    @click.option('--deployment-target', default='kubernetes', 
                  type=click.Choice(['kubernetes', 'docker-compose', 'lambda']),
                  help='Deployment target platform')
    def create_module(module_name: str, module_type: str, domain: str, output_dir: str, 
                     ai_ready: bool, with_docker: bool, deployment_target: str):
        """Create a new standardized module with complete framework structure"""
        
        generator = ModuleGenerator()
        result = generator.generate_module(
            name=module_name,
            module_type=module_type,
            domain=domain,
            output_dir=output_dir,
            ai_ready=ai_ready,
            with_docker=with_docker,
            deployment_target=deployment_target
        )
        
        if result.success:
            click.echo(f"✅ Module '{module_name}' created successfully!")
            click.echo(f"📁 Location: {result.module_path}")
            click.echo(f"🤖 AI completion file: {result.ai_completion_file}")
            
            if with_docker:
                click.echo(f"🐳 Containerized for: {deployment_target}")
                click.echo(f"📦 Docker files generated")
                click.echo(f"☸️  Kubernetes manifests generated")
                click.echo(f"🚀 CI/CD pipeline configured")
                
            click.echo("\nNext steps:")
            click.echo("1. Open the AI completion file in Cursor")
            click.echo("2. Use the provided prompts to complete the module")
            
            if with_docker:
                click.echo("3. Build and test: ./scripts/build.sh")
                click.echo("4. Start locally: docker-compose up")
                click.echo("5. Deploy: ./scripts/deploy.sh staging")
            else:
                click.echo("3. Run tests: pytest {}/tests/".format(result.module_path))
        else:
            click.echo(f"❌ Error: {result.error}")
    
    return cli


# Create the CLI instance for external use
cli = create_cli()


if __name__ == "__main__":
    if cli:
        cli()
    else:
        print("CLI not available. Please install click: pip install click>=8.0.0")
