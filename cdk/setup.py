import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="lambdamap-cdk",
    version="0.0.1",

    description="LambdaMap",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="author",

    package_dir={"": "stack"},
    packages=setuptools.find_packages(where="stack"),

    install_requires=[
        "aws-cdk.core==1.97.0",
    ],

    python_requires=">=3.8",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
