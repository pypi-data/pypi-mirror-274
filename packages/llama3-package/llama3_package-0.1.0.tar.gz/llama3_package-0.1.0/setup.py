from setuptools import setup, find_packages

setup(
    name="llama3_package",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "langchain",
        "notebook",
        "ollama",
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
        ]
    },
    author="Disant Upadhyay",
    description="A Python package to interact with Llama 3 locally using Ollama.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/princeDisant/llama3_package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
