package feed

import (
	"github.com/gofiber/fiber"
)

func GetBooks(c *fiber.Ctx) {
	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
	cursor, err := feedCollection.Find(ctx, bson.M{})
	if err != nil {
	    log.Fatal(err)
	}
	var episodes []bson.M
	if err = cursor.All(ctx, &episodes); err != nil {
	    log.Fatal(err)
	}
	//fmt.Println(episodes)
	
    return c.JSON(episodes)
}