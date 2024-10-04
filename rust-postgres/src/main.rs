use sqlx::postgres::PgPoolOptions;
use sqlx::FromRow;
use rand::Rng;
use names::Generator;

#[derive(Debug, FromRow)]
struct User {
    id: i32,
    name: String,
    cash: i32,
}

#[tokio::main]
async fn main() -> Result<(), sqlx::Error> {
    // For generating random names
    let mut generator = Generator::default();

    // Check that username, password, port and database is correct.
    let pg_connection_str: &str = "postgres://postgres:admin@localhost:5432/transactions";
    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(pg_connection_str)
        .await?;

    // Fetch one row (last row)
    let row: User = sqlx::query_as("SELECT * FROM public.users ORDER BY id DESC LIMIT 1")
        .fetch_one(&pool)
        .await?;
    println!("{:#?}", row);

    // Insert new user
    let new_user: User = User {
        id: row.id + 1,     // Increment last result by 1
        name: "Jane".to_string(),
        cash: rand::thread_rng().gen_range(0..100000),
    };
    sqlx::query("INSERT INTO users VALUES ($1, $2, $3)")
        .bind(new_user.id)
        .bind(new_user.name)
        .bind(new_user.cash)
        .execute(&pool)
        .await?;

    // Fetch all rows
    let all_users: Vec<User> = sqlx::query_as("SELECT * FROM public.users")
        .fetch_all(&pool)
        .await?;
    println!("{:#?}", all_users);

    Ok(())
}
