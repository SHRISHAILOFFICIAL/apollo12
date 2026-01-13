"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import { Bell, Calendar, Award, AlertCircle, Info } from "lucide-react";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

interface Announcement {
    id: number;
    title: string;
    message: string;
    type: string;
    created_at: string;
}

export default function AnnouncementsPage() {
    const router = useRouter();
    const [announcements, setAnnouncements] = useState<Announcement[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchAnnouncements();
    }, []);

    const fetchAnnouncements = async () => {
        try {
            const token = localStorage.getItem("access_token");
            if (!token) {
                router.push("/auth/login");
                return;
            }

            const response = await axios.get(`${API_BASE_URL}/announcements/`, {
                headers: { Authorization: `Bearer ${token}` },
            });

            setAnnouncements(response.data.announcements);
            setLoading(false);
        } catch (error: any) {
            console.error("Failed to fetch announcements", error);
            if (error.response?.status === 401) {
                router.push("/auth/login");
            }
        }
    };

    const getTypeConfig = (type: string) => {
        switch (type) {
            case 'EXAM_DATE':
                return {
                    icon: Calendar,
                    bg: 'bg-blue-50',
                    border: 'border-blue-200',
                    text: 'text-blue-700',
                    badge: 'bg-blue-100 text-blue-700',
                    label: 'Exam Date'
                };
            case 'RESULTS':
                return {
                    icon: Award,
                    bg: 'bg-green-50',
                    border: 'border-green-200',
                    text: 'text-green-700',
                    badge: 'bg-green-100 text-green-700',
                    label: 'Results'
                };
            case 'URGENT':
                return {
                    icon: AlertCircle,
                    bg: 'bg-red-50',
                    border: 'border-red-200',
                    text: 'text-red-700',
                    badge: 'bg-red-100 text-red-700',
                    label: 'Urgent'
                };
            default:
                return {
                    icon: Info,
                    bg: 'bg-gray-50',
                    border: 'border-gray-200',
                    text: 'text-gray-700',
                    badge: 'bg-gray-100 text-gray-700',
                    label: 'General'
                };
        }
    };

    if (loading) {
        return (
            <div className="flex min-h-screen items-center justify-center bg-gray-50">
                <div className="text-center">
                    <div className="h-12 w-12 animate-spin rounded-full border-4 border-blue-600 border-t-transparent mx-auto mb-4"></div>
                    <p className="text-gray-600 font-medium">Loading Announcements...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white border-b border-gray-200 sticky top-0 z-40 shadow-sm">
                <div className="container mx-auto px-4 sm:px-6 h-16 flex items-center max-w-7xl">
                    <button
                        onClick={() => router.push("/dashboard")}
                        className="text-gray-600 hover:text-gray-900 flex items-center gap-2"
                    >
                        ← Back to Dashboard
                    </button>
                </div>
            </header>

            <main className="container mx-auto px-4 sm:px-6 py-8 max-w-4xl">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
                        <Bell className="w-8 h-8 text-blue-600" />
                        Announcements & Updates
                    </h1>
                    <p className="text-gray-600 mt-2">
                        Stay updated with exam dates, results, and important notifications
                    </p>
                </div>

                {announcements.length === 0 ? (
                    <div className="bg-white rounded-lg border border-gray-200 p-12 text-center">
                        <Bell className="w-16 h-16 mx-auto mb-4 text-gray-300" />
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">No Announcements Yet</h3>
                        <p className="text-gray-600">Check back later for updates!</p>
                    </div>
                ) : (
                    <div className="space-y-4">
                        {announcements.map((announcement) => {
                            const config = getTypeConfig(announcement.type);
                            const Icon = config.icon;

                            return (
                                <div
                                    key={announcement.id}
                                    className={`bg-white rounded-lg border-2 ${config.border} p-6 shadow-sm hover:shadow-md transition-shadow`}
                                >
                                    <div className="flex items-start gap-4">
                                        <div className={`p-3 ${config.bg} rounded-lg flex-shrink-0`}>
                                            <Icon className={`w-6 h-6 ${config.text}`} />
                                        </div>
                                        <div className="flex-1">
                                            <div className="flex items-start justify-between gap-4 mb-2">
                                                <h3 className="text-lg font-bold text-gray-900">{announcement.title}</h3>
                                                <span className={`px-3 py-1 rounded-full text-xs font-bold ${config.badge} whitespace-nowrap`}>
                                                    {config.label}
                                                </span>
                                            </div>
                                            <p className="text-gray-700 mb-3">{announcement.message}</p>
                                            <p className="text-sm text-gray-500 flex items-center gap-2">
                                                <Calendar className="w-4 h-4" />
                                                {announcement.created_at}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                )}
            </main>
        </div>
    );
}
