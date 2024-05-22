from setuptools import setup, find_packages

print ("Possible packages: {}".format(find_packages()))

setup (
    name="UnityPredict",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # Currently no dependencies
    ],
)