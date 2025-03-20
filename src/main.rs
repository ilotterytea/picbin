use actix_web::{App, HttpServer, web};
use serde::Serialize;

mod config;
mod database;
mod image;
mod random;
mod view;

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

    HttpServer::new(|| {
        App::new()
            .route("/upload", web::post().to(image::handle_image_upload))
            .route("/{id}", web::get().to(image::handle_image_retrieve))
            .route("/{id}", web::delete().to(image::handle_image_deletion))
            .route("/{id}", web::put().to(image::handle_image_update))
            .route(
                "/static/{filename:.*}",
                web::get().to(view::handle_static_file),
            )
    })
    .bind((host, port))?
    .run()
    .await
}
