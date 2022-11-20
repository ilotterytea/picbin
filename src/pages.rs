use std::fs;
use std::fs::{read, read_to_string, remove_file};
use std::io::Error;
use std::path::{Path, PathBuf};
use multipart::server::nickel::nickel::hyper::mime;
use multipart::server::nickel::nickel::hyper::mime::mime;
use rocket;
use rocket::{Config, Data, Request};
use rocket::data::ToByteUnit;
use rocket::form::error::ErrorKind::Multipart;
use rocket::form::Form;
use rocket::fs::{NamedFile, TempFile};
use rocket::fs::TempFile::File;
use rocket::http::{ContentType, Status};
use rocket::http::uri::{Absolute, Host};
use rocket::request::FromRequest;
use rocket::response::status::{NotFound, Custom, BadRequest};
use rocket::serde::{Serialize, json::Json};
use rocket_dyn_templates::{context, Template};

use crate::file;
use crate::file::InternalFile;
use crate::tire::{TireResponse};

/// Main page of web server.
#[get("/")]
pub fn index() -> (Status, (ContentType, Template)) {
    (Status::Ok, (ContentType::Plain, Template::render("plain", context! {})))
}

/// Retrieve a file from server.
#[get("/<id>")]
pub async fn retrieve(id: &str) -> Result<NamedFile, NotFound<Json<TireResponse>>> {
    let dir = Path::new(concat!(env!("CARGO_MANIFEST_DIR"), "/", "uploaded", "/")).join(id);
    NamedFile::open(&dir).await.map_err(|e| NotFound(Json(TireResponse {
        status: 404,
        message: e.to_string()
    })))
}

#[post("/upload", data="<file>")]
pub async fn upload(mut file: Form<TempFile<'_>>) -> Result<Json<InternalFile>, Error> {
    let ifile = InternalFile::new(6, &file);
    let path = Path::new(concat!(env!("CARGO_MANIFEST_DIR"), "/", "uploaded", "/")).join(format!("{}{}", &ifile.id, &ifile.ext));

    file.copy_to(&path).await?;
    println!("{}", path.into_os_string().to_str().unwrap());

    Ok(Json(ifile))
}