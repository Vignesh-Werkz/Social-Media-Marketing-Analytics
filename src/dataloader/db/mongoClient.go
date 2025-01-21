// Package db provides wrappers for handling database connections and operations.
package db

import (
	"context"

	"github.com/nus-cs3203/24s1-open-project-team03/src/dataloader/reddit"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

// MongoClient is a wrapper for the mongodb driver.
// It provides methods for inserting data into the database fulfilling dbdriver interface.
type MongoClient struct {
	Client       *mongo.Client
	databaseName string
}

// Creates a new dbdriver instance for mongodb with the given URI and database name.
func CreateMongoClient(uri string, databaseName string) (*MongoClient, error) {
	client, err := mongo.Connect(context.TODO(), options.Client().
		ApplyURI(uri))
	if err != nil {
		return nil, err
	}

	return &MongoClient{
		Client:       client,
		databaseName: databaseName,
	}, nil
}

// Disconnect closes the database connection.
func (mc *MongoClient) Disconnect(ctx context.Context) error {
	return mc.Client.Disconnect(ctx)
}

// InsertJSONObjects inserts the given JSON objects into the given collection. This does not overwrite similar objects.
// This is not idempotent and can result in duplicate objects being inserted with different _id values.
func (mc *MongoClient) InsertJSONObjects(ctx context.Context, rawData []interface{}, collection string) (int64, error) {
	result, err := mc.Client.Database(mc.databaseName).Collection(collection).InsertMany(ctx, rawData)
	if err != nil {
		return 0, err
	}
	return (int64(len(result.InsertedIDs))), nil
}

// InsertRedditData upserts the given RedditData into the given collection based on post_id field.
// Due to the nature of upsert, this is idempotent.
func (mc *MongoClient) InsertRedditData(ctx context.Context, redditData []reddit.RedditData, collection string) (int64, error) {
	var numInserted int64 = 0
	for _, data := range redditData {
		filter := bson.D{{Key: "post_id", Value: data.Post_id}}
		new_data := bson.D{
			{Key: "post_id", Value: data.Post_id},
			{Key: "ups", Value: data.Ups},
			{Key: "created_utc", Value: data.Created_utc},
			{Key: "upvote_ratio", Value: data.Upvote_ratio},
			{Key: "comments", Value: data.Comments},
			{Key: "source", Value: data.Source},
			{Key: "subreddit", Value: data.Subreddit},
			{Key: "selftext", Value: data.Selftext},
			{Key: "title", Value: data.Title},
		}
		opts := options.Update().SetUpsert(true)

		result, err := mc.Client.Database(mc.databaseName).Collection(collection).UpdateOne(
			ctx,
			filter,
			bson.D{
				{Key: "$set", Value: new_data},
			},
			opts,
		)
		if err != nil {
			return numInserted, err
		}
		numInserted += result.ModifiedCount
	}
	return numInserted, nil
}
