"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import { Play, Lock, Crown } from "lucide-react";
import { Button } from "@/components/ui/button";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

interface Video {
    id: number;
    title: string;
    description: string;
    youtube_url: string;
    duration_minutes: number;
}

interface VideosData {
    is_pro: boolean;
    topics: {
        [key: string]: Video[];
    };
}

export default function VideosPage() {
    const router = useRouter();
    const [videosData, setVideosData] = useState<VideosData | null>(null);
    const [selectedTopic, setSelectedTopic] = useState<string | null>(null);
    const [selectedVideo, setSelectedVideo] = useState<Video | null>(null);
    const [loading, setLoading] = useState(true);
    const [isPro, setIsPro] = useState(false);

    useEffect(() => {
        fetchVideos();
    }, []);

    const fetchVideos = async () => {
        try {
            const token = localStorage.getItem("access_token");
            if (!token) {
                router.push("/auth/login");
                return;
            }

            const response = await axios.get(`${API_BASE_URL}/videos/`, {
                headers: { Authorization: `Bearer ${token}` },
            });

            setVideosData(response.data);
            setIsPro(response.data.is_pro);

            // Auto-select first topic
            const topics = Object.keys(response.data.topics);
            if (topics.length > 0) {
                setSelectedTopic(topics[0]);
            }

            setLoading(false);
        } catch (error: any) {
            console.error("Failed to fetch videos", error);
            if (error.response?.status === 401) {
                router.push("/auth/login");
            } else if (error.response?.status === 403) {
                // Not PRO user
                setIsPro(false);
                setLoading(false);
            }
        }
    };

    const getYouTubeEmbedUrl = (url: string) => {
        const videoId = url.split('v=')[1]?.split('&')[0] || url.split('/').pop();
        return `https://www.youtube.com/embed/${videoId}`;
    };

    if (loading) {
        return (
            <div className="flex min-h-screen items-center justify-center bg-gray-50">
                <div className="text-center">
                    <div className="h-12 w-12 animate-spin rounded-full border-4 border-purple-600 border-t-transparent mx-auto mb-4"></div>
                    <p className="text-gray-600 font-medium">Loading Videos...</p>
                </div>
            </div>
        );
    }

    // Show upgrade prompt for FREE users
    if (!isPro) {
        return (
            <div className="min-h-screen bg-gray-50">
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

                <main className="container mx-auto px-4 sm:px-6 py-12 max-w-4xl">
                    <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl border-2 border-purple-200 p-12 text-center">
                        <div className="w-20 h-20 mx-auto mb-6 bg-purple-100 rounded-full flex items-center justify-center">
                            <Crown className="w-10 h-10 text-purple-600" />
                        </div>
                        <h1 className="text-3xl font-bold text-gray-900 mb-4">
                            Video Solutions - PRO Only
                        </h1>
                        <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
                            Get access to comprehensive video solutions for all topics. Watch expert explanations and solve problems step-by-step.
                        </p>
                        <div className="flex flex-col sm:flex-row gap-4 justify-center">
                            <Button
                                onClick={() => router.push("/pricing")}
                                className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-6 text-lg"
                                size="lg"
                            >
                                <Crown className="w-5 h-5 mr-2" />
                                Upgrade to PRO
                            </Button>
                            <Button
                                onClick={() => router.push("/dashboard")}
                                variant="outline"
                                size="lg"
                                className="px-8 py-6 text-lg"
                            >
                                Back to Dashboard
                            </Button>
                        </div>
                    </div>
                </main>
            </div>
        );
    }

    // Show videos for PRO users
    const topics = videosData ? Object.keys(videosData.topics) : [];

    return (
        <div className="min-h-screen bg-gray-50">
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

            <main className="container mx-auto px-4 sm:px-6 py-6 max-w-7xl">
                <div className="mb-6">
                    <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                        <Play className="w-6 h-6 text-purple-600" />
                        Video Solutions
                        <span className="px-3 py-1 rounded-full text-sm font-bold bg-purple-100 text-purple-700">
                            PRO
                        </span>
                    </h1>
                    <p className="text-sm text-gray-600 mt-1">
                        Watch comprehensive video solutions for all topics
                    </p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-4 gap-5">
                    {/* Topic Sidebar */}
                    <div className="lg:col-span-1">
                        <div className="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
                            <h2 className="text-sm font-bold text-gray-900 mb-3">Topics</h2>
                            <div className="space-y-1">
                                {topics.map((topic) => (
                                    <button
                                        key={topic}
                                        onClick={() => setSelectedTopic(topic)}
                                        className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${selectedTopic === topic
                                                ? "bg-purple-50 text-purple-700 font-semibold"
                                                : "text-gray-700 hover:bg-gray-50"
                                            }`}
                                    >
                                        {topic}
                                    </button>
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* Videos List */}
                    <div className="lg:col-span-3">
                        {selectedTopic && videosData && (
                            <div className="space-y-4">
                                <h2 className="text-lg font-bold text-gray-900">{selectedTopic}</h2>
                                {videosData.topics[selectedTopic].map((video) => (
                                    <div
                                        key={video.id}
                                        className="bg-white rounded-lg border border-gray-200 p-4 shadow-sm hover:border-purple-300 hover:shadow-md transition-all"
                                    >
                                        <div className="flex items-start gap-4">
                                            <div className="flex-shrink-0">
                                                <div className="w-40 h-24 bg-purple-100 rounded-lg flex items-center justify-center">
                                                    <Play className="w-12 h-12 text-purple-600" />
                                                </div>
                                            </div>
                                            <div className="flex-1">
                                                <h3 className="text-base font-bold text-gray-900 mb-1">{video.title}</h3>
                                                <p className="text-sm text-gray-600 mb-2">{video.description}</p>
                                                <div className="flex items-center gap-4">
                                                    <span className="text-xs text-gray-500">
                                                        {video.duration_minutes} minutes
                                                    </span>
                                                    <Button
                                                        onClick={() => setSelectedVideo(video)}
                                                        size="sm"
                                                        className="bg-purple-600 hover:bg-purple-700 text-white"
                                                    >
                                                        <Play className="w-4 h-4 mr-2" />
                                                        Watch Now
                                                    </Button>
                                                </div>
                                            </div>
                                        </div>

                                        {/* Video Player */}
                                        {selectedVideo?.id === video.id && (
                                            <div className="mt-4 pt-4 border-t border-gray-200">
                                                <div className="aspect-video rounded-lg overflow-hidden">
                                                    <iframe
                                                        src={getYouTubeEmbedUrl(video.youtube_url)}
                                                        className="w-full h-full"
                                                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                                        allowFullScreen
                                                        title={video.title}
                                                    />
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
}
