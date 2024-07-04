# Build: 
	docker build -t feature_db .

# Post-build requirements:
Requires installing and mounting flexFS.

# Usage:
    docker run --cap-add SYS_ADMIN --device /dev/fuse -v /flexfs/bayesics:/flexfs/bayesics -it feature_db
 	python3 featureDB_make_labels.py
  	python3 featureDB_make_df.py
    python3 999-H0-00-IMERG-Analyze-1.py

    sciunit create Project1
    sciunit exec python3 featureDB_make_labels.py
    sciunit exec python3 featureDB_make_df.py
    sciunit exec python3 999-H0-00-IMERG-Analyze-1.py

    
    

