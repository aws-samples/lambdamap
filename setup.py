import setuptools


setuptools.setup(
    name="lambdamap",
    version="0.0.1",
    packages=setuptools.find_packages(where="lambdamap"),

    install_requires=[
        "botocore",
        "boto3",
        "cloudpickle==1.6.0",
        "tqdm"
    ],

    python_requires=">=3.6",

    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
)
