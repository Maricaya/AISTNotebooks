# Build: 
	docker build -t pomd_pf .

# Post-build requirements:
Requires installing and mounting flexFS.
docker run --cap-add SYS_ADMIN --device /dev/fuse -v /flexfs/bayesics:/flexfs/bayesics -it pomd_pf
# Usage
    docker run --cap-add SYS_ADMIN --device /dev/fuse -v /flexfs/bayesics:/flexfs/bayesics -it pomd_pf
    python3 POMD-PF.AIST.10202022.py
    python3 POMD-PF.AIST.SA.Storms.py

    sciunit create pomd_pf && export TZ='America/Chicago'
    sciunit exec python3 POMD-PF.AIST.10202022.py
  	sciunit exec python3 POMD-PF.AIST.SA.Storms.py

    sciunit repeat e1
    sciunit copy # Give it a second, and it returns a code.

    sciunit open <id>
