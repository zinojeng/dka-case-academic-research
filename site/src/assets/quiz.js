// 單選題評分與作答進度；瀏覽器與 Node 測試共用，不依賴 DOM。

export function gradeAnswer(quiz, selected) {
  if (!Number.isInteger(selected) || selected < 0 || selected >= quiz.options.length) {
    throw new RangeError(`選項 ${selected} 不在第 ${quiz.id} 題的範圍內`);
  }
  return {
    correct: selected === quiz.answer,
    selectedText: quiz.options[selected],
    correctIndex: quiz.answer,
    correctText: quiz.options[quiz.answer],
  };
}

// answers: { quizId: selectedIndex }
export function summarize(quizzes, answers) {
  let answered = 0;
  let correct = 0;
  for (const quiz of quizzes) {
    if (!Object.hasOwn(answers, quiz.id)) continue;
    answered += 1;
    if (answers[quiz.id] === quiz.answer) correct += 1;
  }
  return { answered, correct, total: quizzes.length };
}

// localStorage 內容可能是舊版、被手動改過或壞掉：只留下仍存在的題目與有效選項。
export function restoreAnswers(stored, quizzes) {
  let parsed;
  try {
    parsed = JSON.parse(stored ?? '{}');
  } catch {
    return {};
  }
  if (parsed === null || typeof parsed !== 'object' || Array.isArray(parsed)) return {};
  const answers = {};
  for (const quiz of quizzes) {
    const value = parsed[quiz.id];
    if (Number.isInteger(value) && value >= 0 && value < quiz.options.length) answers[quiz.id] = value;
  }
  return answers;
}
