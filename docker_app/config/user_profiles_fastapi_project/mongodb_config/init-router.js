sh.addShard("mongors1/mongors1n1");
sh.addShard("mongors2/mongors2n1");

sh.enableSharding("profiles");

db = db.getSiblingDB('profiles');

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
                required: ["user_id"]
            }
        }
    },
);

sh.shardCollection("profiles.user_profiles", {"user_id": 1}, true);