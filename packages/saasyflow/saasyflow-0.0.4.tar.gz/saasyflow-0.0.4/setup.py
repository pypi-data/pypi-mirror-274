from setuptools import setup, find_packages

print("xxxx", find_packages("."))

setup(
    name="saasyflow",
    version="0.0.4",
    author="Misraj",
    author_email="contact@misraj.com",
    packages=find_packages("."),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
)
