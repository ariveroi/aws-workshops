FROM public.ecr.aws/amazonlinux/amazonlinux:2022
RUN yum install python3 && \
curl -O https://bootstrap.pypa.io/get-pip.py && \
python3 get-pip.py && \
pip install --upgrade pip

RUN alias python=python3

ENV FLASK_APP app.py
ENV PLATFORM 'Amazon ECS'

WORKDIR /app
COPY . /app/

RUN pip install -r requirements.txt

CMD ["python3", "app.py"]
