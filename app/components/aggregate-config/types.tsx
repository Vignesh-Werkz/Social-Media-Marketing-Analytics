export interface ModelData {
    model_name: string;
    model_weight: number;
    title_sentiment: number;
    selftext_sentiment: number;
    comments_sentiment: number;
}

export interface AggregateData {
    aggregateName: string;
    description: string;
    weights: Array<ModelData>;
}
