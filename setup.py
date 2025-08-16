#!/usr/bin/env python3
"""
Setup script for Standardized Modules Framework
"""

from setuptools import setup, find_packages

# Read README for long description
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Standardized module framework for AI-assisted development"

# Read requirements
requirements = [
    "click>=8.0.0",
    "jinja2>=3.0.0", 
    "pyyaml>=6.0.0",
    "aiohttp>=3.8.0",
    "pathlib",
    "dataclasses; python_version<'3.7'",
]

dev_requirements = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-mock>=3.6.0",
    "black>=22.0.0",
    "flake8>=4.0.0",
    "mypy>=0.950",
]

setup(
    name="standardized-modules-framework",
    version="1.1.0",
    author="Standardized Modules Framework",
    author_email="contact@standardized-modules.dev",
    description="AI-optimized module scaffolding framework for rapid development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/standardized-modules/framework",
    
    packages=find_packages(),
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    
    python_requires=">=3.8",
    
    install_requires=requirements,
    
    extras_require={
        "dev": dev_requirements,
        "cli": ["click>=8.0.0"],
        "async": ["aiohttp>=3.8.0"],
        "all": requirements + dev_requirements,
    },
    
    entry_points={
        "console_scripts": [
            "sm=module_scaffolding_system:cli",
        ],
    },
    
    include_package_data=True,
    
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    
    project_urls={
        "Bug Reports": "https://github.com/standardized-modules/framework/issues",
        "Source": "https://github.com/standardized-modules/framework",
        "Documentation": "https://standardized-modules.dev/docs",
    },
    
    keywords="scaffolding, framework, ai, automation, modules, development",
    
    zip_safe=False,
)
