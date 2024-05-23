import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MLRegressions",
    version="1.0.5",
    author="DKVG",
    author_email="gadellidk@gmail.com",
    description="5 ML Model are available to train bassed on provided dataset, user can select one regresion out of 5 "
                "for train.",
    long_description=long_description,
    package_data={'': ['*']},
    include_package_data=True,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
    keywords='ML Regressions, MLRegressions Linear polynomial svr random-forest decision-tree regressors',
)
