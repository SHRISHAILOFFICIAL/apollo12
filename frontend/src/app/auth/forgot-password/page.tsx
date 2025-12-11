"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { authService } from "@/lib/services/auth.service";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { KeyRound, Mail, CheckCircle } from "lucide-react";

type ResetStep = "email" | "otp" | "password";

export default function ForgotPasswordPage() {
    const router = useRouter();
    const [step, setStep] = useState<ResetStep>("email");
    const [email, setEmail] = useState("");
    const [otp, setOtp] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSendOTP = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setLoading(true);

        try {
            await authService.sendPasswordResetOTP(email);
            setStep("otp");
        } catch (err: any) {
            setError("Failed to send OTP. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    const handleVerifyOTP = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        if (otp.length !== 6) {
            setError("Please enter a valid 6-digit OTP");
            return;
        }

        setStep("password");
    };

    const handleResetPassword = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        if (newPassword !== confirmPassword) {
            setError("Passwords do not match");
            return;
        }

        if (newPassword.length < 6) {
            setError("Password must be at least 6 characters long");
            return;
        }

        setLoading(true);

        try {
            await authService.resetPassword(email, otp, newPassword);
            router.push("/auth/login?reset=true");
        } catch (err: any) {
            const errorMessage = err.response?.data?.error || "Failed to reset password. Please try again.";
            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    const handleResendOTP = async () => {
        setError("");
        setLoading(true);
        try {
            await authService.sendPasswordResetOTP(email);
            alert("OTP sent successfully!");
        } catch (err: any) {
            setError("Failed to resend OTP");
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
                            {step === "password" && <KeyRound className="w-6 h-6 text-primary" />}
                        </div>
                    </div>
                    <CardTitle className="text-2xl font-bold">
                        {step === "email" && "Reset Password"}
                        {step === "otp" && "Verify OTP"}
                        {step === "password" && "New Password"}
                    </CardTitle>
                    <p className="text-sm text-muted-foreground">
                        {step === "email" && "Enter your email to receive a reset code"}
                        {step === "otp" && `We sent a code to ${email}`}
                        {step === "password" && "Enter your new password"}
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
                                {loading ? "Sending OTP..." : "Send Reset Code"}
                            </Button>

                            <div className="text-center text-sm text-muted-foreground">
                                Remember your password?{" "}
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

                            <Button type="submit" className="w-full" disabled={otp.length !== 6}>
                                Continue
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

                    {/* Step 3: New Password */}
                    {step === "password" && (
                        <form onSubmit={handleResetPassword} className="space-y-4">
                            <div className="space-y-2">
                                <Input
                                    type="password"
                                    placeholder="New Password (min 6 characters)"
                                    value={newPassword}
                                    onChange={(e) => setNewPassword(e.target.value)}
                                    required
                                    minLength={6}
                                    className="bg-background/50"
                                />
                            </div>
                            <div className="space-y-2">
                                <Input
                                    type="password"
                                    placeholder="Confirm New Password"
                                    value={confirmPassword}
                                    onChange={(e) => setConfirmPassword(e.target.value)}
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
                                {loading ? "Resetting Password..." : "Reset Password"}
                            </Button>
                        </form>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
