package main

import (
	"net/http"
	"strconv"
	"sync"

	"github.com/gin-gonic/gin"
)

type Item struct {
	ID        int    `json:"id"`
	Name      string `json:"name"`
	ViewCount int    `json:"view_count"`
}

var (
	items = []Item{
		{ID: 1, Name: "Galactic Goggles"},
		{ID: 2, Name: "Meteor Muffins"},
		{ID: 3, Name: "Alien Antenna Kit"},
		{ID: 4, Name: "Starlight Lantern"},
		{ID: 5, Name: "Quantum Quill"},
	}
	mu sync.Mutex
)

func main() {
	router := gin.Default()
	router.GET("/", greet)
	router.GET("/items", getItems)
	router.GET("/items/:id", getItemByID)
	router.GET("/items/popular", getPopularItem)
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

func getItemByID(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid item ID"})
		return
	}

	var item *Item
	for i := range items {
		if items[i].ID == id {
			item = &items[i]
			break
		}
	}

	if item == nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Item not found"})
		return
	}

	go incrementViewCount(item)

	c.JSON(http.StatusOK, item)
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
	item := Item{ID: id, Name: newItem.Name}
	items = append(items, item)

	c.JSON(http.StatusOK, item)
}

func incrementViewCount(item *Item) {
	mu.Lock()
	defer mu.Unlock()
	item.ViewCount++
}

func getPopularItem(c *gin.Context) {
	mu.Lock()
	defer mu.Unlock()

	if len(items) == 0 {
		c.JSON(http.StatusNotFound, gin.H{"error": "No items available"})
		return
	}

	var popularItem *Item
	for i := range items {
		if popularItem == nil || items[i].ViewCount > popularItem.ViewCount {
			popularItem = &items[i]
		}
	}

	c.JSON(http.StatusOK, popularItem)
}
