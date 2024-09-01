# hello-docker (blog)
I know it says README.md in the file title but this is more of a blog for me to document my process of getting started with docker. 

## Objective
Post data into a postgres database and containerize the application using docker. Let's go!

## Pre-requisites
Make sure [docker](https://docs.docker.com/desktop/install/mac-install/) is installed on your computer.

## Getting started with Python
We will start with the easy step first, which is to run a simple hello world from a python container in docker.

First, we need to pull Python's image by running the following:

```bash
docker pull python
```
> Note: if `docker pull` does not work on windows, make sure docker desktop is running first.


To run an interactive container with the python image we just pulled, we run 
```bash
docker run -it python sh
```
Running the `run` command with the `-it` flags attaches us to an interactive tty in the container. We can verify that python is correctly installed in the container by running `python --version`, which should give us the following output:
```bash
# python --version
Python 3.12.5
```
Fantastic. Now that it is working, let's exit the container by running `exit`. Now, we know how to run a container in cmd, but what we want to achieve is to run our `hello.py` program in a python container. Turns out we don't have to perform a docker pull everytime we want to run a new container, because we can simply create a `Dockerfile` instead.

In the dockerfile, we first specify the base image we want to use, which is python. 

Next, we add the file we want to run, which is `hello.py` to the root directory of the file image. 
>Syntax for `ADD`
>```dockerfile
>ADD [OPTIONS] <src> ... <dest>
>```
>[Reference](https://docs.docker.com/reference/dockerfile/#add)

Lastly, we add the commands that we want to run with [`CMD`](https://docs.docker.com/reference/dockerfile/#cmd) command.

This is how our `Dockerfile` should look like:
```dockerfile
FROM python:3.12.5

ADD hello.py .

CMD ["python", "hello.py"]
```

To build the image, we need to run:
```sh
# note the dot at the end
docker build -t hello-python .
```
This builds us an image from the Dockerfile located in the root directory called "hello-python". Of course we can name the image anything we want.

Finally, let's run the image "hello-python":
```sh
docker run hello-python

# Output:
> hello world
```