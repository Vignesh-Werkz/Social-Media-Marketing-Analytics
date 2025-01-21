package reddit

// includes tests for redditData.go

import (
	"encoding/json"
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestConvertToRedditData(t *testing.T) {
	redditPost1 := RedditData{
		Post_id:      "abc123",
		Ups:          100,
		Created_utc:  1646873200,
		Upvote_ratio: 0.5,
		Comments:     []string{"comment1", "comment2"},
		Source:       "reddit",
		Subreddit:    "test",
		Selftext:     "this is a test",
		Title:        "test post",
	}

	redditPost2 := RedditData{
		Post_id:      "def456",
		Ups:          200,
		Created_utc:  1646873200,
		Upvote_ratio: 0.5,
		Comments:     []string{"comment3", "comment4"},
		Source:       "reddit",
		Subreddit:    "test",
		Selftext:     "this is a test",
		Title:        "test post",
	}

	redditPost3 := RedditData{
		Post_id:      "ghi789",
		Ups:          300,
		Created_utc:  1646873200,
		Upvote_ratio: 0.5,
		Comments:     []string{"comment5", "comment6"},
		Source:       "reddit",
		Subreddit:    "test",
		Selftext:     "this is a test",
		Title:        "test post",
	}

	singlePost, _ := json.Marshal([]RedditData{redditPost1})
	fmt.Print(singlePost)
	multiplePosts, _ := json.Marshal([]RedditData{redditPost1, redditPost2, redditPost3})
	emptyArray, _ := json.Marshal([]RedditData{})

	testCases := []struct {
		name     string
		input    []byte
		expected []RedditData
	}{
		{
			name:     "single post",
			input:    singlePost,
			expected: []RedditData{redditPost1},
		},
		{
			name:     "multiple posts",
			input:    multiplePosts,
			expected: []RedditData{redditPost1, redditPost2, redditPost3},
		},
		{
			name:     "empty array",
			input:    emptyArray,
			expected: []RedditData{},
		},
	}

	for _, testCase := range testCases {
		t.Run(testCase.name, func(t *testing.T) {
			redditData, err := ConvertToRedditData(testCase.input)
			if err != nil {
				t.Error(err)
			}
			assert.Equal(t, testCase.expected, redditData)
		})
	}
}

func TestConvertToRedditDataError(t *testing.T) {
	testCases := []struct {
		name     string
		input    []byte
		expected error
	}{
		{
			name:  "missing field post_id",
			input: []byte(`{"ups": 100, "created_utc": 1646873200, "upvote_ratio": 0.5, "comments": ["comment1", "comment2"], "source": "reddit", "subreddit": "test", "selftext": "this is a test", "title": "test post"}`),
		},
		{
			name:  "unexpected field",
			input: []byte(`{"post_id": "abc123", "ups": 100, "created_utc": 1646873200, "upvote_ratio": 0.5, "comments": ["comment1", "comment2"], "source": "reddit", "subreddit": "test", "selftext": "this is a test", "title": "test post", "unexpected": "field"}`),
		},
		{
			name:  "invalid field type",
			input: []byte(`{"post_id": "abc123", "ups": "100", "created_utc": 1646873200, "upvote_ratio": 0.5, "comments": ["comment1", "comment2"], "source": "reddit", "subreddit": "test", "selftext": "this is a test", "title": "test post"}`),
		},
	}
	for _, testCase := range testCases {
		t.Run(testCase.name, func(t *testing.T) {
			_, err := ConvertToRedditData(testCase.input)
			if err == nil {
				t.Error("Expected error, got nil")
			}
		})
	}
}
