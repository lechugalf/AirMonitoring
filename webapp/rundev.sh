docker run -itd --name webapp -p 5000:5000/tcp -p 5000:5000/udp --rm --mount type=bind,source="$(pwd)"/app,target=/usr/src/app webapp:dev 
