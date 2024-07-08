# Build: 
	docker build -t pomd_pf .

# Post-build requirements:
Requires installing and mounting flexFS.

# Usage
    docker run --cap-add SYS_ADMIN --device /dev/fuse -v /flexfs/bayesics:/flexfs/bayesics -it pomd_pf
    python3 POMD-PF.AIST.10202022.py
    python3 POMD-PF.AIST.SA.Storms.py

    sciunit create pomd_pf
    sciunit exec python3 POMD-PF.AIST.10202022.py
  	sciunit exec python3 POMD-PF.AIST.SA.Storms.py
