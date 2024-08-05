# Build:
    docker build -t tree-mortality .
    docker run -it tree-mortality

# Post-build requirements:
    wget https://depauledu-my.sharepoint.com/:u:/g/personal/xchu3_depaul_edu/EVkiqIrakgxBi1xsf4VU2EAB-3Ibpt0f8Jenqltd3KwEjA?download=1 -O data.zip
    unzip data.zip


# Usage:
    sciunit create tree-mortality  && export TZ='America/Chicago'
    chmod +x ./01_bcm_pipeline.sh
    chmod +x ./02_mortality_pipeline.sh
    sciunit exec ./01_bcm_pipeline.sh
    sciunit exec ./02_mortality_pipeline.sh
