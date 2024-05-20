import setuptools

with open("README.md", "r",encoding='UTF-8') as fh:
    long_description = fh.read()


setuptools.setup(
    name="tcs34725",
    py_modules=['tcs34725'],
    version="1.0.1",
    author="Radomir Dopieralski",
    author_email="micropython@sheep.art.pl",
    description="Driver for MicroPython for the tcs34725 RGB sensor.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adafruit/micropython-adafruit-tcs34725",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)