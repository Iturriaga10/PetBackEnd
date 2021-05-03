//Import express module

const express = require('express');
const app = express();

//Get values form the database to the server 

app.patch('/increase/:_id', function (req, res) {
    mainIncrease(req.params._id);
    res.send('Succesfully updated the id:' + req.params._id);
});

//Put server Up in a Port of the local host

app.listen(3000, () => {
    console.log(`El servidor se está ejecutando`);
});

//Connect to MongoDB
//Import Mongo Module
const { MongoClient } = require('mongodb');

//Main function

async function mainIncrease(id) {

    //Connection URI
    const uri = "mongodb+srv://dogstagram:tec2021@iturriagacluster.t6mpd.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-lashdc-shard-0&w=majority&readPreference=primary&retryWrites=true&ssl=true"

    const client = new MongoClient(uri);

    //Storage variables
    var increase = [];

    //Database Search
    try {

        await client.connect();

        //SEarch Documents in a database collection
        const database = client.db();
        const data = database.collection("feed");

        //Search an especific Document by his Id

        var mongo = require('mongodb');
        var o_id = new mongo.ObjectID(id);

        var update = {
            $inc: {
                likeCounter: +1,
            }
        }

        increase = await data.updateOne({ '_id': o_id }, update);

        // print a message if no documents were found or if was a success
        if (increase.modifiedCount === 1) {
            console.log(`${increase.matchedCount} document(s) matched the filter, updated ${increase.modifiedCount} document(s)`,
            );
        } else {
            console.log("No documents matched the query. Updated 0 documents.");
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
    return increase;
}