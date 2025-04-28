let flashcards = [], flashIndex = 0, flipped = false;

// Typewriter Effect with MathJax
function typeHTMLContent(id, fullHTML, speed = 15, callback = null) {
const el = document.getElementById(id);
el.innerHTML = '';
let i = 0;
const interval = setInterval(() => {
el.innerHTML = fullHTML.slice(0, i);
i++;
if (i > fullHTML.length) {
  clearInterval(interval);
  if (window.MathJax) MathJax.typesetPromise();
  if (callback) callback();
}
}, speed);
}

// Markdown Formatter
function formatMarkdown(text) {
return text
.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
.replace(/\*(.*?)\*/g, '<em>$1</em>')
.replace(/\n/g, '<br>');
}

// Flashcard Typing
function typeTextLineByLine(elId, lines, delay = 30, callback = null) {
const el = document.getElementById(elId);
el.innerHTML = '';
let i = 0;
const interval = setInterval(() => {
if (i < lines.length) {
  el.innerHTML += `<p>${lines[i]}</p>`;
  i++;
} else {
  clearInterval(interval);
  if (callback) callback();
}
}, delay * 4);
}

// Flashcard Functions
function updateFlashcard() {
const card = flashcards[flashIndex];
flipped = false;
document.getElementById("flashcard").classList.remove("rotate-y-180");
document.getElementById("flashFront").innerHTML = card.term;
document.getElementById("flashBack").innerHTML = card.definition;
if (window.MathJax) MathJax.typesetPromise();
document.getElementById("flashIndex").textContent = `Card ${flashIndex + 1} of ${flashcards.length}`;
}

function flipFlashcard() {
flipped = !flipped;
document.getElementById("flashcard").classList.toggle("rotate-y-180", flipped);
const card = flashcards[flashIndex];
if (flipped) {
document.getElementById("flashBack").innerHTML = card.definition;
if (window.MathJax) MathJax.typesetPromise();
} else {
document.getElementById("flashFront").innerHTML = card.term;
if (window.MathJax) MathJax.typesetPromise();
}
}

function nextFlashcard() {
if (flashIndex < flashcards.length - 1) {
flashIndex++;
updateFlashcard();
}
}

function prevFlashcard() {
if (flashIndex > 0) {
flashIndex--;
updateFlashcard();
}
}

function cleanLines(raw) {
  return raw.split('\n')
            .map(line => line.trim())
            .filter(line => line.length > 0);
}

function smartParseFlashcards(raw) {
  const lines = cleanLines(raw);

  const parsers = [
    parseNumberedExplanationStyle,
    parseMeaningExampleStyle,
    parseSimpleTermColonExplanation,
    parseBulletStyle,
    parsePlainSentenceStyle,
    parseMarkdownStyle,
    mixedParserStyle
  ];

  for (const parser of parsers) {
    const result = parser(lines);
    if (result && result.length > 0 && !result[0].term.includes("Error")) {
      console.log(`Parsed using: ${parser.name}`);
      return result;
    }
  }

  return [{ term: "⚡ Error", definition: "Could not parse flashcards. Please regenerate." }];
}

function parseNumberedExplanationStyle(lines) {
  const cards = [];
  let currentTerm = null;
  lines.forEach((line) => {
    if (/^\d+\.\s+/.test(line)) {
      if (currentTerm) cards.push(currentTerm);
      currentTerm = { term: line.replace(/^\d+\.\s*/, ''), definition: '' };
    }
    else if (line.toLowerCase().startsWith('explanation:') && currentTerm) {
      currentTerm.definition = line.split(':').slice(1).join(':').trim();
    }
  });
  if (currentTerm) cards.push(currentTerm);
  return cards;
}

function parseMeaningExampleStyle(lines) {
  const cards = [];
  let currentTerm = null, currentMeaning = null, currentExample = null;
  lines.forEach((line) => {
    if (/^\d+\.\s+/.test(line)) {
      if (currentTerm && currentMeaning) {
        cards.push({ term: currentTerm, definition: currentMeaning + (currentExample ? "<br><strong>Example:</strong> " + currentExample : '') });
      }
      currentTerm = line.replace(/^\d+\.\s*/, '');
      currentMeaning = null;
      currentExample = null;
    }
    else if (line.toLowerCase().startsWith('meaning:') && currentTerm) {
      currentMeaning = line.split(':').slice(1).join(':').trim();
    }
    else if (line.toLowerCase().startsWith('example:') && currentTerm) {
      currentExample = line.split(':').slice(1).join(':').trim();
    }
  });
  if (currentTerm && currentMeaning) {
    cards.push({ term: currentTerm, definition: currentMeaning + (currentExample ? "<br><strong>Example:</strong> " + currentExample : '') });
  }
  return cards;
}

