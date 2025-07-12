# modules/product_module.py

def get_product_recommendations(prompt):
    """
    यह एक डमी फंक्शन है जो प्रोडक्ट्स रिकमेंड करने का नाटक करता है।
    असली सिस्टम में यहाँ वेब स्क्रैपिंग और रैंकिंग का कोड होगा।
    """
    print("DEBUG: Product module activated.")
    prompt = prompt.lower()
    
    # प्रॉम्प्ट के आधार पर डमी डेटा लौटाना
    if "laptop" in prompt:
        return [
            "Dell XPS 15 (High-end)",
            "HP Spectre x360 (2-in-1)",
            "Lenovo IdeaPad Gaming 3 (Budget Gaming)",
            "Apple MacBook Air M3 (Ultra-portable)",
            "ASUS ROG Zephyrus G14 (Powerful Gaming)"
        ]
    elif "phone" in prompt:
        return [
            "Samsung Galaxy S25 Ultra",
            "iPhone 16 Pro",
            "Google Pixel 9 Pro",
            "OnePlus 13",
            "Nothing Phone (3)"
        ]
    else:
        return ["Sorry, I can only recommend laptops or phones right now."]