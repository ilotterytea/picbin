use std::fs::{copy, create_dir_all, exists};

use actix_multipart::form::{MultipartForm, tempfile::TempFile};
use actix_web::HttpResponse;
use diesel::{ExpressionMethods, QueryDsl, RunQueryDsl, SelectableHelper};

use crate::{
    Response,
    config::DEFAULT_MIME_TYPES,
    database::{
        establish_connection,
        models::{Image, NewImage},
        schema::images::dsl as im,
    },
    random::{self, generate_random_sequence},
};

#[derive(MultipartForm)]
pub struct ImageUpload {
    pub file: TempFile,
}

pub async fn handle_image_upload(MultipartForm(form): MultipartForm<ImageUpload>) -> HttpResponse {
    if !exists("userdata").unwrap_or(false) && create_dir_all("userdata").is_err() {
        return HttpResponse::InternalServerError().json(Response {
            status_code: 500,
            message: Some("Failed to create a directory for user data".into()),
            data: None::<Image>,
        });
    }

    let mime = match form.file.content_type {
        Some(m) => m,
        None => {
            return HttpResponse::BadRequest().json(Response {
                status_code: 400,
                message: Some("Unknown MIME type".into()),
                data: None::<Image>,
            });
        }
    };

    let (_, extension) = match DEFAULT_MIME_TYPES
        .iter()
        .find(|(x, _)| (*x).eq(mime.essence_str()))
    {
        Some(m) => m,
        None => {
            return HttpResponse::BadRequest().json(Response {
                status_code: 400,
                message: Some(format!("Unsupported MIME type: {}", mime.essence_str())),
                data: None::<Image>,
            });
        }
    };

    let id = generate_random_sequence(6, random::CHARACTER_POOL);

    let old_path = form.file.file.path();
    let new_path = format!("userdata/{}.{}", id, extension);

    if copy(old_path, new_path).is_err() {
        return HttpResponse::InternalServerError().json(Response {
            status_code: 500,
            message: Some("Failed to copy the file".into()),
            data: None::<Image>,
        });
    }

    let filename = match form.file.file_name {
        Some(n) => n,
        None => format!("{}.{}", id, extension),
    };

    // saving image data
    let conn = &mut establish_connection();

    let image = diesel::insert_into(im::images)
        .values(NewImage {
            id: &id,
            filename: &filename,
            extension,
            mime: mime.essence_str(),
        })
        .returning(Image::as_returning())
        .get_result(conn)
        .expect("Error saving new image");

    HttpResponse::Created().json(Response {
        status_code: 201,
        message: None,
        data: Some(image),
    })
}
