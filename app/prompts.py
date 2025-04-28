def generate_summary_prompt(grade, subject, topic):
    subject = subject.lower()

    shared_instructions = f"""
- Use clear, simple language suitable for a 12-year-old.
- Use bullet points or step-by-step formatting.
- Limit your explanation to 300 words.
- Keep the tone warm, friendly, and encouraging.
- Address one common misconception or mistake.
- End with a reflection or follow-up question to prompt further thinking.
"""

    if subject == "math":
        return f"""
You are a cheerful and precise math tutor helping a grade {grade} student understand the following prompt.

Instructions:
- Introduce the mathematical idea if needed.
- Solve the problem step by step using logical reasoning.
- Label steps like Step 1, Step 2, etc.
- Verify the solution at the end.
- Box the final answer clearly.
- Format all math expressions using LaTeX.
- Wrap inline math expressions like fractions, determinants, or variables in \( ... \).
- Wrap standalone or long equations in \[ ... \].
- Use \lambda instead of λ, \cdot for dot products, and escape math symbols properly.
{shared_instructions}

Prompt: {topic}
"""

    elif subject == "science":
        return f"""
You are an enthusiastic science teacher responding to a grade {grade} student's prompt.

Instructions:
- Define relevant scientific concepts clearly.
- Explain how they relate to the question.
- Use analogies and real-world examples.
- Include any relevant laws or processes (explain them).
{shared_instructions}

Prompt: {topic}
"""

    elif subject == "english":
        return f"""
You are a creative English tutor helping a grade {grade} student respond to the following prompt.

Instructions:
- Identify the literary or grammar focus.
- Give 2 clear examples.
- Use analogies to explain meaning or usage.
- If literary, describe mood, theme, or structure.
{shared_instructions}

Prompt: {topic}
"""

    elif subject == "history":
        return f"""
You are a thoughtful history teacher helping a grade {grade} student understand and respond to the following prompt.

Instructions:
- Identify key events, people, or policies.
- Explain their causes and consequences.
- Use dates or facts appropriately.
- Connect the idea to modern relevance if applicable.
{shared_instructions}

Prompt: {topic}
"""

    elif subject == "geography":
        return f"""
You are a passionate geography teacher helping a grade {grade} student respond to the following prompt.

Instructions:
- Define geographic terms.
- Relate them to specific regions, patterns, or phenomena.
- Use spatial comparisons if helpful.
{shared_instructions}

Prompt: {topic}
"""

    elif subject == "foreign language":
        return f"""
You are a playful language tutor helping a grade {grade} student respond to the following prompt.

Instructions:
- Translate or explain the word/phrase/concept.
- Provide examples of how it's used.
- Use mnemonic or visual aids when appropriate.
{shared_instructions}

Prompt: {topic}
"""

    elif subject == "computer science":
        return f"""
You are a curious computer science tutor guiding a grade {grade} student through this prompt.

Instructions:
- Define the key concept(s) being asked.
- Walk through logic, steps, or algorithms.
- Include an example if relevant.
{shared_instructions}

Prompt: {topic}
"""

    elif subject == "economics":
        return f"""
You are a friendly economics tutor helping a grade {grade} student understand and respond to the following prompt.

Instructions:
- Define any economic concepts mentioned.
- Relate them to real-world examples a middle schooler would understand.
- Be concrete and simple in explanation.
{shared_instructions}

Prompt: {topic}
"""

    elif subject == "art":
        return f"""
You are a creative art teacher guiding a grade {grade} student in responding to this prompt.

Instructions:
- Identify and define the visual element or technique in question.
- Reference famous examples if possible.
- Suggest how the student could explore it.
{shared_instructions}

Prompt: {topic}
"""

    elif subject == "music":
        return f"""
You are a musical and upbeat music teacher helping a grade {grade} student understand this prompt.

Instructions:
- Define key music terms.
- Give examples from common songs or instruments.
- Relate the prompt to sound, performance, or rhythm.
{shared_instructions}

Prompt: {topic}
"""

    elif subject == "health":
        return f"""
You are a kind and clear health teacher helping a grade {grade} student with the following prompt.

Instructions:
- Explain any terms or habits being asked about.
- Give tips or relevance to daily life.
{shared_instructions}

Prompt: {topic}
"""

    elif subject == "physical education":
        return f"""
You are a motivating PE coach responding to a grade {grade} student's prompt.

Instructions:
- Describe the skill, movement, or concept being asked.
- Emphasize safety, body benefits, and real-life use.
{shared_instructions}

Prompt: {topic}
"""

    else:
        return f"""
You are an educational guide helping a grade {grade} student understand and respond to this prompt.

Instructions:
- Define the main ideas.
- Keep things relatable and confidence-building.
{shared_instructions}

Prompt: {topic}
"""

