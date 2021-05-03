const express = require('express')
const app = express()

app.use(
    express.urlencoded({
        extended: true
    })
)

app.use(express.json())

app.post('/add', (req, res) => {
    mainAdd(req.body);
    res.send('Received');
})

app.listen(3000, () => {
    console.log(`El servidor se está ejecutando en 3000`);
});

const { MongoClient } = require('mongodb');

async function mainAdd(body) {

    //Connection URI
    const uri = "mongodb+srv://dogstagram:tec2021@iturriagacluster.t6mpd.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-lashdc-shard-0&w=majority&readPreference=primary&retryWrites=true&ssl=true"

    const client = new MongoClient(uri);

    //Storage variables
    var update = [];

    //Database Search
    try {

        await client.connect();

        //SEarch Documents in a database collection
        const database = client.db();
        const data = database.collection("feed");

        //Insert body

        body["like"] = false;
        body["likeCounter"] = 0;
        body["date"] = new Date();

        update = await data.insertOne(body);

        console.log(
            `${update.insertedCount} documents were inserted with the _id: ${update.insertedId}`,
        );

        // print a message if no documents were found
        if (update === null) {
            console.log("No document added!");
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
    return update;
}

