# lambdamap

Massively parallel on-demand serverless computing using AWS Lambda.

## Installation

### Python 3.9, `conda`, `npm`

Python 3.9 is preferred, which can be easily installed via `conda`:
- https://docs.conda.io/projects/conda/en/latest/user-guide/install/

You can install these and npm with the below:
```bash
conda create -n <envname> -c conda-forge nodejs python=3.9
conda activate <envname>
```

### Python Package

```bash
# Install the `lambdamap` python package
pip3 install -e .

# (optional) install ipywidgets to visualise the LambdaMap progress bars in Jupyter notebooks
pip3 install ipywidgets
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
- `MEMORY` (default: `MEMORY=256`)
    - memory, in MB, to assign to the Lambda function
- `TIMEOUT` (default: `TIMEOUT=900`)
    - timeout, in seconds, to assign to the Lambda function
- `EXTRA_CMDS` (default: `EXTRA_CMDS=''`)
    - e.g: `EXTRA_CMDS="'pip install pandas'"` 
    - additional commands to execute in a single `RUN` instruction of
      the `Dockerfile`, such as `pip install` for installing additional
      python packages in the Lambda container.
    - note that use of the double and single quotes (`"'...'"`)
- `CDK_TAGS` (default: `CDK_TAGS='--tags Project=lambdamap'`)
    - e.g: `CDK_TAGS='--tags Project=lambdamap --tags Department=Dev'`
    - custom resource tags

```bash
# Deploy the LambdaMap stack
make bootstrap
make deploy EXTRA_CMDS="'pip install pandas'" CDK_TAGS='--tags Project=lambdamap'
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
    max_workers=100,
    lambda_arn="LambdaMapFunction")

# Generate the function payloads
payloads = [{"args": (i,), "kwargs": {"exponent": 2}} for i in range(100)]

# Distribute the function calls over the lambdas
results = executor.map(my_power, payloads)

# Concatenate the list of results into a single dataframe
df_results = pd.concat(results)
df_results
```