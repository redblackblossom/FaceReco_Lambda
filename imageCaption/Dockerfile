FROM amazon/aws-lambda-python:3.8

COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --no-cache-dir -r requirements.txt

COPY ./models ${LAMBDA_TASK_ROOT}/models

COPY imageCaption.py ${LAMBDA_TASK_ROOT}
COPY esQuery.py ${LAMBDA_TASK_ROOT}

CMD ["imageCaption.handler"]