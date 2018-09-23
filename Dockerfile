FROM python:3

RUN pip install obonet
RUN pip install networkx

ADD read_synonym.py /
ENTRYPOINT ["python", "read_synonym.py"]