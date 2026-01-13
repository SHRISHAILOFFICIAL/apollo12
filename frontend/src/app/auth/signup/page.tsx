"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
import { authService } from "@/lib/services/auth.service";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowLeft, User, Mail, Lock, Phone, Eye, EyeOff } from "lucide-react";
import { motion } from "framer-motion";

type SignupStep = "email" | "otp" | "details";

export default function SignupPage() {
  const router = useRouter();
  const [step, setStep] = useState<SignupStep>("email");
  const [email, setEmail] = useState("");
  const [otp, setOtp] = useState("");
  const [formData, setFormData] = useState({
    username: "",
    phone: "",
    password: "",
    confirm_password: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);


  // Clear tokens on load
  useEffect(() => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
  }, []);

  // --- STEP 1: Send OTP ---
  const handleSendOTP = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await authService.sendSignupOTP(email);
      setStep("otp");
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || "Failed to send OTP. Please try again.";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // --- STEP 2: Verify OTP ---
  const handleVerifyOTP = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await authService.verifySignupOTP(email, otp);
      setStep("details");
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || "Invalid or expired OTP. Please try again.";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // --- STEP 3: Complete Signup ---
  const handleCompleteSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await authService.register({
        username: formData.username,
        email: email,
        phone: formData.phone,
        password: formData.password,
        confirm_password: formData.confirm_password,
      });
      router.push("/auth/login?registered=true");
    } catch (err: any) {
      const errorData = err.response?.data;
      let errorMessage = "Registration failed. Please try again.";

      if (errorData) {
        if (typeof errorData === "string") {
          errorMessage = errorData;
        } else if (errorData.username) {
          errorMessage = `Username: ${errorData.username[0]}`;
        } else if (errorData.password) {
          errorMessage = `Password: ${errorData.password[0]}`;
        } else if (errorData.error) {
          errorMessage = errorData.error;
        }
      }
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleResendOTP = async () => {
    setError("");
    setLoading(true);
    try {
      await authService.sendSignupOTP(email);
      setError("");
      alert("OTP sent successfully!");
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to resend OTP");
    } finally {
      setLoading(false);
    }
  };

  // --- UI Components for each step ---

  const renderEmailStep = () => (
    <form onSubmit={handleSendOTP} className="space-y-6">
      <div className="space-y-2">
        <label className="text-sm font-semibold text-gray-700 ml-1">Email</label>
        <div className="relative group">
          <Mail className="absolute left-3 top-3 h-5 w-5 text-gray-400 group-focus-within:text-blue-600 transition-colors" />
          <Input
            type="email"
            placeholder="student@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="pl-10 h-11 bg-gray-50 border-gray-200 focus:bg-white focus:border-blue-500 transition-all"
          />
        </div>
      </div>

      {error && <div className="bg-red-50 text-red-600 text-sm p-3 rounded-lg">{error}</div>}

      <Button type="submit" className="w-full h-11 font-bold text-base bg-blue-600 hover:bg-blue-700 text-white shadow-lg shadow-blue-600/20 transition-all" disabled={loading}>
        {loading ? "Sending OTP..." : "Continue"}
      </Button>

      <div className="text-center text-sm text-gray-500 pt-2">
        Already have an account?{" "}
        <Link href="/auth/login" className="text-blue-600 font-bold hover:underline">
          Log in here
        </Link>
      </div>
    </form>
  );

  const renderOtpStep = () => (
    <form onSubmit={handleVerifyOTP} className="space-y-6">
      <div className="space-y-2">
        <label className="text-sm font-semibold text-gray-700 ml-1">Enter OTP</label>
        <Input
          type="text"
          placeholder="• • • • • •"
          value={otp}
          onChange={(e) => setOtp(e.target.value.replace(/\D/g, "").slice(0, 6))}
          required
          maxLength={6}
          className="h-12 bg-gray-50 border-gray-200 focus:bg-white focus:border-blue-500 transition-all text-center text-2xl tracking-[0.5em] font-bold"
        />
        <p className="text-xs text-gray-500 text-center">Code sent to {email}. Expires in 10 minutes.</p>
      </div>

      {error && <div className="bg-red-50 text-red-600 text-sm p-3 rounded-lg">{error}</div>}

      <Button type="submit" className="w-full h-11 font-bold text-base bg-blue-600 hover:bg-blue-700 text-white shadow-lg shadow-blue-600/20 transition-all" disabled={loading || otp.length !== 6}>
        {loading ? "Verifying..." : "Verify Email"}
      </Button>

      <div className="text-center text-sm space-x-2">
        <button type="button" onClick={handleResendOTP} className="text-blue-600 font-semibold hover:underline" disabled={loading}>
          Resend OTP
        </button>
        <span className="text-gray-400">|</span>
        <button type="button" onClick={() => setStep("email")} className="text-gray-500 hover:text-gray-700 hover:underline">
          Change email
        </button>
      </div>
    </form>
  );

  const renderDetailsStep = () => (
    <form onSubmit={handleCompleteSignup} className="space-y-4">
      <div className="space-y-2">
        <label className="text-sm font-semibold text-gray-700 ml-1">Username</label>
        <div className="relative group">
          <User className="absolute left-3 top-3 h-5 w-5 text-gray-400 group-focus-within:text-blue-600 transition-colors" />
          <Input
            type="text"
            placeholder="Choose a username"
            value={formData.username}
            onChange={(e) => setFormData({ ...formData, username: e.target.value })}
            required
            className="pl-10 h-11 bg-gray-50 border-gray-200 focus:bg-white focus:border-blue-500 transition-all"
          />
        </div>
      </div>
      <div className="space-y-2">
        <label className="text-sm font-semibold text-gray-700 ml-1">Phone Number</label>
        <div className="relative group">
          <Phone className="absolute left-3 top-3 h-5 w-5 text-gray-400 group-focus-within:text-blue-600 transition-colors" />
          <Input
            type="tel"
            placeholder="+91 9876543210"
            value={formData.phone}
            onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
            required
            minLength={10}
            maxLength={15}
            className="pl-10 h-11 bg-gray-50 border-gray-200 focus:bg-white focus:border-blue-500 transition-all"
          />
        </div>
      </div>
      <div className="space-y-2">
        <label className="text-sm font-semibold text-gray-700 ml-1">Password</label>
        <div className="relative group">
          <Lock className="absolute left-3 top-3 h-5 w-5 text-gray-400 group-focus-within:text-blue-600 transition-colors" />
          <Input
            type={showPassword ? "text" : "password"}
            placeholder="Min 6 characters"
            value={formData.password}
            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
            required
            minLength={6}
            className="pl-10 pr-10 h-11 bg-gray-50 border-gray-200 focus:bg-white focus:border-blue-500 transition-all"
          />
          <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-3 text-gray-400 hover:text-gray-600 focus:outline-none">
            {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
          </button>
        </div>
      </div>
      <div className="space-y-2">
        <label className="text-sm font-semibold text-gray-700 ml-1">Confirm Password</label>
        <div className="relative group">
          <Lock className="absolute left-3 top-3 h-5 w-5 text-gray-400 group-focus-within:text-blue-600 transition-colors" />
          <Input
            type={showConfirmPassword ? "text" : "password"}
            placeholder="Re-enter password"
            value={formData.confirm_password}
            onChange={(e) => setFormData({ ...formData, confirm_password: e.target.value })}
            required
            minLength={6}
            className="pl-10 pr-10 h-11 bg-gray-50 border-gray-200 focus:bg-white focus:border-blue-500 transition-all"
          />
          <button type="button" onClick={() => setShowConfirmPassword(!showConfirmPassword)} className="absolute right-3 top-3 text-gray-400 hover:text-gray-600 focus:outline-none">
            {showConfirmPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {error && <div className="bg-red-50 text-red-600 text-sm p-3 rounded-lg">{error}</div>}

      <Button type="submit" className="w-full h-11 font-bold text-base bg-blue-600 hover:bg-blue-700 text-white shadow-lg shadow-blue-600/20 transition-all" disabled={loading}>
        {loading ? "Creating account..." : "Complete Signup"}
      </Button>
    </form>
  );


  return (
    // FULL SCREEN OVERLAY
    <div className="fixed inset-0 z-50 w-screen h-screen bg-gray-50 flex items-center justify-center p-4 overflow-y-auto">

      {/* MAIN CARD */}
      <div className="w-full max-w-5xl bg-white border border-gray-200 rounded-[32px] shadow-xl overflow-hidden flex flex-col lg:flex-row h-auto min-h-[650px] relative">

        {/* LEFT SIDE: Image & Text */}
        <div className="hidden lg:flex w-1/2 relative flex-col items-center justify-center p-12 bg-white border-r border-gray-100">

          {/* Subtle Background Blob */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] bg-purple-50/50 rounded-full blur-3xl -z-10" />

          {/* Text Section */}
          <div className="text-center space-y-3 mb-8 relative z-10">
            <h1 className="text-3xl font-bold font-heading text-gray-900 tracking-tight">
              Join DCET Prep
            </h1>
            <p className="text-gray-500 text-base max-w-xs mx-auto">
              Create your account and start your journey to success.
            </p>
          </div>

          {/* THE ILLUSTRATION - Added negative margin-top (-mt-10) to pull it up */}
          <div className="relative w-full max-w-[420px] aspect-square -mt-10">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              className="relative w-full h-full"
            >
              {/* Make sure to save the new image as 'signup-illustration.png' in your public folder */}
              <Image
                src="/signup-illustration.png"
                alt="Student launching rocket"
                fill
                className="object-contain"
                priority
              />
            </motion.div>
          </div>
        </div>

        {/* RIGHT SIDE: Dynamic Form Section */}
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

          <div className="w-full max-w-[350px] space-y-6 mt-10 lg:mt-0">
            <div className="text-center space-y-2">
              <h2 className="text-2xl font-bold font-heading text-gray-900">
                {step === "email" && "Create Account"}
                {step === "otp" && "Verify Email"}
                {step === "details" && "Final Details"}
              </h2>
              <p className="text-gray-500">
                {step === "email" && "It's free and takes 1 minute"}
                {step === "otp" && "Enter the code we just sent you"}
                {step === "details" && "Almost there! Set up your profile"}
              </p>
            </div>

            {/* Dynamic Form Rendering based on 'step' */}
            {step === "email" && renderEmailStep()}
            {step === "otp" && renderOtpStep()}
            {step === "details" && renderDetailsStep()}

          </div>
        </div>
      </div>
    </div>
  );
}