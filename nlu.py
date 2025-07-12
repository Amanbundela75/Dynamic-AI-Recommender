# nlu.py

def get_intent(prompt):
    """
    यूज़र के प्रॉम्प्ट को पढ़कर उसका इरादा (intent) बताता है।
    """
    prompt = prompt.lower()
    
    # कीवर्ड्स की लिस्ट
    movie_keywords = ['movie', 'film', 'cinema', 'actor', 'actress', 'director']
    product_keywords = ['laptop', 'phone', 'mobile', 'earphones', 'buy', 'product', 'gadget']
    
    # मूवी इंटेंट की जाँच
    if any(keyword in prompt for keyword in movie_keywords):
        return 'recommend_movie'
        
    # प्रोडक्ट इंटेंट की जाँच
    if any(keyword in prompt for keyword in product_keywords):
        return 'find_product'
        
    # अगर कुछ समझ न आए
    return 'unknown'