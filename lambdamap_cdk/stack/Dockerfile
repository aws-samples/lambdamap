FROM public.ecr.aws/lambda/python:3.8

# You can specify custom Dockerfile commands to run at build time e.g:
#
#	$ docker build --build-arg EXTRA_CMDS='echo hello' -t .
#
# This is useful if you need additional prerequisites for the lambda function.
ARG EXTRA_CMDS
ENV EXTRA_CMDS=${EXTRA_CMDS:-"echo 'NO EXTRA COMMANDS'"}

RUN yum update -y \
    && yum install -y shadow-utils.x86_64 zip unzip \
        gcc-c++ make openssl-devel zlib-devel readline-devel git

RUN pip install awswrangler==2.6.0
RUN pip install awslambdaric cloudpickle==1.6.0 scikit-learn==0.24.1
RUN ${EXTRA_CMDS}
RUN touch ${LAMBDA_TASK_ROOT}/logs.log && chmod a+rwx ${LAMBDA_TASK_ROOT}/logs.log

COPY lambda.py ${LAMBDA_TASK_ROOT}

CMD ["lambda.handler"]
