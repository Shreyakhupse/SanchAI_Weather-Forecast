# Weather Forecast Application

A minimal web application with React frontend and FastAPI backend that uses Langchain + OpenRouter to answer weather queries for any city.

## Features

- React-based frontend with clean UI
- FastAPI backend with Langchain agent
- OpenRouter integration for LLM responses
- Weather tool for fetching real-time weather data
- Simple input box and send button interface

## Prerequisites

- Python 3.8+
- Node.js 16+
- OpenRouter API key ([Get one here](https://openrouter.ai/))
- (Optional) OpenWeatherMap API key ([Get one here](https://openweathermap.org/api))

## Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the backend directory:
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

Note: If you don't provide OPENWEATHER_API_KEY, the app will use mock weather data.

6. Run the backend server:
```bash
python main.py
```

The backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to the Frontend directory:
```bash
cd Frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## Usage

1. Make sure both backend and frontend servers are running
2. Open your browser and go to `http://localhost:3000`
3. Type a weather query like:
   - "What's the weather of Pune?"
   - "weather of Mumbai today?"
   - "Tell me the weather in London"
4. Click Send or press Enter
5. The application will use the Langchain agent with OpenRouter to understand your query and fetch the weather data

## How It Works

1. User sends a query through the frontend
2. Frontend sends POST request to `/query` endpoint
3. Backend receives the query and initializes a Langchain agent with:
   - OpenRouter LLM (GPT-4o-mini by default)
   - Weather tool for fetching city weather
4. Agent processes the query, identifies the city, and calls the weather tool
5. Response is sent back to frontend and displayed to the user

## Project Structure

```
Weather Forecast/
├── backend/
│   ├── main.py           # FastAPI application with Langchain agent
│   └── requirements.txt  # Python dependencies
├── Frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js       # Main React component
│   │   ├── App.css      # Styles
│   │   ├── index.js     # React entry point
│   │   └── index.css    # Global styles
│   └── package.json     # Node dependencies
└── README.md
```

## Configuration

You can change the OpenRouter model by editing the `model` parameter in `backend/main.py`:
```python
llm = ChatOpenAI(
    model="openai/gpt-4o-mini",  # Change this to any model on OpenRouter
    ...
)
```

## Troubleshooting

- **CORS errors**: Make sure the frontend proxy in `package.json` points to the correct backend URL
- **API key errors**: Verify your OpenRouter API key is set correctly in the `.env` file
- **Weather not working**: Check if OpenWeatherMap API key is valid, or the app will use mock data

