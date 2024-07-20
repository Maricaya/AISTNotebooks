# todo explain readme

docker build -t tree-mortality .
docker run --cap-add SYS_ADMIN --device /dev/fuse -v /flexfs/bayesics:/flexfs/bayesics -it tree-mortality

sciunit create tree-mortality  && export TZ='America/Chicago'