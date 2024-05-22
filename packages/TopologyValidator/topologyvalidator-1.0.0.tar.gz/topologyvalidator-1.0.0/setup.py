from setuptools import setup, find_packages

setup(
    name="TopologyValidator",
    version="1.0.0",
    author="Sai Krishna Voruganti",
    author_email="saikrishnavoruganti@gmail.com",
    description="Validates the converted topology against the given OpenAPI specifications",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=["pyyaml", "jsonref", "jsonschema"],
)