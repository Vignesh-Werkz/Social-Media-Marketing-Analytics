package db

import (
	"context"

	"github.com/nus-cs3203/24s1-open-project-team03/src/dataloader/reddit"
)

type DbDriver interface {
	Disconnect(ctx context.Context) error
	InsertJSONObjects(ctx context.Context, rawData []interface{}, collection string) (int64, error)
	InsertRedditData(ctx context.Context, redditData []reddit.RedditData, collection string) (int64, error)
}
