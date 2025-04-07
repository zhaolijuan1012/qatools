FROM python:3.7
WORKDIR ./qa_tools
ADD . .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN sed -i 's/flask._compat/flask_script._compat/g' /usr/local/lib/python3.7/site-packages/flask_script/__init__.py
CMD [ "/bin/bash", "init_db.sh" ]