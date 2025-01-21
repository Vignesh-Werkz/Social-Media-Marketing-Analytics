package kafka

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/twmb/franz-go/pkg/kgo"
)

func die(msg string, args ...any) {
	fmt.Fprintf(os.Stderr, msg, args...)
	os.Exit(1)
}

// KafkaWrapper is a struct that handles the kafka connection.
// Messages are output via the InputCh channel.
// Sigs is used to listen for interrupt signals.
type KafkaWrapper struct {
	topic       string
	group       string
	seedBrokers []string
	cl          *kgo.Client

	InputCh chan *kgo.Record
	Sigs    chan os.Signal
}

// NewKafkaWrapper returns a new KafkaWrapper with the given parameters.
func NewKafkaWrapper(topic string, group string, seedBrokers []string) *KafkaWrapper {
	return &KafkaWrapper{
		topic:       topic,
		group:       group,
		seedBrokers: seedBrokers,
		InputCh:     make(chan *kgo.Record, 10),
		Sigs:        make(chan os.Signal, 2),
	}
}

// InitKafkaClient initializes the kafka client using configs from the KafkaWrapper.
func (kw *KafkaWrapper) InitKafkaClient() error {
	opts := []kgo.Opt{
		kgo.SeedBrokers(kw.seedBrokers...),
		kgo.ConsumerGroup(kw.group),
		kgo.ConsumeTopics(kw.topic),
	}

	cl, err := kgo.NewClient(opts...)
	if err != nil {
		return err
	}
	kw.cl = cl
	return nil
}

// Run starts the kafka client and consumes messages.
// It listens for interrupt signals and closes the client when received.
func (kw *KafkaWrapper) Run() {
	go kw.consume()

	<-kw.Sigs
	log.Println("received interrupt signal; closing client")

	done := make(chan struct{})
	go func() {
		defer close(done)
		kw.cl.Close()
	}()

	select {
	case <-kw.Sigs:
		fmt.Println("received second interrupt signal; quitting without waiting for graceful close")
	case <-done:
	}
}

// consume listens for messages on the kafka client and sends them to the InputCh channel.
func (kw *KafkaWrapper) consume() {
	fmt.Println("starting to listen to kafka")
	for {
		fetches := kw.cl.PollFetches(context.Background())
		log.Println("polled fetches")
		if fetches.IsClientClosed() {
			return
		}
		fetches.EachError(func(t string, p int32, err error) {
			die("fetch err topic %s partition %d: %v", t, p, err)
		})

		fetches.EachRecord(func(record *kgo.Record) {
			log.Printf("processing offset %d\n", record.Offset)
			kw.InputCh <- record
		})
	}
}
