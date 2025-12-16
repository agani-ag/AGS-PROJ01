# Quick Start Guide

## Windows Quick Start

### 1. Setup (First Time Only)

```powershell
# Navigate to project
cd e:\Software\PRJ-01\answer-feedback-bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
copy .env.example .env

# Edit .env and add your OpenAI API key
notepad .env
```

### 2. Run the App

```powershell
# Make sure you're in the project directory
cd e:\Software\PRJ-01\answer-feedback-bot

# Activate virtual environment
.\venv\Scripts\activate

# Run Streamlit app
streamlit run app.py
```

### 3. Access the App

The app will automatically open in your browser at:
```
http://localhost:8501
```

### 4. Stop the App

Press `Ctrl + C` in the terminal

---

## macOS/Linux Quick Start

### 1. Setup (First Time Only)

```bash
# Navigate to project
cd answer-feedback-bot

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env

# Edit .env and add your OpenAI API key
nano .env  # or use your preferred editor
```

### 2. Run the App

```bash
# Make sure you're in the project directory
cd answer-feedback-bot

# Activate virtual environment
source venv/bin/activate

# Run Streamlit app
streamlit run app.py
```

### 3. Access the App

Open your browser and go to:
```
http://localhost:8501
```

### 4. Stop the App

Press `Ctrl + C` in the terminal

---

## Common Commands

### Deactivate Virtual Environment
```bash
deactivate
```

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Clear Data (Start Fresh)
```bash
# Windows
del data\evaluations.csv

# macOS/Linux
rm data/evaluations.csv
```

---

## First Time Usage

1. **Get OpenAI API Key**
   - Go to https://platform.openai.com
   - Sign up/Login
   - Create API key
   - Copy key

2. **Set API Key**
   - Open `.env` file
   - Replace `your_openai_api_key_here` with your actual key
   - Save file

3. **Test the App**
   - Run: `streamlit run app.py`
   - Enter a simple question like "What is water?"
   - Enter an answer
   - Click "Evaluate Answer"

---

## Troubleshooting

### "Command not found: streamlit"
→ Make sure virtual environment is activated

### "OpenAI API key not found"
→ Check your `.env` file has the correct API key

### Port already in use
→ Stop other Streamlit apps or use: `streamlit run app.py --server.port 8502`

### Import errors
→ Reinstall dependencies: `pip install -r requirements.txt`

---

**Need help?** Check the full README.md for detailed documentation.
