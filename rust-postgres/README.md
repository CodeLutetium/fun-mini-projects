# rust-postgres

Explore connecting to a postgres instance using [sqlx](https://crates.io/crates/sqlx/0.8.2). In this project, I will connect to a postgres instance and perform simple query and insert operations.

## Getting started

Make sure you have an instance of postgres running. The database name is called "transactions".

### Running postgres container with docker

```sh
docker run -p 5432:5432 -e POSTGRES_PASSWORD=admin -d postgres
```

### Create simple table instance

Create a simple table titled "users" with the same schema as the Users struct.