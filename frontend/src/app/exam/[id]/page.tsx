"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter, useParams } from "next/navigation";
import { examTimerService } from "@/lib/services/exam-timer.service";
import { MathText } from "@/components/MathText";

interface Question {
  id: number;
  text: string;
  option_a: string;
  option_b: string;
  option_c: string;
  option_d: string;
  marks: number;
  section_name: string;
  section_order: number;
  question_number: number;
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

  // New state for UI
  const [activeSection, setActiveSection] = useState<string>("");
  const [markedForReview, setMarkedForReview] = useState<Set<number>>(new Set());

  // Report Issue state
  const [showReportModal, setShowReportModal] = useState(false);
  const [issueType, setIssueType] = useState("");
  const [issueDescription, setIssueDescription] = useState("");

  // Answer Review state
  const [showReviewModal, setShowReviewModal] = useState(false);

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

      // Redirect directly to results page (no popup needed)
      router.push(`/results/${attemptId}`);
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

        console.log("Questions response:", questionsResponse);
        console.log("First question:", questionsResponse.questions[0]);

        setQuestions(questionsResponse.questions);
        setAnswers(questionsResponse.saved_answers || {});

        setLoading(false);
        setTimerStatus("running");
      } catch (err: any) {
        console.error("Failed to start exam", err);

        // Handle specific error cases
        if (err.response?.status === 401) {
          alert("Authentication failed. Please login again.");
          router.push("/auth/login");
        } else if (err.response?.status === 404) {
          alert("Exam not found.");
          router.push("/dashboard");
        } else if (err.response?.status === 400) {
          const errorMsg = err.response?.data?.error || "Invalid exam request.";
          alert(`Cannot start exam: ${errorMsg}`);
          router.push("/dashboard");
        } else {
          const errorMsg = err.response?.data?.error || "Failed to start exam.";
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
          alert("Exam time has expired! Submitting automatically...");
          await handleSubmitExam();
        } else if (response.status === "completed") {
          setTimerStatus("completed");
          router.push("/dashboard");
        } else {
          setRemainingSeconds(response.remaining_seconds);
        }
      } catch (err) {
        console.error("Failed to check remaining time", err);
      }
    };

    checkRemainingTime();
    timerCheckIntervalRef.current = setInterval(checkRemainingTime, 10000);

    return () => {
      if (timerCheckIntervalRef.current) {
        clearInterval(timerCheckIntervalRef.current);
      }
    };
  }, [attemptId, timerStatus, router]);

  // Local countdown
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

  // Group questions by section
  const sections = Array.from(new Set(questions.map(q => q.section_name)));

  // Calculate section statistics
  const getSectionStats = (sectionName: string) => {
    const sectionQuestions = questions.filter(q => q.section_name === sectionName);
    const answered = sectionQuestions.filter(q => answers[q.id]).length;
    const marked = sectionQuestions.filter(q => markedForReview.has(q.id)).length;
    const unanswered = sectionQuestions.length - answered;
    return { total: sectionQuestions.length, answered, marked, unanswered };
  };

  // Initialize active section
  useEffect(() => {
    if (sections.length > 0 && !activeSection) {
      setActiveSection(sections[0]);
    }
  }, [sections, activeSection]);

  // Navigation handlers
  const handleSectionChange = (section: string) => {
    setActiveSection(section);
    const firstQuestionOfSection = questions.findIndex(q => q.section_name === section);
    if (firstQuestionOfSection !== -1) {
      setCurrentQuestionIndex(firstQuestionOfSection);
    }
  };

  const handleMarkForReview = () => {
    const questionId = questions[currentQuestionIndex].id;
    setMarkedForReview(prev => {
      const newSet = new Set(prev);
      if (newSet.has(questionId)) {
        newSet.delete(questionId);
      } else {
        newSet.add(questionId);
      }
      return newSet;
    });
  };

  const handleNext = () => {
    if (currentQuestionIndex < questions.length - 1) {
      const nextIndex = currentQuestionIndex + 1;
      setCurrentQuestionIndex(nextIndex);
      if (questions[nextIndex].section_name !== activeSection) {
        setActiveSection(questions[nextIndex].section_name);
      }
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      const prevIndex = currentQuestionIndex - 1;
      setCurrentQuestionIndex(prevIndex);
      if (questions[prevIndex].section_name !== activeSection) {
        setActiveSection(questions[prevIndex].section_name);
      }
    }
  };

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
        alert("Exam time has expired!");
        setTimerStatus("timeout");
        await handleSubmitExam();
      }
    }
  };

  // Handle report issue submission
  const handleReportIssue = () => {
    if (!issueType) {
      alert("Please select an issue type");
      return;
    }

    const question = questions[currentQuestionIndex];
    const report = {
      questionId: question.id,
      questionNumber: currentQuestionIndex + 1,
      questionText: question.text.substring(0, 100),
      issueType,
      description: issueDescription,
      timestamp: new Date().toISOString(),
      attemptId,
    };

    // For now, log to console (can be sent to backend later)
    console.log("Issue Reported:", report);

    // Show confirmation
    alert(`Issue reported successfully!\n\nQuestion ${currentQuestionIndex + 1}\nIssue: ${issueType}\n\nThank you for your feedback.`);

    // Reset and close modal
    setShowReportModal(false);
    setIssueType("");
    setIssueDescription("");
  };

  // Calculate stats
  const answeredCount = Object.keys(answers).length;

  if (loading || questions.length === 0) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="h-10 w-10 animate-spin rounded-full border-4 border-blue-600 border-t-transparent mx-auto mb-4"></div>
          <p className="text-gray-500 font-medium">Loading Exam...</p>
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
    <div className="min-h-screen bg-gray-100 font-sans flex flex-col">
      {/* Top Header */}
      <header className="bg-white shadow-sm px-6 py-3 flex justify-between items-center sticky top-0 z-30 h-16">
        <div className="flex items-center gap-3">
          <img
            src="/logo.jpg"
            alt="DCET Platform Logo"
            className="h-8 w-8 rounded-lg object-cover"
          />
          <h1 className="text-lg font-bold text-gray-800 truncate max-w-md">
            {examTitle}
          </h1>
        </div>

        <div className="flex items-center gap-4">
          <div className={`flex items-center gap-2 px-3 py-1.5 rounded-md font-mono font-bold text-lg border ${examTimerService.isTimeCritical(remainingSeconds)
            ? "bg-red-50 text-red-600 border-red-200"
            : "bg-blue-50 text-blue-600 border-blue-200"
            }`}>
            <span>⏱️</span>
            {examTimerService.formatTime(remainingSeconds)}
          </div>
        </div>
      </header>

      {/* Main Layout */}
      <div className="flex-1 flex overflow-hidden max-w-[1600px] mx-auto w-full p-4 gap-4">

        {/* Left Side - Main Content */}
        <main className="flex-1 flex flex-col min-w-0 bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">

          {/* Section Tabs with Statistics */}
          <div className="flex border-b border-gray-200 overflow-x-auto scrollbar-hide bg-gray-50">
            {sections.map((section) => {
              const stats = getSectionStats(section);
              return (
                <button
                  key={section}
                  onClick={() => handleSectionChange(section)}
                  className={`px-6 py-3 text-sm font-semibold whitespace-nowrap transition-all relative min-w-fit ${activeSection === section
                    ? "text-blue-600 bg-white"
                    : "text-gray-600 hover:text-gray-800 hover:bg-gray-100"
                    }`}
                >
                  <div className="flex flex-col items-start gap-1.5">
                    <span className="text-sm">{section}</span>
                    <div className="flex gap-3 text-xs">
                      <span className="flex items-center gap-1">
                        <span className="w-2 h-2 rounded-full bg-green-500"></span>
                        <span className="text-gray-600">{stats.answered}</span>
                      </span>
                      <span className="flex items-center gap-1">
                        <span className="w-2 h-2 rounded-full bg-yellow-500"></span>
                        <span className="text-gray-600">{stats.marked}</span>
                      </span>
                      <span className="flex items-center gap-1">
                        <span className="w-2 h-2 rounded-full bg-gray-400"></span>
                        <span className="text-gray-600">{stats.unanswered}</span>
                      </span>
                    </div>
                  </div>
                  {activeSection === section && (
                    <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600"></div>
                  )}
                </button>
              );
            })}
          </div>

          {/* Question Area */}
          <div className="flex-1 overflow-y-auto p-6 md:p-10">
            <div className="max-w-4xl mx-auto">
              <div className="flex justify-between items-start mb-6">
                <div className="text-gray-500 font-medium">
                  Question: <span className="text-gray-900 font-bold">{String(currentQuestionIndex + 1).padStart(2, '0')}</span>/{questions.length}
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-gray-500 uppercase">
                    {currentQuestion.marks} Mark{currentQuestion.marks !== 1 && 's'}
                  </span>
                  <button
                    onClick={handleMarkForReview}
                    className="text-yellow-600 hover:text-yellow-700"
                    title="Mark for Review"
                  >
                    {markedForReview.has(currentQuestion.id) ? '★' : '☆'}
                  </button>
                  <button
                    onClick={() => setShowReportModal(true)}
                    className="text-red-600 hover:text-red-700 text-sm font-medium"
                    title="Report an issue with this question"
                  >
                    🚩 Report Issue
                  </button>
                </div>
              </div>

              <div className="mb-8">
                <h2 className="text-xl md:text-2xl font-medium text-gray-800 leading-relaxed">
                  {currentQuestionIndex + 1}. <MathText text={currentQuestion.text} />
                </h2>
              </div>

              <div className="space-y-4">
                {options.map((option) => (
                  <label
                    key={option.key}
                    className={`flex items-center gap-4 p-4 rounded-lg border-2 cursor-pointer transition-all ${answers[currentQuestion.id] === option.key
                      ? "border-blue-500 bg-blue-50"
                      : "border-gray-200 hover:border-gray-300 hover:bg-gray-50"
                      }`}
                  >
                    <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center flex-shrink-0 ${answers[currentQuestion.id] === option.key
                      ? "border-blue-600"
                      : "border-gray-400"
                      }`}>
                      {answers[currentQuestion.id] === option.key && (
                        <div className="w-2.5 h-2.5 rounded-full bg-blue-600"></div>
                      )}
                    </div>
                    <input
                      type="radio"
                      name={`question-${currentQuestion.id}`}
                      className="hidden"
                      checked={answers[currentQuestion.id] === option.key}
                      onChange={() => handleOptionSelect(option.key)}
                      disabled={timerStatus !== "running"}
                    />
                    <span className="text-gray-700 text-lg"><MathText text={option.text} /></span>
                  </label>
                ))}
              </div>
            </div>
          </div>

          {/* Footer Buttons */}
          <div className="p-4 border-t border-gray-200 bg-white flex justify-between items-center">
            <button
              onClick={handlePrevious}
              disabled={currentQuestionIndex === 0}
              className="px-6 py-2 rounded-full border border-gray-300 text-gray-600 font-medium hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>

            <div className="flex gap-3">
              <button
                onClick={handleMarkForReview}
                className={`px-6 py-2 rounded-full font-medium transition-colors ${markedForReview.has(currentQuestion.id)
                  ? "bg-yellow-100 text-yellow-700 border border-yellow-200"
                  : "bg-yellow-400 hover:bg-yellow-500 text-white shadow-sm"
                  }`}
              >
                {markedForReview.has(currentQuestion.id) ? "Unmark Review" : "Mark for Review"}
              </button>

              <button
                onClick={handleNext}
                disabled={currentQuestionIndex === questions.length - 1}
                className="px-8 py-2 rounded-full bg-gray-900 hover:bg-gray-800 text-white font-medium shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Save & Next
              </button>
            </div>
          </div>
        </main>

        {/* Right Sidebar */}
        <aside className="w-80 flex flex-col gap-4">
          {/* User Profile Card */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-4 mb-6">
              <div className="h-12 w-12 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-xl">
                {typeof window !== 'undefined' ? localStorage.getItem('username')?.charAt(0).toUpperCase() || 'U' : 'U'}
              </div>
              <div>
                <h3 className="font-bold text-gray-900">
                  {localStorage.getItem("username") || "Student"}
                </h3>
                <div className="text-xs text-gray-500 mt-1">
                  <span className="text-blue-600 font-medium">{answeredCount}/{questions.length}</span> Attempted
                </div>
              </div>
            </div>

            <h4 className="font-bold text-gray-800 mb-4 text-sm">Number of Questions</h4>

            {/* Scrollable Question Grid */}
            <div className="max-h-96 overflow-y-auto mb-6 pr-2 scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100">
              <div className="grid grid-cols-5 gap-2">
                {questions.map((q, idx) => {
                  let statusClass = "bg-gray-100 text-gray-600 border-gray-200"; // Not visited/Default

                  if (currentQuestionIndex === idx) {
                    statusClass = "ring-2 ring-blue-500 ring-offset-1 bg-white text-blue-600 border-blue-200";
                  } else if (markedForReview.has(q.id)) {
                    statusClass = "bg-yellow-400 text-white border-yellow-400";
                  } else if (answers[q.id]) {
                    statusClass = "bg-green-500 text-white border-green-500";
                  }

                  return (
                    <button
                      key={q.id}
                      onClick={() => {
                        setCurrentQuestionIndex(idx);
                        setActiveSection(q.section_name);
                      }}
                      className={`aspect-square rounded-full flex items-center justify-center text-xs font-bold border ${statusClass} hover:opacity-80 transition-all`}
                    >
                      {idx + 1}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Legend */}
            <div className="grid grid-cols-2 gap-3 text-xs text-gray-600">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-green-500"></div>
                <span>Answered</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-yellow-400"></div>
                <span>Marked for review</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-gray-100 border border-gray-300"></div>
                <span>Not Attempted</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-white border-2 border-blue-500"></div>
                <span>Current</span>
              </div>
            </div>
          </div>

          {/* Review Answers Button */}
          <button
            onClick={() => setShowReviewModal(true)}
            className="w-full py-3 bg-gray-700 hover:bg-gray-800 text-white font-bold rounded-xl shadow-md transition-colors mb-3"
          >
            📋 Review Answers
          </button>

          {/* Submit Button */}
          <button
            onClick={handleSubmitExam}
            className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl shadow-md transition-colors"
          >
            Submit Exam
          </button>
        </aside>

      </div>

      {/* Timeout overlay */}
      {timerStatus === "timeout" && (
        <div className="fixed inset-0 bg-slate-900/80 backdrop-blur-sm flex items-center justify-center z-50 animate-in fade-in duration-300">
          <div className="bg-white rounded-3xl p-10 max-w-md text-center shadow-2xl transform scale-100 animate-in zoom-in duration-300">
            <div className="text-7xl mb-6 animate-bounce">⏰</div>
            <h2 className="text-3xl font-bold text-slate-800 mb-3">
              Time's Up!
            </h2>
            <p className="text-slate-600 text-lg">
              Your exam has been automatically submitted.
            </p>
          </div>
        </div>
      )}

      {/* Report Issue Modal */}
      {showReportModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6 animate-in zoom-in duration-200">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-bold text-gray-900">Report Issue</h3>
              <button
                onClick={() => {
                  setShowReportModal(false);
                  setIssueType("");
                  setIssueDescription("");
                }}
                className="text-gray-400 hover:text-gray-600 text-2xl leading-none"
              >
                ×
              </button>
            </div>

            <div className="mb-4">
              <p className="text-sm text-gray-600 mb-2">
                Question {currentQuestionIndex + 1} of {questions.length}
              </p>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Issue Type *
                </label>
                <div className="space-y-2">
                  {[
                    { value: "wrong_answer", label: "Wrong Answer/Incorrect Solution" },
                    { value: "latex_format", label: "LaTeX Formatting Issue" },
                    { value: "unclear_question", label: "Question is Unclear" },
                    { value: "typo", label: "Typo/Spelling Error" },
                    { value: "other", label: "Other" },
                  ].map((option) => (
                    <label
                      key={option.value}
                      className="flex items-center gap-3 p-3 rounded-lg border-2 cursor-pointer transition-all hover:bg-gray-50 ${issueType === option.value ? 'border-red-500 bg-red-50' : 'border-gray-200'}"
                    >
                      <input
                        type="radio"
                        name="issueType"
                        value={option.value}
                        checked={issueType === option.value}
                        onChange={(e) => setIssueType(e.target.value)}
                        className="w-4 h-4 text-red-600"
                      />
                      <span className="text-sm font-medium text-gray-700">
                        {option.label}
                      </span>
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Additional Details (Optional)
                </label>
                <textarea
                  value={issueDescription}
                  onChange={(e) => setIssueDescription(e.target.value)}
                  placeholder="Provide more details about the issue..."
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-red-500 focus:ring-2 focus:ring-red-200 outline-none transition-all resize-none"
                  rows={4}
                />
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button
                onClick={() => {
                  setShowReportModal(false);
                  setIssueType("");
                  setIssueDescription("");
                }}
                className="flex-1 px-4 py-2.5 rounded-lg border-2 border-gray-300 text-gray-700 font-medium hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleReportIssue}
                className="flex-1 px-4 py-2.5 rounded-lg bg-red-600 hover:bg-red-700 text-white font-medium transition-colors"
              >
                Submit Report
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Answer Review Modal */}
      {showReviewModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 overflow-y-auto">
          <div className="bg-white rounded-2xl shadow-2xl max-w-5xl w-full my-8 max-h-[90vh] flex flex-col">
            {/* Header */}
            <div className="flex justify-between items-center p-6 border-b border-gray-200 sticky top-0 bg-white rounded-t-2xl">
              <div>
                <h3 className="text-2xl font-bold text-gray-900">Answer Review</h3>
                <p className="text-sm text-gray-600 mt-1">
                  Review your answers before final submission
                </p>
              </div>
              <button
                onClick={() => setShowReviewModal(false)}
                className="text-gray-400 hover:text-gray-600 text-3xl leading-none w-10 h-10 flex items-center justify-center rounded-full hover:bg-gray-100"
              >
                ×
              </button>
            </div>

            {/* Summary Stats */}
            <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
              <div className="grid grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900">{questions.length}</div>
                  <div className="text-xs text-gray-600">Total Questions</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">{answeredCount}</div>
                  <div className="text-xs text-gray-600">Answered</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-yellow-600">{markedForReview.size}</div>
                  <div className="text-xs text-gray-600">Marked for Review</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-red-600">{questions.length - answeredCount}</div>
                  <div className="text-xs text-gray-600">Unanswered</div>
                </div>
              </div>
            </div>

            {/* Questions by Section */}
            <div className="flex-1 overflow-y-auto p-6">
              {sections.map((section) => {
                const sectionQuestions = questions.filter(q => q.section_name === section);
                const stats = getSectionStats(section);

                return (
                  <div key={section} className="mb-8 last:mb-0">
                    {/* Section Header */}
                    <div className="flex justify-between items-center mb-4 pb-2 border-b-2 border-gray-300">
                      <h4 className="text-lg font-bold text-gray-900">{section}</h4>
                      <div className="flex gap-4 text-sm">
                        <span className="text-green-600 font-medium">✓ {stats.answered}</span>
                        <span className="text-yellow-600 font-medium">★ {stats.marked}</span>
                        <span className="text-red-600 font-medium">✗ {stats.unanswered}</span>
                      </div>
                    </div>

                    {/* Question Grid */}
                    <div className="grid grid-cols-10 gap-2">
                      {sectionQuestions.map((q, idx) => {
                        const globalIdx = questions.findIndex(question => question.id === q.id);
                        const isAnswered = !!answers[q.id];
                        const isMarked = markedForReview.has(q.id);

                        let statusClass = "bg-red-50 border-red-300 text-red-700"; // Unanswered
                        if (isAnswered && isMarked) {
                          statusClass = "bg-yellow-100 border-yellow-400 text-yellow-800"; // Answered + Marked
                        } else if (isAnswered) {
                          statusClass = "bg-green-50 border-green-400 text-green-700"; // Answered
                        } else if (isMarked) {
                          statusClass = "bg-yellow-50 border-yellow-300 text-yellow-700"; // Marked only
                        }

                        return (
                          <button
                            key={q.id}
                            onClick={() => {
                              setCurrentQuestionIndex(globalIdx);
                              setActiveSection(q.section_name);
                              setShowReviewModal(false);
                            }}
                            className={`aspect-square rounded-lg border-2 flex flex-col items-center justify-center text-sm font-bold hover:opacity-80 transition-all ${statusClass}`}
                            title={`Question ${globalIdx + 1}${isAnswered ? ` - Answer: ${answers[q.id]}` : ' - Not answered'}${isMarked ? ' (Marked)' : ''}`}
                          >
                            <span>{globalIdx + 1}</span>
                            {isAnswered && <span className="text-xs mt-0.5">{answers[q.id]}</span>}
                            {isMarked && <span className="text-xs">★</span>}
                          </button>
                        );
                      })}
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Footer */}
            <div className="p-6 border-t border-gray-200 bg-gray-50 rounded-b-2xl flex justify-between items-center">
              <div className="flex gap-6 text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 rounded border-2 border-green-400 bg-green-50"></div>
                  <span className="text-gray-700">Answered</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 rounded border-2 border-yellow-400 bg-yellow-100"></div>
                  <span className="text-gray-700">Answered + Marked</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 rounded border-2 border-yellow-300 bg-yellow-50"></div>
                  <span className="text-gray-700">Marked Only</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 rounded border-2 border-red-300 bg-red-50"></div>
                  <span className="text-gray-700">Unanswered</span>
                </div>
              </div>
              <button
                onClick={() => setShowReviewModal(false)}
                className="px-6 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium transition-colors"
              >
                Close Review
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
