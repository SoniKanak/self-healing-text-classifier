from text_classifier import SelfHealingTextClassifier

def main():
    # Create classifier
    classifier = SelfHealingTextClassifier()
    
    # Example texts
    texts = [
        "I absolutely loved this movie! The acting was fantastic.",
        "This was a terrible movie. I regret watching it.",
        "The movie was okay. It had some good moments.",
        "I didn't really like it but it wasn't terrible either."
    ]
    
    for text in texts:
        print(f"\nAnalyzing: {text}")
        prediction, confidence, used_fallback = classifier.classify_with_fallback(text)
        
        print(f"Prediction: {prediction}")
        print(f"Confidence: {confidence:.2f}")
        print(f"Used fallback: {used_fallback}")

if __name__ == "__main__":
    main()
