package main

import (
	"net/http"
	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()
	router.GET("/", greet)
	router.GET("/items", items)
	router.HEAD("/healthcheck", healthcheck)

	router.Run()
}

func greet(c *gin.Context) {
	c.IndentedJSON(http.StatusOK, "Welcome, Go navigator, to the Anythink cosmic catalog.")
}

func healthcheck(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status": "ok",
	})
}
func items(c *gin.Context) {
	items := []struct {
		ID   int    `json:"id"`
		Name string `json:"name"`
	}{
		{ID: 1, Name: "Galactic Goggles"},
		{ID: 2, Name: "Meteor Muffins"},
		{ID: 3, Name: "Alien Antenna Kit"},
		{ID: 4, Name: "Starlight Lantern"},
		{ID: 5, Name: "Quantum Quill"},
	}

	c.JSON(http.StatusOK, items)
}