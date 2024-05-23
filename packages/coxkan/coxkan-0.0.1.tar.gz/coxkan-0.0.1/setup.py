import setuptools

# # Load the long_description from README.md
# with open("README.md", "r", encoding="utf8") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="coxkan",
    version="0.0.1",
    author="Will Knottenbelt",
    author_email="knottenbeltwill@gmail.com",
    description="Lorem Ipsum",
    long_description="Lorem Ipsum",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)