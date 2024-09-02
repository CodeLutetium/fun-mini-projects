# hello-docker (blog)
I know it says README.md in the file title but this is more of a blog for me to document my process of getting started with docker. I titled it 'README' (not clickbait) so that github will show this page when I open the directory without needing me to open the markdown. 

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

## Getting started with Postgres 
Let's move on to postgres. Similar to Python, we will start by test pulling the postgres image to my machine with `docker pull postgres:14.5`.

To run the postgres container, we run the following command:
```bash
docker run -e POSTGRES_PASSWORD=admin -d postgres
```
Some notes:
- We can use the flag `--name` to give our container a custom name. Without this argument, docker will automatically generate a random name for us.   
- postgres requires a password to function properly, which is why a default password of admin is specified.

When we run `docker ps`, we can see that a container running postgres at port 5432.

```bash
CONTAINER ID   IMAGE      COMMAND                  CREATED         STATUS         PORTS      NAMES
e0db6a77cc42   postgres   "docker-entrypoint.s…"   9 seconds ago   Up 7 seconds   5432/tcp   nice_mcclintock
```

And if you try to connect to that instance of postgres using pgadmin...it doesn't work. Why?

Luckily my current internship at Credit Agricole gave me some experience working with helm charts and minikube, so I had a rough sense why. I didn't port forward! Let's try running it again and specify the ports using the `-p` flag.

```bash
# Kill previous instance. Get the container id by running `docker ps`
docker stop <container-id>
# Verify instance has been killed (should be empty)
docker ps

# Now we run it with port forwarding
docker run -p 5432:5432 -e POSTGRES_PASSWORD=admin -d postgres
```

Some notes again: 
- MAKE SURE YOU HAVE **NO OTHER POSTGRES INSTANCES** RUNNING ON YOUR MACHINE!!

I will now try to connect to my container using pgadmin by connecting to localhost:5432 with the password I had set earlier. It successfully connects, and there is no tables or anything in my database (named postgres) because I have not done anything yet. 

My next step now is to try and create a table in pgadmin and insert some data there (which I won't be explaining how here because...basic GUI), and see if I can query it from the interactive shell. 

#### Getting into the docker container's shell (step by step)
```sh
docker exec -it <container-name> sh
su postgres
psql
```

Let's perform a simple select statement from the shell:
```sql
SELECT * FROM "Users";

-- We get: 
 id | name  | age 
----+-------+-----
  1 | John  |  20
  2 | Alice |  24
```

Some notes: 
- Remember to add semicolon ';' at the end of statement
- Table name must be surrounded by `"` (double quotes not single quotes)\

## Connecting to Postgres with Python
From here, everything should be quite easy. 

Running hello-postgres.py, we are able to see the rows in our postgres database "Users".