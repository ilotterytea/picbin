#[macro_use] extern crate rocket;

use rocket_dyn_templates::Template;

mod tire;
mod pages;
mod file;

#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", routes![pages::index, pages::retrieve, pages::upload])
        .attach(Template::fairing())
}
