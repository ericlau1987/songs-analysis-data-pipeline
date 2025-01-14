FROM cluster-base

# -- Layer: JupyterLab

ARG spark_version=3.3.1
ARG jupyterlab_version=3.6.1

# RUN apt-get update -y
# RUN apt-get install -y pipx
# RUN pipx install pyspark==${spark_version} jupyterlab==${jupyterlab_version}
RUN apt-get update -y 
RUN apt-get upgrade -y
RUN apt-get install -y python3-pip 
# https://stackoverflow.com/questions/75608323/how-do-i-solve-error-externally-managed-environment-every-time-i-use-pip-3
RUN pip3 install wget pyspark==${spark_version} jupyterlab==${jupyterlab_version} --break-system-packages

# -- Runtime

EXPOSE 8888
WORKDIR ${SHARED_WORKSPACE}

CMD jupyter-lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=
