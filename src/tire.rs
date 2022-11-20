use rocket::serde::{Serialize};

#[derive(Serialize)]
/// JSON response.
pub struct TireResponse {
    /// The status code of response.
    pub status: u16,
    /// The message of response.
    pub message: String
}
