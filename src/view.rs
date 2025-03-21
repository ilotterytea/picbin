use std::path::Path;

use actix_web::{HttpResponse, Responder, web};
use handlebars::Handlebars;
use serde_json::json;

const STATIC_FILES: include_dir::Dir = include_dir::include_dir!("static");
const TEMPLATE_FILES: include_dir::Dir = include_dir::include_dir!("templates");

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

pub fn register_handlebars_templates(hb: &mut Handlebars<'_>) {
    for template in TEMPLATE_FILES.files() {
        let Some(contents) = template.contents_utf8() else {
            continue;
        };

        let name = template.path().file_name().unwrap().to_str().unwrap();

        hb.register_template_string(name, contents)
            .expect("Error loading template");
    }
}

pub async fn get_index_view(hb: web::Data<Handlebars<'_>>) -> impl Responder {
    let body = hb.render("index.hbs", &json!({})).unwrap();

    web::Html::new(body)
}
