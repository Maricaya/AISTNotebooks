1. Download the required data.
```
wget https://depauledu-my.sharepoint.com/:u:/g/personal/xchu3_depaul_edu/EVkiqIrakgxBi1xsf4VU2EAB-3Ibpt0f8Jenqltd3KwEjA?download=1 -O data.zip
unzip data.zip
```

2. Build and run the Docker container to execute the workflow.
```
docker build -t tree-mortality .
docker run -v ./:/shared -it tree-mortality
```
3. sequential execution
```
sciunit create tree-mortality  && export TZ='America/Chicago'
chmod +x *.sh
sciunit exec ./time.sh
```
4. parallel computing

Thank you for your patience. The code for parallel computing is still being refined and has not been released yet. We will send you an email as soon as it becomes available.
