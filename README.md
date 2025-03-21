<h1>
    <img src="./static/img/favicon.png" width=28> rusti
</h1>

a tiny image service, written in Rust and using `actix-web`

## Prerequisites

+ Rust compiler
+ SQLite
+ Diesel CLI `(cargo install diesel_cli --no-default-features -F sqlite)`

## Compile from sources

```bash
diesel migration run --database-url database.db
cargo run
```

