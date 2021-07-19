FROM public.ecr.aws/lambda/python:3.8

RUN yum update -y \
    && yum install -y shadow-utils.x86_64 zip unzip \
        gcc-c++ make openssl-devel zlib-devel readline-devel git

RUN pip install awswrangler==2.6.0
RUN pip install awslambdaric cloudpickle==1.6.0 scikit-learn==0.24.1

RUN touch ${LAMBDA_TASK_ROOT}/logs.log && chmod a+rwx ${LAMBDA_TASK_ROOT}/logs.log

COPY lambda.py ${LAMBDA_TASK_ROOT}

CMD ["lambda.handler"]
