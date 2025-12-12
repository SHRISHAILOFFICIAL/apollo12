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
  access_tier: string;
  is_premium: boolean;
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
    tier: string;
    is_pro: boolean;
  };
  subscription: {
    is_paid: boolean;
    subscription_end: string | null;
    is_active: boolean;
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
        {/* PRO Upgrade Banner for FREE users */}
        {!dashboardData.user.is_pro && (
          <div className="mb-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl shadow-lg p-6 text-white">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold mb-2">🚀 Upgrade to PRO</h2>
                <p className="text-blue-100">
                  Get unlimited access to all 3 PYQs, 10 Mock Tests, and Video Solutions for just ₹149/year
                </p>
              </div>
              <button
                onClick={() => router.push("/pricing")}
                className="px-8 py-3 bg-white text-blue-600 font-bold rounded-lg hover:bg-gray-100 transition-colors shadow-md"
              >
                Upgrade Now
              </button>
            </div>
          </div>
        )}

        {/* User Tier Badge */}
        {dashboardData.user.is_pro && (
          <div className="mb-6 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-xl shadow-lg p-4 text-white">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="text-3xl">⭐</span>
                <div>
                  <h3 className="text-xl font-bold">PRO Member</h3>
                  <p className="text-sm text-yellow-100">
                    {dashboardData.subscription.subscription_end
                      ? `Valid until ${new Date(dashboardData.subscription.subscription_end).toLocaleDateString()}`
                      : "Active"}
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-sm text-yellow-100">Enjoying PRO benefits</p>
              </div>
            </div>
          </div>
        )}
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
                    className={`border-2 rounded-xl p-6 transition-colors ${exam.is_premium && !dashboardData.user.is_pro
                        ? "border-gray-300 bg-gray-50 opacity-75"
                        : "border-gray-200 hover:border-blue-500"
                      }`}
                  >
                    <div className="flex justify-between items-start mb-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <h3 className="text-xl font-bold text-gray-900">{exam.name}</h3>
                          {exam.is_premium && (
                            <span className="px-2 py-1 bg-gradient-to-r from-yellow-400 to-orange-500 text-white text-xs font-bold rounded">
                              PRO
                            </span>
                          )}
                        </div>
                        <div className="flex gap-4 mt-2 text-sm text-gray-600">
                          <span>⏱️ {exam.duration_minutes} mins</span>
                          <span>📝 {exam.total_questions} questions</span>
                          <span>📊 {exam.total_marks} marks</span>
                          <span>📑 {exam.sections_count} sections</span>
                        </div>
                      </div>
                      {exam.is_premium && !dashboardData.user.is_pro ? (
                        <button
                          onClick={() => router.push("/pricing")}
                          className="px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold rounded-lg shadow-md transition-colors flex items-center gap-2"
                        >
                          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path
                              fillRule="evenodd"
                              d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z"
                              clipRule="evenodd"
                            />
                          </svg>
                          Unlock with PRO
                        </button>
                      ) : (
                        <button
                          onClick={() => router.push(`/exam/${exam.id}`)}
                          className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-md transition-colors"
                        >
                          Start Exam
                        </button>
                      )}
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