function parseSimpleTermColonExplanation(lines) {
  const cards = [];
  lines.forEach((line) => {
    if (line.includes(':')) {
      const parts = line.split(':');
      if (parts.length >= 2) {
        cards.push({ term: parts[0].trim(), definition: parts.slice(1).join(':').trim() });
      }
    }
  });
  return cards;
}

function parseBulletStyle(lines) {
  const cards = [];
  lines.forEach((line) => {
    if (/^[•*-]\s+/.test(line)) {
      const cleanLine = line.replace(/^[•*-]\s*/, '');
      const parts = cleanLine.split(':');
      if (parts.length >= 2) {
        cards.push({ term: parts[0].trim(), definition: parts.slice(1).join(':').trim() });
      }
    }
  });
  return cards;
}

function parsePlainSentenceStyle(lines) {
  const cards = [];
  lines.forEach((line) => {
    if (line.includes('means')) {
      const parts = line.split('means');
      cards.push({ term: parts[0].trim(), definition: parts[1].trim() });
    }
  });
  return cards;
}

function parseMarkdownStyle(lines) {
  const cards = [];
  let currentTerm = null;
  lines.forEach((line) => {
    if (line.startsWith('###')) {
      if (currentTerm) cards.push(currentTerm);
      currentTerm = { term: line.replace('###', '').trim(), definition: '' };
    }
    else if (line.toLowerCase().startsWith('**explanation:**') && currentTerm) {
      currentTerm.definition = line.split('**explanation:**')[1].trim();
    }
  });
  if (currentTerm) cards.push(currentTerm);
  return cards;
}

function mixedParserStyle(lines) {
  const cards = [];
  let tempTerm = null;
  lines.forEach((line) => {
    if (line.length <= 4 && /^\d+$/.test(line)) {
      // Likely a broken number, ignore
    }
    else if (line.length < 20) {
      // Short term name
      tempTerm = line;
    }
    else if (tempTerm) {
      // Following long text is explanation
      cards.push({ term: tempTerm, definition: line });
      tempTerm = null;
    }
  });
  return cards;
}

// Quiz Renderer
function renderQuizTyped(raw, quizType) {
const lines = raw.split('\n');
const quizBlock = document.getElementById("quizOutput");
const answersBlock = document.getElementById("quizAnswers");
quizBlock.innerHTML = '';
answersBlock.innerHTML = '';

let htmls = [];
let buffer = '';
let questionNum = 0;
let answerLine = '';
let isAnswerSection = false;

lines.forEach(line => {
line = line.trim();

if (line.toLowerCase().startsWith("answers:") || line.toLowerCase().startsWith("answer:")) {
  isAnswerSection = true;
  return;
}

if (isAnswerSection) {
  answerLine += line + ' ';
  return;
}

if (line.startsWith("Q")) {
  if (buffer) htmls.push(buffer);
  questionNum++;
  buffer = `<p class='font-semibold mt-2'>${line}</p>`;
} else if (quizType === "mcq" && line.match(/^[A-D]\./)) {
  const name = 'q' + questionNum;
  buffer += `<label class='block ml-4'><input type='radio' name='${name}' class='mr-2'> ${line}</label>`;
} else {
  // for true/false, short answer, fill_blank — just plain text lines
  buffer += `<p class="ml-4">${line}</p>`;
}
});

if (buffer) htmls.push(buffer);

typeHTMLContent("quizOutput", htmls.join(''), 5);

// Format answers
let formatted = '';
// Match A/B/C answers like "Q1: A"
const abcFormat = [...answerLine.matchAll(/(Q\d+):\s*([A-D])/g)];
if (abcFormat.length) {
formatted = abcFormat.map(match => `<li><strong>${match[1]}</strong>: ${match[2]}</li>`).join('');
} else {
// Match longer answers like "Q1. Answer sentence..."
const longFormat = [...answerLine.matchAll(/(Q\d+)[.:]\s*(.+?)(?=Q\d+|$)/gs)];
formatted = longFormat.map(match => `<li><strong>${match[1]}</strong>: ${match[2].trim()}</li>`).join('');
}


if (formatted) {
typeHTMLContent("quizAnswers", `<ul class='list-disc pl-5'>${formatted}</ul>`, 8);
}
}