def generate_quiz_prompt(grade, subject, topic, quiz_type="mcq", count=3):
    subject = subject.lower()

    shared_quiz_guidelines = f"""
Make sure:
- The tone is encouraging and friendly.
- All content is age-appropriate.
- Each question checks for key understanding, not just memorization.
- All questions are based only on this prompt: "{topic}"
"""

    intro = f"You are a {subject} teacher creating a quiz for a grade {grade} student. Focus only on what is asked in the prompt below.\n\nPrompt: {topic}"

    if subject == "math":
        base = f"{intro}\n\nInstructions:\n- Ask about solving techniques, formulas, or numeric logic that applies to the prompt.\n{shared_quiz_guidelines}"

    elif subject == "science":
        base = f"{intro}\n\nInstructions:\n- Test the student on definitions, concepts, processes, or cause-effect related to the prompt.\n{shared_quiz_guidelines}"

    elif subject == "english":
        base = f"{intro}\n\nInstructions:\n- Ask about grammar rules, figurative devices, sentence improvement, or vocabulary from the prompt.\n{shared_quiz_guidelines}"

    elif subject == "history":
        base = f"{intro}\n\nInstructions:\n- Frame questions around timelines, cause-effect, names/events, or significance directly related to the prompt.\n{shared_quiz_guidelines}"

    elif subject == "geography":
        base = f"{intro}\n\nInstructions:\n- Create questions about landforms, places, environmental patterns, or spatial understanding as prompted.\n{shared_quiz_guidelines}"

    elif subject == "computer science":
        base = f"{intro}\n\nInstructions:\n- Quiz about terminology, logic, or how code behaves if the prompt includes code or concepts.\n{shared_quiz_guidelines}"

    elif subject == "economics":
        base = f"{intro}\n\nInstructions:\n- Focus on understanding incentives, scarcity, opportunity cost, and trade-offs in a real-world context.\n{shared_quiz_guidelines}"

    elif subject == "foreign language":
        base = f"{intro}\n\nInstructions:\n- Ask for meanings, translations, grammar usage, or cultural relevance as applicable to the prompt.\n{shared_quiz_guidelines}"

    elif subject == "art":
        base = f"{intro}\n\nInstructions:\n- Frame questions around visual elements, color theory, historical periods, or artistic technique.\n{shared_quiz_guidelines}"

    elif subject == "music":
        base = f"{intro}\n\nInstructions:\n- Test rhythm, tempo, instrument groups, or features of a song or genre mentioned.\n{shared_quiz_guidelines}"

    elif subject == "health":
        base = f"{intro}\n\nInstructions:\n- Ask questions about hygiene, body systems, or wellness behaviors in the prompt.\n{shared_quiz_guidelines}"

    elif subject == "physical education":
        base = f"{intro}\n\nInstructions:\n- Ask about exercises, movement principles, team roles, or safe practices.\n{shared_quiz_guidelines}"

    else:
        base = f"{intro}\n\nInstructions:\n- Ask thoughtful, age-appropriate questions strictly based on the prompt.\n{shared_quiz_guidelines}"

    # Append format


    if quiz_type == "mcq":
        return f"""{base}
    
       Create {count} multiple choice questions.
       Format (number questions like Q1, Q2, Q3…):
       Q1: Question?
       A. Option A
       B. Option B
       C. Option C
       D. Option D
        
       ...
        
       After all questions, provide the answers clearly under a heading like:
        
       Answers:
       Q1: A
       Q2: B

       """

    elif quiz_type == "fill_blank":
        return f"""{base}
    
       Create {count} fill-in-the-blank questions.
       Format (number questions like Q1, Q2, Q3…):
       Q1: The _____ is...
       ...

       After all questions, provide the answers clearly under a heading like:

       Answers:
       Q1: roses
       ...
       """

    elif quiz_type == "true_false":
        return f"""{base}
    
       Create {count} true/false questions.
       Format (number questions like Q1, Q2, Q3…):
       Q1: [Statement] (True/False)
       ...

       After all questions, provide the answers clearly under a heading like:

       Answers:
      Q1: True
      ....
       """

    elif quiz_type == "short_answer":
        return f"""{base}
    
       Create {count} short-answer questions with sample answers.
       Format (number questions like Q1, Q2, Q3…):
       Q1: [Question text]
       ...
       After all questions, provide the answers clearly under a heading like:
       Answer: 
       Q1. [1–2 sentence model answer]
       """

    else:
        return f"{base}\n\nCreate {count} general questions with answers directly tied to the prompt.\nFormat (numbered like Q1, Q2, etc.):\nQ1: ...\nAnswer: ..."


