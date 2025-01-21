package reddit

import "encoding/json"

// RedditData struct that contains the data from a single reddit post
type RedditData struct {
	Post_id      string   `json:"post_id"`
	Ups          int      `json:"ups"`
	Created_utc  float64  `json:"created_utc"`
	Upvote_ratio float64  `json:"upvote_ratio"`
	Comments     []string `json:"comments"`
	Source       string   `json:"source"`
	Subreddit    string   `json:"subreddit"`
	Selftext     string   `json:"selftext"`
	Title        string   `json:"title"`
}

// converts the raw data from the kafka record to a slice of RedditData
func ConvertToRedditData(data []byte) ([]RedditData, error) {
	var redditData []RedditData
	err := json.Unmarshal(data, &redditData)
	if err != nil {
		return nil, err
	}
	return redditData, nil
}
