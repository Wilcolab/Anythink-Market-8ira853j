package main

import (
	"net/http"
	"github.com/gin-gonic/gin"
)

var items = []gin.H{
	{"id": 1, "name": "Galactic Goggles"},
	{"id": 2, "name": "Meteor Muffins"},
	{"id": 3, "name": "Alien Antenna Kit"},
	{"id": 4, "name": "Starlight Lantern"},
	{"id": 5, "name": "Quantum Quill"},
}

func main() {
	router := gin.Default()
	router.GET("/", greet)
	router.GET("/items", getItems)
	router.POST("/items", addItem)
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

func getItems(c *gin.Context) {
	c.JSON(http.StatusOK, items)
}

func addItem(c *gin.Context) {
	var newItem struct {
		Name string `json:"name" binding:"required"`
	}

	if err := c.ShouldBindJSON(&newItem); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	id := len(items) + 1
	item := gin.H{"id": id, "name": newItem.Name}
	items = append(items, item)

	c.JSON(http.StatusOK, item)
}