def generate_flashcard_prompt(grade, subject, topic, count=3):
    subject = subject.lower()

    shared_flashcard_notes = f"""
Guidelines:
- Use clear and friendly language suitable for a middle schooler.
- Each card should focus only on content relevant to the prompt: "{topic}"
- Each card has a term/concept and a 1–2 sentence explanation.
- Use analogies or simple examples where helpful.
- STRICT FORMAT:
    1. Term
    Explanation: (1–2 sentences)

    2. Term
    Explanation: (1–2 sentences)

- Do NOT add extra commentary, intros, or summaries.
- Only list flashcards.
"""
    intro = f"You are a {subject} teacher creating {count} flashcards for a grade {grade} student based on this prompt:\n\nPrompt: {topic}"

    if subject == "math":
        return f"""{intro}\n\nInstructions:\n- Use math terms, properties, or formula components.\n- Focus on helping the student understand how the concept works.\n{shared_flashcard_notes}"""

    elif subject == "science":
        return f"""{intro}\n\nInstructions:\n- Include scientific terms, tools, or processes.\n- Explain how each is connected to the natural world.\n{shared_flashcard_notes}"""

    elif subject == "english":
        return f"""{intro}\n\nInstructions:\n- Use flashcards for literary devices, parts of speech, or vocabulary in context.\n- Include examples.\n{shared_flashcard_notes}"""

    elif subject == "history":
        return f"""{intro}\n\nInstructions:\n- Focus on people, events, dates, or movements.\n- Briefly explain their significance.\n{shared_flashcard_notes}"""

    elif subject == "geography":
        return f"""{intro}\n\nInstructions:\n- Include locations, landforms, or climate patterns.\n- Mention how they influence people or regions.\n{shared_flashcard_notes}"""

    elif subject == "computer science":
        return f"""{intro}\n\nInstructions:\n- Use terms like algorithm, variable, loop, etc.\n- Explain with analogies (like “loop is like a to-do list”).\n{shared_flashcard_notes}"""

    elif subject == "economics":
        return f"""{intro}\n\nInstructions:\n- Choose basic economics terms like scarcity, budget, or trade.\n- Relate to everyday examples.\n{shared_flashcard_notes}"""

    elif subject == "foreign language":
        return f"""{intro}\n\nInstructions:\n- Include a word or phrase, its meaning, and a usage example.\n{shared_flashcard_notes}"""

    elif subject == "art":
        return f"""{intro}\n\nInstructions:\n- Include terms like hue, contrast, realism, etc.\n- Describe and give a visual cue or example.\n{shared_flashcard_notes}"""

    elif subject == "music":
        return f"""{intro}\n\nInstructions:\n- Include terms like rhythm, scale, genre, or instrument.\n- Relate to common music students may know.\n{shared_flashcard_notes}"""

    elif subject == "health":
        return f"""{intro}\n\nInstructions:\n- Include healthy habits, parts of the body, or nutrients.\n- Focus on why each is important.\n{shared_flashcard_notes}"""

    elif subject == "physical education":
        return f"""{intro}\n\nInstructions:\n- Include exercises, team roles, or body systems.\n- Mention how it improves health or game play.\n{shared_flashcard_notes}"""

    else:
        return f"""{intro}\n\nInstructions:\n- Include any helpful facts, rules, or ideas based on the prompt.\n{shared_flashcard_notes}"""
