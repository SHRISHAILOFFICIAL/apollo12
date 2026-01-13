"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import axios from "axios";
import { motion } from "framer-motion";
import {
  Clock,
  FileText,
  Award,
  Calendar,
  BookOpen,
  PlayCircle,
  ChevronRight,
  Info
} from "lucide-react";
import { Button } from "@/components/ui/button";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

// Hardcoded DCET Syllabus (5 sections)
const DCET_SYLLABUS = [
  {
    category: "IT Skills",
    topics: [
      "Cyber Security & Cyber Crimes",
      "Algorithms & Flowcharts",
      "MIT App Inventor & Scratch",
      "HTML, CSS, JavaScript",
      "Web Browsers & Servers",
      "Workflow Management & ERP",
      "IoT & Cloud Computing"
    ]
  },
  {
    category: "Fundamentals of Electrical & Electronics Engineering",
    topics: [
      "Electrical Power & Energy",
      "Ohm's Law & Kirchhoff's Laws",
      "Resistors & Capacitors",
      "Semiconductors & Diodes",
      "Transistors & Logic Gates",
      "Digital Electronics"
    ]
  },
  {
    category: "Engineering Mathematics",
    topics: [
      "Matrices & Determinants",
      "Differential Calculus",
      "Integral Calculus",
      "Differential Equations",
      "Vectors & 3D Geometry",
      "Probability & Statistics"
    ]
  },
  {
    category: "Statistics & Analytics",
    topics: [
      "Data Representation",
      "Measures of Central Tendency",
      "Measures of Dispersion",
      "Probability Distributions",
      "Python Programming Basics",
      "Data Analysis with Excel"
    ]
  },
  {
    category: "Project Management Skills",
    topics: [
      "Project Planning & Scheduling",
      "Resource Management",
      "Risk Management",
      "Quality Management",
      "Project Documentation"
    ]
  }
];

interface ExamDetails {
  id: number;
  name: string;
  year: number;
  duration_minutes: number;
  total_marks: number;
  total_questions: number;
  sections_count: number;
  access_tier: string;
  is_premium: boolean;
  sections: {
    name: string;
    question_count: number;
  }[];
}

interface Attempt {
  id: number;
  attempt_number?: number;
  exam_name: string;
  started_at: string;
  score: number;
  total_marks: number;
  percentage: number;
  status: string;
}

