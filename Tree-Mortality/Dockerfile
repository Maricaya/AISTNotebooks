# docker build -t tree-mortality .
# docker run --cap-add SYS_ADMIN --device /dev/fuse -v /flexfs/bayesics:/flexfs/bayesics -it tree-mortality
FROM ubuntu:20.04

ENV TZ=US \
    DEBIAN_FRONTEND=noninteractive

# Installing package dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git wget bzip2 libtool m4 automake build-essential python3 python3-pip python3-dev python3-venv libblas-dev liblapack-dev libatlas-base-dev gfortran libopenblas-dev libblis-dev libmkl-dev curl openssl libssl-dev libcurl4-openssl-dev libgeos-dev python3-tk libhdf4-dev libproj-dev proj-data proj-bin vim tzdata

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

# Clone Tree-Mortality repository
RUN git clone https://github.com/Maricaya/Tree-Mortality --branch main

# Installing Sciunit
RUN /opt/conda/bin/pip install sciunit2

# Setting current time zone
RUN ln -fs /usr/share/zoneinfo/America/Chicago /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

# Set the working directory
WORKDIR /Tree-Mortality

# Initialize conda
RUN /bin/bash -c "source /opt/conda/etc/profile.d/conda.sh && conda init"

# Create and activate the conda environment
RUN /bin/bash -c "source /opt/conda/etc/profile.d/conda.sh && \
    conda create -n ecopro python=3.10.6 -y && \
    echo 'source /opt/conda/etc/profile.d/conda.sh' >> ~/.bashrc && \
    echo 'conda activate ecopro' >> ~/.bashrc"

# Add channels and install primary packages
RUN /bin/bash -c "source /opt/conda/etc/profile.d/conda.sh && \
    conda activate ecopro && \
    conda config --add channels conda-forge && \
    conda config --add channels bioconda && \
    conda install -y xarray matplotlib cartopy numpy requests pandas"

# Install additional packages
RUN /bin/bash -c "source /opt/conda/etc/profile.d/conda.sh && \
    conda activate ecopro && \
    conda install -y netcdf4 rioxarray rasterio dask zarr tqdm h5netcdf dask-jobqueue && \
    conda install -y fiona scikit-learn geopandas ray-default snakemake cdsapi skops werkzeug && \
    pip install sciunit2"

RUN /bin/bash -c "source /opt/conda/etc/profile.d/conda.sh && conda activate ecopro && conda install libsqlite --force-reinstall -y"

ENTRYPOINT [ "/bin/bash", "-c", "source /root/.bashrc && exec bash" ]
