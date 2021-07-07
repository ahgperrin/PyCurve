from setuptools import setup
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='PyCurve',
    version='0.0.2',
    author="Antoine Perrin",
    author_email="antoineperrin.pro1@gmail.com",
    description='Interest rate yield curve packages',
    py_modules=["actuarial_implementation",
                "bjork_christensen",
                "bjork_christensen_augmented",
                "cubic",
                "curve",
                "simulation",
                "linear",
                "nelson_siegel",
                "svensson_nelson_siegel",
                "vasicek"],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["matplotlib", "pandas", "numpy", "scipy", "typing"],
    url="https://github.com/ahgperrin/PyCurve"
)
