import setuptools, modulefinder

with open("README.md", "r", encoding="UTF-8") as f:
    description = f.read()

with open("LICENSE", "r") as f:
    license = f.read()

setuptools.setup(
    name="xplainable-client",
    version="1.2.4.post2",
    author="xplainable pty ltd",
    author_email="contact@xplainable.io",
    packages=["xplainable_client"],
    description="The client for persisting and deploying models to Xplainable cloud.",
    long_description=description,
    long_description_content_type="text/markdown",
    license=license,
    python_requires='>=3.11',
    install_requires=[
        "ipywidgets==8.0.6",
        "numpy>=1.26",
        "pandas>=1.5.2",
        "pyperclip==1.8.2",
        "Requests==2.31.0",
        "scikit_learn",
        "setuptools",
        "urllib3==2.2.0",
        "xplainable==1.2.4"
    ]
)
