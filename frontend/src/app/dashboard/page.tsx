"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import { motion } from "framer-motion";
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
  Calendar
} from "lucide-react";
import { Button } from "@/components/ui/button";

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
      <div className="flex min-h-screen items-center justify-center bg-background">
        <div className="text-center">
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-primary border-t-transparent mx-auto mb-4"></div>
          <p className="text-muted-foreground font-medium">Loading Dashboard...</p>
        </div>
      </div>
    );
  }

  const user = dashboardData.user;
  const isPro = user.is_pro;

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Header */}
      <header className="fixed top-0 w-full z-40 glass border-b border-border/50">
        <div className="container mx-auto px-6 h-16 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center text-white font-bold text-lg">D</div>
            <div>
              <h1 className="text-lg font-heading font-bold leading-tight">DCET Platform</h1>
              <p className="text-xs text-muted-foreground">Welcome back, {user.username}</p>
            </div>
          </div>
          <Button
            variant="ghost"
            onClick={handleLogout}
            className="text-muted-foreground hover:text-destructive gap-2"
          >
            <LogOut className="w-4 h-4" />
            <span className="hidden sm:inline">Logout</span>
          </Button>
        </div>
      </header>

      <main className="container mx-auto px-6 pt-24 pb-12">
        {/* PRO Upgrade Banner for FREE users */}
        {!isPro && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8 rounded-2xl bg-gradient-to-r from-primary to-purple-600 p-1 shadow-lg"
          >
            <div className="bg-background/10 backdrop-blur-sm rounded-xl p-6 sm:flex items-center justify-between text-white">
              <div className="mb-4 sm:mb-0">
                <h2 className="text-2xl font-bold mb-2 flex items-center gap-2">
                  <Crown className="w-6 h-6 text-yellow-300 fill-yellow-300" />
                  Upgrade to PRO
                </h2>
                <p className="text-white/90 max-w-xl">
                  Get unlimited access to all 3 PYQs, 10 Mock Tests, and Video Solutions for a full year.
                </p>
              </div>
              <Button
                onClick={() => router.push("/pricing")}
                className="bg-white text-primary hover:bg-white/90 font-bold border-0 shadow-xl"
                size="lg"
              >
                Upgrade Now
              </Button>
            </div>
          </motion.div>
        )}

        {/* User Tier Badge - Only visible if PRO */}
        {isPro && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="mb-8 bg-gradient-to-r from-yellow-100 to-orange-100 dark:from-yellow-900/20 dark:to-orange-900/20 border border-yellow-200 dark:border-yellow-800 rounded-xl p-4 flex items-center justify-between"
          >
            <div className="flex items-center gap-3">
              <div className="p-2 bg-yellow-400 rounded-full text-white shadow-sm">
                <Crown className="w-5 h-5 fill-white" />
              </div>
              <div>
                <h3 className="font-heading font-bold text-yellow-800 dark:text-yellow-200">PRO Member</h3>
                <span className="text-xs text-yellow-600 dark:text-yellow-300 font-medium">
                  {dashboardData.subscription.subscription_end
                    ? `Valid until ${new Date(dashboardData.subscription.subscription_end).toLocaleDateString()}`
                    : "Active"}
                </span>
              </div>
            </div>
            <span className="text-sm font-medium text-yellow-700 dark:text-yellow-400">Premium Access Unlocked</span>
          </motion.div>
        )}

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
          <StatCard
            title="Total Attempts"
            value={dashboardData.stats.total_attempts}
            icon={<FileText className="w-6 h-6 text-blue-500" />}
            delay={0.1}
          />
          <StatCard
            title="Average Score"
            value={`${dashboardData.stats.average_score}%`}
            icon={<BarChart2 className="w-6 h-6 text-purple-500" />}
            delay={0.2}
          />
          <StatCard
            title="Best Score"
            value={`${dashboardData.stats.best_score}%`}
            icon={<Award className="w-6 h-6 text-green-500" />}
            delay={0.3}
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Available Exams Column */}
          <div className="lg:col-span-2 space-y-6">
            <h2 className="text-2xl font-heading font-bold flex items-center gap-2">
              <FileText className="w-6 h-6 text-primary" /> Available Exams
            </h2>

            <div className="grid gap-4">
              {dashboardData.available_exams.map((exam, index) => {
                const isLocked = exam.is_premium && !isPro;
                return (
                  <motion.div
                    key={exam.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className={`group relative rounded-2xl border p-6 transition-all duration-200 ${isLocked
                        ? "bg-muted/50 border-border opacity-75"
                        : "bg-card border-border hover:border-primary/50 hover:shadow-lg hover:shadow-primary/5"
                      }`}
                  >
                    <div className="flex flex-col md:flex-row justify-between md:items-center gap-4">
                      <div>
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="text-xl font-bold font-heading">{exam.name}</h3>
                          {exam.is_premium && (
                            <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-gradient-to-r from-yellow-400 to-orange-500 text-white shadow-sm">
                              PRO
                            </span>
                          )}
                        </div>
                        <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                          <span className="flex items-center gap-1"><Clock className="w-4 h-4" /> {exam.duration_minutes} mins</span>
                          <span className="flex items-center gap-1"><FileText className="w-4 h-4" /> {exam.total_questions} Qs</span>
                          <span className="flex items-center gap-1"><Award className="w-4 h-4" /> {exam.total_marks} Marks</span>
                        </div>
                      </div>

                      {isLocked ? (
                        <Button
                          onClick={() => router.push("/pricing")}
                          className="bg-muted-foreground/10 text-foreground hover:bg-primary hover:text-white transition-colors gap-2"
                          variant="outline"
                        >
                          <Lock className="w-4 h-4" /> Unlock
                        </Button>
                      ) : (
                        <Button
                          onClick={() => router.push(`/exam/${exam.id}`)}
                          className="gap-2 shadow-md shadow-primary/20"
                        >
                          <PlayCircle className="w-4 h-4" /> Start Exam
                        </Button>
                      )}
                    </div>
                  </motion.div>
                );
              })}

              {dashboardData.available_exams.length === 0 && (
                <div className="text-center py-12 bg-muted/20 rounded-2xl border border-dashed border-border text-muted-foreground">
                  No exams available at the moment.
                </div>
              )}
            </div>
          </div>

          {/* Recent Attempts Column */}
          <div className="space-y-6">
            <h2 className="text-2xl font-heading font-bold flex items-center gap-2">
              <TrendingUp className="w-6 h-6 text-primary" /> Recents
            </h2>

            <div className="bg-card rounded-2xl border border-border shadow-sm overflow-hidden">
              {dashboardData.recent_attempts.length > 0 ? (
                <div className="divide-y divide-border">
                  {dashboardData.recent_attempts.slice(0, 5).map((attempt) => (
                    <div
                      key={attempt.id}
                      className="p-4 hover:bg-muted/50 transition-colors cursor-pointer group"
                      onClick={() => router.push(`/results/${attempt.id}`)}
                    >
                      <div className="flex justify-between items-start mb-1">
                        <p className="font-semibold text-sm group-hover:text-primary transition-colors">{attempt.exam_name}</p>
                        <span className={`text-xs font-bold px-2 py-0.5 rounded ${attempt.percentage >= 80 ? "bg-green-100 text-green-700" :
                            attempt.percentage >= 60 ? "bg-blue-100 text-blue-700" :
                              "bg-orange-100 text-orange-700"
                          }`}>
                          {attempt.percentage}%
                        </span>
                      </div>
                      <div className="flex justify-between items-center text-xs text-muted-foreground">
                        <span className="flex items-center gap-1"><Calendar className="w-3 h-3" /> {attempt.date}</span>
                        <span className="font-medium">Score: {attempt.score}/{attempt.total_marks}</span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="p-8 text-center text-muted-foreground text-sm">
                  No attempts yet. Start an exam to see your progress here!
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

function StatCard({ title, value, icon, delay }: { title: string, value: string | number, icon: React.ReactNode, delay: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      className="bg-card p-6 rounded-2xl border border-border shadow-sm hover:shadow-md transition-shadow"
    >
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-medium text-muted-foreground">{title}</h3>
        <div className="p-2 bg-muted/50 rounded-lg">{icon}</div>
      </div>
      <p className="text-3xl font-bold font-heading tracking-tight">{value}</p>
    </motion.div>
  )
}
