# todo explain readme

Build:
    docker build -t tree-mortality .
    docker run --cap-add SYS_ADMIN --device /dev/fuse -v /flexfs/bayesics:/flexfs/bayesics -it tree-mortality

Post-build requirements:
    Requires installing and mounting flexFS.
    If you don't know how to mount flexFS, please send me email.(xchu3@depaul.edu)

Usage:
    sciunit create tree-mortality  && export TZ='America/Chicago'
    chmod +x ./01_bcm_pipeline.sh
    chmod +x ./02_mortality_pipeline.sh
    sciunit exec ./01_bcm_pipeline.sh
    sciunit exec ./02_mortality_pipeline.sh
