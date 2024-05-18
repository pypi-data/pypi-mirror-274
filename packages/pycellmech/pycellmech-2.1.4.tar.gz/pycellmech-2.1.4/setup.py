import os
from setuptools import setup, find_packages

# Get the directory where setup.py is located
current_directory = os.path.abspath(os.path.dirname(__file__))

# Read the README.md file
with open(os.path.join(current_directory, './README.md'), encoding='utf-8') as f:
    long_description = f.read()    

setup(
    name="pycellmech",
    version="2.1.4",
    author="Janan Arslan",
    author_email="janan.arslan@icm-institute.org",
    description="A shape-based feature extractor for medical and biological studies",
    long_description_content_type="text/markdown",
    url="https://github.com/icm-dac/pycellmech",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "matplotlib",
        "numpy",
        "opencv-python",
        "pandas",
        "scikit-learn"
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pycellmech=pycellmech.cli:main',
        ],
    },
)
