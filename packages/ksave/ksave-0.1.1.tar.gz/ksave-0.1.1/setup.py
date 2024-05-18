from setuptools import setup, find_packages

setup(
    name="ksave",
    version="0.1.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to backup Kubernetes YAML configurations.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/serbayacar/ksave",
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    scripts=['bin/ksave.py'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

