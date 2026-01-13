"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import {
  BookOpen,
  CheckCircle,
  Trophy,
  TrendingUp,
  Users,
  ShieldCheck,
  Quote,
  Target,
  Clock,
  Video,
  FileText,
  BarChart3,
  Zap,
  Brain,
  Calendar,
  Award,
  ChevronDown,
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
                Start Practicing
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
              Why Choose DCEThelper?
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

      {/* Stats Section */}
      <section className="py-20 bg-gradient-to-br from-blue-50 to-purple-50 relative overflow-hidden">
        <div className="container mx-auto px-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center"
            >
              <div className="text-4xl md:text-5xl font-bold text-primary mb-2">
                500+
              </div>
              <div className="text-slate-600 font-medium">
                Practice Questions
              </div>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="text-center"
            >
              <div className="text-4xl md:text-5xl font-bold text-green-600 mb-2">
                10+
              </div>
              <div className="text-slate-600 font-medium">Full Mock Tests</div>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
              className="text-center"
            >
              <div className="text-4xl md:text-5xl font-bold text-purple-600 mb-2">
                100%
              </div>
              <div className="text-slate-600 font-medium">
                Syllabus Coverage
              </div>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.3 }}
              className="text-center"
            >
              <div className="text-4xl md:text-5xl font-bold text-orange-600 mb-2">
                24/7
              </div>
              <div className="text-slate-600 font-medium">Study Access</div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-24 bg-white">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-heading font-bold mb-4">
              How It Works
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Your journey to DCET success in 4 simple steps
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <StepCard
              number="1"
              icon={<Users className="w-8 h-8" />}
              title="Sign Up Free"
              description="Create your account in seconds. No credit card required."
              color="blue"
            />
            <StepCard
              number="2"
              icon={<Target className="w-8 h-8" />}
              title="Choose Your Path"
              description="Select your engineering branch and set your target score."
              color="green"
            />
            <StepCard
              number="3"
              icon={<Brain className="w-8 h-8" />}
              title="Practice Smart"
              description="Take mock tests and track your improvement with analytics."
              color="purple"
            />
            <StepCard
              number="4"
              icon={<Award className="w-8 h-8" />}
              title="Ace the Exam"
              description="Enter the exam hall confident and prepared to succeed."
              color="orange"
            />
          </div>
        </div>
      </section>

      {/* Detailed Features Section */}
      <section className="py-24 bg-slate-50">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-heading font-bold mb-4">
              Everything You Need to Excel
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Powerful features designed for serious DCET aspirants
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <DetailedFeatureCard
              icon={<Clock className="w-10 h-10 text-blue-500" />}
              title="Timed Mock Tests"
              description="Practice with real exam time limits. Build speed and accuracy under pressure."
            />
            <DetailedFeatureCard
              icon={<Video className="w-10 h-10 text-red-500" />}
              title="Video Solutions"
              description="Watch detailed explanations for every question. Learn from expert teachers."
            />
            <DetailedFeatureCard
              icon={<FileText className="w-10 h-10 text-green-500" />}
              title="Previous Year Papers"
              description="Access and practice all DCET previous year questions with solutions."
            />
            <DetailedFeatureCard
              icon={<BarChart3 className="w-10 h-10 text-purple-500" />}
              title="Performance Analytics"
              description="Detailed insights into your strengths, weaknesses, and improvement areas."
            />
            <DetailedFeatureCard
              icon={<Zap className="w-10 h-10 text-yellow-500" />}
              title="Instant Results"
              description="Get your scores immediately with detailed analysis of each attempt."
            />
            <DetailedFeatureCard
              icon={<Calendar className="w-10 h-10 text-pink-500" />}
              title="Study Planner"
              description="Track your preparation with daily goals and progress monitoring."
            />
          </div>
        </div>
      </section>

      {/* Motivational Quotes Section */}
      <section className="py-20 bg-gradient-to-br from-slate-50 to-blue-50 relative overflow-hidden">
        <div className="container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="max-w-4xl mx-auto"
          >
            <QuoteCarousel />
          </motion.div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="pt-24 pb-12 bg-white">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-heading font-bold mb-4">
              Frequently Asked Questions
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Everything you need to know about DCEThelper
            </p>
          </div>

          <div className="max-w-3xl mx-auto space-y-4">
            <FAQItem
              question="Is DCEThelper really free to use?"
              answer="Yes! We offer a free plan with access to practice questions and mock tests. Premium plans unlock additional features like video solutions and advanced analytics."
            />
            <FAQItem
              question="Are the mock tests similar to the actual DCET exam?"
              answer="Absolutely. Our mock tests are designed to replicate the actual DCET exam pattern, difficulty level, and computer-based test interface to give you authentic practice."
            />
            <FAQItem
              question="Can I access the platform on my mobile device?"
              answer="Yes! DCEThelper is fully responsive and works seamlessly on smartphones, tablets, and computers. Study anywhere, anytime."
            />
            <FAQItem
              question="How often is the content updated?"
              answer="We regularly update our question bank and add new mock tests. Content is reviewed and updated to match the latest DCET syllabus and exam pattern."
            />
            <FAQItem
              question="Do you provide solutions for all questions?"
              answer="Yes! Every question comes with detailed written solutions. Premium members also get access to video explanations from expert teachers."
            />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 relative overflow-hidden bg-gradient-to-br from-blue-600 to-purple-600">
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
        <div className="container mx-auto px-6 text-center text-white relative z-10">
          <h2 className="text-3xl md:text-5xl font-heading font-bold mb-6">
            Ready to Top the Rank List?
          </h2>
          <p className="text-xl mb-10 max-w-2xl mx-auto">
            Join thousands of students preparing smarter, not harder. Start your
            journey today.
          </p>
          <Link href="/auth/signup">
            <Button
              size="lg"
              variant="secondary"
              className="text-lg px-10 h-14 rounded-full font-bold shadow-2xl bg-white text-blue-600 hover:bg-slate-100"
            >
              Get Started
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-16 bg-slate-900 text-white">
        <div className="container mx-auto px-6">
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-12 mb-12">
            {/* Brand Column */}
            <div>
              <div className="flex items-center gap-2 mb-4">
                <img
                  src="/logo_sample.png"
                  alt="DCEThelper Logo"
                  className="h-16 w-auto object-contain brightness-0 invert"
                />
              </div>
              <p className="text-slate-400 leading-relaxed mb-4">
                Your trusted companion for DCET exam preparation. Practice
                smarter, perform better.
              </p>
              <div className="flex gap-4">
                <a
                  href="#"
                  className="w-10 h-10 rounded-full bg-slate-800 hover:bg-primary flex items-center justify-center transition-colors"
                >
                  <svg
                    className="w-5 h-5"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
                  </svg>
                </a>
                <a
                  href="#"
                  className="w-10 h-10 rounded-full bg-slate-800 hover:bg-primary flex items-center justify-center transition-colors"
                >
                  <svg
                    className="w-5 h-5"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z" />
                  </svg>
                </a>
                <a
                  href="#"
                  className="w-10 h-10 rounded-full bg-slate-800 hover:bg-primary flex items-center justify-center transition-colors"
                >
                  <svg
                    className="w-5 h-5"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm4.441 16.892c-2.102.144-6.784.144-8.883 0C5.282 16.736 5.017 15.622 5 12c.017-3.629.285-4.736 2.558-4.892 2.099-.144 6.782-.144 8.883 0C18.718 7.264 18.982 8.378 19 12c-.018 3.629-.285 4.736-2.559 4.892zM10 9.658l4.917 2.338L10 14.342V9.658z" />
                  </svg>
                </a>
              </div>
            </div>

            {/* Quick Links */}
            <div>
              <h4 className="font-bold text-lg mb-4">Quick Links</h4>
              <ul className="space-y-2">
                <li>
                  <Link
                    href="/auth/signup"
                    className="text-slate-400 hover:text-white transition-colors"
                  >
                    Sign Up Free
                  </Link>
                </li>
                <li>
                  <Link
                    href="/auth/login"
                    className="text-slate-400 hover:text-white transition-colors"
                  >
                    Login
                  </Link>
                </li>
                <li>
                  <Link
                    href="/pricing"
                    className="text-slate-400 hover:text-white transition-colors"
                  >
                    Pricing Plans
                  </Link>
                </li>
                <li>
                  <Link
                    href="/dashboard"
                    className="text-slate-400 hover:text-white transition-colors"
                  >
                    Dashboard
                  </Link>
                </li>
              </ul>
            </div>

            {/* Resources */}
            <div>
              <h4 className="font-bold text-lg mb-4">Resources</h4>
              <ul className="space-y-2">
                <li>
                  <Link
                    href="/pyqs"
                    className="text-slate-400 hover:text-white transition-colors"
                  >
                    Previous Year Papers
                  </Link>
                </li>
                <li>
                  <Link
                    href="/notes"
                    className="text-slate-400 hover:text-white transition-colors"
                  >
                    Study Notes
                  </Link>
                </li>
                <li>
                  <Link
                    href="/videos"
                    className="text-slate-400 hover:text-white transition-colors"
                  >
                    Video Solutions
                  </Link>
                </li>
                <li>
                  <Link
                    href="/results"
                    className="text-slate-400 hover:text-white transition-colors"
                  >
                    My Results
                  </Link>
                </li>
              </ul>
            </div>

            {/* Support */}
            <div>
              <h4 className="font-bold text-lg mb-4">Support</h4>
              <ul className="space-y-2">
                <li>
                  <Link
                    href="/contact"
                    className="text-slate-400 hover:text-white transition-colors"
                  >
                    Contact Us
                  </Link>
                </li>
                <li>
                  <Link
                    href="#"
                    className="text-slate-400 hover:text-white transition-colors"
                  >
                    Help Center
                  </Link>
                </li>
                <li>
                  <Link
                    href="#"
                    className="text-slate-400 hover:text-white transition-colors"
                  >
                    Privacy Policy
                  </Link>
                </li>
                <li>
                  <Link
                    href="#"
                    className="text-slate-400 hover:text-white transition-colors"
                  >
                    Terms of Service
                  </Link>
                </li>
              </ul>
            </div>
          </div>

          {/* Bottom Bar */}
          <div className="pt-8 border-t border-slate-800 flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="text-sm text-slate-400">
              © 2026 DCEThelper by Apollo12 EdTech. All rights reserved.
            </div>
            <div className="flex items-center gap-4 text-sm text-slate-400">
              <span>Made with ❤️ for DCET aspirants</span>
            </div>
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

