# Setup
Data files can be manually downloaded from: https://aura.gesdisc.eosdis.nasa.gov/data/Aura_OMI_Level2/OMO3PR.003/2021/. 

Registration is required to download files: https://disc.gsfc.nasa.gov/data-access. 

Follow instructions to download files via wget: https://disc.gsfc.nasa.gov/information/howto?title=How%20to%20Access%20GES%20DISC%20Data%20Using%20wget%20and%20curl.

All files required by the Kriging application can be downloaded by running the following commands:

 	mkdir data_src
  	cd data_src
   	# --user=<uid> 
   	wget --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies --user=xchu -r -c -nH -nd -np -A "$p" --content-disposition "https://aura.gesdisc.eosdis.nasa.gov/data/Aura_OMI_Level2/OMO3PR.003/2021/001"
# Build	
 	docker build -t krigging .

# Usage
 	docker run -it krigging
	cd NOGGIN && echo 'PYTHONPATH=./ python3 ./Krige/noggin_krige.py -d ./data_src/ -n HDFEOS/SWATHS/O3Profile/Data\ Fields/O3 -m gamma_rayleigh_nuggetless_variogram_model -v' > start.sh
    chmod +x ./start.sh 
    ./start.sh

# Usage With Sciunit
    sciunit create Kriging && export TZ='America/Chicago'
    sciunit exec ./start.sh
