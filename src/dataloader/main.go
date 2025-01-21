package main

import (
	"log"
	"os"
	"os/signal"

	"github.com/nus-cs3203/24s1-open-project-team03/src/dataloader/db"
	"github.com/nus-cs3203/24s1-open-project-team03/src/dataloader/kafka"

	"github.com/joho/godotenv"
)

func main() {
	if os.Getenv("CONTAINERISED") == "" {
		log.Println("Running in non-containerised mode")

		if err := godotenv.Load("../../.env"); err != nil {
			log.Panicln("No .env file found")
		}
	} else {
		log.Println("Running in containerised mode")
	}

	// ==============================
	// Initialise database connection
	// ==============================
	uri := os.Getenv("MONGODB_URI")
	if uri == "" {
		log.Panicln("Set your 'MONGODB_URI' environment variable. " +
			"See: " +
			"www.mongodb.com/docs/drivers/go/current/usage-examples/#environment-variable")
	}

	databaseName := os.Getenv("DATABASE_NAME")
	if databaseName == "" {
		log.Panicln("Set your 'DATABASE_NAME' environment variable. ")
	}

	mongoClient, err := db.CreateMongoClient(uri, databaseName)
	if err != nil {
		panic(err)
	}
	log.Println("initiated db succesfully")

	// ===========================
	// Initialise Kafka connection
	// ===========================
	kafkaWrapper := kafka.NewKafkaWrapper(os.Getenv("REDDIT_TOPIC"), os.Getenv("DEFAULT_REDDIT_CONSUMER_GROUP"), []string{os.Getenv("KAFKA_BOOTSTRAP")})
	kafkaWrapper.InitKafkaClient()
	go kafkaWrapper.Run()

	dl := DataLoader{
		kw:   kafkaWrapper,
		db:   mongoClient,
		Sigs: make(chan os.Signal, 2),
	}

	// one ctrl+c will gracefully close
	// the second ctrl+c will force close
	signal.Notify(dl.Sigs, os.Interrupt)
	signal.Notify(dl.kw.Sigs, os.Interrupt)
	dl.Run()
}
