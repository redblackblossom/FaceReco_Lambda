FROM amazon/aws-lambda-python:3.8

COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --no-cache-dir -r requirements.txt

COPY imageCompaction.py ${LAMBDA_TASK_ROOT}
CMD ["imageCompaction.handler"]