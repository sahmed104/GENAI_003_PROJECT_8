function openReportModal(quiz) {
    console.log("openReportModal triggered!", quiz);
  
    const modal = document.getElementById("reportModal");
    const reportContent = document.getElementById("reportContent");
    reportContent.innerHTML = "";
  
    const questions = JSON.parse(quiz.questions_json);
    const userAnswers = JSON.parse(quiz.user_answers_json);
  
    questions.forEach((q, idx) => {
      const userAnswer = userAnswers[idx];
      const correctAnswer = q.answer;
      const isCorrect = userAnswer === correctAnswer;
  
      let resultHTML = `
        <div class="p-4 border rounded-lg bg-gray-50">
          <div class="flex justify-between items-center cursor-pointer" onclick="toggleAccordion('accordion${idx}')">
            <div>
              <p class="font-semibold text-gray-800">Q${idx + 1}: ${q.question}</p>
              <p class="text-sm ${isCorrect ? 'text-green-700' : 'text-red-700'}">
                Your Answer: ${userAnswer} ${isCorrect ? '✅' : '❌'}
              </p>
            </div>
            <div class="text-xl text-gray-400" id="arrow${idx}">+</div>
          </div>
  
          <div id="accordion${idx}" class="hidden mt-3 space-y-2">
      `;
  
      // Options inside accordion
      q.options.forEach(option => {
        const optionLetter = option.charAt(0);
        const isSelected = userAnswer === optionLetter;
        const isCorrectOption = correctAnswer === optionLetter;
  
        resultHTML += `
          <div class="flex items-center space-x-2 ${isSelected ? (isCorrectOption ? 'text-green-700' : 'text-red-700') : 'text-gray-700'}">
            <input type="radio" disabled ${isSelected ? 'checked' : ''}>
            <label>${option}</label>
          </div>
        `;
      });
  
      if (!isCorrect) {
        resultHTML += `
          <p class="text-sm text-green-700 mt-2">
            Correct Answer: ${correctAnswer}
          </p>
        `;
      }
  
      resultHTML += `
          </div>
        </div>
      `;
  
      reportContent.innerHTML += resultHTML;
    });
  
    modal.classList.remove("hidden");
  }
  
  // Toggle Accordion
  function toggleAccordion(id) {
    const section = document.getElementById(id);
    section.classList.toggle('hidden');
  
    const arrow = document.getElementById('arrow' + id.replace('accordion', ''));
    if (section.classList.contains('hidden')) {
      arrow.textContent = '+';
    } else {
      arrow.textContent = '−';
    }
  }
  
  
  function closeReportModal() {
    document.getElementById("reportModal").classList.add("hidden");
  }
  
  function openReportModalFromButton(btn) {
    const quizData = btn.getAttribute('data-quiz');
    const quiz = JSON.parse(quizData);
    openReportModal(quiz);
  }
  