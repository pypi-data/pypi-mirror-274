from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "Your go-to solution for database connectivity in Python"
LONG_DESCRIPTION = """PyDataBridge is your go-to solution for database connectivity in Python. Whether you're working with Firebase or other databases, PyDataBridge offers a versatile and intuitive package for seamless integration. Simplify your backend development and unleash the power of Python with PyDataBridge."""

# Setting up
setup(
    name="PyDataBridgeX",
    version=VERSION,
    author="Ranuga Disansa Gamage",
    author_email="go2ranuga@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["requests", "typing"],
    keywords=[
        "python",
        "database",
        "connectivity",
        "firebase",
        "backend",
        "development",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
