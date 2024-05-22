import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="senweaver",
    version="0.0.1",
    author="sw",
    author_email="",
    include_package_data=True,
    description="data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
	license='MIT',
    packages=setuptools.find_packages(),
    python_requires='>=3.9, <4',
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