export default function ExamOverviewPage() {
  const router = useRouter();
  const params = useParams();
  const examId = params.id as string;

  const [exam, setExam] = useState<ExamDetails | null>(null);
  const [attempts, setAttempts] = useState<Attempt[]>([]);
  const [loading, setLoading] = useState(true);
  const [showInstructions, setShowInstructions] = useState(false);

  useEffect(() => {
    const fetchExamDetails = async () => {
      try {
        const token = localStorage.getItem("access_token");
        if (!token) {
          router.push("/auth/login");
          return;
        }

        // Fetch exam details
        const examResponse = await axios.get(`${API_BASE_URL}/exams/${examId}/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setExam(examResponse.data);

        // Fetch previous attempts
        try {
          const attemptsResponse = await axios.get(
            `${API_BASE_URL}/exams/${examId}/attempts/`,
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          );
          console.log("Attempts response:", attemptsResponse.data);
          setAttempts(attemptsResponse.data.attempts || []);
        } catch (error: any) {
          console.error("Error fetching attempts:", error.response?.data || error.message);
          setAttempts([]);
        }

        setLoading(false);
      } catch (error: any) {
        console.error("Failed to fetch exam details", error);
        if (error.response?.status === 401) {
          router.push("/auth/login");
        }
      }
    };

    fetchExamDetails();
  }, [examId, router]);

  const handleStartExam = () => {
    router.push(`/exam/${examId}/start`);
  };

  if (loading || !exam) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-blue-600 border-t-transparent mx-auto mb-4"></div>
          <p className="text-gray-600 font-medium">Loading Exam Details...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40 shadow-sm">
        <div className="container mx-auto px-4 sm:px-6 h-16 flex items-center">
          <button
            onClick={() => router.push("/dashboard")}
            className="text-gray-600 hover:text-gray-900 flex items-center gap-2"
          >
            ← Back
          </button>
        </div>
      </header>

      <main className="container mx-auto px-4 sm:px-6 py-8 max-w-6xl">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Exam Header */}
            <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <span className="inline-block px-2 py-1 text-xs font-semibold bg-blue-100 text-blue-700 rounded mb-2">
                    Test
                  </span>
                  <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">
                    {exam.name} {exam.year}
                  </h1>
                </div>
              </div>

              {/* Test Details */}
              <div className="grid grid-cols-3 gap-4 mb-6">
                <div className="flex items-center gap-2 text-gray-700">
                  <div className="p-2 bg-blue-50 rounded-lg">
                    <FileText className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Questions</p>
                    <p className="font-semibold">100 Questions</p>
                  </div>
                </div>

                <div className="flex items-center gap-2 text-gray-700">
                  <div className="p-2 bg-purple-50 rounded-lg">
                    <Award className="w-5 h-5 text-purple-600" />
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Marks</p>
                    <p className="font-semibold">100</p>
                  </div>
                </div>

                <div className="flex items-center gap-2 text-gray-700">
                  <div className="p-2 bg-green-50 rounded-lg">
                    <Clock className="w-5 h-5 text-green-600" />
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Duration</p>
                    <p className="font-semibold">{exam.duration_minutes} mins</p>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row gap-3">
                <Button
                  onClick={handleStartExam}
                  className="bg-green-600 hover:bg-green-700 text-white font-semibold flex-1"
                  size="lg"
                >
                  <PlayCircle className="w-5 h-5 mr-2" />
                  {attempts.length > 0 ? "Reattempt Test" : "Start Test"}
                </Button>
                <Button
                  onClick={() => setShowInstructions(!showInstructions)}
                  variant="outline"
                  className="sm:w-auto"
                  size="lg"
                >
                  <Info className="w-5 h-5 mr-2" />
                  Instructions
                </Button>
              </div>
            </div>

            {/* Instructions */}
            {showInstructions && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-blue-50 border border-blue-200 rounded-lg p-6"
              >
                <h3 className="font-bold text-gray-900 mb-4 text-lg flex items-center gap-2">
                  <Info className="w-5 h-5 text-blue-600" />
                  Test Instructions
                </h3>

                <div className="space-y-4 text-sm text-gray-700">
                  {/* General Instructions */}
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">General Instructions</h4>
                    <ul className="space-y-2">
                      <li className="flex items-start gap-2">
                        <span className="text-blue-600 mt-0.5">•</span>
                        <span>Total duration of this test is {exam.duration_minutes} minutes.</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-blue-600 mt-0.5">•</span>
                        <span>The countdown timer in the top right corner will display the remaining time. When the timer reaches zero, the test will end automatically.</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-blue-600 mt-0.5">•</span>
                        <span>The question palette on the right shows the status of each question using color codes.</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-blue-600 mt-0.5">•</span>
                        <span>Questions marked and answered will be considered for evaluation.</span>
                      </li>
                    </ul>
                  </div>

                  {/* Navigating Questions */}
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Navigating to a Question</h4>
                    <ul className="space-y-2">
                      <li className="flex items-start gap-2">
                        <span className="text-blue-600 mt-0.5">•</span>
                        <span>Click on the question number in the question palette to go directly to that question.</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-blue-600 mt-0.5">•</span>
                        <span>Click on "Save & Next" to save your answer and move to the next question.</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-blue-600 mt-0.5">•</span>
                        <span>Click on "Mark for Review" to mark a question for later review.</span>
                      </li>
                    </ul>
                  </div>

                  {/* Answering Questions */}
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Answering a Question</h4>
                    <ul className="space-y-2">
                      <li className="flex items-start gap-2">
                        <span className="text-blue-600 mt-0.5">•</span>
                        <span>To select an answer, click on one of the option buttons.</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-blue-600 mt-0.5">•</span>
                        <span>To deselect your answer, click the "Clear Response" button.</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-blue-600 mt-0.5">•</span>
                        <span>To change your answer, simply click on a different option.</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-blue-600 mt-0.5">•</span>
                        <span>Your answers are auto-saved as you navigate through questions.</span>
                      </li>
                    </ul>
                  </div>

                  {/* Sections */}
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Navigating Through Sections</h4>
                    <ul className="space-y-2">
                      <li className="flex items-start gap-2">
                        <span className="text-blue-600 mt-0.5">•</span>
                        <span>This test has {DCET_SYLLABUS.length} sections. You can switch between sections anytime.</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-blue-600 mt-0.5">•</span>
                        <span>Sections are displayed in tabs at the top of the exam page.</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-blue-600 mt-0.5">•</span>
                        <span>You can navigate between sections and questions at any time during the test.</span>
                      </li>
                    </ul>
                  </div>

                  {/* Marking Scheme */}
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Marking Scheme</h4>
                    <ul className="space-y-2">
                      <li className="flex items-start gap-2">
                        <span className="text-blue-600 mt-0.5">•</span>
                        <span>Each question carries 1 mark.</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-blue-600 mt-0.5">•</span>
                        <span>There is no negative marking for incorrect answers.</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </motion.div>
            )}

            {/* Syllabus */}
            <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Syllabus</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {DCET_SYLLABUS.map((section, index) => (
                  <div key={index} className="flex items-center gap-2 text-gray-700">
                    <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                    <span className="text-sm font-medium">{section.category}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Sidebar - Previous Attempts */}
          <div className="space-y-6">
            <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
              <h2 className="text-lg font-bold text-gray-900 mb-4">Your Attempts</h2>

              {attempts.length > 0 ? (
                <div className="space-y-3">
                  {attempts.map((attempt) => (
                    <div
                      key={attempt.id}
                      onClick={() => router.push(`/results/${attempt.id}`)}
                      className="p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-all cursor-pointer group"
                    >
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-semibold text-gray-900">
                          Attempt {attempt.attempt_number || attempt.id}
                        </span>
                        <ChevronRight className="w-4 h-4 text-gray-400 group-hover:text-blue-600" />
                      </div>
                      <div className="flex items-center gap-2 text-xs text-gray-600 mb-2">
                        <Calendar className="w-3 h-3" />
                        {new Date(attempt.started_at).toLocaleString()}
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">
                          Score: {attempt.score}/{attempt.total_marks}
                        </span>
                        <span
                          className={`text-xs font-bold px-2 py-1 rounded ${attempt.percentage >= 80
                            ? "bg-green-100 text-green-700"
                            : attempt.percentage >= 60
                              ? "bg-blue-100 text-blue-700"
                              : "bg-orange-100 text-orange-700"
                            }`}
                        >
                          {attempt.percentage}%
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <FileText className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                  <p className="text-sm">No attempts yet</p>
                  <p className="text-xs mt-1">Start the test to track your progress!</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
