docker stop bsb-beta
docker rm bsb-beta
docker build -t bsb-beta .
docker run --name bsb-beta -d bsb-beta
