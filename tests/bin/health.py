#!/usr/bin/env python3
import numpy as np
import pandas as pd

from lambdamap import LambdaFunction, LambdaExecutor

def my_power(x, **kwargs):
    import numpy as np
    import pandas as pd

    exponent = kwargs.get("exponent", 2)

    df = pd.DataFrame()
    df["formula"] = [f"{x}**{exponent}"]
    df["result"] = np.power(x, exponent)

    return df

payloads = [{"args": (i,), "kwargs": {"exponent": 2}} for i in range(100)]
executor = LambdaExecutor(10, "LambdaMapFunction")
results = executor.map(my_power, payloads)

print(results)

assert len(results) == len(payloads)
assert np.all([isinstance(r, pd.DataFrame) for r in results])

df = pd.concat(results)

assert df.shape[0] == len(payloads)