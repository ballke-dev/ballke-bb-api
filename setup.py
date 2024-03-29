import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apiBB",
    version="0.0.1",
    author="Diogo Baltazar",
    author_email="ti3@ballke.com.br",
    description="Pacote para facilitar o uso da api do BB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ballke-dev/bb-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True
)