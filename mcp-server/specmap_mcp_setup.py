# setup.py - SpecMap MCP Server Installation
"""
SpecMap MCP Server Package
===========================
Installation package for the SpecMap MCP Server.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="specmap-mcp-server",
    version="1.0.0",
    description="Model Context Protocol server for SpecMap CLI integration with Claude Code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Monomoy Strategies",
    author_email="your-email@example.com",
    url="https://github.com/your-username/specmap",
    license="MIT",
    
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    python_requires=">=3.8",
    
    install_requires=[
        "fastmcp>=2.0.0",
        # Note: specmap should be installed separately or added as local dependency
    ],
    
    entry_points={
        "console_scripts": [
            "specmap-mcp=specmap_mcp.server:main",
        ],
    },
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Code Generators",
    ],
    
    keywords="mcp model-context-protocol claude-code ai specmap rulemap specification",
)
