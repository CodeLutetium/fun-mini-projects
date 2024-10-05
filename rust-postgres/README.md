# rust-postgres

Explore connecting to a postgres instance using [sqlx](https://crates.io/crates/sqlx/0.8.2). In this project, I will connect to a postgres instance and perform simple query and insert operations.

## Getting started

Make sure you have an instance of postgres running. The database name is called "transactions".

### Running postgres container with docker

```sh
docker run -p 5432:5432 -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=transactions -d postgres
```

This creates a Docker container with PostgresSQL running, with port 5432 exposed. The default superuser password is set to admin, and a default database transactions is created. `-d` allows the container to run in the background after the script terminates. 

### Create simple table instance

Create a simple table titled "users" with the same schema as the Users struct.