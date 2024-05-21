from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tempclone",
    version="1.0.2",
    author="Matheus",
    author_email="matheusmlfg@gmail.com",
    description="CLI to automate the creation of new projects from GitHub templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tempclone",  # URL do repositório do seu projeto
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "click",
        "requests"
    ],
    entry_points={
        'console_scripts': [
            'tempclone=tempclone.cli:cli',
        ],
    },
)
