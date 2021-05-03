//Import express module

const express = require('express');
const app = express();

//Get values form the database to the server 

app.get('/delete/:_id', function (req, res) {
    mainDelete(req.params._id);
    res.send('Succesfully deleted the id:' + req.params._id);
});

//Put server Up in a Port of the local host

app.listen(3000, () => {
    console.log(`El servidor se está ejecutando`);
});

//Connect to MongoDB
//Import Mongo Module
const { MongoClient } = require('mongodb');

//Main function

async function mainDelete(id) {

    //Connection URI
    const uri = "mongodb+srv://dogstagram:tec2021@iturriagacluster.t6mpd.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-lashdc-shard-0&w=majority&readPreference=primary&retryWrites=true&ssl=true"

    const client = new MongoClient(uri);

    //Storage variables
    var done = [];

    //Database Search
    try {

        await client.connect();

        //SEarch Documents in a database collection
        const database = client.db();
        const data = database.collection("feed");

        //Search an especific Document by his Id

        var mongo = require('mongodb');

        var o_id = new mongo.ObjectID(id);

        done = await data.deleteOne({ '_id': o_id });

        // cursor.stream().on("data", doc => docs.push(doc));

        // print a message if no documents were found or if was a success
        if (done.deletedCount === 1) {
            console.dir("Successfully deleted one document.");
        } else {
            console.log("No documents matched the query. Deleted 0 documents.");
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
    return done;
}