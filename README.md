# Zilch Dice Game Backend

This is the backend service for the Zilch dice game, built with FastAPI.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- virtualenv (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd zilch-backend
   ```

2. **Set up a virtual environment**
   ```bash
   # Create a virtual environment
   python -m venv venv
   
   # Activate the virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   # .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e .
   ```

### Running the Application

Start the FastAPI development server:

```bash
uvicorn zilch_dice_game.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### Running Tests

To run the test suite:

```bash
pytest
```

### API Documentation

Once the server is running, you can access:

- Interactive API documentation: `http://127.0.0.1:8000/docs`
- Alternative documentation: `http://127.0.0.1:8000/redoc`

## 📦 Project Structure

```
zilch-backend/
├── zilch_dice_game/
│   ├── __init__.py
│   ├── main.py         # Main application and routes
│   └── models.py       # Pydantic models
├── tests/              # Test files
├── setup.py            # Package configuration
└── README.md           # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
workon zilch-backend