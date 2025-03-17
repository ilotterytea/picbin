use actix_web::{App, HttpServer, web};
use serde::Serialize;

mod image;
mod random;

#[derive(Serialize)]
pub struct Response<T> {
    pub status_code: u16,
    pub message: Option<String>,
    pub data: Option<T>,
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let (host, port) = ("0.0.0.0", 18080);

    println!("Running an image web service on {}:{}!", host, port);

    HttpServer::new(|| App::new().route("/upload", web::post().to(image::handle_image_upload)))
        .bind((host, port))?
        .run()
        .await
}
