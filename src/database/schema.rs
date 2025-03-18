// @generated automatically by Diesel CLI.

diesel::table! {
    images (id) {
        id -> Text,
        filename -> Text,
        extension -> Text,
        mime -> Text,
        uploaded_at -> Timestamp,
    }
}