function toggleAnswers() {
document.getElementById("quizAnswers").classList.toggle("hidden");
}

// Owl & Splash
function updateOwlMessage(msg) {
document.getElementById("owlMessage").textContent = msg;
}

function dismissOwl() {
document.getElementById("owlAssistant").classList.add("opacity-0");
setTimeout(() => document.getElementById("owlAssistant").style.display = "none", 300);
}

function hideSplash() {
document.getElementById("splashScreen").classList.add("opacity-0");
setTimeout(() => document.getElementById("splashScreen").style.display = "none", 700);
}

function showParwaazToast(message) {
const toast = document.getElementById("parwaazToast");
const msg = document.getElementById("toastMsg");
msg.textContent = message;
toast.classList.add("toast-show");

setTimeout(() => {
hideToast();
}, 4000);
}

function hideToast() {
const toast = document.getElementById("parwaazToast");
toast.classList.remove("toast-show");
toast.classList.add("hidden");
}

// GENERATE Button Handler
document.getElementById("generateBtn").addEventListener("click", function () {
  const generateBtn = document.getElementById("generateBtn");

  const grade = document.getElementById("gradeSelect").value;
  const subject = document.getElementById("subjectSelect").value;
  const prompt = document.getElementById("promptInput").value.trim();
  const quiz_type = document.getElementById("quizTypeSelect").value;
  const quiz_count = document.getElementById("quizCountSelect").value;
  const flashcard_count = document.getElementById("flashCountSelect").value;

  // Validate all required fields
  if (!grade || !subject || !prompt || !quiz_type || !quiz_count || !flashcard_count) {
    showParwaazToast("Please fill out all fields before generating content.");
    return;
  }

  const payload = {
    grade,
    subject,
    prompt,
    quiz_type,
    quiz_count,
    flashcard_count
  };

  // 🚀 Disable Generate Button and Show Spinner
  generateBtn.disabled = true;
  generateBtn.innerHTML = `
    <svg class="animate-spin h-5 w-5 mr-2 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
    </svg>
    Generating...
  `;
  generateBtn.classList.add('opacity-50', 'cursor-not-allowed');

  updateOwlMessage("🧠 Generating content...");
  document.getElementById("learnArea").classList.add("hidden");
  document.getElementById("summaryOutput").textContent = "Typing...";
  document.getElementById("quizOutput").innerHTML = "";
  document.getElementById("quizAnswers").innerHTML = "";
  document.getElementById("quizAnswers").classList.add("hidden");
  document.getElementById("flashFront").textContent = "";
  document.getElementById("flashBack").textContent = "";
  document.getElementById("flashIndex").textContent = "";

  fetch('/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  .then(res => res.json())
  .then(data => {
    // Restore Button
    generateBtn.disabled = false;
    generateBtn.innerHTML = "Generate";
    generateBtn.classList.remove('opacity-50', 'cursor-not-allowed');

    document.getElementById("learnArea").classList.remove("hidden");
    const formatted = formatMarkdown(data.summary);
    typeHTMLContent("summaryOutput", formatted, 10);
    renderQuizTyped(data.quiz);
    flashcards = smartParseFlashcards(data.flashcards);
    flashIndex = 0;
    updateFlashcard();
    updateOwlMessage("Lesson ready! Flip cards or try the quiz.");
    document.getElementById("takeQuizSection").classList.remove("hidden");
  })
  .catch(error => {
    console.error(error);
    showParwaazToast("Something went wrong while generating!");

    // Restore Button on Error too
    generateBtn.disabled = false;
    generateBtn.innerHTML = "Generate";
    generateBtn.classList.remove('opacity-50', 'cursor-not-allowed');
  });
});



let quickQuizQuestions = [];
let currentQuestionIndex = 0;
let userAnswers = [];
let timerInterval;
let timeLeft = 60;

// MODAL: Open
function openQuizModal() {
  document.getElementById("quizModal").classList.remove("hidden");
  document.getElementById("mainContent").classList.add("blur-sm");
}

// MODAL: Close
function closeQuizModal() {
  clearInterval(timerInterval);
  document.getElementById("quizModal").classList.add("hidden");
  document.getElementById("mainContent").classList.remove("blur-sm");

  // Reset state
  document.getElementById("startQuizBtn").classList.remove("hidden");
  document.getElementById("loadingSpinner").classList.add("hidden");
  document.getElementById("quizArea").classList.add("hidden");
  document.getElementById("resultArea").classList.add("hidden");
}

// Start Quiz (inside Modal)
function startModalQuiz() {
  document.getElementById("startQuizBtn").classList.add("hidden");
  document.getElementById("loadingSpinner").classList.remove("hidden");

  fetch('/generate_quiz', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert("Failed to load quiz. Try again!");
        return;
      }

      quickQuizQuestions = data.questions;
      currentQuestionIndex = 0;
      userAnswers = [];

      document.getElementById("loadingSpinner").classList.add("hidden");
      document.getElementById("quizArea").classList.remove("hidden");
      showModalQuestion();
      startModalTimer();
    })
    .catch(err => {
      console.error(err);
      alert("Failed to load quiz. Please try again.");
    });
}

