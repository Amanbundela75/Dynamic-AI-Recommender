import os
import google.generativeai as genai
from serpapi import GoogleSearch
from dotenv import load_dotenv
import json

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")

llm = genai.GenerativeModel('gemini-1.5-flash-latest')

def get_image_url(query: str) -> str:
    """SerpApi का उपयोग करके इमेज URL खोजता है।"""
    params = {
        "engine": "google_images",
        "q": query,
        "api_key": SERPAPI_KEY,
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    # पहला इमेज रिजल्ट का थंबनेल लौटाएं
    if "images_results" in results and results["images_results"]:
        return results["images_results"][0].get("thumbnail", "https://i.imgur.com/gLoOC5h.png")
    # अगर इमेज न मिले तो एक प्लेसहोल्डर इमेज दें
    return "https://i.imgur.com/gLoOC5h.png"

def get_dynamic_recommendation(user_prompt: str) -> list:
    """AI एजेंट जो JSON फॉर्मेट में रिकमेंडेशन और इमेज URL देता है।"""
    print("--- 1. यूज़र प्रॉम्प्ट को समझना... ---")
    deconstruction_prompt = f"""
    Analyze the user's request and break it down into a JSON object with two keys: 'search_query' and 'ranking_criteria'.
    'search_query' should be a concise string for a Google search. 'ranking_criteria' should be a clear instruction on how to judge the results.
    User Request: "{user_prompt}"
    JSON Output:
    """
    try:
        response = llm.generate_content(deconstruction_prompt)
        analysis_json = json.loads(response.text.strip().replace("```json", "").replace("```", ""))
        search_query = analysis_json.get('search_query')
    except Exception:
        return [{"title": "Request Error", "description": "I had trouble understanding your request.", "image_url": "https://i.imgur.com/gLoOC5h.png"}]

    print(f"खोजने के लिए क्वेरी: '{search_query}'")

    print("\n--- 2. वेब पर जानकारी खोजना... ---")
    # ... (सर्च लॉजिक) ...
    search_params = {"api_key": SERPAPI_KEY, "q": search_query, "engine": "google"}
    search = GoogleSearch(search_params)
    results = search.get_dict()
    search_context = ""
    if 'organic_results' in results:
        for result in results['organic_results'][:5]:
            search_context += f"Title: {result.get('title')}\nSnippet: {result.get('snippet')}\n---\n"
    
    print("\n--- 3. जानकारी को मिलाकर जवाब बनाना... ---")
    synthesis_prompt = f"""
    You are an expert recommendation AI. Your task is to generate recommendations based on the user's request and provided search results.
    Original User Request: "{user_prompt}"
    Web Search Results:
    {search_context}
    Based *only* on the provided search results, generate a JSON array of the top 4-5 recommendations.
    Each JSON object must have three keys: "title", "description", and "image_search_query".
    Your entire output must be a valid JSON array.
    """
    try:
        final_response = llm.generate_content(synthesis_prompt)
        recommendations = json.loads(final_response.text.strip().replace("```json", "").replace("```", ""))
    except Exception as e:
        return [{"title": "Analysis Error", "description": "I found information but couldn't create a list.", "image_url": "https://i.imgur.com/gLoOC5h.png"}]

    print("\n--- 4. हर आइटम के लिए इमेज खोजना... ---")
    for item in recommendations:
        print(f"'{item['title']}' के लिए इमेज खोजी जा रही है...")
        item['image_url'] = get_image_url(item['image_search_query'])
        
    return recommendations