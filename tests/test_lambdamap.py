import sys
import base64
import json
import cloudpickle
import numpy as np
import pandas as pd
import pytest

from lambdamap import LambdaFunction, LambdaExecutor
from stack.index import handler
from unittest.mock import patch


def my_power(x, **kwargs):
    import numpy as np
    import pandas as pd

    exponent = kwargs.get("exponent", 2)

    df = pd.DataFrame()
    df["formula"] = [f"{x}**{exponent}"]
    df["result"] = np.power(x, exponent)

    return df


def test_lambdamap():
    def invoke_handler(payload):
        payload = base64.b64encode(cloudpickle.dumps(payload)).decode("ascii")
        payload = json.dumps(payload)
        result = cloudpickle.loads(handler(payload, None))
        return result
    
    with patch("lambdamap.LambdaFunction.invoke_handler",
               side_effect=invoke_handler):
        executor = LambdaExecutor(10, "LambdaMapFunction")
        payloads = [{"args": (i,), "kwargs": {"exponent": 2}} for i in range(100)]
        results = executor.map(my_power, payloads)

    assert len(results) == len(payloads)
    assert np.all([isinstance(r, pd.DataFrame) for r in results])

    df = pd.concat(results)

    assert df.shape[0] == len(payloads)

    return