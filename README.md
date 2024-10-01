# uber-ride-api
Create and get ride status

# Build the development Docker image
`docker build -t uber-api-dev -f Dockerfile.dev .`

# Run the development Docker container
```shell
docker run -d \
  --name uber-api-dev \
  -p 8000:8000 \
  -v $(pwd)/app:/code/app \
  uber-api-dev
```

# Build the production Docker image
`docker build -t uber-api-prod -f Dockerfile.prod .`

# Run the production Docker container
```shell
docker run -d \
  --name uber-api-prod \
  -p 8000:8000 \
  uber-api-prod
```
