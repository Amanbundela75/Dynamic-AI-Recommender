# modules/movie_module.py

import requests
import re

# अपनी TMDB API KEY यहाँ डालें
API_KEY = "c7ec19ffdd3279641fb606d19ceb9bb1" 

def get_movie_recommendations(prompt):
    """
    TMDB API का उपयोग करके मूवी रिकमेंडेशन्स देता है।
    यह प्रॉम्प्ट से मूवी का नाम निकालने की कोशिश करता है।
    """
    if not API_KEY or API_KEY == "YOUR_TMDB_API_KEY_HERE":
        return ["Error: Please add your TMDB API key to movie_module.py"]

    # प्रॉम्प्ट से मूवी का नाम निकालने का सरल तरीका
    # "movies like Inception" -> "Inception"
    match = re.search(r'(?:like|about|recommend)\s+([\w\s]+)', prompt.lower())
    if not match:
        return ["Sorry, I couldn't figure out which movie you're asking about. Try 'movies like Inception'."]
        
    movie_title = match.group(1).strip()

    # 1. मूवी के नाम से उसकी ID खोजना
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
    response = requests.get(search_url).json()
    
    if not response['results']:
        return [f"Sorry, couldn't find any movie named '{movie_title}'."]
        
    movie_id = response['results'][0]['id']
    
    # 2. उस ID से रिकमेंडेशन्स पाना
    reco_url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={API_KEY}"
    reco_response = requests.get(reco_url).json()
    
    if not reco_response['results']:
        return [f"Found the movie '{movie_title}', but couldn't find recommendations for it."]
        
    # टॉप 5 रिकमेंडेशन्स के नाम निकालना
    recommendations = [movie['title'] for movie in reco_response['results'][:5]]
    return recommendations