package main

import (
	"log"
	"github.com/gofiber/fiber/v2"
)

func main() {
	app := fiber.New()

	app.Get("/", func(c *fiber.Ctx) error {
		return c.SendString("Hello, my beloved world!")
	})

	log.Fatal(app.Listen(":5001"))
}