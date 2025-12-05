"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

interface Exam {
  id: number;
  name: string;
  duration_minutes: number;
  total_marks: number;
  total_questions: number;
  sections_count: number;
}

interface Attempt {
  id: number;
  exam_name: string;
  date: string;
  score: number;
  total_marks: number;
  percentage: number;
  status: string;
}

interface PerformanceTrend {
  date: string;
  score: number;
  exam: string;
}

interface DashboardData {
  user: {
    username: string;
    email: string;
  };
  stats: {
    total_attempts: number;
    average_score: number;
    best_score: number;
  };
  available_exams: Exam[];
  recent_attempts: Attempt[];
  performance_trend: PerformanceTrend[];
}

export default function DashboardPage() {
  const router = useRouter();
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const token = localStorage.getItem("access_token");
        if (!token) {
          router.push("/auth/login");
          return;
        }

        const response = await axios.get(`${API_BASE_URL}/dashboard/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setDashboardData(response.data);
        setLoading(false);
      } catch (error: any) {
        console.error("Failed to fetch dashboard", error);
        if (error.response?.status === 401) {
          router.push("/auth/login");
        }
      }
    };

    fetchDashboard();
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("username");
    router.push("/auth/login");
  };

  if (loading || !dashboardData) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-blue-600 border-t-transparent mx-auto mb-4"></div>
          <p className="text-gray-500 font-medium">Loading Dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <img
              src="/logo.jpg"
              alt="DCET Platform Logo"
              className="h-10 w-10 rounded-lg object-cover"
            />
            <div>
              <h1 className="text-xl font-bold text-gray-900">DCET Platform</h1>
              <p className="text-sm text-gray-600">{dashboardData.user.username}</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
          >
            Logout
          </button>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Attempts</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">
                  {dashboardData.stats.total_attempts}
                </p>
              </div>
              <div className="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">📝</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Average Score</p>
                <p className="text-3xl font-bold text-blue-600 mt-2">
                  {dashboardData.stats.average_score}%
                </p>
              </div>
              <div className="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">📊</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-md p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Best Score</p>
                <p className="text-3xl font-bold text-green-600 mt-2">
                  {dashboardData.stats.best_score}%
                </p>
              </div>
              <div className="h-12 w-12 bg-green-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">🏆</span>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Available Exams */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Available Exams</h2>
              <div className="space-y-4">
                {dashboardData.available_exams.map((exam) => (
                  <div
                    key={exam.id}
                    className="border-2 border-gray-200 rounded-xl p-6 hover:border-blue-500 transition-colors"
                  >
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-xl font-bold text-gray-900">{exam.name}</h3>
                        <div className="flex gap-4 mt-2 text-sm text-gray-600">
                          <span>⏱️ {exam.duration_minutes} mins</span>
                          <span>📝 {exam.total_questions} questions</span>
                          <span>📊 {exam.total_marks} marks</span>
                          <span>📑 {exam.sections_count} sections</span>
                        </div>
                      </div>
                      <button
                        onClick={() => router.push(`/exam/${exam.id}`)}
                        className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-md transition-colors"
                      >
                        Start Exam
                      </button>
                    </div>
                  </div>
                ))}
                {dashboardData.available_exams.length === 0 && (
                  <p className="text-center text-gray-500 py-8">
                    No exams available at the moment
                  </p>
                )}
              </div>
            </div>
          </div>

          {/* Recent Attempts */}
          <div>
            <div className="bg-white rounded-xl shadow-md p-6 mb-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Attempts</h2>
              <div className="space-y-3">
                {dashboardData.recent_attempts.slice(0, 5).map((attempt) => (
                  <div
                    key={attempt.id}
                    className="border border-gray-200 rounded-lg p-4 hover:border-blue-500 transition-colors cursor-pointer"
                    onClick={() => router.push(`/results/${attempt.id}`)}
                  >
                    <div className="flex justify-between items-start mb-2">
                      <p className="font-semibold text-gray-900 text-sm">
                        {attempt.exam_name}
                      </p>
                      <span
                        className={`text-xs px-2 py-1 rounded font-semibold ${attempt.percentage >= 80
                          ? "bg-green-100 text-green-800"
                          : attempt.percentage >= 60
                            ? "bg-blue-100 text-blue-800"
                            : "bg-yellow-100 text-yellow-800"
                          }`}
                      >
                        {attempt.percentage}%
                      </span>
                    </div>
                    <p className="text-xs text-gray-600">{attempt.date}</p>
                    <p className="text-xs text-gray-600 mt-1">
                      Score: {attempt.score}/{attempt.total_marks}
                    </p>
                  </div>
                ))}
                {dashboardData.recent_attempts.length === 0 && (
                  <p className="text-center text-gray-500 py-4 text-sm">
                    No attempts yet
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
