docker rm $(docker ps --all -q -f status=exited)
docker-compose up -d
