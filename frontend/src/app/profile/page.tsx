"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import { User, Mail, Calendar, Crown, Award, TrendingUp, LogOut, Phone } from "lucide-react";
import { Button } from "@/components/ui/button";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

interface UserProfile {
    username: string;
    email: string;
    mobile: string;
    is_pro: boolean;
    total_attempts: number;
    average_score: number;
    best_score: number;
    member_since: string;
}

export default function ProfilePage() {
    const router = useRouter();
    const [profile, setProfile] = useState<UserProfile | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchProfile();
    }, []);

    const fetchProfile = async () => {
        try {
            const token = localStorage.getItem("access_token");
            if (!token) {
                router.push("/auth/login");
                return;
            }

            const response = await axios.get(`${API_BASE_URL}/dashboard/`, {
                headers: { Authorization: `Bearer ${token}` },
            });

            const data = response.data;

            // Debug: Log full response to see structure
            console.log('Full API response:', data);

            setProfile({
                username: data.user.username,
                email: data.user.email,
                mobile: data.user.mobile || 'Not provided',
                is_pro: data.user.is_pro,
                total_attempts: data.stats?.total_attempts ?? 0,
                average_score: data.stats?.average_score ?? 0,
                best_score: data.stats?.best_score ?? 0,
                member_since: new Date(data.user.date_joined).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                })
            });

            console.log('Profile data:', {
                total_attempts: data.total_attempts,
                average_score: data.average_score,
                best_score: data.best_score
            });

            setLoading(false);
        } catch (error: any) {
            console.error("Failed to fetch profile", error);
            if (error.response?.status === 401) {
                router.push("/auth/login");
            }
        }
    };

    const handleLogout = () => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        router.push("/auth/login");
    };

    if (loading || !profile) {
        return (
            <div className="flex min-h-screen items-center justify-center bg-gray-50">
                <div className="text-center">
                    <div className="h-12 w-12 animate-spin rounded-full border-4 border-blue-600 border-t-transparent mx-auto mb-4"></div>
                    <p className="text-gray-600 font-medium">Loading Profile...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white border-b border-gray-200 sticky top-0 z-40 shadow-sm">
                <div className="container mx-auto px-4 sm:px-6 h-16 flex items-center justify-between max-w-7xl">
                    <button
                        onClick={() => router.push("/dashboard")}
                        className="text-gray-600 hover:text-gray-900 flex items-center gap-2"
                    >
                        ← Back to Dashboard
                    </button>
                    <Button
                        onClick={handleLogout}
                        variant="outline"
                        size="sm"
                        className="gap-2"
                    >
                        <LogOut className="w-4 h-4" />
                        Logout
                    </Button>
                </div>
            </header>

            <main className="container mx-auto px-4 sm:px-6 py-8 max-w-4xl">
                {/* Profile Header */}
                <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm mb-6">
                    <div className="flex items-start justify-between mb-6">
                        <div className="flex items-center gap-4">
                            <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center">
                                <User className="w-10 h-10 text-blue-600" />
                            </div>
                            <div>
                                <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                                    {profile.username}
                                    {profile.is_pro && (
                                        <span className="px-3 py-1 rounded-full text-sm font-bold bg-amber-100 text-amber-700 flex items-center gap-1">
                                            <Crown className="w-4 h-4" />
                                            PRO
                                        </span>
                                    )}
                                </h1>
                                <p className="text-gray-600 flex items-center gap-2 mt-1">
                                    <Mail className="w-4 h-4" />
                                    {profile.email}
                                </p>
                                <p className="text-gray-600 flex items-center gap-2 mt-1">
                                    <Phone className="w-4 h-4" />
                                    {profile.mobile}
                                </p>
                            </div>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg">
                            <Calendar className="w-5 h-5 text-gray-600" />
                            <div>
                                <p className="text-xs text-gray-600">Member Since</p>
                                <p className="font-semibold text-gray-900">{profile.member_since}</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg">
                            <Crown className="w-5 h-5 text-gray-600" />
                            <div>
                                <p className="text-xs text-gray-600">Membership</p>
                                <p className="font-semibold text-gray-900">
                                    {profile.is_pro ? "PRO Member" : "FREE Member"}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Statistics */}
                <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm mb-6">
                    <h2 className="text-lg font-bold text-gray-900 mb-4">Your Statistics</h2>
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                        <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                            <div className="flex items-center justify-between mb-2">
                                <Award className="w-6 h-6 text-blue-600" />
                                <span className="text-2xl font-bold text-blue-700">{profile.total_attempts}</span>
                            </div>
                            <p className="text-xs text-gray-600">Total Attempts</p>
                        </div>
                        <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                            <div className="flex items-center justify-between mb-2">
                                <TrendingUp className="w-6 h-6 text-green-600" />
                                <span className="text-2xl font-bold text-green-700">{profile.average_score.toFixed(1)}%</span>
                            </div>
                            <p className="text-xs text-gray-600">Average Score</p>
                        </div>
                        <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
                            <div className="flex items-center justify-between mb-2">
                                <Award className="w-6 h-6 text-purple-600" />
                                <span className="text-2xl font-bold text-purple-700">{profile.best_score}%</span>
                            </div>
                            <p className="text-xs text-gray-600">Best Score</p>
                        </div>
                    </div>
                </div>

                {/* Upgrade Section for FREE users */}
                {!profile.is_pro && (
                    <div className="bg-gradient-to-br from-amber-50 to-orange-50 rounded-lg border-2 border-amber-200 p-6 shadow-sm">
                        <div className="flex items-start gap-4">
                            <div className="p-3 bg-amber-100 rounded-lg">
                                <Crown className="w-6 h-6 text-amber-600" />
                            </div>
                            <div className="flex-1">
                                <h3 className="text-lg font-bold text-gray-900 mb-2">Upgrade to PRO</h3>
                                <p className="text-sm text-gray-600 mb-4">
                                    Get access to premium exams, video solutions, and exclusive content!
                                </p>
                                <Button
                                    onClick={() => router.push("/pricing")}
                                    className="bg-amber-600 hover:bg-amber-700 text-white"
                                >
                                    <Crown className="w-4 h-4 mr-2" />
                                    View Plans
                                </Button>
                            </div>
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}
