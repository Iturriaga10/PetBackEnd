//Import express module

const express = require('express');
const app = express();

//Get values form the database to the server 

app.get('/id/:_id', function (req, res) {
    main(req.params._id).then(data => res.json(data));
});

//Put server Up in a Port of the local host

app.listen(3000, () => {
    console.log(`El servidor se está ejecutando`);
});

//Connect to MongoDB
//Import Mongo Module
const { MongoClient } = require('mongodb');

//Main function

async function main(id) {

    //Connection URI
    const uri = "mongodb+srv://dogstagram:tec2021@iturriagacluster.t6mpd.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-lashdc-shard-0&w=majority&readPreference=primary&retryWrites=true&ssl=true"

    const client = new MongoClient(uri);

    //Storage variables
    var cursor = [];

    //Database Search
    try {

        await client.connect();

        //SEarch Documents in a database collection
        const database = client.db();
        const data = database.collection("feed");

        //Search an especific Document by his Id

        var mongo = require('mongodb');

        var o_id = new mongo.ObjectID(id);

        cursor = await data.findOne({ '_id': o_id });
        console.log(cursor);

        //Assign finded data to a variable
        // cursor.stream().on("data", doc => docs.push(doc));

        // print a message if no documents were found
        if (cursor === null) {
            console.log("No document found!");
        }

    }

    //Sends e in case of error
    catch (e) {
        console.error(e);
    }

    //Close connection
    finally {
        await client.close();
    }

    //Returns finded values
    return cursor;
}