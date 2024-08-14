FROM ubuntu:bionic

RUN apt-get update --fix-missing && apt-get install -y \
	clang-7 \
	gfortran \
	libboost-all-dev \
	libfftw3-dev \
	libgsl-dev \
	libtiff-dev \
	liblapack-dev \
	libblas-dev \
	libboost-dev \
	make \
	libarmadillo-dev \
	curl \
        python3-pip \
        wget 

RUN DEBIAN_FRONTEND=noninteractive apt-get -y install tzdata

RUN apt-get update --fix-missing
RUN apt-get install -y --no-install-recommends make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

ENV HOME="/root"
WORKDIR ${HOME}
RUN apt-get install -y git
RUN git clone --depth=1 https://github.com/pyenv/pyenv.git .pyenv
ENV PYENV_ROOT="${HOME}/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"


ENV PYTHON_VERSION=3.6
RUN pyenv install ${PYTHON_VERSION}
RUN pyenv global ${PYTHON_VERSION}
RUN pip install numpy
RUN pip install matplotlib
RUN pip install pandas


COPY /source /accuRT/source

ENV ACCURT_PATH=/accuRT/source/trunk
ENV LD_LIBRARY_PATH=$ACCURT_PATH/lib:/usr/lib:/usr/local/lib:$LD_LIBRARY_PATH
ENV PATH=$ACCURT_PATH/main:$PATH

# Avoid ascii errors when reading files in Python
RUN apt-get install -y locales && locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'

RUN mkdir /work
WORKDIR /work

# The /src folder of this repository should be in the same location of this Dockerfile after cloning from the GitHub repo, 
# Copy /src into the Docker work folder so that it is accessible when the container is run
RUN cp -r src/ /work
  
RUN apt-get install -y vim nano

ENV PORT=8000
EXPOSE 8000 8000

CMD npm run start
# CMD npm run debug
# CMD tail -f /dev/null
