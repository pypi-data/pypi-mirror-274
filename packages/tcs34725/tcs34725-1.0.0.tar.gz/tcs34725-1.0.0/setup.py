import setuptools

setuptools.setup(
    name="tcs34725",
    py_modules=['tcs34725'],
    version="1.0.0",
    author="Radomir Dopieralski",
    author_email="micropython@sheep.art.pl",
    description="Driver for MicroPython for the tcs34725 RGB sensor.",
    long_description="""\
        This library lets you communicate with a TCS34725 RGB sensor.
        """,
    url="https://github.com/adafruit/micropython-adafruit-tcs34725",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)