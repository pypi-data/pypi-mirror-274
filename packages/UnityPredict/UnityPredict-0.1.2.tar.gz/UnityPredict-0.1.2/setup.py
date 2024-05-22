from setuptools import setup, find_packages

description = ""
with open("README.md", "r") as rdf:
    description = rdf.read()

print ("Possible packages: {}".format(find_packages()))

setup (
    name="UnityPredict",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        # Currently no dependencies
    ],

    long_description=description,
    long_description_content_type="text/markdown"
)