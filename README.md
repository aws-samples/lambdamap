# lambdamap

Massively parallel serverless computing using AWS Lambda.

## Installation

### Python 3.8, `conda`, `npm`

Python 3.8 is preferred, which can be easily via [`conda`](https://docs.conda.io/projects/conda/en/latest/user-guide/install/).

You can install these and npm with the below:
```bash
conda create -n <envname> -c conda-forge nodejs python=3.8
conda activate <envname>
```

### Python Package

```bash
# Install the `lambdamap` python package
pip3 install -e .
```

### Lambda Container Stack

```bash
# Install the AWS CDK Toolkit and CLI
npm i -g aws-cdk

cd ./cdk

# Install the AWS CDK Python 3.x dependencies
pip3 install -r requirements.txt

# Deploy the LambdaMap stack
cdk bootstrap
cdk deploy

# Generate the CFN template
cdk synth
```

### Dockerfile

You can specify additional system and Python packages to be used by the Lambda container in `./cdk/stack/Dockerfile`.
```
lambdamap
├── cdk/
│   ├── app.py
│   ├── cdk.json
│   ├── requirements.txt
│   ├── setup.py
│   ├── source.bat
│   └── stack/
│       ├── Dockerfile <--- modify to include custom system and Python packages
│       ├── __init__.py
│       ├── lambda.py
│       └── stack.py
├── lambdamap/
│   ├── core.py
│   └── __init__.py
├── README.md
└── setup.py
```

## Example Usage

```python
import pandas as pd
from lambdamap import LambdaExecutor

# Define your custom function
def my_power(x, **kwargs):
    import numpy as np
    import pandas as pd
    
    exponent = kwargs.get("exponent", 2)
    
    df = pd.DataFrame()
    df["formula"] = [f"{x}**{exponent}"]
    df["result"] = np.power(x, exponent)
    
    return df

# Instantiate the Lambda executor
executor = LambdaExecutor(
    max_workers=1000,
    lambda_arn="LambdaMapFunction")

# Generate the function payloads
payloads = [{"args": (i,), "kwargs": {"exponent": 2}} for i in range(1000)]

# Distribute the function calls over the lambdas
results = executor.map(my_power, payloads)

# Concatenate the list of results into a single dataframe
df_results = pd.concat(results)
df_results
```
