//Import express module

const express = require('express');
const app = express();

//Import Swagger

const swaggerUi = require('swagger-ui-express'),
    swaggerDocument = require('./swagger.json');

app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

//Get values form the database to the server  GET

app.get('/feed', function (req, res) {
    main().then(data => res.json(data));
});

//Get value form the database to the server using Id GET

app.get('/feed/:_id', function (req, res) {
    mainId(req.params._id).then(data => res.json(data));
});

//Post new body from Postman, POST

app.use(
    express.urlencoded({
        extended: true
    })
)

app.use(express.json())

app.post('/feed', (req, res) => {
    if (req.body.name == undefined || req.body.description == undefined ||
        req.body.image == undefined) {
        console.log('Unable to receive document, lacks information')
        res.send('Not Received')
    }
    else if (typeof req.body.name != "string" || typeof req.body.description != "string" ||
        typeof req.body.image != "string") {
        console.log('Unable to receive document, wrong type of value')
        res.send('Not Received, wrong type of value')
    }

    else {
        mainAdd(req.body);
        res.send('Received');
    }
})

//Delete an object by ID, DELETE

app.delete('/feed/:_id', function (req, res) {
    mainDelete(req.params._id);
    res.send('Succesfully deleted the id: ' + req.params._id);
});

//Increase likes, PUT

app.put('/feed/like/increase/:_id', function (req, res) {
    mainIncrease(req.params._id);
    res.send('Succesfully updated the id:' + req.params._id);
});

//Decrease Likes, PUT

app.put('/feed/like/decrease/:_id', function (req, res) {
    mainDecrease(req.params._id)
    res.send('Succesfully updated the id:' + req.params._id);

});

//Update description object in document, PATCH

app.patch('/feed/description/:_id', function (req, res) {
    if (req.body.description == undefined || typeof req.body.description != "string") {
        console.log('Unable to update, description is empty or wrong type')
        res.send('Description empty or wrong type, unable to update')
    }

    else {
        mainUpdateD(req.params._id, req.body.description);
        res.send('Succesfully updated the id:' + req.params._id);
    }
});

//Update image object in document , PATCH

app.patch('/feed/image/:_id', function (req, res) {
    if (req.body.image == undefined || typeof req.body.image != "string") {
        console.log('Unable to update, image is empty or wrong type')
        res.send('Image empty or wrong type, unable to update')
    }

    else {
        mainUpdateI(req.params._id, req.body.image);
        res.send('Succesfully updated the id:' + req.params._id);
    }
});


//Put server Up in a Port of the local host

app.listen(3000, () => {
    console.log(`El servidor se está ejecutando en 3000`);
});

//Connect to MongoDB
//Import Mongo Module

const { MongoClient } = require('mongodb');

//Main function to search all documents

async function main() {

    //Connection URI
    const uri = "mongodb+srv://dogstagram:tec2021@iturriagacluster.t6mpd.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-lashdc-shard-0&w=majority&readPreference=primary&retryWrites=true&ssl=true"

    const client = new MongoClient(uri);

    //Storaga variables
    var cursor = [];

    var docs = [];

    //Database Search
    try {

        await client.connect();

        //Search Documents in a database collection
        const database = client.db();
        const data = database.collection("feed");

        cursor = await data.find({});

        //Assign finded data to a variable
        cursor.stream().on("data", doc => docs.push(doc));

        // print a message if no documents were found
        if ((await cursor.count()) === 0) {
            console.log("No documents found!");
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
    return docs;
}

//Main function for search document by ID

async function mainId(id) {

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

// Main function to add new document to the data base

async function mainAdd(body) {

    //Connection URI
    const uri = "mongodb+srv://dogstagram:tec2021@iturriagacluster.t6mpd.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-lashdc-shard-0&w=majority&readPreference=primary&retryWrites=true&ssl=true"

    const client = new MongoClient(uri);

    //Storage variables
    var update = [];

    //Database Search and Update
    try {

        await client.connect();

        //Search Documents in a database collection
        const database = client.db();
        const data = database.collection("feed");

        //Insert body and new properties

        body["like"] = false;
        body["likeCounter"] = 0;
        body["date"] = new Date();

        update = await data.insertOne(body);

        console.log(
            `${update.insertedCount} documents were inserted with the _id: ${update.insertedId}`,
        );

        // print a message if no documents were added
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

//Main function for delete document by ID

async function mainDelete(id) {

    //Connection URI
    const uri = "mongodb+srv://dogstagram:tec2021@iturriagacluster.t6mpd.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-lashdc-shard-0&w=majority&readPreference=primary&retryWrites=true&ssl=true"

    const client = new MongoClient(uri);

    //Storage variables
    var done = [];

    //Database Search
    try {

        await client.connect();

        //Search Documents in a database collection
        const database = client.db();
        const data = database.collection("feed");

        //Search an especific Document by his Id and delete

        var mongo = require('mongodb');

        var o_id = new mongo.ObjectID(id);

        done = await data.deleteOne({ '_id': o_id });

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

//Main function to increase a parameter

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

//Main function to decrease a parameter

async function mainDecrease(id) {

    //Connection URI
    const uri = "mongodb+srv://dogstagram:tec2021@iturriagacluster.t6mpd.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-lashdc-shard-0&w=majority&readPreference=primary&retryWrites=true&ssl=true"

    const client = new MongoClient(uri);

    //Storage variables
    var decrease = [];

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
                likeCounter: -1,
            }
        }

        var fieldName = "likeCounter";

        var distinct = await data.distinct(fieldName, { '_id': o_id })

        if (distinct <= 0) {
            console.log("Unable to update the value")
        }
        else {
            decrease = await data.updateOne({ '_id': o_id }, update);
        }
        // print a message if no documents were found or if was a success
        if (decrease.modifiedCount === 1) {
            console.log(`${decrease.matchedCount} document(s) matched the filter, updated ${decrease.modifiedCount} document(s)`,
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
    return decrease;
}

//Main function to update description object

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

//Main function to update image object

async function mainUpdateI(id, body) {

    //Connection URI
    const uri = "mongodb+srv://dogstagram:tec2021@iturriagacluster.t6mpd.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-lashdc-shard-0&w=majority&readPreference=primary&retryWrites=true&ssl=true"

    const client = new MongoClient(uri);

    //Storage variables
    var updateI = [];

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
                image: body,
            }
        }

        updateI = await data.updateOne({ '_id': o_id }, update);

        // print a message if no documents were found or if was a success
        if (updateI.modifiedCount === 1) {
            console.log(`${updateI.matchedCount} document(s) matched the filter, updated ${updateI.modifiedCount} document(s)`,
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
    return updateI;
}