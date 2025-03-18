use std::fs::{copy, create_dir_all, exists};

use actix_multipart::form::{MultipartForm, tempfile::TempFile};
use actix_web::HttpResponse;
use serde::Serialize;

use crate::{
    Response,
    config::DEFAULT_MIME_TYPES,
    random::{self, generate_random_sequence},
};

#[derive(MultipartForm)]
pub struct ImageUpload {
    pub file: TempFile,
}

#[derive(Serialize)]
struct ImageData {
    pub id: String,
    pub mime: String,
    pub extension: String,
}

pub async fn handle_image_upload(MultipartForm(form): MultipartForm<ImageUpload>) -> HttpResponse {
    if !exists("userdata").unwrap_or(false) && create_dir_all("userdata").is_err() {
        return HttpResponse::InternalServerError().json(Response {
            status_code: 500,
            message: Some("Failed to create a directory for user data".into()),
            data: None::<ImageData>,
        });
    }

    let mime = match form.file.content_type {
        Some(m) => m,
        None => {
            return HttpResponse::BadRequest().json(Response {
                status_code: 400,
                message: Some("Unknown MIME type".into()),
                data: None::<ImageData>,
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
                data: None::<ImageData>,
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
            data: None::<ImageData>,
        });
    }

    let image_data = ImageData {
        id,
        mime: mime.essence_str().to_string(),
        extension: extension.to_string(),
    };

    HttpResponse::Created().json(Response {
        status_code: 201,
        message: None,
        data: Some(image_data),
    })
}
