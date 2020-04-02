FROM nvidia/cudagl:9.2-runtime-ubuntu18.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-dev ipython3 module-init-tools curl build-essential python3-pip

# OpenCV's runtime dependencies
RUN apt-get install -y libglib2.0-0 libsm6 libxrender-dev libxext6

RUN pip3 install -U pip setuptools wheel

RUN pip3 install numpy posix_ipc holodeck pytest opencv-python

RUN adduser --disabled-password --gecos "" holodeckuser

WORKDIR /home/holodeckuser/source/holodeck/

# This should be COPY ../ but docker doesn't allow copying files outside the context
# To copy the project files either run the build command in this directory with the
# previous directory as the context: docker build -t pccl/holodeck[:tag] -f ./Dockerfile ..
# or run it from the parent directory and provide the docekr file location
# docker build -t pccl/holodeck[:tag] -f ./docker/Dockerfile .
COPY ./ .

USER holodeckuser

CMD ["/bin/bash"]
