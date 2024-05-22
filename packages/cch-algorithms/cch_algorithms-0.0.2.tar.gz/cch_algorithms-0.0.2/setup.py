import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cch_algorithms",
    version="0.0.2",
    author="Center for Computational Health",
    author_email="wade.schulz@yale.edu",
    description="Machine learning algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://dev.azure.com/yalecch/cch-research",
    project_urls={
        "Repository": "https://dev.azure.com/yalecch/cch-research/_git/cch-algorithms",
    },
    install_requires=[
        "mlflow",
        "matplotlib",
        "numpy",
        "pandas",
        "qiskit-aer",
        "qiskit-ibm-runtime",
        "qiskit-machine-learning",
        "scikit-learn",
        "scikit-learn",
        "tqdm",
        "urllib3",
        "xgboost"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)