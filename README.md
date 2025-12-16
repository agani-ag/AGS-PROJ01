# 📝 Answer Feedback Bot

A web application that helps students improve their answers through AI-powered feedback and iterative evaluation using OpenAI's GPT models.

## 🎯 Features

- **Answer Evaluation**: Get detailed feedback on student answers including scores, strengths, areas for improvement, and missing concepts
- **Iterative Learning**: Submit improved answers and track progress across multiple attempts
- **Analytics Dashboard**: Visualize learning progress with comprehensive charts and metrics
- **Session Management**: Track multiple questions and attempts within isolated sessions
- **Data Persistence**: All evaluations are stored in CSV format for future analysis

## 🛠️ Tech Stack

- **Backend**: Python
- **Frontend**: Streamlit
- **AI Model**: OpenAI GPT-4o-mini
- **Data Storage**: CSV files with pandas
- **Visualization**: Matplotlib

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key
- pip (Python package installer)

## 🚀 Installation & Setup

### 1. Clone or Download the Project

```bash
cd e:\Software\PRJ-01\answer-feedback-bot
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure OpenAI API Key

Create a `.env` file in the project root:

```bash
copy .env.example .env
```

Edit the `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**How to get an OpenAI API key:**
1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Navigate to API keys section
4. Create a new secret key
5. Copy and paste it into your `.env` file

## 📂 Project Structure

```
answer-feedback-bot/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                    # Example environment variables
├── .env                           # Your actual API key (not in git)
├── .gitignore                     # Git ignore file
│
├── modules/                       # Core functionality modules
│   ├── __init__.py               # Package initializer
│   ├── openai_integration.py     # OpenAI API integration
│   ├── data_storage.py           # CSV data handling
│   └── analytics.py              # Analytics and visualization
│
├── data/                          # Data storage directory
│   └── evaluations.csv           # Evaluation records (auto-created)
│
└── README.md                      # This file
```

## 🎮 Usage

### 1. Start the Application

With your virtual environment activated:

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

### 2. Using the Application

**Evaluation Tab:**
1. Enter a question in the first text area
2. Enter your answer in the second text area
3. Click "Evaluate Answer"
4. Review the feedback:
   - Score (0-10)
   - Strengths (what you did well)
   - Areas for Improvement
   - Teacher's Feedback
   - Missing Concepts
5. Improve your answer based on feedback
6. Re-submit to see your progress

**Analytics Tab:**
- View overall performance metrics
- See question-wise summary table
- Explore visualization charts:
  - Before vs After Score Comparison
  - Learning Gain per Question
  - Error Reduction per Question
- View detailed attempt history

### 3. Session Management

- Each session has a unique ID
- All evaluations within a session are tracked together
- Click "New Session" in the sidebar to start fresh
- Data persists across sessions in the CSV file

## 📊 Metrics Explained

- **Score**: Rating from 0-10 for the answer quality
- **Improvement**: Difference between last and first attempt scores
- **Learning Gain %**: (Improvement / 10) × 100
- **Error Reduction**: Number of missing concepts addressed between attempts
- **Strengths**: Positive aspects of the answer
- **Areas for Improvement**: Suggestions for enhancement
- **Missing Concepts**: Key concepts not addressed in the answer

## 🗃️ Data Storage

Evaluation data is stored in `data/evaluations.csv` with the following fields:

- `session_id`: Unique session identifier
- `question`: The question text
- `attempt_no`: Attempt number for that question
- `score`: Score out of 10
- `strengths`: What was done well (pipe-separated)
- `areas_for_improvement`: What needs work (pipe-separated)
- `feedback`: Detailed teacher feedback
- `missing_concepts`: Concepts not addressed (pipe-separated)
- `answer_text`: The student's answer
- `timestamp`: When the evaluation occurred

## 🔧 Configuration

### Change AI Model

Edit `modules/openai_integration.py`, line 26:

```python
self.model = "gpt-4o-mini"  # or "gpt-4", "gpt-3.5-turbo", etc.
```

### Modify Evaluation Criteria

Edit the `system_prompt` in `modules/openai_integration.py` to change how answers are evaluated.

### Adjust CSV Storage Location

Edit `modules/data_storage.py`, change the default path:

```python
def __init__(self, csv_path: str = "data/evaluations.csv"):
```

## 🐛 Troubleshooting

### "OpenAI API key not found" Error

- Make sure your `.env` file exists in the project root
- Verify the API key is correctly set: `OPENAI_API_KEY=sk-...`
- Restart the Streamlit app after creating/modifying `.env`

### Import Errors

- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### CSV File Issues

- The `data/` directory and CSV file are created automatically
- If you get permission errors, check folder permissions
- Delete `data/evaluations.csv` to start fresh (all data will be lost)

### Visualization Not Showing

- Make sure matplotlib is installed: `pip install matplotlib`
- Check if you have multiple attempts for meaningful charts

## 💡 Tips for Best Results

1. **Be Specific**: Enter clear, well-defined questions
2. **Iterative Improvement**: Use feedback to genuinely improve your answer
3. **Multiple Questions**: Try different questions to see overall learning trends
4. **Review Analytics**: Regularly check the Analytics tab to track progress
5. **API Usage**: Be mindful of OpenAI API costs with extensive usage

## 📝 Example Workflow

```
Session Start
    ↓
Enter Question: "What is photosynthesis?"
    ↓
Enter Answer: "Process where plants make food using sunlight"
    ↓
Evaluate → Score: 4/10
    ↓
Review Feedback (missing: chlorophyll, glucose, oxygen, etc.)
    ↓
Improve Answer: "Photosynthesis is the process where plants use 
                 chlorophyll to convert sunlight, water, and CO2 
                 into glucose and oxygen..."
    ↓
Evaluate Again → Score: 8/10
    ↓
View Analytics → +4 point improvement, 60% error reduction
```

## 🔒 Security Notes

- **Never commit** your `.env` file to version control
- Keep your OpenAI API key private
- The `.gitignore` file prevents accidental commits
- Consider using environment variables in production

## 📄 License

This project is provided as-is for educational purposes.

## 🤝 Contributing

Feel free to fork, modify, and enhance this project for your needs.

## 📞 Support

For issues related to:
- **OpenAI API**: Check [OpenAI documentation](https://platform.openai.com/docs)
- **Streamlit**: Visit [Streamlit docs](https://docs.streamlit.io)
- **Python packages**: Refer to respective package documentation

---

**Happy Learning! 🎓**
