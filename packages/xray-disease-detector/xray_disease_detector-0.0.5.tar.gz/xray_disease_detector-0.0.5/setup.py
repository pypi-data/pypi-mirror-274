# setup.py

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xray_disease_detector",
    version="0.0.5",
    author="Gong Zhan",
    author_email="gongzhan34@yahoo.co.jp",
    description="A package for detecting diseases in X-ray images using a pre-trained PyTorch model",
    long_description=long_description,      
    long_description_content_type="text/markdown",
    url="https://github.com/KONMIO34/xray_disease_detector",
    project_urls={
        "Bug Tracker": "https://github.com/KONMIO34/xray_disease_detector/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=["xray_disease_detector"],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "torch",
        "torchvision",
        "Pillow"
    ],
    entry_points={
        "console_scripts": [
            "xray_disease_detector=xray_disease_detector:main",
        ],
    },
)
