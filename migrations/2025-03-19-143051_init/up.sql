-- Your SQL goes here
CREATE TABLE "images" (
    "id" TEXT NOT NULL UNIQUE PRIMARY KEY,
    "filename" TEXT NOT NULL,
    "extension" TEXT NOT NULL,
    "mime" TEXT NOT NULL,
    "uploaded_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);