// Timer
function startModalTimer() {
  timeLeft = 60;
  document.getElementById("timer").textContent = `${timeLeft}s`;

  timerInterval = setInterval(() => {
    timeLeft--;
    document.getElementById("timer").textContent = `${timeLeft}s`;

    if (timeLeft <= 0) {
      clearInterval(timerInterval);
      submitModalQuiz();
    }
  }, 1000);
}

// Show Question
function showModalQuestion() {
  const questionObj = quickQuizQuestions[currentQuestionIndex];
  document.getElementById("questionText").innerHTML = `<strong>Q${currentQuestionIndex + 1}:</strong> ${questionObj.question}`;

  const optionsHtml = questionObj.options.map(opt => {
    const optionValue = opt.charAt(0);
    const checked = userAnswers[currentQuestionIndex] === optionValue ? 'checked' : '';
    return `
      <label class="block p-2 border rounded mb-2 cursor-pointer">
        <input type="radio" name="option" value="${optionValue}" ${checked} class="mr-2">${opt}
      </label>
    `;
  }).join('');

  document.getElementById("optionsContainer").innerHTML = optionsHtml;

  updateModalNavButtons();
}

// Nav Buttons
function updateModalNavButtons() {
  document.getElementById("prevBtn").disabled = (currentQuestionIndex === 0);
  document.getElementById("nextBtn").textContent = (currentQuestionIndex === quickQuizQuestions.length - 1) ? "Submit" : "Next";
}

// Next Question
function nextQuestion() {
  const selected = document.querySelector('input[name="option"]:checked');
  if (!selected) {
    alert("Please select an answer!");
    return;
  }

  userAnswers[currentQuestionIndex] = selected.value;

  if (currentQuestionIndex < quickQuizQuestions.length - 1) {
    currentQuestionIndex++;
    showModalQuestion();
  } else {
    clearInterval(timerInterval);
    submitModalQuiz();
  }
}

// Previous Question
function prevQuestion() {
  if (currentQuestionIndex > 0) {
    currentQuestionIndex--;
    showModalQuestion();
  }
}

// Submit
function submitModalQuiz() {
  document.getElementById("quizArea").classList.add("hidden");
  document.getElementById("resultArea").classList.remove("hidden");

  let score = 0;
  quickQuizQuestions.forEach((q, idx) => {
    if (userAnswers[idx] && userAnswers[idx] === q.answer) {
      score++;
    }
  });

  document.getElementById("scoreText").textContent = `🎯 You scored ${score} out of ${quickQuizQuestions.length}!`;
  // Save score to backend
  fetch('/save_quiz_result', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      score: score,
      total: quickQuizQuestions.length,
      questions: quickQuizQuestions,  // Pass full questions
      user_answers: userAnswers        // Pass user answers
    })
  });

}

// Retry
function retryQuiz() {
  closeQuizModal();
  openQuizModal();
}


function handleBegin() {
  fetch('/check_login_status')
    .then(response => response.json())
    .then(data => {
      if (data.logged_in) {
        hideSplash();
      } else {
        // Show Parwaaz Toast nicely
        showParwaazToast("Please login first to start your learning journey!");

        // After 1.5 seconds, redirect to login
        setTimeout(() => {
          window.location.href = "/login";
        }, 1500);
      }
    })
    .catch(error => {
      console.error('Error checking login status:', error);
      window.location.href = "/login"; // fallback
    });
}