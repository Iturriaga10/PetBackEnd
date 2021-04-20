package main

import (
	// "fmt"
	"log"
	"context"
	"time"
	"github.com/gofiber/fiber/v2"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

type ErrorMessage struct {
	Message string
}

type Post struct {
    Name string `json:"name" xml:"name" form:"name"`
    Image string `json:"image" xml:"image" form:"image"`
	Description string `json:"description" xml:"description" form:"description"`
	Video string `json:"video" xml:"video" form:"video"`
	
	Media struct {
		Image string `json:"image" xml:"image" form:"image"`
		Video string `json:"video" xml:"video" form:"video"`
	}
}

func main() {
  	app := fiber.New()

	// Connection to MongoDB Server.
	client, err := mongo.NewClient(options.Client().ApplyURI("mongodb+srv://dogstagram:tec2021@iturriagacluster.t6mpd.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-lashdc-shard-0&w=majority&readPreference=primary&retryWrites=true&ssl=true"))
	if err != nil {
		log.Fatal(err)
	}

	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
	err = client.Connect(ctx)
	if err != nil {
		log.Fatal(err)
	}
	defer client.Disconnect(ctx)
	
	myFirstDatabase := client.Database("myFirstDatabase")
	feedCollection := myFirstDatabase.Collection("feed")

	
  	app.Get("/feed", func(c *fiber.Ctx) error {
		
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
  })

  	app.Post("/feed", func(c *fiber.Ctx) error {
		c.Accepts("application/json") // "application/json"
		
		// Parsing Data.
		p := new(Post)
        if err := c.BodyParser(p); err != nil {
            return c.JSON(ErrorMessage{ Message: "name, image, description and date field must be a string."})
        }

		ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
		cursor, err := feedCollection.InsertOne(ctx, bson.D{
			{"name", p.Name}, 
			{"image", p.Image}, 
			{"description", p.Description },
			{"like", false},
			{"likeCounter", 0},
			{"date", time.Now()},
			{"media", bson.D{
				{"image", p.Media.Image}, 
				{"video", p.Media.Video },
			}},
		})
		if err != nil {
			log.Fatal(err)
		}

		log.Println(cursor)

	return c.JSON(ErrorMessage{ Message: "OK"})
	//return c.JSON(episodes)
	})

	app.Delete("/feed/:id", func(c *fiber.Ctx) error {
		// Convert id string to ObjectId
		objectId, err := primitive.ObjectIDFromHex(c.Params("id"))
		if err != nil{
    		return c.JSON(ErrorMessage{ Message: c.Params("id") + " format incorrect."})
		}
		
		// Retrive data from DataBase.
		ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
		cursor, err := feedCollection.Find(ctx, bson.M{ "_id": objectId })
		if err != nil {
		    log.Println(err)
			return fiber.ErrServiceUnavailable
		}

		var feed []bson.M
		if err = cursor.All(ctx, &feed); err != nil {
			log.Println(err)
			return fiber.ErrServiceUnavailable
		}

		// Find if the Id exists.
		if len(feed) == 0 {
			return c.JSON(ErrorMessage{ Message: c.Params("id") + " doesn''t exists."})
		}

		feedCollection.DeleteOne(ctx, bson.M{ "_id": objectId })

		return c.JSON(ErrorMessage{ Message: c.Params("id") + " deleted succesfully."})
	})

	app.Get("/feed/:id", func(c *fiber.Ctx) error {

		// Convert id string to ObjectId
		objectId, err := primitive.ObjectIDFromHex(c.Params("id"))
		if err != nil{
    		return c.JSON(ErrorMessage{ Message: c.Params("id") + " doesn''t exists."})
		}

		// Retrive data from DataBase.
		ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
		cursor, err := feedCollection.Find(ctx, bson.M{ "_id": objectId })
		if err != nil {
		    log.Println(err)
			return fiber.ErrServiceUnavailable
		}
		
		var feed []bson.M
		if err = cursor.All(ctx, &feed); err != nil {
			log.Println(err)
			return fiber.ErrServiceUnavailable
		}
	
    	return c.JSON(feed)
		
		// return c.SendString("value: " + c.Params("value"))
  	})
 
	app.Put("/feed/like/increase/:id", func(c *fiber.Ctx) error {
	
	// Convert id string to ObjectId
	objectId, err := primitive.ObjectIDFromHex(c.Params("id"))
	if err != nil{
		return c.JSON(ErrorMessage{ Message: c.Params("id") + " format incorrect."})
	}
		
	// Retrive data from DataBase.
	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
	cursor, err := feedCollection.Find(ctx, bson.M{ "_id": objectId })
	if err != nil {
	    log.Println(err)
		return fiber.ErrServiceUnavailable
	}

	var feed []bson.M
	if err = cursor.All(ctx, &feed); err != nil {
		log.Println(err)
		return fiber.ErrServiceUnavailable
	}

	// Find if the Id exists.
	if len(feed) == 0 {
		return c.JSON(ErrorMessage{ Message: c.Params("id") + " doesn''t exists."})
	}

	feedCollection.UpdateOne(ctx, bson.M{ "_id": objectId },  bson.D{
		{"$inc", bson.D{{"likeCounter", 1 }}},}, options.Update().SetUpsert(true))

	return c.JSON(ErrorMessage{ Message: c.Params("id") + " likeCounter updated Successfully."})
	})

	app.Put("/feed/like/decrease/:id", func(c *fiber.Ctx) error {
	
		// Convert id string to ObjectId
		objectId, err := primitive.ObjectIDFromHex(c.Params("id"))
		if err != nil{
			return c.JSON(ErrorMessage{ Message: c.Params("id") + " format incorrect."})
		}
			
		// Retrive data from DataBase.
		ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
		cursor, err := feedCollection.Find(ctx, bson.M{ "_id": objectId })
		if err != nil {
			log.Println(err)
			return fiber.ErrServiceUnavailable
		}
	
		var feed []bson.M
		if err = cursor.All(ctx, &feed); err != nil {
			log.Println(err)
			return fiber.ErrServiceUnavailable
		}
	
		// Find if the Id exists.
		if len(feed) == 0 {
			return c.JSON(ErrorMessage{ Message: c.Params("id") + " doesn''t exists."})
		}

		if feed[0]["likeCounter"].(int32) == 0 {
			return c.JSON(ErrorMessage{ Message: c.Params("id") + " likeCounter can''t be lower than 0."})
		}	
		
		feedCollection.UpdateOne(ctx, bson.M{ "_id": objectId },  bson.D{
			{"$inc", bson.D{{"likeCounter", -1 }}},}, options.Update().SetUpsert(true))
	
		return c.JSON(ErrorMessage{ Message: c.Params("id") + " likeCounter updated Successfully."})
	})

	app.Patch("/feed/description/:id", func(c *fiber.Ctx) error {
	
		c.Accepts("application/json") // "application/json"
		
		// Parsing Data.
		p := new(Post)
        if err := c.BodyParser(p); err != nil {
            return c.JSON(ErrorMessage{ Message: "description field must be a string."})
        }

		// Convert id string to ObjectId
		objectId, err := primitive.ObjectIDFromHex(c.Params("id"))
		if err != nil{
			return c.JSON(ErrorMessage{ Message: c.Params("id") + " format incorrect."})
		}
			
		// Retrive data from DataBase.
		ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
		cursor, err := feedCollection.Find(ctx, bson.M{ "_id": objectId })
		if err != nil {
			log.Println(err)
			return fiber.ErrServiceUnavailable
		}
	
		var feed []bson.M
		if err = cursor.All(ctx, &feed); err != nil {
			log.Println(err)
			return fiber.ErrServiceUnavailable
		}
	
		// Find if the Id exists.
		if len(feed) == 0 {
			return c.JSON(ErrorMessage{ Message: c.Params("id") + " doesn''t exists."})
		}
		
		feedCollection.UpdateOne(ctx, bson.M{ "_id": objectId },  bson.D{
			{"$set", bson.D{{"description", p.Description }}},}, options.Update().SetUpsert(true))
	
		return c.JSON(ErrorMessage{ Message: c.Params("id") + " description updated Successfully."})
	})

	app.Patch("/feed/image/:id", func(c *fiber.Ctx) error {

		c.Accepts("application/json") // "application/json"
		
		// Parsing Data.
		p := new(Post)
		if err := c.BodyParser(p); err != nil {
			return c.JSON(ErrorMessage{ Message: "description field must be a string."})
		}

		// Convert id string to ObjectId
		objectId, err := primitive.ObjectIDFromHex(c.Params("id"))
		if err != nil{
			return c.JSON(ErrorMessage{ Message: c.Params("id") + " format incorrect."})
		}
			
		// Retrive data from DataBase.
		ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
		cursor, err := feedCollection.Find(ctx, bson.M{ "_id": objectId })
		if err != nil {
			log.Println(err)
			return fiber.ErrServiceUnavailable
		}
	
		var feed []bson.M
		if err = cursor.All(ctx, &feed); err != nil {
			log.Println(err)
			return fiber.ErrServiceUnavailable
		}
	
		// Find if the Id exists.
		if len(feed) == 0 {
			return c.JSON(ErrorMessage{ Message: c.Params("id") + " doesn''t exists."})
		}
		
		feedCollection.UpdateOne(ctx, bson.M{ "_id": objectId },  bson.D{
			{"$set", bson.D{{"media", bson.D{
				{"image", p.Image}, 
				{"video", "" },
			}}}},}, options.Update().SetUpsert(true))
	
		return c.JSON(ErrorMessage{ Message: c.Params("id") + " image updated Successfully."})
	})

	app.Patch("/feed/video/:id", func(c *fiber.Ctx) error {

		c.Accepts("application/json") // "application/json"
		
		// Parsing Data.
		p := new(Post)
		if err := c.BodyParser(p); err != nil {
			return c.JSON(ErrorMessage{ Message: "description field must be a string."})
		}

		// Convert id string to ObjectId
		objectId, err := primitive.ObjectIDFromHex(c.Params("id"))
		if err != nil{
			return c.JSON(ErrorMessage{ Message: c.Params("id") + " format incorrect."})
		}
			
		// Retrive data from DataBase.
		ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
		cursor, err := feedCollection.Find(ctx, bson.M{ "_id": objectId })
		if err != nil {
			log.Println(err)
			return fiber.ErrServiceUnavailable
		}
	
		var feed []bson.M
		if err = cursor.All(ctx, &feed); err != nil {
			log.Println(err)
			return fiber.ErrServiceUnavailable
		}
	
		// Find if the Id exists.
		if len(feed) == 0 {
			return c.JSON(ErrorMessage{ Message: c.Params("id") + " doesn''t exists."})
		}
		
		feedCollection.UpdateOne(ctx, bson.M{ "_id": objectId },  bson.D{
			{"$set", bson.D{{"media", bson.D{
				{"image", ""}, 
				{"video", p.Video },
			}}}},}, options.Update().SetUpsert(true))
	
		return c.JSON(ErrorMessage{ Message: c.Params("id") + " video updated Successfully."})
	})

	app.Listen(":3000")
}

