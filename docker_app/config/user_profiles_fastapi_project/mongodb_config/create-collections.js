db = db.getSiblingDB('ugc');

db.createCollection(
    "user_profiles",
    {
        clusteredIndex: {
            "key": { _id: 1 },
            "unique": true,
            "name": "stocks clustered key"
        },
        validator: {
            $jsonSchema: {
                bsonType: "object",
                required: ["user_id", "purchased_films"],
                properties: {
                    user_id: {
                        bsonType: "string",
                        description: "must be a string and is required"
                    },
                    purchased_films: {
                        bsonType: [ "array" ],
                        items: {
                            bsonType: "object",
                            required:["film_id"],
                            properties:{
                                film_id:{
                                    bsonType: "string",
                                    description: "must be a string and is required"
                                }
                            }
                        },
                        description: "must be a array of objects containing film_ids"
                    }
                }
            }
        }
    },
);