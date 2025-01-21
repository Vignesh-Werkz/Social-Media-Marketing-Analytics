package main

import (
	"context"
	"encoding/json"
	"log"
	"os"

	"github.com/nus-cs3203/24s1-open-project-team03/src/dataloader/db"
	"github.com/nus-cs3203/24s1-open-project-team03/src/dataloader/kafka"
	"github.com/nus-cs3203/24s1-open-project-team03/src/dataloader/reddit"
	"github.com/twmb/franz-go/pkg/kgo"
)

// DataLoader is a struct that handles the kafka connection and database connection.
type DataLoader struct {
	kw   *kafka.KafkaWrapper
	db   db.DbDriver
	Sigs chan os.Signal
}

// run is the main loop of the dataloader.
func (dl DataLoader) Run() {
	log.Println("starting dataloader runtime")
	for {
		select {
		case record := <-dl.kw.InputCh:
			numUploaded, err := dl.ProcessRedditRecord(record)
			if err != nil {
				log.Panic(err)
			}
			log.Printf("uploaded %d records at offset %d\n", numUploaded, record.Offset)

		case <-dl.Sigs:
			dl.CloseDataLoader()
			return
		}
	}
}

// ProcessRedditRecord processes a converts a reddit record to a slice of RedditData and upserts it into the database.
// Note that this is idempotent and will not insert duplicate objects based on post_id.
func (dl DataLoader) ProcessRedditRecord(record *kgo.Record) (numUploaded int64, err error) {
	redditData, err := reddit.ConvertToRedditData(record.Value)
	if err != nil {
		return 0, err
	}

	return dl.db.InsertRedditData(context.Background(), redditData, record.Topic)
}

// ProcessJSONRecord processes a converts a JSON record to a slice of interface{} and inserts it into the database.
// Note that this is not idempotent and can result in duplicate objects being inserted with different _id values.
func (dl DataLoader) ProcessJSONRecord(record *kgo.Record) (numUploaded int64, err error) {
	var unmarshalledJson []interface{}
	err = json.Unmarshal(record.Value, &unmarshalledJson)
	if err != nil {
		return 0, err
	}
	return dl.db.InsertJSONObjects(context.Background(), unmarshalledJson, record.Topic)
}

// CloseDataLoader closes the database connection.
// Kafka connection is automatically closed when receiving a ctrl+c signal independent of this function.
func (dl DataLoader) CloseDataLoader() error {
	log.Println("received interrupt signal; closing dataloader")
	done := make(chan struct{})

	go func() {
		if err := dl.db.Disconnect(context.TODO()); err != nil {
			panic(err)
		}
		log.Println("closed db succesfully")
		close(done)
	}()

	select {
	case <-dl.Sigs:
		log.Println("received second interrupt signal; quitting without waiting for graceful close")
	case <-done:
	}

	return nil
}
