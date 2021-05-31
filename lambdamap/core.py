import time
import base64
import json
import warnings
import botocore
import boto3
import cloudpickle

from concurrent import futures

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from tqdm.autonotebook import tqdm


class LambdaFunction:
    """
    """
    
    def __init__(self, func, client, lambda_arn):
        """
        """
        
        self.func = func
        self.client = client
        self._lambda_arn = lambda_arn
        
        return
    
    def __call__(self, *args, **kwargs):
        """
        """
        
        payload = {
            "func": self.func,
            "args": args,
            "kwargs": kwargs
        }
        
        return self.invoke_handler(payload)
    
    def invoke_handler(self, payload):
        """
        """
        
        client = self.client
        payload = base64.b64encode(cloudpickle.dumps(payload)).decode("ascii")
        payload = json.dumps(payload)
        
        resp = client.invoke(
            FunctionName=self._lambda_arn,
            InvocationType="RequestResponse",
            Payload=payload
        )
        
        resp_bytes = resp["Payload"].read()
        
        if "FunctionError" in resp:
            result = resp_bytes
        else:
            result = cloudpickle.loads(resp_bytes)
        
        return result

    
class LambdaExecutor:
    """
    """
    
    def __init__(self, max_workers, lambda_arn):
        """
        """
        
        lambda_config = botocore.config.Config(
            retries={'max_attempts': 128},
            connect_timeout=60*10,
            read_timeout=60*10,
            max_pool_connections=10000
        )
        
        self._client = boto3.client("lambda", config=lambda_config)
        self._max_workers = max_workers
        self._executor = futures.ThreadPoolExecutor(max_workers=max_workers)
        self._lambda_arn = lambda_arn
        
        return
    
    def map(self, func, payloads, local_mode=False):
        """
        """
        
        from tqdm.autonotebook import tqdm
        
        if local_mode:
            f = func
        else:
            f = LambdaFunction(func, self._client, self._lambda_arn)
        
        ex = self._executor
        wait_for = [ex.submit(f, *p["args"], **p["kwargs"]) for p in payloads]
        tbar = tqdm(total=len(wait_for))
        prev_n_done = 0
        n_done = sum(f.done() for f in wait_for)
        
        while n_done != len(wait_for):
            tbar.update(n_done - prev_n_done)
            prev_n_done = n_done
            n_done = sum(f.done() for f in wait_for)
            time.sleep(0.5)
            
        tbar.update(n_done - prev_n_done)   
        tbar.close()
            
        results = [f.result() for f in futures.as_completed(wait_for)]
        return results