function StepCard({
  number,
  icon,
  title,
  description,
  color,
}: {
  number: string;
  icon: React.ReactNode;
  title: string;
  description: string;
  color: string;
}) {
  const colorClasses = {
    blue: "from-blue-500 to-blue-600 shadow-blue-500/50",
    green: "from-green-500 to-green-600 shadow-green-500/50",
    purple: "from-purple-500 to-purple-600 shadow-purple-500/50",
    orange: "from-orange-500 to-orange-600 shadow-orange-500/50",
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      className="relative"
    >
      <div className="text-center">
        <div
          className={`inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br ${
            colorClasses[color as keyof typeof colorClasses]
          } text-white shadow-lg mb-4`}
        >
          {icon}
        </div>
        <div className="absolute top-0 right-0 w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center font-bold text-slate-700 text-sm">
          {number}
        </div>
        <h3 className="text-xl font-bold mb-2 text-slate-900">{title}</h3>
        <p className="text-slate-600">{description}</p>
      </div>
    </motion.div>
  );
}

function DetailedFeatureCard({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      whileHover={{ y: -5 }}
      className="bg-white rounded-2xl p-8 shadow-md hover:shadow-xl transition-all duration-300 border border-slate-100"
    >
      <div className="mb-4">{icon}</div>
      <h3 className="text-xl font-bold mb-3 text-slate-900">{title}</h3>
      <p className="text-slate-600 leading-relaxed">{description}</p>
    </motion.div>
  );
}

