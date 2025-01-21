from typing import Dict, List


class WeightedAggregator:
    def aggregate(self, normalized_post: Dict, model_keys: List[str], weights: Dict[str, Dict[str, float]]) -> float:
        """
        Aggregates sentiment scores from multiple models based on specified weights.

        Models with zero weights are ignored, and calculations adjust for empty dates or components.

        :param normalized_post: The post with normalized sentiment scores.
        :param model_keys: The list of model keys to be processed.
        :param weights: A dictionary with weights for each model's components and overall model weights.
                        Example:
                        {
                            'vader': {'title_sentiment': 0.3, 'selftext_sentiment': 0.2, 'comments_sentiment': 0.5},
                            'textblob': {'title_sentiment': 0.4, 'selftext_sentiment': 0.4, 'comments_sentiment': 0.2},
                            'model_weights': {'vader': 0.4, 'textblob': 0.6}
                        }
        :return: The aggregated sentiment score for the post.
        """
        model_scores = {}
        total_model_weight = 0.0

        # Calculate the weighted average for each model's sentiment scores
        for model in model_keys:
            model_weight = weights['model_weights'].get(model, 0)

            # Skip models with zero weights to ensure they do not impact the final calculation
            if model_weight == 0 or model not in normalized_post['model_output']:
                continue

            normalized_scores = normalized_post['model_output'][model]
            component_weights = weights.get(model, {})
            weighted_score = 0.0
            total_component_weight = 0.0

            # Iterate over each component (e.g., title, selftext, comments) and its weight
            for component, weight in component_weights.items():
                if weight == 0:
                    continue  # Skip components with zero weight

                component_score = normalized_scores.get(component, 0)

                # Handle list of scores (e.g., comments sentiments)
                aggregated_component_score = 0.0
                if isinstance(component_score, list):
                    if len(component_score) > 0:
                        # Average the list of scores to get a single score for the component
                        aggregated_component_score = sum(
                            component_score) / len(component_score)
                else:
                    # Use the single score directly for other components like title or selftext
                    aggregated_component_score = component_score

                # Apply the component weight to the aggregated score
                weighted_score += aggregated_component_score * weight
                total_component_weight += weight

            # Normalize the model score by the sum of its component weights to avoid skewed results
            model_scores[model] = 0.0
            if total_component_weight > 0:
                model_scores[model] = weighted_score / total_component_weight

            total_model_weight += model_weight

        # Calculate the final aggregated score using the model weights
        final_score = 0.0  # Handle the case where all model weights are zero
        if total_model_weight > 0:
            final_score = sum(
                model_scores[model] * weights['model_weights'][model]
                for model in model_scores
            ) / total_model_weight

        return final_score