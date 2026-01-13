"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
import { authService } from "@/lib/services/auth.service";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowLeft, User, Lock, Eye, EyeOff } from "lucide-react";
import { motion } from "framer-motion";

export default function LoginPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  // Clear tokens on load
  useEffect(() => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await authService.login(formData);
      router.push("/dashboard");
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.error ||
        err.response?.data?.detail ||
        "Invalid credentials. Please try again.";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    // FULL SCREEN OVERLAY
    <div className="fixed inset-0 z-50 w-screen h-screen bg-gray-50 flex items-center justify-center p-4">

      {/* MAIN CARD */}
      <div className="w-full max-w-5xl bg-white rounded-[32px] shadow-xl overflow-hidden flex flex-col lg:flex-row h-auto lg:h-[650px] border border-gray-200">

        {/* LEFT SIDE: Image & Text */}
        {/* Added 'border-r' here creates the vertical line between sections */}
        <div className="hidden lg:flex w-1/2 relative flex-col items-center justify-center p-12 bg-white border-r border-gray-100">

          {/* Subtle Background Blob */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] bg-blue-50/50 rounded-full blur-3xl -z-10" />

          {/* Text Section */}
          <div className="text-center space-y-3 mb-8 relative z-10">
            <h1 className="text-3xl font-bold font-heading text-gray-900 tracking-tight">
              Welcome to DCET Prep
            </h1>
            <p className="text-gray-500 text-base max-w-xs mx-auto">
              Your gateway to engineering excellence.
            </p>
          </div>

          {/* THE ILLUSTRATION */}
          <div className="relative w-full max-w-[420px] aspect-square">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              className="relative w-full h-full"
            >
              <Image
                src="/study-illustration.png"
                alt="Student studying"
                fill
                className="object-contain"
                priority
              />
            </motion.div>
          </div>
        </div>

        {/* RIGHT SIDE: Login Form */}
        <div className="w-full lg:w-1/2 flex flex-col items-center justify-center p-8 lg:p-16 bg-white relative">

          {/* Back Button */}
          <div className="absolute top-6 left-6">
            <Link href="/">
              <Button variant="ghost" size="sm" className="text-gray-500 gap-2 hover:bg-gray-50 pl-2 transition-colors">
                <ArrowLeft className="w-4 h-4" />
                Back
              </Button>
            </Link>
          </div>

          <div className="w-full max-w-[350px] space-y-6">
            <div className="text-center space-y-2">
              <h2 className="text-2xl font-bold font-heading text-gray-900">Sign In</h2>
              <p className="text-gray-500">Access your dashboard</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-4">

                {/* Email Field */}
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-gray-700 ml-1">Email</label>
                  <div className="relative group">
                    <User className="absolute left-3 top-3 h-5 w-5 text-gray-400 group-focus-within:text-blue-600 transition-colors" />
                    <Input
                      type="text"
                      placeholder="student@example.com"
                      value={formData.username}
                      onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                      required
                      className="pl-10 h-11 bg-gray-50 border-gray-200 focus:bg-white focus:border-blue-500 transition-all"
                    />
                  </div>
                </div>

                {/* Password Field */}
                <div className="space-y-2">
                  <div className="flex justify-between items-center ml-1">
                    <label className="text-sm font-semibold text-gray-700">Password</label>
                    <Link href="/auth/forgot-password" className="text-xs font-semibold text-blue-600 hover:underline">
                      Forgot?
                    </Link>
                  </div>
                  <div className="relative group">
                    <Lock className="absolute left-3 top-3 h-5 w-5 text-gray-400 group-focus-within:text-blue-600 transition-colors" />
                    <Input
                      type={showPassword ? "text" : "password"}
                      placeholder="••••••••"
                      value={formData.password}
                      onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                      required
                      className="pl-10 pr-10 h-11 bg-gray-50 border-gray-200 focus:bg-white focus:border-blue-500 transition-all"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-3 text-gray-400 hover:text-gray-600 transition-colors focus:outline-none"
                    >
                      {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                    </button>
                  </div>
                </div>
              </div>

              {/* Error Message */}
              {error && (
                <div className="bg-red-50 text-red-600 text-sm p-3 rounded-lg flex items-center gap-2">
                  <div className="w-1.5 h-1.5 bg-red-600 rounded-full" />
                  {error}
                </div>
              )}

              {/* Submit Button */}
              <Button type="submit" className="w-full h-11 font-bold text-base bg-blue-600 hover:bg-blue-700 text-white shadow-lg shadow-blue-600/20 transition-all" disabled={loading}>
                {loading ? "Signing in..." : "Sign In"}
              </Button>

              {/* Sign Up Link */}
              <div className="text-center text-sm text-gray-500 pt-2">
                New here?{" "}
                <Link href="/auth/signup" className="text-blue-600 font-bold hover:underline">
                  Create account
                </Link>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}