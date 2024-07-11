FROM ubuntu:20.04

ENV TZ=US \
    DEBIAN_FRONTEND=noninteractive

# Installing package dependencies
RUN apt-get update && \
	apt-get upgrade -y && \
	apt-get install -y git wget bzip2 libtool m4 automake build-essential python3 python3-pip python3-dev python3-venv libblas-dev liblapack-dev libatlas-base-dev gfortran libopenblas-dev libblis-dev libmkl-dev curl openssl libssl-dev libcurl4-openssl-dev libgeos-dev python3-tk libhdf4-dev libproj-dev proj-data proj-bin vim
RUN wget https://ftp.gnu.org/gnu/autoconf/autoconf-2.71.tar.xz && \
	tar -xf autoconf-2.71.tar.xz && \
	cd autoconf-2.71/ && \
	chmod -R 777 ./ && \
	./configure && \
	make && \
	make install

# Setting up Python virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m pip install virtualenv && \
	python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Installing HDF5 library and h5py
RUN wget https://hdf-wordpress-1.s3.amazonaws.com/wp-content/uploads/manual/HDF5/HDF5_1_14_3/src/hdf5-1.14.3.tar.bz2 && \
	tar -xvjf hdf5-1.14.3.tar.bz2 && \
	cd hdf5-1.14.3 && \
	libtoolize --force && \
	aclocal && \
	autoheader && \
	automake --force-missing --add-missing && \
	autoconf && \
	./configure CFLAGS="-fPIC" --enable-shared --with-pic --enable-ros3-vfd && \
	make && \
	make install && \
	make check-install && \
	mv hdf5 /usr/local/ && \
	HDF5_DIR=/usr/local/hdf5 pip3 install --no-binary=h5py h5py && \
	apt-get install -y libhdf5-dev hdf5-helpers hdf5-tools

# Installing Python dependencies
RUN python3 -m pip install connected-components-3d netCDF4 pandas starepandas
RUN python3 -m pip install versioneer
RUN python3 -m pip install pythreejs ipywidgets pystareplotlib
RUN python3 -m pip install cartopy
RUN python3 -m pip install -U git+https://github.com/skoch9/meshplot.git@v0.4.0


# Installing Sciunit
RUN python3 -m pip install wheel
RUN python3 -m pip install sciunit2
# Setting current time zone
RUN export TZ='America/Chicago'

# Copying script
COPY ./featureDB_make_df.py ./featureDB_make_df.py
COPY ./featureDB_make_labels.py ./featureDB_make_labels.py
COPY ./999-H0-00-IMERG-Analyze-1.py ./999-H0-00-IMERG-Analyze-1.py

# Creating directory to store pickle files
RUN mkdir pickles
RUN ulimit -n 4096


# Installing dependence files
RUN wget https://www2.census.gov/geo/tiger/TIGER2019/STATE/tl_2019_us_state.zip
