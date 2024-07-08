examples for sciunit

# Feature Database
## Build: 
	docker build -t feature_db .

## Post-build requirements:
Requires installing and mounting flexFS.

## Usage:
    docker run --cap-add SYS_ADMIN --device /dev/fuse -v /flexfs/bayesics:/flexfs/bayesics -it feature_db
 	python3 featureDB_make_labels.py
  	python3 featureDB_make_df.py
    python3 999-H0-00-IMERG-Analyze-1.py

    sciunit create feature_db
    sciunit exec python3 featureDB_make_labels.py
    sciunit exec python3 featureDB_make_df.py
    sciunit exec python3 999-H0-00-IMERG-Analyze-1.py

# POMD-PF
## Build: 
	docker build -t pomd_pf .

## Post-build requirements:
Requires installing and mounting flexFS.

## Usage
    docker run --cap-add SYS_ADMIN --device /dev/fuse -v /flexfs/bayesics:/flexfs/bayesics -it pomd_pf
    python3 POMD-PF.AIST.10202022.py
    python3 POMD-PF.AIST.SA.Storms.py

    sciunit create pomd_pf
    sciunit exec python3 POMD-PF.AIST.10202022.py
  	sciunit exec python3 POMD-PF.AIST.SA.Storms.py


# Kriging
## Setup
Data files can be manually downloaded from: https://aura.gesdisc.eosdis.nasa.gov/data/Aura_OMI_Level2/OMO3PR.003/2021/. 

Registration is required to download files: https://disc.gsfc.nasa.gov/data-access. 

Follow instructions to download files via wget: https://disc.gsfc.nasa.gov/information/howto?title=How%20to%20Access%20GES%20DISC%20Data%20Using%20wget%20and%20curl.

All files required by the Kriging application can be downloaded by running the following commands:

 	mkdir data_src
  	cd data_src
 	while read p;do wget --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies --user=xchu -r -c -nH -nd -np -A "$p" --content-disposition "https://aura.gesdisc.eosdis.nasa.gov/data/Aura_OMI_Level2/OMO3PR.003/2021/001"; done < spec_list.txt
## Build	
 	docker build -t krigging .

## Usage
 	docker run -it krigging
	cd NOGGIN && echo 'PYTHONPATH=./ python3 ./Krige/noggin_krige.py -d ./data_src/ -n HDFEOS/SWATHS/O3Profile/Data\ Fields/O3 -m gamma_rayleigh_nuggetless_variogram_model -v' > start.sh
    chmod +x ./run_kriging.sh 
    ./run_kriging.sh 

## Usage With Sciunit
    sciunit create Kriging
    sciunit exec ./run_kriging.sh 

# Tree-Mortality

# Kelp-Forest-Projection