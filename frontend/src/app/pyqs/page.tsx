"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import { FileText, Lock, ChevronLeft, Calendar } from "lucide-react";
import { Button } from "@/components/ui/button";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

interface PYQ {
    id: number;
    exam_name: string;
    description: string;
    access_tier: string;
    can_access: boolean;
    is_locked: boolean;
}

interface PYQsData {
    years: {
        [key: string]: PYQ[];
    };
}

export default function PYQsPage() {
    const router = useRouter();
    const [pyqsData, setPyqsData] = useState<PYQsData | null>(null);
    const [selectedYear, setSelectedYear] = useState<string | null>(null);
    const [selectedPYQ, setSelectedPYQ] = useState<PYQ | null>(null);
    const [pdfUrl, setPdfUrl] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);
    const [loadingPdf, setLoadingPdf] = useState(false);

    useEffect(() => {
        fetchPYQs();
    }, []);

    // Cleanup blob URL when component unmounts or PDF changes
    useEffect(() => {
        return () => {
            if (pdfUrl && pdfUrl.startsWith('blob:')) {
                URL.revokeObjectURL(pdfUrl);
            }
        };
    }, [pdfUrl]);

    const fetchPYQs = async () => {
        try {
            const token = localStorage.getItem("access_token");
            if (!token) {
                router.push("/auth/login");
                return;
            }

            const response = await axios.get(`${API_BASE_URL}/pyqs/`, {
                headers: { Authorization: `Bearer ${token}` },
            });

            setPyqsData(response.data);

            // Auto-select most recent year
            const years = Object.keys(response.data.years).sort((a, b) => parseInt(b) - parseInt(a));
            if (years.length > 0) {
                setSelectedYear(years[0]);
            }

            setLoading(false);
        } catch (error: any) {
            console.error("Failed to fetch PYQs", error);
            if (error.response?.status === 401) {
                router.push("/auth/login");
            }
        }
    };

    const handlePYQClick = async (pyq: PYQ) => {
        if (!pyq.can_access) {
            router.push("/pricing");
            return;
        }

        setSelectedPYQ(pyq);
        setLoadingPdf(true);

        try {
            // Fetch PDF with authentication
            const token = localStorage.getItem("access_token");
            const response = await axios.get(`${API_BASE_URL}/pyqs/${pyq.id}/view/`, {
                headers: { Authorization: `Bearer ${token}` },
                responseType: 'blob',
            });

            // Create blob URL
            const blob = new Blob([response.data], { type: 'application/pdf' });
            const url = URL.createObjectURL(blob);
            setPdfUrl(url);
        } catch (error) {
            console.error("Failed to load PDF", error);
            alert("Failed to load PDF. Please try again.");
            setSelectedPYQ(null);
        } finally {
            setLoadingPdf(false);
        }
    };

    const handleBackToList = () => {
        // Cleanup blob URL
        if (pdfUrl && pdfUrl.startsWith('blob:')) {
            URL.revokeObjectURL(pdfUrl);
        }
        setSelectedPYQ(null);
        setPdfUrl(null);
    };

    if (loading || !pyqsData) {
        return (
            <div className="flex min-h-screen items-center justify-center bg-gray-50">
                <div className="text-center">
                    <div className="h-12 w-12 animate-spin rounded-full border-4 border-blue-600 border-t-transparent mx-auto mb-4"></div>
                    <p className="text-gray-600 font-medium">Loading PYQs...</p>
                </div>
            </div>
        );
    }

    // If a PYQ is selected, show PDF viewer
    if (selectedPYQ && pdfUrl) {
        return (
            <div className="min-h-screen bg-gray-50">
                {/* Header */}
                <header className="bg-white border-b border-gray-200 sticky top-0 z-40 shadow-sm">
                    <div className="container mx-auto px-4 sm:px-6 h-16 flex items-center gap-4 max-w-7xl">
                        <Button
                            variant="ghost"
                            onClick={handleBackToList}
                            className="gap-2"
                            size="sm"
                        >
                            <ChevronLeft className="w-4 h-4" />
                            Back to PYQs
                        </Button>
                        <div className="flex-1">
                            <h1 className="text-lg font-bold text-gray-900">{selectedPYQ.exam_name}</h1>
                            <p className="text-xs text-gray-500">{selectedPYQ.description}</p>
                        </div>
                    </div>
                </header>

                {/* PDF Viewer */}
                <main className="container mx-auto px-4 py-6 max-w-7xl">
                    {loadingPdf ? (
                        <div className="flex items-center justify-center" style={{ height: 'calc(100vh - 180px)' }}>
                            <div className="text-center">
                                <div className="h-12 w-12 animate-spin rounded-full border-4 border-blue-600 border-t-transparent mx-auto mb-4"></div>
                                <p className="text-gray-600 font-medium">Loading PDF...</p>
                            </div>
                        </div>
                    ) : (
                        <div className="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden" style={{ height: 'calc(100vh - 180px)' }}>
                            <object
                                data={`${pdfUrl}#toolbar=0`}
                                type="application/pdf"
                                className="w-full h-full"
                                style={{ border: 'none' }}
                            >
                                <div className="flex items-center justify-center h-full">
                                    <div className="text-center p-8">
                                        <FileText className="w-16 h-16 mx-auto mb-4 text-gray-400" />
                                        <p className="text-gray-600 mb-4">Unable to display PDF in browser</p>
                                        <Button
                                            onClick={() => window.open(pdfUrl, '_blank')}
                                            className="bg-blue-600 hover:bg-blue-700 text-white"
                                        >
                                            Open in New Tab
                                        </Button>
                                    </div>
                                </div>
                            </object>
                        </div>
                    )}
                </main>
            </div>
        );
    }

    // Show PYQs list
    const years = Object.keys(pyqsData.years).sort((a, b) => parseInt(b) - parseInt(a));

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

            <main className="container mx-auto px-4 sm:px-6 py-6 max-w-7xl">
                <div className="mb-6">
                    <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                        <FileText className="w-6 h-6 text-blue-600" />
                        Previous Year Questions
                    </h1>
                    <p className="text-sm text-gray-600 mt-1">
                        Access complete question papers from previous years
                    </p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-4 gap-5">
                    {/* Year Sidebar */}
                    <div className="lg:col-span-1">
                        <div className="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
                            <h2 className="text-sm font-bold text-gray-900 mb-3">Years</h2>
                            <div className="space-y-1">
                                {years.map((year) => (
                                    <button
                                        key={year}
                                        onClick={() => setSelectedYear(year)}
                                        className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors flex items-center gap-2 ${selectedYear === year
                                                ? "bg-blue-50 text-blue-700 font-semibold"
                                                : "text-gray-700 hover:bg-gray-50"
                                            }`}
                                    >
                                        <Calendar className="w-4 h-4" />
                                        {year}
                                    </button>
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* PYQs List */}
                    <div className="lg:col-span-3">
                        {selectedYear && (
                            <div className="space-y-3">
                                <h2 className="text-lg font-bold text-gray-900">{selectedYear} Papers</h2>
                                {pyqsData.years[selectedYear].map((pyq) => (
                                    <div
                                        key={pyq.id}
                                        className={`bg-white rounded-lg border p-4 shadow-sm ${pyq.is_locked
                                                ? "border-gray-200 opacity-75"
                                                : "border-gray-200 hover:border-blue-300 hover:shadow-md transition-all cursor-pointer"
                                            }`}
                                        onClick={() => handlePYQClick(pyq)}
                                    >
                                        <div className="flex items-start justify-between gap-3">
                                            <div className="flex-1">
                                                <div className="flex items-center gap-2 mb-1">
                                                    <FileText className="w-4 h-4 text-blue-600" />
                                                    <h3 className="text-base font-bold text-gray-900">{pyq.exam_name}</h3>
                                                    {pyq.access_tier === 'PRO' && (
                                                        <span className="px-2 py-0.5 rounded text-xs font-bold bg-amber-100 text-amber-700">
                                                            PRO
                                                        </span>
                                                    )}
                                                </div>
                                                <p className="text-sm text-gray-600">{pyq.description}</p>
                                            </div>
                                            {pyq.is_locked ? (
                                                <Button variant="outline" size="sm" className="text-sm">
                                                    <Lock className="w-4 h-4 mr-2" /> Unlock
                                                </Button>
                                            ) : (
                                                <Button size="sm" className="bg-blue-600 hover:bg-blue-700 text-white text-sm">
                                                    View Paper
                                                </Button>
                                            )}
                                        </div>
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
