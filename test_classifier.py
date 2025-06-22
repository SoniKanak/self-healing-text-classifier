from text_classifier import SelfHealingTextClassifier
import json

def classify_text(text: str) -> str:
    """
    Classify text and return the result in JSON format.
    
    Args:
        text: Input text to classify
        
    Returns:
        JSON string with prediction results
    """
    classifier = SelfHealingTextClassifier()
    result = classifier.classify_with_fallback(text)
    
    # Convert confidence to percentage
    result['confidence'] = round(result['confidence'], 1)
    
    return json.dumps(result, indent=2)

# Example usage
if __name__ == "__main__":
    test_texts = [
        "I absolutely loved this movie! The acting was fantastic.",
        "This was a terrible movie. I regret watching it.",
        "The movie was okay. It had some good moments.",
        "I didn't really like it but it wasn't terrible either."
    ]
    
    for text in test_texts:
        print(f"\nAnalyzing: {text}")
        print(classify_text(text))
