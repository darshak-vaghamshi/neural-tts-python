# Neural TTS Python

A multilingual Text-to-Speech (TTS) API built with FastAPI and Microsoft Edge TTS, supporting Indian languages and English.

## Features

- **Multilingual Support**: Supports 14 languages including English and major Indian languages
- **Neural Voices**: High-quality female neural voices for all supported languages
- **FastAPI Backend**: RESTful API with automatic documentation
- **Audio Processing**: Audio format conversion and processing capabilities
- **Language Detection**: Automatic language detection for input text

## Supported Languages

| Language | Code | Voice |
|----------|------|-------|
| English | en | en-IN-NeerjaNeural |
| Gujarati | gu | gu-IN-DhwaniNeural |
| Hindi | hi | hi-IN-SwaraNeural |
| Tamil | ta | ta-IN-PallaviNeural |
| Telugu | te | te-IN-ShrutiNeural |
| Kannada | kn | kn-IN-SapnaNeural |
| Malayalam | ml | ml-IN-SobhanaNeural |
| Bengali | bn | bn-IN-TanishaaNeural |
| Marathi | mr | mr-IN-AarohiNeural |
| Punjabi | pa | pa-IN-KiranNeural |
| Odia | or | or-IN-AnanyaNeural |
| Assamese | as | as-IN-BanitaNeural |
| Urdu | ur | ur-IN-GulNeural |
| Nepali | ne | ne-NP-HemkalaNeural |

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd neural-tts-python
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Server

Start the FastAPI server:
```bash
python -m audio.run
```

The server will start on `http://localhost:5000`

### API Endpoints

#### Text to Speech
- **POST** `/tts`
  - Convert text to speech
  - Request body: `{"text": "Hello world", "language": "en"}`
  - Returns: Audio file

#### Health Check
- **GET** `/health`
  - Check API status

### API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:5000/docs`
- ReDoc: `http://localhost:5000/redoc`

## Project Structure

```
neural-tts-python/
├── audio/
│   ├── api/           # API routes
│   ├── services/      # Business logic
│   ├── utils/         # Utility functions
│   ├── config.py      # Configuration
│   └── run.py         # Application entry point
├── static/            # Static files
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Dependencies

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server
- **edge-tts**: Microsoft Edge Text-to-Speech
- **pydub**: Audio processing
- **langdetect**: Language detection
- **nltk**: Natural language processing

## Configuration

The application uses the following configuration files:
- `audio/config.py`: Language and voice mappings
- `requirements.txt`: Python dependencies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Notes

- All voices are female neural voices from Microsoft Edge TTS
- For exact voice names, run `edge-tts --list-voices`
- The server runs in development mode with auto-reload enabled
