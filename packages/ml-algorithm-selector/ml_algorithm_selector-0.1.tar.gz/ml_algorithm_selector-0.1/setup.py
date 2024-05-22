# setup.py
from setuptools import setup, find_packages

setup(
    name="ml_algorithm_selector",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ml-selector=ml_algorithm_selector.selector:main',
        ],
    },
    install_requires=[
        # Add any dependencies if needed
    ],
    author="Jameson Augustin",
    author_email="jamesjamesonja@gmail.com",
    description="A tool to help select machine learning algorithms based on scikit-learn cheat-sheet.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/James-chrypto/ml_algorithm_selector",  # Replace with your GitHub URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
