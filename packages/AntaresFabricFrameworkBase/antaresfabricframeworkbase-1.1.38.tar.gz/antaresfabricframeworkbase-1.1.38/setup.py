import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "AntaresFabricFrameworkBase",
    version = "1.1.38",
    author = "Antares Solutions",
    author_email = "martonm@antaressolutions.com.au",
    description = "Microsoft Fabric data ingestion accelerator",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://antares.solutions/",
    project_urls = {
        "Bug Tracker": "https://antares.solutions/",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)