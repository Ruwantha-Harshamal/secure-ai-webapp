# 🔒 Secure AI Webapp

A comprehensive web application designed to detect and mask sensitive information in AI prompts before they are sent to language models. This tool helps prevent data leaks and maintains privacy when interacting with AI systems.

## 🌟 Features

- **Multi-layered Detection**: Combines regex patterns, spaCy NER, Presidio PII detection, zero-shot classification, and custom keyword matching
- **Real-time Processing**: Fast detection and masking of sensitive data
- **Web Interface**: User-friendly Streamlit frontend for interactive use
- **REST API**: FastAPI backend for programmatic access
- **Browser Extension**: Chrome extension for seamless integration
- **Comprehensive Coverage**: Detects emails, phone numbers, SSNs, credit cards, API keys, IP addresses, and more

## 🏗️ Architecture

The application consists of three main components:

1. **Detection Engine** (`detector/`): Core logic for identifying and masking sensitive data
2. **Web Frontend** (`streamlit_app.py`): Streamlit-based user interface
3. **REST API** (`api.py`): FastAPI backend for external integrations
4. **Browser Extension** (`secure-prompt-extension/`): Chrome extension for web integration

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. Clone or download this repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download required spaCy models:
   ```bash
   python -m spacy download en_core_web_sm
   python -m spacy download en_core_web_lg
   ```

### Running the Application

#### Option 1: Streamlit Web Interface
```bash
streamlit run streamlit_app.py
```
Access the application at: http://localhost:8501

#### Option 2: FastAPI Backend
```bash
uvicorn api:app --reload
```
API will be available at: http://127.0.0.1:8000
API documentation: http://127.0.0.1:8000/docs

#### Option 3: Run Both Services
```bash
# Terminal 1 - Start API
uvicorn api:app --reload

# Terminal 2 - Start Streamlit
streamlit run streamlit_app.py
```

## 🔍 Detection Methods

### 1. Regex Patterns
- **Email addresses**: Standard email format detection
- **IP addresses**: IPv4 address detection
- **API keys**: OpenAI API key format (sk-...)
- **Phone numbers**: US phone number formats
- **SSN**: Social Security Number format (###-##-####)
- **Credit cards**: Standard credit card number formats
- **GitHub tokens**: GitHub personal access tokens (ghp_...)
- **AWS keys**: AWS access key format (AKIA...)

### 2. spaCy Named Entity Recognition
- **PERSON**: People's names
- **GPE/LOC**: Geographic locations
- **ORG**: Organizations
- **MONEY**: Monetary values

### 3. Presidio PII Detection
- Advanced PII detection using Microsoft's Presidio
- Covers various entity types including addresses, bank accounts, etc.

### 4. Zero-Shot Classification
- Uses BART model for contextual understanding
- Detects: personal information, private data, financial information, medical information, confidential data, passwords, internal data

### 5. Custom Keywords
- Configurable keyword list in `keywords.txt`
- Currently includes: jenkins, vault access, admin password, production secret, NDA

## 📁 Project Structure

```
secure-ai-webapp/
├── detector/                           # Core detection engine
│   ├── __init__.py
│   ├── secure_prompt_advanced.py       # Main detection logic
│   └── contextual_detector.py          # Additional detection methods
├── secure-prompt-extension/            # Chrome browser extension
│   ├── manifest.json                   # Extension configuration
│   ├── background.js                   # Background script
│   ├── content.js                      # Content script
│   ├── popup.html                      # Extension popup UI
│   ├── popup.js                        # Popup functionality
│   └── icons/                          # Extension icons
├── streamlit_app.py                    # Streamlit web interface
├── api.py                              # FastAPI backend
├── requirements.txt                    # Python dependencies
├── keywords.txt                        # Custom sensitive keywords
└── README.md                           # This file
```

## 🔧 Configuration

### Custom Keywords
Edit `keywords.txt` to add organization-specific sensitive terms:
```
internal_api_key
company_secret
proprietary_algorithm
customer_database
```

### Detection Thresholds
Modify confidence thresholds in `secure_prompt_advanced.py`:
```python
# Zero-shot classification threshold
if score >= 0.7:  # Adjust this value (0.0-1.0)
```

## 🌐 API Usage

### POST /api/filter

Filter and mask sensitive content in a prompt.

**Request:**
```json
{
  "prompt": "My email is john@example.com and my SSN is 123-45-6789"
}
```

**Response:**
```json
{
  "masked_prompt": "My email is [EMAIL] and my SSN is [SSN]"
}
```

### Example with curl:
```bash
curl -X POST "http://127.0.0.1:8000/api/filter" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Contact me at john@example.com"}'
```

## 🔌 Browser Extension

### Installation
1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked" and select the `secure-prompt-extension/` folder

### Usage
- Click the extension icon in your browser
- Paste your prompt in the extension popup
- Get the masked version instantly

## 🛡️ Security Features

- **No Data Storage**: Prompts are processed in memory only
- **Local Processing**: All detection happens locally (except for model inference)
- **Customizable**: Easily configure detection rules for your organization
- **Multi-format Support**: Handles various data formats and patterns

## 🧪 Testing

Test the detection with sample inputs:

```python
from detector.secure_prompt_advanced import run_secure_prompt_filter

# Test email detection
result = run_secure_prompt_filter("Contact me at john@example.com")
print(result)  # Output: "Contact me at [EMAIL]"

# Test multiple entities
text = "John Smith's email is john@example.com, phone: 555-123-4567"
result = run_secure_prompt_filter(text)
print(result)  # Output: "[PERSON]'s email is [EMAIL], phone: [PHONE_NUMBER]"
```

## 📋 Requirements

### Python Packages
- fastapi: Web framework for API
- uvicorn: ASGI server
- spacy: Natural language processing
- transformers: Hugging Face transformers library
- torch: PyTorch for deep learning models
- presidio-analyzer: Microsoft's PII detection
- presidio-anonymizer: Data anonymization
- scikit-learn: Machine learning utilities
- streamlit: Web application framework

### Pre-trained Models
- `en_core_web_sm`: spaCy English model (small)
- `en_core_web_lg`: spaCy English model (large)
- `facebook/bart-large-mnli`: BART model for zero-shot classification

## 🚀 Deployment

### Local Development
Follow the Quick Start guide above.

### Production Deployment
1. Set up a virtual environment
2. Install dependencies
3. Configure environment variables if needed
4. Use a production ASGI server like Gunicorn
5. Set up reverse proxy (nginx) if required

### Docker Deployment (Optional)
Create a Dockerfile for containerized deployment:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download en_core_web_lg
COPY . .
EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔄 Version History

- **v1.0.0**: Initial release with core detection capabilities
- Multi-layered detection system
- Streamlit and FastAPI interfaces
- Browser extension support

## 🎯 Roadmap

- [ ] Add support for more languages
- [ ] Implement custom entity training
- [ ] Add batch processing capabilities
- [ ] Create Docker container
- [ ] Add logging and monitoring
- [ ] Implement user authentication
- [ ] Add configuration management interface

---

**⚠️ Important**: This tool is designed to help identify potential sensitive information, but it may not catch all cases. Always review the output and use additional security measures as needed for your specific use case.
