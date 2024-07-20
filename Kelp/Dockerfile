# docker build -t kelp-forest-projection .
# docker run --cap-add SYS_ADMIN --device /dev/fuse -v /flexfs/bayesics:/flexfs/bayesics -it kelp-forest-projection
FROM ubuntu:20.04

ENV TZ=US \
    DEBIAN_FRONTEND=noninteractive

# Installing package dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git wget bzip2 libtool m4 automake build-essential python3 python3-pip python3-dev python3-venv libblas-dev liblapack-dev libatlas-base-dev gfortran libopenblas-dev libblis-dev libmkl-dev curl openssl libssl-dev libcurl4-openssl-dev libgeos-dev python3-tk libhdf4-dev libproj-dev proj-data proj-bin vim tzdata git-lfs

# Install Autoconf
RUN wget https://ftp.gnu.org/gnu/autoconf/autoconf-2.71.tar.xz && \
    tar -xf autoconf-2.71.tar.xz && \
    cd autoconf-2.71/ && \
    chmod -R 777 ./ && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -rf autoconf-2.71 autoconf-2.71.tar.xz

# Installing conda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    chmod +x miniconda.sh && \
    ./miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh && \
    /opt/conda/bin/conda init bash

# Set the PATH environment variable to include conda
ENV PATH=/opt/conda/bin:$PATH

# Clone kelp-forest-projection repository
RUN git clone https://github.com/EcoPro-Systems/Kelp-Forest-Projection.git --branch main

# Installing Sciunit
RUN /opt/conda/bin/pip install sciunit2

# Setting current time zone
RUN ln -fs /usr/share/zoneinfo/America/Chicago /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

# Set the working directory
WORKDIR /Kelp-Forest-Projection

# Initialize conda
RUN /bin/bash -c "source /opt/conda/etc/profile.d/conda.sh && conda init"

# Create and activate the conda environment
RUN /bin/bash -c "source /opt/conda/etc/profile.d/conda.sh && \
    conda create -n kelp python=3.10 -y && \
    echo 'source /opt/conda/etc/profile.d/conda.sh' >> ~/.bashrc && \
    echo 'conda activate kelp' >> ~/.bashrc"

# Add channels and install primary packages
RUN /bin/bash -c "source /opt/conda/etc/profile.d/conda.sh && \
    conda activate kelp && \
    conda install -y ipython jupyter pandas matplotlib scipy scikit-learn"

# Install additional packages
RUN /bin/bash -c "source /opt/conda/etc/profile.d/conda.sh && \
    conda activate kelp && \
    conda install -c conda-forge xarray dask netCDF4 bottleneck && \
    pip install tqdm statsmodels astropy && \
    pip install sciunit2"

## Ensure the container starts with the conda environment activated
ENTRYPOINT [ "/bin/bash", "-c", "source /root/.bashrc && exec bash" ]

