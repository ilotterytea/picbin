use diesel::prelude::*;

pub mod models;
pub mod schema;

pub fn establish_connection() -> SqliteConnection {
    // TODO: make the url changeable
    let database_url = "database.db";

    SqliteConnection::establish(&database_url)
        .unwrap_or_else(|_| panic!("Error connecting to {}", database_url))
}
