from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pof-engine",
    version="0.1.0",
    author="Platon Pavluk",
    author_email="",
    description="A lightweight 2D game engine with ECS architecture written in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/platonpavluk16/POF_ENGINE",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: pygame",
    ],
    python_requires=">=3.8",
    install_requires=[
        "glfw>=2.6.0",
        "PyOpenGL>=3.1.5",
        "numpy>=1.20.0",
    ],
    entry_points={
        "console_scripts": [
            "pof-engine=main:main",
        ],
    },
)
