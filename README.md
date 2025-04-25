# Parwaaz - AI-Powered Learning Assistant for Middle School

**Parwaaz** is a generative AI-powered educational assistant designed specifically for middle school students (Grades 6–8). It helps learners explore subjects like English, Science, and Math through interactive tools including quizzes, flashcards, summaries, and visual explanations.
## 🚀 Features

- 📚 **Subject-Based Learning**: Choose your grade and subject to generate topic-specific educational content.
- 🧠 **AI-Generated Flashcards**: Instantly create interactive flashcards for key concepts.
- ✍️ **Quiz Generator**: Auto-generate multiple-choice quizzes to reinforce understanding.
- 📝 **Summarizer**: Get clean, structured summaries of any topic in simple language.
- 🎓 **Student-Friendly UI**: Built with TailwindCSS and Flask for a smooth learning experience.
## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML + TailwindCSS
- **AI Integration**: OpenAI API
- **Version Control**: Git & GitHub
## 📁 Folder Structure

<pre>
Parwaaz/
├── static/                 # CSS, JS, and image files
├── templates/              # Jinja2 HTML templates
├── app/                    # Flask backend logic (views, API handling)
├── run.py                  # Entry point to run the Flask app
├── .env                    # Environment variables (excluded from Git)
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
</pre>

## ⚙️ Setup Instructions

1. **Clone the repository**

<pre>
git clone https://github.com/sahmed104/GENAI_003_PROJECT_8.git
cd GENAI_003_PROJECT_8
</pre>

2. **Create a virtual environment and install dependencies**

<pre>
python -m venv venv
venv\Scripts\activate        # (Windows)
# or
source venv/bin/activate     # (macOS/Linux)

pip install -r requirements.txt
</pre>

3. **Add your OpenAI API key to `.env`**

<pre>
OPENAI_API_KEY=your_key_here
</pre>

4. **Run the app**

<pre>
python run.py
</pre>

## ✨ Authors

This project was developed by a dedicated team of three collaborators focused on building accessible, AI-powered educational tools for middle school students. Each team member contributed to design, development, and testing to bring Parwaaz to life.
<pre>
👩‍💻 Zainab Siddiqi  
👨‍💻 Saud Ahmed  
👨‍💻 Shehzad Ahmed
</pre>