function FAQItem({ question, answer }: { question: string; answer: string }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true }}
      className="border border-slate-200 rounded-xl overflow-hidden bg-white"
    >
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-6 py-5 flex items-center justify-between text-left hover:bg-slate-50 transition-colors"
      >
        <span className="font-semibold text-slate-900 pr-8">{question}</span>
        <ChevronDown
          className={`w-5 h-5 text-slate-500 transition-transform flex-shrink-0 ${
            isOpen ? "rotate-180" : ""
          }`}
        />
      </button>
      <motion.div
        initial={false}
        animate={{ height: isOpen ? "auto" : 0 }}
        className="overflow-hidden"
      >
        <div className="px-6 pb-5 text-slate-600 leading-relaxed">{answer}</div>
      </motion.div>
    </motion.div>
  );
}

function QuoteCarousel() {
  const quotes = [
    {
      text: "Success is not final, failure is not fatal: it is the courage to continue that counts.",
      author: "Winston Churchill",
    },
    {
      text: "The expert in anything was once a beginner. Keep learning, keep growing.",
      author: "Helen Hayes",
    },
    {
      text: "Education is the most powerful weapon which you can use to change the world.",
      author: "Nelson Mandela",
    },
    {
      text: "The beautiful thing about learning is that no one can take it away from you.",
      author: "B.B. King",
    },
    {
      text: "Success is the sum of small efforts repeated day in and day out.",
      author: "Robert Collier",
    },
    {
      text: "Your only limit is you. Believe in yourself and great things will happen.",
      author: "Anonymous",
    },
  ];

  const [currentQuote, setCurrentQuote] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentQuote((prev) => (prev + 1) % quotes.length);
    }, 5000); // Change quote every 5 seconds

    return () => clearInterval(interval);
  }, [quotes.length]);

  return (
    <div className="relative">
      {/* Decorative Background Elements */}
      <div className="absolute -inset-4 bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-pink-500/10 rounded-3xl blur-2xl"></div>

      <div className="relative bg-white/80 backdrop-blur-sm rounded-3xl p-12 shadow-xl border border-white/60">
        {/* Decorative Quote Marks */}
        <div className="absolute top-6 left-6 text-blue-100 opacity-50">
          <svg className="w-10 h-10" fill="currentColor" viewBox="0 0 24 24">
            <path d="M6 17h3l2-4V7H5v6h3zm8 0h3l2-4V7h-6v6h3z" />
          </svg>
        </div>
        <div className="absolute bottom-6 right-6 text-blue-100 opacity-50 rotate-180">
          <svg className="w-10 h-10" fill="currentColor" viewBox="0 0 24 24">
            <path d="M6 17h3l2-4V7H5v6h3zm8 0h3l2-4V7h-6v6h3z" />
          </svg>
        </div>

        {/* Quote Content */}
        <div className="relative z-10 text-center">
          <motion.div
            key={currentQuote}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.5 }}
          >
            <p className="text-2xl md:text-3xl font-semibold text-slate-800 mb-6 leading-relaxed italic">
              "{quotes[currentQuote].text}"
            </p>
            <p className="text-lg text-slate-600 font-medium">
              — {quotes[currentQuote].author}
            </p>
          </motion.div>
        </div>

        {/* Progress Bars */}
        <div className="flex gap-2 mt-8 justify-center">
          {quotes.map((_, index) => (
            <div
              key={index}
              className="relative h-1 flex-1 max-w-[60px] bg-slate-200 rounded-full overflow-hidden"
            >
              <motion.div
                className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full"
                initial={{ width: "0%" }}
                animate={{
                  width: currentQuote === index ? "100%" : "0%",
                }}
                transition={{
                  duration: currentQuote === index ? 5 : 0,
                  ease: "linear",
                }}
              />
            </div>
          ))}
        </div>

        {/* Navigation Dots */}
        <div className="flex gap-2 mt-4 justify-center">
          {quotes.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentQuote(index)}
              className={`w-2.5 h-2.5 rounded-full transition-all duration-300 ${
                currentQuote === index
                  ? "bg-blue-500 scale-125"
                  : "bg-slate-300 hover:bg-slate-400"
              }`}
              aria-label={`Go to quote ${index + 1}`}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
