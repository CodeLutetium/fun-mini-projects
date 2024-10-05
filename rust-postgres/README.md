# rust-postgres

Explore connecting to a postgres instance using [sqlx](https://crates.io/crates/sqlx/0.8.2). In this project, I will connect to a postgres instance and perform simple query and insert operations.

## Getting started

Make sure you have an instance of postgres running. The database name is called "transactions".

### Running postgres container with docker

```sh
docker run -p 5432:5432 -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=transactions -d postgres
```

This creates a Docker container with PostgresSQL running, with port 5432 exposed. The default superuser password is set to admin, and a default database transactions is created. `-d` allows the container to run in the background after the script terminates. 

### What this code does

#### Step 1
Create a connection pool to the `transactions` database. 

#### Step 2
Perform [migrations](https://github.com/launchbadge/sqlx/tree/main/sqlx-cli) the migration script. Migrations ensure that we get the same tables if we run from a different postgres instance. 

In the migrations script, if the table `users` does not exist, we create a table called users (following the schema of the User struct) and populate it with one user. 

As this is just a proof-of-concept for me to explore sqlx, id is an auto incrementing value and I do not really care about writing code that skills in this snippet. 

#### Step 3
Fetch the last row and print. 

#### Step 4
Insert a new user with a randomly generated name and starting cash. 
Create a simple table titled "users" with the same schema as the Users struct.

#### Step 5
Lastly, I fetch all rows and print them.