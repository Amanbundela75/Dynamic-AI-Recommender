import os
import google.generativeai as genai
from serpapi import GoogleSearch
from dotenv import load_dotenv
import json

# .env फाइल से API Keys लोड करना
load_dotenv()

# API Clients को कॉन्फ़िगर करना
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")

# Gemini Pro मॉडल को इनिशियलाइज़ करना
llm = genai.GenerativeModel('gemini-1.5-flash-latest')

def get_dynamic_recommendation(user_prompt: str) -> str:
    """
    यह फंक्शन एक AI एजेंट की तरह काम करता है।
    """
    print("--- 1. यूज़र प्रॉम्प्ट को समझना... ---")

    # फेज 1: प्रॉम्प्ट को समझने के लिए LLM का उपयोग
    deconstruction_prompt = f"""
    Analyze the user's request and break it down into a JSON object with two keys: 'search_query' and 'ranking_criteria'.
    'search_query' should be a concise string for a Google search.
    'ranking_criteria' should be a clear instruction on how to judge the results.

    User Request: "{user_prompt}"

    JSON Output:
    """
    
    try:
        response = llm.generate_content(deconstruction_prompt)
        # LLM से मिले JSON को साफ करना
        analysis_json = json.loads(response.text.strip().replace("```json", "").replace("```", ""))
        search_query = analysis_json.get('search_query')
        ranking_criteria = analysis_json.get('ranking_criteria')
        print(f"खोजने के लिए क्वेरी: '{search_query}'")
        print(f"रैंकिंग का आधार: '{ranking_criteria}'")
    except Exception as e:
        print(f"Error in Phase 1: {e}")
        return "Sorry, I had trouble understanding your request. Please try rephrasing."

    # ---
    print("\n--- 2. वेब पर जानकारी खोजना... ---")

    # फेज 2: SerpApi से गूगल सर्च करना
    search_params = {
        "api_key": SERPAPI_KEY,
        "q": search_query,
        "engine": "google",
        "gl": "in", # भारत में सर्च करने के लिए
        "hl": "en"
    }
    search = GoogleSearch(search_params)
    results = search.get_dict()
    
    # सर्च से मिली जानकारी को इकट्ठा करना
    search_context = ""
    if 'organic_results' in results:
        for result in results['organic_results'][:5]: # टॉप 5 रिजल्ट्स
            search_context += f"Title: {result.get('title')}\nSnippet: {result.get('snippet')}\n---\n"
    
    if not search_context:
        return "Sorry, I couldn't find enough information online to answer your request."

    # ---
    print("\n--- 3. जानकारी को मिलाकर जवाब बनाना... ---")
    
    # फेज 3: LLM को सारी जानकारी देकर फाइनल जवाब बनवाना
    synthesis_prompt = f"""
    You are an expert recommendation AI. Your task is to answer the user's original request based on the provided web search results.
    
    Original User Request: "{user_prompt}"
    Your ranking criteria are: "{ranking_criteria}"
    
    Here are the top web search results to use as your knowledge base:
    --- START OF SEARCH RESULTS ---
    {search_context}
    --- END OF SEARCH RESULTS ---
    
    Based *only* on the provided search results, generate a JSON array of the top 5 recommendations.
    Each JSON object in the array must have three keys:
    1. "title": A concise title for the item.
    2. "description": A short, engaging one-sentence description.
    3. "image_search_query": A simple, effective query to find a relevant image for this item on Google Images (e.g., "The 5 AM Club book cover").

    Do not include any text outside of the JSON array. Your entire output should be a valid JSON.
    Example format:
    [
      {{
        "title": "Example Title 1",
        "description": "This is a great first choice for users.",
        "image_search_query": "Image search term 1"
      }},
      {{
        "title": "Example Title 2",
        "description": "This is a strong alternative.",
        "image_search_query": "Image search term 2"
      }}
    ]
    """
    
    try:
        final_response = llm.generate_content(synthesis_prompt)
        return final_response.text
    except Exception as e:
        print(f"Error in Phase 3: {e}")
        return "Sorry, I found some information but had trouble putting together a final recommendation."

# --- टेस्टिंग ---
if __name__ == "__main__":
    # user_query = "best gaming laptop under 1 lakh with RTX 4060"
    user_query = "weekend getaways from Bhopal in monsoon"
    
    print(f"यूज़र ने पूछा: {user_query}\n")
    final_answer = get_dynamic_recommendation(user_query)
    print("\n--- FINAL AI RECOMMENDATION ---")
    print(final_answer)