package main

import (
	"context"
	"testing"

	"github.com/nus-cs3203/24s1-open-project-team03/src/dataloader/reddit"
	"github.com/stretchr/testify/mock"
	"github.com/twmb/franz-go/pkg/kgo"
)

type MockDBDriver struct {
	mock.Mock
}

func (m *MockDBDriver) InsertRedditData(ctx context.Context, redditData []reddit.RedditData, topic string) (int64, error) {
	args := m.Called(ctx, redditData, topic)
	return args.Get(0).(int64), args.Error(1)
}

func (m *MockDBDriver) InsertJSONObjects(ctx context.Context, jsonObjects []interface{}, topic string) (int64, error) {
	args := m.Called(ctx, jsonObjects, topic)
	return args.Get(0).(int64), args.Error(1)
}

func (m *MockDBDriver) Disconnect(ctx context.Context) error {
	args := m.Called(ctx)
	return args.Error(0)
}

func TestProcessRedditRecord(t *testing.T) {
	testCases := []struct {
		name     string
		input    []byte
		expected int64
	}{
		{
			name:     "single post",
			input:    []byte(`[{"post_id": "abc123", "ups": 100, "created_utc": 1646873200, "upvote_ratio": 0.5, "comments": ["comment1", "comment2"], "source": "reddit", "subreddit": "test", "selftext": "this is a test", "title": "test post"}]`),
			expected: 1,
		},
		{
			name:     "multiple posts",
			input:    []byte(`[{"post_id": "abc123", "ups": 100, "created_utc": 1646873200, "upvote_ratio": 0.5, "comments": ["comment1", "comment2"], "source": "reddit", "subreddit": "test", "selftext": "this is a test", "title": "test post"}, {"post_id": "def456", "ups": 200, "created_utc": 1646873200, "upvote_ratio": 0.5, "comments": ["comment3", "comment4"], "source": "reddit", "subreddit": "test", "selftext": "this is a test", "title": "test post"}, {"post_id": "ghi789", "ups": 300, "created_utc": 1646873200, "upvote_ratio": 0.5, "comments": ["comment5", "comment6"], "source": "reddit", "subreddit": "test", "selftext": "this is a test", "title": "test post"}]`),
			expected: 3,
		},
		{
			name:     "empty array",
			input:    []byte(`[]`),
			expected: 0,
		},
	}
	for _, testCase := range testCases {
		t.Run(testCase.name, func(t *testing.T) {
			mockDBdriver := &MockDBDriver{}
			dl := DataLoader{
				db: mockDBdriver,
			}
			mockDBdriver.On("InsertRedditData", mock.Anything, mock.Anything, mock.Anything).Return(testCase.expected, nil)
			numUploaded, err := dl.ProcessRedditRecord(&kgo.Record{Value: testCase.input})
			if err != nil {
				t.Error(err)
			}
			if numUploaded != testCase.expected {
				t.Errorf("Expected %d records to be uploaded, got %d", testCase.expected, numUploaded)
			}
		})
	}
}
