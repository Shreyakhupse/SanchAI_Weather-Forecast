from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
import os
import requests
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS middleware to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class QueryRequest(BaseModel):
    message: str

class QueryResponse(BaseModel):
    response: str

# Weather tool function
def get_weather(city: str) -> str:
    """
    Get current weather information for a city.
    
    Args:
        city: Name of the city (e.g., "Pune", "Mumbai", "London")
    
    Returns:
        String describing the weather conditions
    """
    try:
        # Using OpenWeatherMap API (free tier)
        # You can get a free API key from https://openweathermap.org/api
        api_key = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here")
        
        if api_key == "your_api_key_here":
            # Fallback: Return mock data if API key is not set
            return f"The weather in {city} is 24°C, partly cloudy with a gentle breeze."
        
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }
        
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            
            return f"The weather in {city} is {temp}°C, {description}. Humidity is {humidity}% and wind speed is {wind_speed} m/s."
        else:
            return f"Sorry, I couldn't fetch the weather for {city}. Please check if the city name is correct."
    
    except Exception as e:
        return f"Error fetching weather for {city}: {str(e)}"

# Create Langchain tool
weather_tool = Tool(
    name="get_weather",
    func=get_weather,
    description="Get the current weather information for a city. Input should be the city name as a string."
)

@app.get("/")
def read_root():
    return {"message": "Weather Forecast API is running"}

@app.post("/query", response_model=QueryResponse)
async def query_weather(request: QueryRequest):
    """
    Handle user queries about weather using Langchain agent.
    """
    try:
        # Get OpenRouter API key from environment variable
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        
        if not openrouter_api_key:
            raise HTTPException(
                status_code=500,
                detail="OPENROUTER_API_KEY environment variable is not set"
            )
        
        # Initialize LLM with OpenRouter
        # Using OpenRouter's OpenAI-compatible endpoint
        llm = ChatOpenAI(
            model="openai/gpt-4o-mini",  # You can change this to any model on OpenRouter
            temperature=0,
            openai_api_key=openrouter_api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": "http://localhost:3000",  # Optional: for OpenRouter analytics
            }
        )
        
        # Initialize agent with tools
        agent = initialize_agent(
            tools=[weather_tool],
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True
        )
        
        # Run the agent with user query
        response = agent.run(request.message)
        
        return QueryResponse(response=response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

