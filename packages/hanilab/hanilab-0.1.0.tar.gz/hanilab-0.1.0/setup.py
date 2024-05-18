from setuptools import setup, find_packages

setup(
    name="hanilab",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "opencv-python-headless",
        "torch",
        "torchvision",
        "matplotlib",
        "flask",
    ],
    entry_points={
        "console_scripts": [
            "hanilab=hanilab.app:main",
        ],
    },
)
