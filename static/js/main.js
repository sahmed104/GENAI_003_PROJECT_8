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

function parseFlashcards(raw) {
const cards = [];
const lines = raw.split('\n');

for (let i = 0; i < lines.length; i++) {
const line = lines[i].trim();

// Format 1: Numbered format - "1. Term"
if (/^\d+\.\s+/.test(line)) {
const term = line.replace(/^\d+\.\s+/, '').trim();
const nextLine = lines[i + 1]?.trim();
if (nextLine?.toLowerCase().startsWith("explanation:")) {
  const explanation = nextLine.split(":").slice(1).join(":").trim();
  cards.push({ term, definition: explanation });
  i++;
  continue;
}
}

// Format 2: Term: Explanation:
if (line.toLowerCase().startsWith("term:")) {
const term = line.split(":").slice(1).join(":").trim();
const nextLine = lines[i + 1]?.trim();
if (nextLine?.toLowerCase().startsWith("explanation:")) {
  const explanation = nextLine.split(":").slice(1).join(":").trim();
  cards.push({ term, definition: explanation });
  i++;
  continue;
}
}

// Format 3: Term - Explanation on same line
if (/^.*term.*:.*explanation.*:/i.test(line)) {
const [_, termPart, explanationPart] = line.match(/term\s*:\s*(.*?)\s*-+\s*explanation\s*:\s*(.*)/i) || [];
if (termPart && explanationPart) {
  cards.push({ term: termPart.trim(), definition: explanationPart.trim() });
}
}
}

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

// Continue with generation...
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
document.getElementById("learnArea").classList.remove("hidden");
const formatted = formatMarkdown(data.summary);
typeHTMLContent("summaryOutput", formatted, 10);
renderQuizTyped(data.quiz);
flashcards = parseFlashcards(data.flashcards);
flashIndex = 0;
updateFlashcard();
updateOwlMessage("✅ Lesson ready! Flip cards or try the quiz.");
})
.catch(error => {
console.error(error);
alert("Something went wrong!");
});
});