import json
import base64
import cloudpickle
import pandas as pd

from unittest.mock import Mock
from stack.index import handler


def my_power(x, **kwargs):
    import numpy as np
    import pandas as pd

    exponent = kwargs.get("exponent", 2)

    df = pd.DataFrame()
    df["formula"] = [f"{x}**{exponent}"]
    df["result"] = np.power(x, exponent)

    return df


def test_handler():
    payload = {"func": my_power, "args": (2,), "kwargs": {"exponent": 2}}

    payload = base64.b64encode(cloudpickle.dumps(payload)).decode("ascii")
    payload = json.dumps(payload)

    df = cloudpickle.loads(handler(payload, None))
    df_exp = pd.DataFrame()
    df_exp["formula"] = ["2**2"]
    df_exp["result"] = [4]

    pd.testing.assert_frame_equal(df, df_exp)

    return