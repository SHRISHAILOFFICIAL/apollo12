"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter, useParams } from "next/navigation";
import { examTimerService } from "@/lib/services/exam-timer.service";

interface Question {
  id: number;
  text: string;
  option_a: string;
  option_b: string;
  option_c: string;
  option_d: string;
  marks: number;
}

export default function ExamPage() {
  const router = useRouter();
  const params = useParams();
  const [attemptId, setAttemptId] = useState<number | null>(null);
  const [examTitle, setExamTitle] = useState("");
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<{ [key: number]: string }>({});
  const [remainingSeconds, setRemainingSeconds] = useState(0);
  const [timerStatus, setTimerStatus] = useState<
    "running" | "timeout" | "completed"
  >("running");
  const [loading, setLoading] = useState(true);
  const timerCheckIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const localCountdownRef = useRef<NodeJS.Timeout | null>(null);

  // Submit exam function
  const handleSubmitExam = async () => {
    if (!attemptId) return;

    const confirmSubmit = window.confirm(
      "Are you sure you want to submit the exam?"
    );
    if (!confirmSubmit) return;

    try {
      const result = await examTimerService.submitExam(attemptId);

      // Clear all timers
      if (timerCheckIntervalRef.current) {
        clearInterval(timerCheckIntervalRef.current);
      }
      if (localCountdownRef.current) {
        clearInterval(localCountdownRef.current);
      }

      alert(
        `Exam Submitted!\n\nScore: ${result.score}/${result.total_marks}\nPercentage: ${result.percentage}%\nCorrect Answers: ${result.correct_answers}/${result.total_questions}`
      );

      router.push("/dashboard");
    } catch (err: any) {
      console.error("Failed to submit exam", err);
      alert(err.response?.data?.error || "Failed to submit exam.");
    }
  };

  // Start exam on mount
  useEffect(() => {
    const startExam = async () => {
      try {
        // Check if user is authenticated
        if (typeof window !== "undefined") {
          const token = localStorage.getItem("access_token");
          if (!token) {
            alert("Please login to start the exam");
            router.push("/auth/login");
            return;
          }
        }

        // Start exam with Redis timer
        const startResponse = await examTimerService.startExam(
          Number(params.id)
        );

        setAttemptId(startResponse.attempt_id);
        setExamTitle(startResponse.exam_title);
        setRemainingSeconds(startResponse.remaining_seconds);

        // Get questions
        const questionsResponse = await examTimerService.getExamQuestions(
          startResponse.attempt_id
        );
        setQuestions(questionsResponse.questions);
        setAnswers(questionsResponse.saved_answers || {});

        setLoading(false);
        setTimerStatus("running");
      } catch (err: any) {
        console.error("Failed to start exam - Full error:", err);
        console.error("Error response:", err.response);
        console.error("Error data:", err.response?.data);
        console.error("Error status:", err.response?.status);

        // Handle specific error cases
        if (err.response?.status === 401) {
          alert("Authentication failed. Please login again.");
          router.push("/auth/login");
        } else if (err.response?.status === 404) {
          alert("Exam not found.");
          router.push("/dashboard");
        } else if (err.response?.status === 400) {
          const errorMsg =
            err.response?.data?.error ||
            err.response?.data?.detail ||
            "Invalid exam request.";
          alert(`Cannot start exam: ${errorMsg}`);
          router.push("/dashboard");
        } else {
          const errorMsg =
            err.response?.data?.error ||
            err.response?.data?.detail ||
            err.message ||
            "Failed to start exam.";
          alert(`Cannot start exam: ${errorMsg}`);
          router.push("/dashboard");
        }
      }
    };

    startExam();

    // Cleanup on unmount
    return () => {
      if (timerCheckIntervalRef.current) {
        clearInterval(timerCheckIntervalRef.current);
      }
      if (localCountdownRef.current) {
        clearInterval(localCountdownRef.current);
      }
    };
  }, [params.id, router]);

  // Poll server for remaining time every 10 seconds
  useEffect(() => {
    if (!attemptId || timerStatus !== "running") return;

    const checkRemainingTime = async () => {
      try {
        const response = await examTimerService.getRemainingTime(attemptId);

        if (response.status === "timeout") {
          setTimerStatus("timeout");
          setRemainingSeconds(0);

          // Clear timers
          if (timerCheckIntervalRef.current) {
            clearInterval(timerCheckIntervalRef.current);
          }
          if (localCountdownRef.current) {
            clearInterval(localCountdownRef.current);
          }

          alert("Exam time has expired! Submitting automatically...");
          await handleSubmitExam();
        } else if (response.status === "completed") {
          setTimerStatus("completed");
          router.push("/dashboard");
        } else {
          // Sync with server time
          setRemainingSeconds(response.remaining_seconds);
        }
      } catch (err) {
        console.error("Failed to check remaining time", err);
      }
    };

    // Check immediately
    checkRemainingTime();

    // Then check every 10 seconds
    timerCheckIntervalRef.current = setInterval(checkRemainingTime, 10000);

    return () => {
      if (timerCheckIntervalRef.current) {
        clearInterval(timerCheckIntervalRef.current);
      }
    };
  }, [attemptId, timerStatus, router]);

  // Local countdown (UI only, server is source of truth)
  useEffect(() => {
    if (remainingSeconds <= 0 || timerStatus !== "running") return;

    localCountdownRef.current = setInterval(() => {
      setRemainingSeconds((prev) => Math.max(0, prev - 1));
    }, 1000);

    return () => {
      if (localCountdownRef.current) {
        clearInterval(localCountdownRef.current);
      }
    };
  }, [remainingSeconds, timerStatus]);

  // Submit answer
  const handleOptionSelect = async (selectedOption: string) => {
    if (!attemptId || timerStatus !== "running") return;

    const question = questions[currentQuestionIndex];
    setAnswers((prev) => ({ ...prev, [question.id]: selectedOption }));

    try {
      await examTimerService.submitAnswer({
        attempt_id: attemptId,
        question_id: question.id,
        selected_option: selectedOption,
      });
    } catch (err: any) {
      console.error("Failed to save answer", err);

      if (err.response?.status === 410) {
        // 410 Gone = Timer expired
        alert("Exam time has expired!");
        setTimerStatus("timeout");
        await handleSubmitExam();
      }
    }
  };

  if (loading || questions.length === 0) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="mb-4 text-lg font-medium">Loading Exam...</div>
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-indigo-600 border-t-transparent mx-auto"></div>
        </div>
      </div>
    );
  }

  const currentQuestion = questions[currentQuestionIndex];
  const options = [
    { key: "A", text: currentQuestion.option_a },
    { key: "B", text: currentQuestion.option_b },
    { key: "C", text: currentQuestion.option_c },
    { key: "D", text: currentQuestion.option_d },
  ];

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header with Timer */}
      <header className="bg-white shadow px-6 py-4 flex justify-between items-center sticky top-0 z-10">
        <h1 className="text-xl font-bold text-gray-800">{examTitle}</h1>

        <div
          className={`text-xl font-mono font-bold ${
            examTimerService.isTimeCritical(remainingSeconds)
              ? "text-red-600 animate-pulse"
              : examTimerService.isTimeWarning(remainingSeconds)
              ? "text-orange-600"
              : "text-gray-700"
          }`}
        >
          ⏱️ {examTimerService.formatTime(remainingSeconds)}
        </div>

        <button
          onClick={handleSubmitExam}
          disabled={timerStatus !== "running"}
          className="bg-green-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Submit Exam
        </button>
      </header>

      <div className="flex-1 flex overflow-hidden">
        {/* Question Navigator Sidebar */}
        <aside className="w-64 bg-white border-r overflow-y-auto hidden md:block p-4">
          <h3 className="font-semibold mb-4 text-gray-700">
            Questions ({questions.length})
          </h3>
          <div className="grid grid-cols-4 gap-2">
            {questions.map((q, idx) => (
              <button
                key={q.id}
                onClick={() => setCurrentQuestionIndex(idx)}
                className={`h-10 w-10 rounded flex items-center justify-center text-sm font-medium transition-all
                  ${
                    currentQuestionIndex === idx
                      ? "ring-2 ring-indigo-500 scale-110"
                      : ""
                  }
                  ${
                    answers[q.id]
                      ? "bg-green-500 text-white hover:bg-green-600"
                      : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                  }`}
              >
                {idx + 1}
              </button>
            ))}
          </div>

          {/* Progress Summary */}
          <div className="mt-6 p-3 bg-gray-50 rounded">
            <div className="text-sm text-gray-600 space-y-1">
              <div className="flex justify-between">
                <span>Answered:</span>
                <span className="font-semibold text-green-600">
                  {Object.keys(answers).length}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Remaining:</span>
                <span className="font-semibold text-gray-800">
                  {questions.length - Object.keys(answers).length}
                </span>
              </div>
            </div>
          </div>
        </aside>

        {/* Main Question Area */}
        <main className="flex-1 p-6 overflow-y-auto">
          <div className="max-w-3xl mx-auto bg-white rounded-lg shadow-sm p-8 min-h-[400px]">
            {/* Question Header */}
            <div className="mb-6">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-500">
                  Question {currentQuestionIndex + 1} of {questions.length}
                </span>
                <span className="text-sm font-medium text-indigo-600 bg-indigo-50 px-3 py-1 rounded-full">
                  {currentQuestion.marks}{" "}
                  {currentQuestion.marks === 1 ? "Mark" : "Marks"}
                </span>
              </div>
              <h2 className="text-xl font-semibold text-gray-900 mt-2 leading-relaxed">
                {currentQuestion.text}
              </h2>
            </div>

            {/* Options */}
            <div className="space-y-3">
              {options.map((option) => (
                <button
                  key={option.key}
                  onClick={() => handleOptionSelect(option.key)}
                  disabled={timerStatus !== "running"}
                  className={`w-full text-left p-4 rounded-lg border-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed
                    ${
                      answers[currentQuestion.id] === option.key
                        ? "border-indigo-600 bg-indigo-50 shadow-md"
                        : "border-gray-200 hover:border-indigo-300 hover:bg-gray-50"
                    }`}
                >
                  <div className="flex items-start">
                    <span
                      className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center font-semibold mr-3 ${
                        answers[currentQuestion.id] === option.key
                          ? "bg-indigo-600 text-white"
                          : "bg-gray-100 text-gray-600"
                      }`}
                    >
                      {option.key}
                    </span>
                    <span className="flex-1 text-gray-800">{option.text}</span>
                  </div>
                </button>
              ))}
            </div>

            {/* Navigation */}
            <div className="mt-8 flex justify-between items-center">
              <button
                onClick={() =>
                  setCurrentQuestionIndex((prev) => Math.max(0, prev - 1))
                }
                disabled={currentQuestionIndex === 0}
                className="px-6 py-2 border-2 border-gray-300 rounded-lg text-gray-700 font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition-colors"
              >
                ← Previous
              </button>

              <div className="text-sm text-gray-500">
                {answers[currentQuestion.id] ? (
                  <span className="text-green-600 font-medium">✓ Answered</span>
                ) : (
                  <span className="text-gray-400">Not answered</span>
                )}
              </div>

              <button
                onClick={() =>
                  setCurrentQuestionIndex((prev) =>
                    Math.min(questions.length - 1, prev + 1)
                  )
                }
                disabled={currentQuestionIndex === questions.length - 1}
                className="px-6 py-2 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Next →
              </button>
            </div>
          </div>
        </main>
      </div>

      {/* Timeout overlay */}
      {timerStatus === "timeout" && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-md text-center">
            <div className="text-6xl mb-4">⏰</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Time's Up!
            </h2>
            <p className="text-gray-600">
              Your exam has been automatically submitted.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
