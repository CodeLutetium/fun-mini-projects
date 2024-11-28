# docker-watch-golang

This project aims to make use of `docker compose watch` to live reload the container during development with a simple Go server in backend. 

Live reload takes approx. 10s with the default Dockerfile. In this project, I optimized the Dockerfile following the blog article below to bring the build time down to **~1 second**.

Also check out [Air](https://github.com/air-verse/air) as an alternative to live reloading in Golang.

## Getting started
To start development, simply run `docker compose watch`. Edit `main.go` and watch your changes get updated live. To ping the container, run `curl localhost:8080/ping`.

## References
[eblog's fast docker](https://eblog.fly.dev/fastdocker.html)