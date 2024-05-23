import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="khmersegment",
    version="0.1.0",
    description="A Khmer word segmentation tool built for NIPTICT Khmer Word Segmentation CRF model.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seanghay/khmersegment",
    author="Seanghay Yath",
    author_email="seanghay.dev@gmail.com",
    license="Apache License 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: English",
    ],
    python_requires=">=3.7",
    packages=setuptools.find_packages(),
    package_dir={"khmersegment": "khmersegment"},
    install_requires=[
        "pycrfpp",
    ],
)
