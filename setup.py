"""
Setup configuration for F1 WHO IS BETTER DRIVER?
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="f1-who-is-better-driver",
    version="1.0.1",
    author="F1 Analysis Team",
    author_email="",
    description="A comprehensive Formula 1 driver performance analysis tool with interactive web dashboard",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Glocktoyou/F1-WHO-IS-BETTER-DRIVER-",
    project_urls={
        "Bug Tracker": "https://github.com/Glocktoyou/F1-WHO-IS-BETTER-DRIVER-/issues",
        "Documentation": "https://github.com/Glocktoyou/F1-WHO-IS-BETTER-DRIVER-#readme",
        "Source Code": "https://github.com/Glocktoyou/F1-WHO-IS-BETTER-DRIVER-",
        "Contributing": "https://github.com/Glocktoyou/F1-WHO-IS-BETTER-DRIVER-/blob/main/CONTRIBUTING.md",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Sports/Racing Enthusiasts",
        "Intended Audience :: Developers", 
        "Intended Audience :: Data Scientists",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Sports :: Motor Racing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Framework :: Flask",
        "Environment :: Web Environment",
        "Environment :: Console",
    ],
    python_requires=">=3.10",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "test": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "f1-analysis=src.main:main",
            "f1-web=src.app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "src": [
            "../templates/*.html",
            "../static/css/*.css",
            "../static/plots/.gitkeep",
        ],
    },
    keywords=[
        "formula1", "f1", "racing", "telemetry", "data-analysis", 
        "visualization", "motorsport", "driver-comparison", 
        "performance-analysis", "web-dashboard"
    ],
    zip_safe=False,
)