# lambdamap

Massively parallel on-demand serverless computing using AWS Lambda.

## Installation

### Python 3.9, `conda`, `npm`

Python 3.9 is preferred, which can be easily via `conda`:
- https://docs.conda.io/projects/conda/en/latest/user-guide/install/)

`npm` can then be installed as follows
```bash
conda install -c conda-forge nodejs
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
```

Deploy the LambdaMap stack, you can configure the stack using the following
`make` variables:
- `STACK_NAME` (default: `STACK_NAME=LambdaMapStack`)
    - name of the lambdamap cloudformation stack
- `FUNCTION_NAME` (default: `FUNCTION_NAME=LambdaMapFunction`)
    - name of the AWS Lambda function that will execute your python function
- `EXTRA_CMDS` (default: `EXTRA_CMDS=''`)
    - e.g: `EXTRA_CMDS='pip install pandas'` 
    - additional commands to execute in a single `RUN` instruction of
      the `Dockerfile`, such as `pip install` for installing additional
      python packages in the lambda container.
```bash
# Deploy the LambdaMap stack
make bootstrap
make deploy EXTRA_CMDS='pip install pandas'
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
