use actix_web::{App, HttpServer};

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let (host, port) = ("0.0.0.0", 18080);

    println!("Running an image web service on {}:{}!", host, port);

    HttpServer::new(|| App::new())
        .bind((host, port))?
        .run()
        .await
}
