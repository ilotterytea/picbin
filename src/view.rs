use std::path::Path;

use actix_web::{HttpResponse, web};

const STATIC_FILES: include_dir::Dir = include_dir::include_dir!("static");

pub async fn handle_static_file(filename: web::Path<String>) -> HttpResponse {
    let path = &*filename;

    let Some(file) = STATIC_FILES.get_file(path) else {
        return HttpResponse::NotFound().body(format!("{} not found", path));
    };

    let Some(mime) = mime_guess::from_path(path).first_raw() else {
        return HttpResponse::NotFound().body(format!("{} cannot be sent", path));
    };

    let path = Path::new(path);

    HttpResponse::Ok()
        .insert_header(("Content-Type", mime))
        .insert_header((
            "Content-Disposition",
            format!(
                "inline; filename=\"{}\"",
                path.file_name().unwrap().to_str().unwrap()
            ),
        ))
        .body(file.contents())
}
