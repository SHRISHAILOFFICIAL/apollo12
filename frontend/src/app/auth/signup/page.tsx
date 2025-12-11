"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { authService } from "@/lib/services/auth.service";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { UserPlus, Mail, CheckCircle } from "lucide-react";

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

  // Clear any existing tokens when visiting signup page
  useState(() => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
  });

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
      setError(""); // Clear any previous errors
      alert("OTP sent successfully!");
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to resend OTP");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-secondary/30 px-4 py-12">
      <Card className="w-full max-w-md glass">
        <CardHeader className="space-y-1 text-center">
          <div className="flex justify-center mb-4">
            <div className="p-3 rounded-full bg-primary/10">
              {step === "email" && <Mail className="w-6 h-6 text-primary" />}
              {step === "otp" && <CheckCircle className="w-6 h-6 text-primary" />}
              {step === "details" && <UserPlus className="w-6 h-6 text-primary" />}
            </div>
          </div>
          <CardTitle className="text-2xl font-bold">
            {step === "email" && "Create an account"}
            {step === "otp" && "Verify your email"}
            {step === "details" && "Complete your profile"}
          </CardTitle>
          <p className="text-sm text-muted-foreground">
            {step === "email" && "Enter your email to get started"}
            {step === "otp" && `We sent a code to ${email}`}
            {step === "details" && "Just a few more details"}
          </p>
        </CardHeader>
        <CardContent>
          {/* Step 1: Email Entry */}
          {step === "email" && (
            <form onSubmit={handleSendOTP} className="space-y-4">
              <div className="space-y-2">
                <Input
                  type="email"
                  placeholder="Email address"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="bg-background/50"
                />
              </div>

              {error && (
                <div className="text-destructive text-sm text-center bg-destructive/10 p-2 rounded-md">
                  {error}
                </div>
              )}

              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? "Sending OTP..." : "Continue"}
              </Button>

              <div className="text-center text-sm text-muted-foreground">
                Already have an account?{" "}
                <Link href="/auth/login" className="text-primary hover:underline font-medium">
                  Sign in
                </Link>
              </div>
            </form>
          )}

          {/* Step 2: OTP Verification */}
          {step === "otp" && (
            <form onSubmit={handleVerifyOTP} className="space-y-4">
              <div className="space-y-2">
                <Input
                  type="text"
                  placeholder="Enter 6-digit OTP"
                  value={otp}
                  onChange={(e) => setOtp(e.target.value.replace(/\D/g, "").slice(0, 6))}
                  required
                  maxLength={6}
                  className="bg-background/50 text-center text-2xl tracking-widest"
                />
                <p className="text-xs text-muted-foreground text-center">
                  Code expires in 10 minutes
                </p>
              </div>

              {error && (
                <div className="text-destructive text-sm text-center bg-destructive/10 p-2 rounded-md">
                  {error}
                </div>
              )}

              <Button type="submit" className="w-full" disabled={loading || otp.length !== 6}>
                {loading ? "Verifying..." : "Verify Email"}
              </Button>

              <div className="text-center text-sm">
                <button
                  type="button"
                  onClick={handleResendOTP}
                  className="text-primary hover:underline"
                  disabled={loading}
                >
                  Resend OTP
                </button>
                {" | "}
                <button
                  type="button"
                  onClick={() => setStep("email")}
                  className="text-muted-foreground hover:underline"
                >
                  Change email
                </button>
              </div>
            </form>
          )}

          {/* Step 3: Complete Signup */}
          {step === "details" && (
            <form onSubmit={handleCompleteSignup} className="space-y-4">
              <div className="space-y-2">
                <Input
                  type="text"
                  placeholder="Username"
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  required
                  className="bg-background/50"
                />
              </div>
              <div className="space-y-2">
                <Input
                  type="tel"
                  placeholder="Phone Number (optional)"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  className="bg-background/50"
                />
              </div>
              <div className="space-y-2">
                <Input
                  type="password"
                  placeholder="Password (min 6 characters)"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  required
                  minLength={6}
                  className="bg-background/50"
                />
              </div>
              <div className="space-y-2">
                <Input
                  type="password"
                  placeholder="Confirm Password"
                  value={formData.confirm_password}
                  onChange={(e) => setFormData({ ...formData, confirm_password: e.target.value })}
                  required
                  minLength={6}
                  className="bg-background/50"
                />
              </div>

              {error && (
                <div className="text-destructive text-sm text-center bg-destructive/10 p-2 rounded-md">
                  {error}
                </div>
              )}

              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? "Creating account..." : "Complete Signup"}
              </Button>
            </form>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

