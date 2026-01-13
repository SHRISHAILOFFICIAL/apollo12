"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import { motion, AnimatePresence } from "framer-motion";
import {
  LogOut,
  Crown,
  Clock,
  FileText,
  Award,
  BarChart2,
  Lock,
  PlayCircle,
  TrendingUp,
  Calendar,
  BookOpen,
  Play,
  Bell,
  User,
  Menu,
  X,
  Home,
  Video,
  ChevronRight,
  Target,
} from "lucide-react";
import { Button } from "@/components/ui/button";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

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
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(
    null
  );
  const [loading, setLoading] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(false);

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
    router.push("/");
  };

  if (loading || !dashboardData) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-blue-600 border-t-transparent mx-auto mb-4"></div>
          <p className="text-gray-600 font-medium">Loading Dashboard...</p>
        </div>
      </div>
    );
  }

  const user = dashboardData.user;
  const isPro = user.is_pro;

  const navigationItems = [
    { icon: Home, label: "Dashboard", path: "/dashboard", active: true },
    { icon: BookOpen, label: "Study Notes", path: "/notes", active: false },
    { icon: FileText, label: "PYQ Papers", path: "/pyqs", active: false },
    {
      icon: Video,
      label: "Video Solutions",
      path: "/videos",
      active: false,
      isPro: true,
    },
    { icon: BarChart2, label: "My Progress", path: "/profile", active: false },
    {
      icon: Bell,
      label: "Announcements",
      path: "/announcements",
      active: false,
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
      <AnimatePresence>
        {(sidebarOpen ||
          (typeof window !== "undefined" && window.innerWidth >= 1024)) && (
          <>
            {/* Mobile Overlay */}
            {sidebarOpen && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={() => setSidebarOpen(false)}
                className="fixed inset-0 bg-black/50 z-40 lg:hidden"
              />
            )}

            {/* Sidebar */}
            <motion.aside
              initial={{ x: -280 }}
              animate={{ x: 0 }}
              exit={{ x: -280 }}
              transition={{ type: "spring", damping: 25, stiffness: 200 }}
              className="fixed lg:sticky top-0 left-0 h-screen w-64 bg-white border-r border-gray-200 z-50 flex flex-col"
            >
              {/* Logo */}
              <div className="h-16 flex items-center justify-between px-6 border-b border-gray-200">
                <img
                  src="/logo_sample.png"
                  alt="DCEThelper"
                  className="h-16 w-auto object-contain"
                />
                <button
                  onClick={() => setSidebarOpen(false)}
                  className="lg:hidden text-gray-500 hover:text-gray-700"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Navigation */}
              <nav className="flex-1 px-3 py-6 space-y-1 overflow-y-auto">
                {navigationItems.map((item) => {
                  const Icon = item.icon;
                  return (
                    <button
                      key={item.path}
                      onClick={() => {
                        router.push(item.path);
                        setSidebarOpen(false);
                      }}
                      className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all ${
                        item.active
                          ? "bg-blue-50 text-blue-600 font-semibold"
                          : "text-gray-700 hover:bg-gray-50"
                      }`}
                    >
                      <Icon className="w-5 h-5" />
                      <span className="flex-1 text-left">{item.label}</span>
                      {item.isPro && (
                        <span className="px-2 py-0.5 text-xs font-bold bg-amber-100 text-amber-700 rounded">
                          PRO
                        </span>
                      )}
                    </button>
                  );
                })}
              </nav>

              {/* User Section */}
              <div className="p-4 border-t border-gray-200">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
                    <User className="w-5 h-5 text-blue-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-semibold text-gray-900 truncate">
                      {user.username}
                    </p>
                    <p className="text-xs text-gray-500 truncate">
                      {user.email}
                    </p>
                  </div>
                </div>
              </div>
            </motion.aside>
          </>
        )}
      </AnimatePresence>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top Header */}
        <header className="h-16 bg-white border-b border-gray-200 sticky top-0 z-30 flex items-center px-4 lg:px-6">
          <button
            onClick={() => setSidebarOpen(true)}
            className="lg:hidden mr-4 text-gray-600 hover:text-gray-900"
          >
            <Menu className="w-6 h-6" />
          </button>

          <div className="flex-1">
            <h1 className="text-lg font-bold text-gray-900">
              Welcome back, {user.username}! 👋
            </h1>
          </div>

          <div className="flex items-center gap-3">
            {isPro && (
              <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 bg-gradient-to-r from-amber-400 to-orange-500 rounded-full">
                <Crown className="w-4 h-4 text-white" />
                <span className="text-xs font-bold text-white">PRO</span>
              </div>
            )}
            <Button
              onClick={() => router.push("/profile")}
              variant="ghost"
              size="sm"
              className="gap-2"
            >
              <User className="w-4 h-4" />
              <span className="hidden sm:inline">Profile</span>
            </Button>
            <Button
              onClick={handleLogout}
              variant="ghost"
              size="sm"
              className="gap-2 text-gray-600 hover:text-red-600"
            >
              <LogOut className="w-4 h-4" />
              <span className="hidden sm:inline">Logout</span>
            </Button>
          </div>
        </header>

        {/* Main Content Area */}
        <main className="flex-1 overflow-y-auto p-4 lg:p-6">
          <div className="max-w-7xl mx-auto space-y-6">
            {/* PRO Upgrade Banner */}
            {!isPro && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-gradient-to-r from-amber-50 via-orange-50 to-amber-50 border-2 border-amber-200 rounded-xl p-4 flex items-center justify-between shadow-sm"
              >
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-gradient-to-br from-amber-400 to-orange-500 rounded-xl">
                    <Crown className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="font-bold text-gray-900">Upgrade to PRO</h3>
                    <p className="text-sm text-gray-600">
                      Unlock all 3 PYQs, 10 Mock Tests & Video Solutions
                    </p>
                  </div>
                </div>
                <Button
                  onClick={() => router.push("/pricing")}
                  className="bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white font-semibold"
                >
                  Upgrade Now
                </Button>
              </motion.div>
            )}

            {/* Stats Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Total Attempts */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="p-2.5 bg-blue-50 rounded-lg">
                    <FileText className="w-5 h-5 text-blue-600" />
                  </div>
                  <span className="text-xs font-medium text-gray-500">
                    Total
                  </span>
                </div>
                <p className="text-3xl font-bold text-gray-900 mb-1">
                  {dashboardData.stats.total_attempts}
                </p>
                <p className="text-sm text-gray-600">Attempts</p>
              </motion.div>

              {/* Average Score */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="p-2.5 bg-blue-50 rounded-lg">
                    <BarChart2 className="w-5 h-5 text-blue-600" />
                  </div>
                  <span className="text-xs font-medium text-green-600">
                    ↑ 12%
                  </span>
                </div>
                <p className="text-3xl font-bold text-gray-900 mb-1">
                  {dashboardData.stats.average_score.toFixed(1)}%
                </p>
                <p className="text-sm text-gray-600">Average Score</p>
              </motion.div>

              {/* Best Score */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="p-2.5 bg-green-50 rounded-lg">
                    <Award className="w-5 h-5 text-green-600" />
                  </div>
                  <span className="text-xs font-medium text-gray-500">
                    Best
                  </span>
                </div>
                <p className="text-3xl font-bold text-gray-900 mb-1">
                  {dashboardData.stats.best_score}%
                </p>
                <p className="text-sm text-gray-600">Top Score</p>
              </motion.div>

              {/* Accuracy Rate */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="p-2.5 bg-blue-50 rounded-lg">
                    <Target className="w-5 h-5 text-blue-600" />
                  </div>
                  <span className="text-xs font-medium text-gray-500">
                    Rate
                  </span>
                </div>
                <p className="text-3xl font-bold text-gray-900 mb-1">
                  {dashboardData.stats.total_attempts > 0
                    ? dashboardData.stats.average_score.toFixed(0)
                    : 0}
                  %
                </p>
                <p className="text-sm text-gray-600">Accuracy</p>
              </motion.div>
            </div>

            {/* Quick Actions */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <button
                onClick={() => router.push("/notes")}
                className="bg-gradient-to-br from-blue-50 to-indigo-50 border-2 border-blue-200 rounded-xl p-6 text-left hover:shadow-lg transition-all hover:scale-[1.02] group"
              >
                <div className="p-3 bg-blue-600 rounded-xl shadow-lg group-hover:shadow-xl transition-shadow mb-4 w-fit">
                  <BookOpen className="w-7 h-7 text-white" />
                </div>
                <h3 className="font-bold text-lg mb-2 text-gray-900">
                  Study Notes
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  Comprehensive study materials
                </p>
                <div className="flex items-center text-blue-600 font-semibold text-sm group-hover:gap-2 transition-all">
                  <span>View Notes</span>
                  <ChevronRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
                </div>
              </button>

              <button
                onClick={() => router.push("/pyqs")}
                className="bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200 rounded-xl p-6 text-left hover:shadow-lg transition-all hover:scale-[1.02] group"
              >
                <div className="p-3 bg-green-600 rounded-xl shadow-lg group-hover:shadow-xl transition-shadow mb-4 w-fit">
                  <FileText className="w-7 h-7 text-white" />
                </div>
                <h3 className="font-bold text-lg mb-2 text-gray-900">
                  PYQ Papers
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  Practice past exam papers
                </p>
                <div className="flex items-center text-green-600 font-semibold text-sm group-hover:gap-2 transition-all">
                  <span>View PYQs</span>
                  <ChevronRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
                </div>
              </button>

              <button
                onClick={() => router.push("/videos")}
                className="bg-gradient-to-br from-purple-50 to-pink-50 border-2 border-purple-200 rounded-xl p-6 text-left hover:shadow-lg transition-all hover:scale-[1.02] group relative"
              >
                {!isPro && (
                  <div className="absolute top-3 right-3 px-2 py-1 bg-amber-100 border border-amber-300 rounded-full text-xs font-bold text-amber-700">
                    PRO
                  </div>
                )}
                <div className="p-3 bg-purple-600 rounded-xl shadow-lg group-hover:shadow-xl transition-shadow mb-4 w-fit">
                  <Play className="w-7 h-7 text-white" />
                </div>
                <h3 className="font-bold text-lg mb-2 text-gray-900">
                  Video Solutions
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  Expert video explanations
                </p>
                <div className="flex items-center text-purple-600 font-semibold text-sm group-hover:gap-2 transition-all">
                  <span>Watch Videos</span>
                  <ChevronRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
                </div>
              </button>
            </div>

            {/* Available Exams & Recent Activity */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Available Exams */}
              <div className="lg:col-span-2 space-y-4">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                    <Target className="w-6 h-6 text-blue-600" />
                    Available Exams
                  </h2>
                </div>

                <div className="space-y-3">
                  {dashboardData.available_exams.map((exam) => {
                    const isLocked = exam.is_premium && !isPro;
                    return (
                      <div
                        key={exam.id}
                        className={`bg-white rounded-xl border p-5 transition-all ${
                          isLocked
                            ? "border-gray-200 opacity-75"
                            : "border-gray-200 hover:border-blue-300 hover:shadow-md"
                        }`}
                      >
                        <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-4">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-2">
                              <h3 className="text-lg font-bold text-gray-900">
                                {exam.name}
                              </h3>
                              {exam.is_premium && (
                                <span className="px-2 py-0.5 rounded-full text-xs font-bold bg-amber-100 text-amber-700">
                                  PRO
                                </span>
                              )}
                            </div>
                            <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                              <span className="flex items-center gap-1">
                                <Clock className="w-4 h-4" />{" "}
                                {exam.duration_minutes} mins
                              </span>
                              <span className="flex items-center gap-1">
                                <FileText className="w-4 h-4" />{" "}
                                {exam.total_questions} Qs
                              </span>
                              <span className="flex items-center gap-1">
                                <Award className="w-4 h-4" /> {exam.total_marks}{" "}
                                Marks
                              </span>
                            </div>
                          </div>

                          {isLocked ? (
                            <Button
                              onClick={() => router.push("/pricing")}
                              variant="outline"
                              className="w-full sm:w-auto"
                            >
                              <Lock className="w-4 h-4 mr-2" /> Unlock
                            </Button>
                          ) : (
                            <Button
                              onClick={() => router.push(`/exam/${exam.id}`)}
                              className="bg-blue-600 hover:bg-blue-700 text-white w-full sm:w-auto"
                            >
                              <PlayCircle className="w-4 h-4 mr-2" /> Start Exam
                            </Button>
                          )}
                        </div>
                      </div>
                    );
                  })}

                  {dashboardData.available_exams.length === 0 && (
                    <div className="text-center py-12 bg-white rounded-xl border border-gray-200 text-gray-500">
                      No exams available at the moment.
                    </div>
                  )}
                </div>
              </div>

              {/* Recent Activity */}
              <div className="space-y-4">
                <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                  <TrendingUp className="w-6 h-6 text-blue-600" />
                  Recent Activity
                </h2>

                <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
                  {dashboardData.recent_attempts.length > 0 ? (
                    <div className="divide-y divide-gray-200">
                      {dashboardData.recent_attempts
                        .slice(0, 5)
                        .map((attempt) => (
                          <div
                            key={attempt.id}
                            className="p-4 hover:bg-gray-50 transition-colors cursor-pointer"
                            onClick={() =>
                              router.push(`/results/${attempt.id}`)
                            }
                          >
                            <div className="flex justify-between items-start mb-2">
                              <p className="font-semibold text-sm text-gray-900">
                                {attempt.exam_name}
                              </p>
                              <span
                                className={`text-xs font-bold px-2 py-1 rounded ${
                                  attempt.percentage >= 80
                                    ? "bg-green-100 text-green-700"
                                    : attempt.percentage >= 60
                                    ? "bg-blue-100 text-blue-700"
                                    : "bg-orange-100 text-orange-700"
                                }`}
                              >
                                {attempt.percentage}%
                              </span>
                            </div>
                            <div className="flex justify-between items-center text-xs text-gray-600">
                              <span className="flex items-center gap-1">
                                <Calendar className="w-3 h-3" /> {attempt.date}
                              </span>
                              <span>
                                Score: {attempt.score}/{attempt.total_marks}
                              </span>
                            </div>
                          </div>
                        ))}
                    </div>
                  ) : (
                    <div className="p-8 text-center text-gray-500 text-sm">
                      <FileText className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                      <p>No attempts yet.</p>
                      <p className="text-xs mt-1">
                        Start an exam to see your progress!
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
