use multipart::server::nickel::nickel::hyper::mime::mime;
use rand::{self, Rng};
use rocket::fs::TempFile;
use rocket::serde::Serialize;

/// Internal file.
#[derive(Serialize)]
pub struct InternalFile {
    /// File ID.
    pub id: String,
    /// Mime type of file.
    pub mime: String,
    /// File extension.
    pub ext: String,

    /// Secret key of file.
    pub secret_key: String
}

const CHAR_RANGE: &[u8] = b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

impl InternalFile {
    pub fn new(
        char_length: usize,
        file: &TempFile<'_>
    ) -> InternalFile {
        let mut id = String::with_capacity(char_length);
        let mut secret_key = String::with_capacity(32);
        let mut rng = rand::thread_rng();

        for _ in 0..char_length {
            id.push(CHAR_RANGE[rng.gen::<usize>() % CHAR_RANGE.len()] as char);
            secret_key.push(CHAR_RANGE[rng.gen::<usize>() % CHAR_RANGE.len()] as char);
        }

        let mime = file.content_type().unwrap().to_string();
        let ext = mime_guess::get_mime_extensions_str(&mime);
        println!("{} -- {}", "test", &mime);

        for i in ext.unwrap() {
            println!("{}", i)
        }

        InternalFile {
            id,
            mime,
            ext: ".png".to_string(),
            secret_key
        }
    }
}