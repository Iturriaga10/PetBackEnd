//Import express module

const express = require('express');
const app = express();

//Get values form the database to the server 
app.use(
    express.urlencoded({
        extended: true
    })
)

app.use(express.json())

app.patch('/updateDescription/:_id', function (req, res) {
    console.log(req.body)
    mainUpdateD(req.params._id, req.body.description);
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

async function mainUpdateD(id, body) {

    //Connection URI
    const uri = "mongodb+srv://dogstagram:tec2021@iturriagacluster.t6mpd.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-lashdc-shard-0&w=majority&readPreference=primary&retryWrites=true&ssl=true"

    const client = new MongoClient(uri);

    //Storage variables
    var updateD = [];

    //Database Search
    try {

        await client.connect();

        //SEarch Documents in a database collection
        const database = client.db();
        const data = database.collection("feed");

        //Search an especific Document by his Id

        var mongo = require('mongodb');
        var o_id = new mongo.ObjectID(id);

        console.log(body)

        var update = {
            $set: {
                description: body,
            }
        }

        updateD = await data.updateOne({ '_id': o_id }, update);

        // print a message if no documents were found or if was a success
        if (updateD.modifiedCount === 1) {
            console.log(`${updateD.matchedCount} document(s) matched the filter, updated ${updateD.modifiedCount} document(s)`,
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
    return updateD;
}