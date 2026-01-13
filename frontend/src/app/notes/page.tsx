"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import { BookOpen, Lock, FileText, ChevronLeft } from "lucide-react";
import { Button } from "@/components/ui/button";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

interface Note {
    id: number;
    topic: string;
    description: string;
    access_tier: string;
    can_access: boolean;
    is_locked: boolean;
}

interface NotesData {
    subjects: {
        [key: string]: Note[];
    };
}

export default function NotesPage() {
    const router = useRouter();
    const [notesData, setNotesData] = useState<NotesData | null>(null);
    const [selectedSubject, setSelectedSubject] = useState<string | null>(null);
    const [selectedNote, setSelectedNote] = useState<Note | null>(null);
    const [pdfUrl, setPdfUrl] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);
    const [loadingPdf, setLoadingPdf] = useState(false);

    useEffect(() => {
        fetchNotes();
    }, []);

    // Cleanup blob URL when component unmounts or PDF changes
    useEffect(() => {
        return () => {
            if (pdfUrl && pdfUrl.startsWith('blob:')) {
                URL.revokeObjectURL(pdfUrl);
            }
        };
    }, [pdfUrl]);

    const fetchNotes = async () => {
        try {
            const token = localStorage.getItem("access_token");
            if (!token) {
                router.push("/auth/login");
                return;
            }

            const response = await axios.get(`${API_BASE_URL}/notes/`, {
                headers: { Authorization: `Bearer ${token}` },
            });

            setNotesData(response.data);

            // Auto-select first subject
            const subjects = Object.keys(response.data.subjects);
            if (subjects.length > 0) {
                setSelectedSubject(subjects[0]);
            }

            setLoading(false);
        } catch (error: any) {
            console.error("Failed to fetch notes", error);
            if (error.response?.status === 401) {
                router.push("/auth/login");
            }
        }
    };

    const handleNoteClick = async (note: Note) => {
        if (!note.can_access) {
            router.push("/pricing");
            return;
        }

        setSelectedNote(note);
        setLoadingPdf(true);

        try {
            // Fetch PDF with authentication
            const token = localStorage.getItem("access_token");
            const response = await axios.get(`${API_BASE_URL}/notes/${note.id}/view/`, {
                headers: { Authorization: `Bearer ${token}` },
                responseType: 'blob', // Important: get binary data
            });

            // Create blob URL
            const blob = new Blob([response.data], { type: 'application/pdf' });
            const url = URL.createObjectURL(blob);
            setPdfUrl(url);
        } catch (error) {
            console.error("Failed to load PDF", error);
            alert("Failed to load PDF. Please try again.");
            setSelectedNote(null);
        } finally {
            setLoadingPdf(false);
        }
    };

    const handleBackToList = () => {
        // Cleanup blob URL
        if (pdfUrl && pdfUrl.startsWith('blob:')) {
            URL.revokeObjectURL(pdfUrl);
        }
        setSelectedNote(null);
        setPdfUrl(null);
    };

    if (loading || !notesData) {
        return (
            <div className="flex min-h-screen items-center justify-center bg-gray-50">
                <div className="text-center">
                    <div className="h-12 w-12 animate-spin rounded-full border-4 border-blue-600 border-t-transparent mx-auto mb-4"></div>
                    <p className="text-gray-600 font-medium">Loading Notes...</p>
                </div>
            </div>
        );
    }

    // If a note is selected, show PDF viewer
    if (selectedNote && pdfUrl) {
        const token = localStorage.getItem("access_token");

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
                            Back to Notes
                        </Button>
                        <div className="flex-1">
                            <h1 className="text-lg font-bold text-gray-900">{selectedNote.topic}</h1>
                            <p className="text-xs text-gray-500">{selectedNote.description}</p>
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
                </main>            </div>
        );
    }

    // Show notes list
    const subjects = Object.keys(notesData.subjects);

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
                        <BookOpen className="w-6 h-6 text-blue-600" />
                        Study Notes
                    </h1>
                    <p className="text-sm text-gray-600 mt-1">
                        Access comprehensive notes for all subjects
                    </p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-4 gap-5">
                    {/* Subject Sidebar */}
                    <div className="lg:col-span-1">
                        <div className="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
                            <h2 className="text-sm font-bold text-gray-900 mb-3">Subjects</h2>
                            <div className="space-y-1">
                                {subjects.map((subject) => (
                                    <button
                                        key={subject}
                                        onClick={() => setSelectedSubject(subject)}
                                        className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${selectedSubject === subject
                                            ? "bg-blue-50 text-blue-700 font-semibold"
                                            : "text-gray-700 hover:bg-gray-50"
                                            }`}
                                    >
                                        {subject}
                                    </button>
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* Notes List */}
                    <div className="lg:col-span-3">
                        {selectedSubject && (
                            <div className="space-y-3">
                                <h2 className="text-lg font-bold text-gray-900">{selectedSubject}</h2>
                                {notesData.subjects[selectedSubject].map((note) => (
                                    <div
                                        key={note.id}
                                        className={`bg-white rounded-lg border p-4 shadow-sm ${note.is_locked
                                            ? "border-gray-200 opacity-75"
                                            : "border-gray-200 hover:border-blue-300 hover:shadow-md transition-all cursor-pointer"
                                            }`}
                                        onClick={() => handleNoteClick(note)}
                                    >
                                        <div className="flex items-start justify-between gap-3">
                                            <div className="flex-1">
                                                <div className="flex items-center gap-2 mb-1">
                                                    <FileText className="w-4 h-4 text-blue-600" />
                                                    <h3 className="text-base font-bold text-gray-900">{note.topic}</h3>
                                                    {note.access_tier === 'PRO' && (
                                                        <span className="px-2 py-0.5 rounded text-xs font-bold bg-amber-100 text-amber-700">
                                                            PRO
                                                        </span>
                                                    )}
                                                </div>
                                                <p className="text-sm text-gray-600">{note.description}</p>
                                            </div>
                                            {note.is_locked ? (
                                                <Button variant="outline" size="sm" className="text-sm">
                                                    <Lock className="w-4 h-4 mr-2" /> Unlock
                                                </Button>
                                            ) : (
                                                <Button size="sm" className="bg-blue-600 hover:bg-blue-700 text-white text-sm">
                                                    View Notes
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
