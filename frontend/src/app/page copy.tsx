"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import {
  BookOpen,
  CheckCircle,
  Trophy,
  TrendingUp,
  Users,
  ShieldCheck,
} from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-background text-foreground overflow-x-hidden">
      {/* Navbar */}
      <nav className="fixed top-0 w-full z-50 glass border-b border-white/20">
        <div className="container mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <img
              src="/logo_sample.png"
              alt="DCEThelper Logo"
              className="h-20 w-auto object-contain"
            />
          </div>
          <div className="flex gap-4">
            <Link href="/contact">
              <Button
                variant="ghost"
                className="font-medium text-muted-foreground hover:text-primary"
              >
                Contact Us
              </Button>
            </Link>
            <Link href="/auth/login">
              <Button
                variant="ghost"
                className="font-medium text-muted-foreground hover:text-primary"
              >
                Login
              </Button>
            </Link>
            <Link href="/auth/signup">
              <Button className="rounded-full px-6 shadow-lg shadow-primary/25">
                Get Started
              </Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 px-6 overflow-hidden">
        {/* Background Gradients */}
        <div className="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top_right,_var(--tw-gradient-stops))] from-blue-100/50 via-background to-background dark:from-blue-900/20"></div>
        <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-purple-200/30 rounded-full blur-3xl opacity-50 pointer-events-none mix-blend-multiply"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-blue-200/30 rounded-full blur-3xl opacity-50 pointer-events-none mix-blend-multiply"></div>

        <div className="container mx-auto text-center max-w-5xl relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-50 border border-blue-100 text-blue-700 text-sm font-medium mb-8"
          >
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
            </span>
            #1 Platform for Diploma CET Preparation
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-5xl md:text-7xl lg:text-8xl font-heading font-extrabold tracking-tight mb-8 text-foreground"
          >
            Ace Your{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-purple-600">
              DCET Exam
            </span>{" "}
            <br className="hidden md:block" /> with Confidence.
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-xl md:text-2xl text-muted-foreground mb-10 max-w-3xl mx-auto leading-relaxed"
          >
            The comprehensive platform designed for diploma students. Unlock
            mock tests, track analytics, and secure your seat in a top
            engineering college.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center"
          >
            <Link href="/auth/signup">
              <Button
                size="lg"
                className="text-lg px-8 h-14 rounded-full shadow-xl shadow-primary/20 hover:shadow-primary/40 transition-all hover:scale-105 active:scale-95"
              >
                Start Practicing Free
              </Button>
            </Link>
            <Link href="/pricing">
              <Button
                size="lg"
                variant="outline"
                className="text-lg px-8 h-14 rounded-full border-2 hover:bg-secondary/50"
              >
                View Plans
              </Button>
            </Link>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 40, rotateX: -10 }}
            animate={{ opacity: 1, y: 0, rotateX: 0 }}
            transition={{ delay: 0.5, duration: 0.8 }}
            className="mt-16 relative mx-auto max-w-6xl"
          >
            {/* Modern Dashboard Preview */}
            <div className="relative">
              {/* Floating Cards Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-8 bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50 rounded-3xl border border-white/60 shadow-2xl backdrop-blur-sm">
                {/* Card 1: Performance Stats */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.6 }}
                  className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 hover:scale-105 cursor-pointer group"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="p-3 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg group-hover:shadow-blue-500/50 transition-shadow">
                      <svg
                        className="w-6 h-6 text-white"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                        />
                      </svg>
                    </div>
                    <span className="text-xs font-semibold text-blue-600 bg-blue-50 px-3 py-1 rounded-full">
                      Live
                    </span>
                  </div>
                  <h3 className="text-sm font-medium text-gray-500 mb-2">
                    Performance
                  </h3>
                  <div className="flex items-baseline gap-2">
                    <span className="text-3xl font-bold text-gray-900">
                      85%
                    </span>
                    <span className="text-sm text-green-600 font-medium">
                      ↑ 12%
                    </span>
                  </div>
                  <div className="mt-4 h-2 bg-gray-100 rounded-full overflow-hidden">
                    <div className="h-full w-[85%] bg-gradient-to-r from-blue-500 to-purple-500 rounded-full"></div>
                  </div>
                </motion.div>

                {/* Card 2: Mock Tests */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.7 }}
                  className="bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 cursor-pointer text-white group"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="p-3 bg-white/20 backdrop-blur-sm rounded-xl group-hover:bg-white/30 transition-colors">
                      <svg
                        className="w-6 h-6 text-white"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                        />
                      </svg>
                    </div>
                    <span className="text-xs font-semibold bg-white/20 backdrop-blur-sm px-3 py-1 rounded-full">
                      10 Tests
                    </span>
                  </div>
                  <h3 className="text-sm font-medium text-white/80 mb-2">
                    Mock Tests
                  </h3>
                  <div className="text-3xl font-bold mb-4">Ready</div>
                  <div className="flex gap-2">
                    {[90, 85, 65, 45].map((width, i) => (
                      <div
                        key={i}
                        className="h-1.5 flex-1 bg-white/30 rounded-full overflow-hidden"
                      >
                        <div
                          className="h-full bg-white rounded-full"
                          style={{ width: `${width}%` }}
                        ></div>
                      </div>
                    ))}
                  </div>
                </motion.div>

                {/* Card 3: Study Streak */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.8 }}
                  className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 hover:scale-105 cursor-pointer group"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="p-3 bg-gradient-to-br from-amber-400 to-orange-500 rounded-xl shadow-lg group-hover:shadow-amber-500/50 transition-shadow">
                      <svg
                        className="w-6 h-6 text-white"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z"
                        />
                      </svg>
                    </div>
                    <span className="text-xs font-semibold text-amber-600 bg-amber-50 px-3 py-1 rounded-full">
                      🔥 Streak
                    </span>
                  </div>
                  <h3 className="text-sm font-medium text-gray-500 mb-2">
                    Study Days
                  </h3>
                  <div className="text-3xl font-bold text-gray-900 mb-4">
                    7 Days
                  </div>
                  <div className="flex gap-1">
                    {[1, 2, 3, 4, 5, 6, 7].map((i) => (
                      <div
                        key={i}
                        className="flex-1 h-8 bg-gradient-to-t from-amber-400 to-amber-300 rounded-md"
                      ></div>
                    ))}
                  </div>
                </motion.div>

                {/* Card 4: Quick Actions */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.9 }}
                  className="bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 cursor-pointer text-white group md:col-span-2 lg:col-span-1"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="p-3 bg-white/20 backdrop-blur-sm rounded-xl group-hover:bg-white/30 transition-colors">
                      <svg
                        className="w-6 h-6 text-white"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M13 10V3L4 14h7v7l9-11h-7z"
                        />
                      </svg>
                    </div>
                  </div>
                  <h3 className="text-sm font-medium text-white/80 mb-2">
                    Quick Start
                  </h3>
                  <div className="text-2xl font-bold mb-4">Begin Practice</div>
                  <button className="w-full bg-white/20 hover:bg-white/30 backdrop-blur-sm text-white font-semibold py-2 px-4 rounded-xl transition-colors">
                    Start Now →
                  </button>
                </motion.div>

                {/* Card 5: Recent Activity */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 1.0 }}
                  className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 md:col-span-2 hover:scale-105 cursor-pointer group"
                >
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-sm font-semibold text-gray-900">
                      Recent Activity
                    </h3>
                    <span className="text-xs text-gray-500">Last 7 days</span>
                  </div>
                  <div className="space-y-3">
                    {[
                      {
                        name: "DCET 2023",
                        score: "92%",
                        color: "bg-green-500",
                      },
                      {
                        name: "Mock Test 5",
                        score: "85%",
                        color: "bg-blue-500",
                      },
                      {
                        name: "Practice Set",
                        score: "78%",
                        color: "bg-purple-500",
                      },
                    ].map((item, i) => (
                      <div key={i} className="flex items-center gap-3">
                        <div
                          className={`w-2 h-2 ${item.color} rounded-full`}
                        ></div>
                        <div className="flex-1 flex items-center justify-between">
                          <span className="text-sm text-gray-700">
                            {item.name}
                          </span>
                          <span className="text-sm font-semibold text-gray-900">
                            {item.score}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </motion.div>
              </div>

              {/* Decorative Elements */}
              <div className="absolute -inset-8 bg-gradient-to-r from-blue-500/20 via-purple-500/20 to-pink-500/20 rounded-3xl blur-3xl -z-10 animate-pulse"></div>
              <div className="absolute top-0 right-0 w-32 h-32 bg-blue-400/30 rounded-full blur-2xl -z-10"></div>
              <div className="absolute bottom-0 left-0 w-32 h-32 bg-purple-400/30 rounded-full blur-2xl -z-10"></div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-white relative">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-heading font-bold mb-4">
              Why Choose DCET Prep?
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Everything you need to crack the exam, all in one modern platform.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard
              icon={<BookOpen className="w-8 h-8 text-primary" />}
              title="Comprehensive Syllabus"
              description="Full coverage of Mathematics, Science, and specialized Engineering branches tailored for DCET."
              delay={0.1}
            />
            <FeatureCard
              icon={<ShieldCheck className="w-8 h-8 text-green-500" />}
              title="Real Exam Simulation"
              description="Practice in an environment that mimics the actual computer-based test to eliminate exam-day anxiety."
              delay={0.2}
            />
            <FeatureCard
              icon={<Trophy className="w-8 h-8 text-purple-500" />}
              title="In-Depth Analytics"
              description="Get detailed insights into your strong and weak areas with our advanced performance tracking."
              delay={0.3}
            />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 relative overflow-hidden">
        <div className="absolute inset-0 bg-primary -z-20"></div>
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10 -z-10"></div>
        <div className="container mx-auto px-6 text-center text-primary-foreground">
          <h2 className="text-3xl md:text-5xl font-heading font-bold mb-6">
            Ready to Top the Rank List?
          </h2>
          <p className="text-xl opacity-90 mb-10 max-w-2xl mx-auto">
            Join thousands of students preparing smarter, not harder. Start your
            journey today.
          </p>
          <Link href="/auth/signup">
            <Button
              size="lg"
              variant="secondary"
              className="text-lg px-10 h-14 rounded-full font-bold shadow-2xl"
            >
              Get Started for Free
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-slate-50 border-t border-border">
        <div className="container mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-2">
            <img
              src="/logo_sample.png"
              alt="DCEThelper Logo"
              className="h-16 w-auto object-contain"
            />
          </div>
          <div className="text-sm text-muted-foreground">
            © 2025 Apollo11 EdTech. All rights reserved.
          </div>
          <div className="flex gap-6 text-sm text-muted-foreground">
            <Link
              href="/contact"
              className="hover:text-primary transition-colors"
            >
              Contact
            </Link>
            <Link href="#" className="hover:text-primary transition-colors">
              Privacy
            </Link>
            <Link href="#" className="hover:text-primary transition-colors">
              Terms
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  description,
  delay,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
  delay: number;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay }}
      whileHover={{ y: -5 }}
      className="p-8 rounded-2xl bg-slate-50 border border-slate-100 shadow-sm hover:shadow-xl hover:shadow-primary/5 transition-all duration-300"
    >
      <div className="mb-6 w-14 h-14 rounded-xl bg-white shadow-sm flex items-center justify-center border border-slate-100">
        {icon}
      </div>
      <h3 className="text-2xl font-bold mb-3 text-slate-900">{title}</h3>
      <p className="text-slate-600 leading-relaxed">{description}</p>
    </motion.div>
  );
}
