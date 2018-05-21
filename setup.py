from setuptools import setup, find_packages

setup(
    name="white_brush",
    version="0.1.0-dev",
    packages=find_packages(exclude=['tests']),
    install_requires=[
        "numpy",
        "opencv-python",
        "sklearn",
        "scipy",
        "webcolors"
    ],
    description="White Brush is a tool for enhancing hand-written notes.",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: End Users/Desktop"
    ],
    package_data={
        "": ["LICENSE", "README.md"]
    },
    include_package_data=True,
    entry_points={
        "console_scripts":
            ["white-brush=white_brush.__main__:main"]
    }
)
