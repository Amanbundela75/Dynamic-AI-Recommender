import os
import google.generativeai as genai
from serpapi import GoogleSearch
from dotenv import load_dotenv
import json
from urllib.parse import quote_plus
from fastapi import FastAPI
from pydantic import BaseModel

# Environment variables load karna
load_dotenv()

# FastAPI app initialize karna
app = FastAPI(
    title="Dynamic Recommendation AI Service",
    description="Ek AI service jo kisi bhi prompt ke liye live recommendations deta hai."
)

# API Keys configure karna
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")
    llm = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    print(f"API Key configuration error: {e}")
    llm = None

# Request ka format define karna
class RecommendationRequest(BaseModel):
    prompt: str

# Helper function jo image URL khojega
def get_image_url(query: str) -> str:
    # ... (yeh function pichle code se same rahega) ...
    params = {"engine": "google_images", "q": query, "api_key": SERPAPI_KEY}
    search = GoogleSearch(params)
    results = search.get_dict()
    if "images_results" in results and results["images_results"]:
        return results["images_results"][0].get("thumbnail", "https://i.imgur.com/gLoOC5h.png")
    return "https://i.imgur.com/gLoOC5h.png"

@app.get("/")
def read_root():
    return {"message": "AI Recommendation Service is running. Go to /docs to test the API."}

# Hamara main API endpoint
@app.post("/recommend/")
async def get_recommendations_endpoint(request: RecommendationRequest):
    """
    Yeh endpoint user se prompt leta hai aur dynamic recommendations deta hai.
    """
    if not llm:
        return {"error": "AI Model is not configured. Check your API keys."}

    user_prompt = request.prompt
    print(f"Received prompt: {user_prompt}")

    # Phase 1: Deconstruction
    deconstruction_prompt = f"Analyze the user's request '{user_prompt}' and return a JSON with 'search_query' and 'ranking_criteria'."
    try:
        response = llm.generate_content(deconstruction_prompt)
        analysis_json = json.loads(response.text.strip().replace("```json", "").replace("```", ""))
        search_query = analysis_json.get('search_query')
        ranking_criteria = analysis_json.get('ranking_criteria')
    except Exception:
        return {"error": "Could not understand the prompt."}

    # Phase 2: Information Retrieval
    search_params = {"api_key": SERPAPI_KEY, "q": search_query, "engine": "google"}
    search = GoogleSearch(search_params)
    results = search.get_dict()
    search_context = "".join([f"Title: {res.get('title')}\nSnippet: {res.get('snippet')}\n---\n" for res in results.get('organic_results', [])[:5]])
    
    if not search_context:
        return {"error": "Could not find information online."}

    # Phase 3: Synthesis
    synthesis_prompt = f"""
    User Request: "{user_prompt}"
    Ranking Criteria: "{ranking_criteria}"
    Search Results Context: "{search_context}"
    Based on this, generate a JSON array of top 4 recommendations with keys: "title", "description", "image_search_query".
    """
    try:
        final_response = llm.generate_content(synthesis_prompt)
        recommendations = json.loads(final_response.text.strip().replace("```json", "").replace("```", ""))
    except Exception:
        return {"error": "Could not synthesize recommendations."}

    # Phase 4: Enrichment (Images and URLs)
    for item in recommendations:
        item['image_url'] = get_image_url(item['image_search_query'])
        search_term = quote_plus(item['title'])
        item['url'] = f"https://www.google.com/search?q={search_term}"
        
    return recommendations