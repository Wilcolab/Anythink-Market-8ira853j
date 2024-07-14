package main

import (
	"net/http"
	"github.com/gin-gonic/gin"
	"math/rand"
)

func main() {
	router := gin.Default()
	router.GET("/", greet)
	router.HEAD("/healthcheck", healthcheck)
	router.POST("/items", addItem)
	router.GET("/items", items)

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
var inventory = []struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
}{
	{ID: 1, Name: "Galactic Goggles"},
	{ID: 2, Name: "Meteor Muffins"},
	{ID: 3, Name: "Alien Antenna Kit"},
	{ID: 4, Name: "Starlight Lantern"},
	{ID: 5, Name: "Quantum Quill"},
}
func items(c *gin.Context) {
	c.JSON(http.StatusOK, inventory)
}
func addItem(c *gin.Context) {
	var newItem struct {
		Name string `json:"name"`
	}

	if err := c.ShouldBindJSON(&newItem); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Generate a random number between 1 and 100
	newID := rand.Intn(100) + 1

	// Create the new item
	item := struct {
		ID   int    `json:"id"`
		Name string `json:"name"`
	}{
		ID:   newID,
		Name: newItem.Name,
	}

	// Add the new item to the inventory
	inventory = append(inventory, item)

	c.JSON(http.StatusOK, item)
}