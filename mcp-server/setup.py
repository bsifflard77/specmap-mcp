from setuptools import setup, find_packages

setup(
    name="specmap-mcp-server",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=["fastmcp>=2.0.0"],
    entry_points={"console_scripts": ["specmap-mcp=specmap_mcp.server:main"]},
)
