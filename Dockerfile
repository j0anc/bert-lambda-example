FROM public.ecr.aws/lambda/python:3.9

RUN pip3 install pdm==1.13.3
COPY app ${LAMBDA_TASK_ROOT}/app
WORKDIR ${LAMBDA_TASK_ROOT}/app

RUN pdm install -G main -v && \
    mv __pypackages__/3.9/lib/* ${LAMBDA_TASK_ROOT} && \
    mv app/* ${LAMBDA_TASK_ROOT}/app

CMD [ "app.main.handler" ]