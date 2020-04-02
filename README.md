To build:
```
docker build -t containeroso .
```
To run:
```
docker run -t -p 5000:5000 -v /var/run/docker.sock:/var/run/docker.sock containeroso
```
