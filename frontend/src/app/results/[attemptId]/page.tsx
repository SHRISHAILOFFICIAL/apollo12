"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import { MathText } from "@/components/MathText";
import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

interface Question {
    question_id: number;
    question_number: number;
    section_name: string;
    question_text: string;
    option_a: string;
    option_b: string;
    option_c: string;
    option_d: string;
    user_answer: string | null;
    correct_answer: string;
    is_correct: boolean;
    marks: number;
}

interface SectionPerformance {
    section_name: string;
    score: number;
    total_marks: number;
    accuracy: number;
    answered: number;
    total_questions: number;
}

interface ResultsData {
    attempt_id: number;
    exam_name: string;
    user: string;
    started_at: string;
    finished_at: string;
    time_spent: string;
    status: string;
    total_score: number;
    total_marks: number;
    percentage: number;
    correct_answers: number;
    total_questions: number;
    section_performance: SectionPerformance[];
    questions: Question[];
    insights: {
        strengths: string[];
        improvements: string[];
        overall_performance: string;
    };
}

export default function ResultsPage() {
    const router = useRouter();
    const params = useParams();
    const [results, setResults] = useState<ResultsData | null>(null);
    const [loading, setLoading] = useState(true);
    const [activeSection, setActiveSection] = useState<string>("");

    useEffect(() => {
        const fetchResults = async () => {
            try {
                const token = localStorage.getItem("access_token");
                if (!token) {
                    router.push("/auth/login");
                    return;
                }

                const response = await axios.get(
                    `${API_BASE_URL}/results/${params.attemptId}/`,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );

                setResults(response.data);
                if (response.data.section_performance.length > 0) {
                    setActiveSection(response.data.section_performance[0].section_name);
                }
                setLoading(false);
            } catch (error: any) {
                console.error("Failed to fetch results", error);
                alert(error.response?.data?.error || "Failed to load results");
                router.push("/dashboard");
            }
        };

        fetchResults();
    }, [params.attemptId, router]);

    if (loading || !results) {
        return (
            <div className="flex min-h-screen items-center justify-center bg-gray-50">
                <div className="text-center">
                    <div className="h-12 w-12 animate-spin rounded-full border-4 border-blue-600 border-t-transparent mx-auto mb-4"></div>
                    <p className="text-gray-500 font-medium">Loading Results...</p>
                </div>
            </div>
        );
    }

    const sectionQuestions = activeSection
        ? results.questions.filter((q) => q.section_name === activeSection)
        : results.questions;

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-7xl mx-auto px-4">
                {/* Header */}
                <div className="mb-6">
                    <button
                        onClick={() => router.push("/dashboard")}
                        className="text-blue-600 hover:text-blue-700 font-medium mb-4 flex items-center gap-2"
                    >
                        ← Back to Dashboard
                    </button>
                    <h1 className="text-3xl font-bold text-gray-900">{results.exam_name}</h1>
                    <p className="text-gray-600 mt-1">Exam Results</p>
                </div>

                {/* Score Summary Card */}
                <div className="bg-white rounded-2xl shadow-lg p-8 mb-6">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                        <div className="text-center">
                            <div className="text-5xl font-bold text-blue-600 mb-2">
                                {results.percentage}%
                            </div>
                            <div className="text-sm text-gray-600">Overall Score</div>
                        </div>
                        <div className="text-center">
                            <div className="text-3xl font-bold text-gray-900 mb-2">
                                {results.total_score}/{results.total_marks}
                            </div>
                            <div className="text-sm text-gray-600">Marks Obtained</div>
                        </div>
                        <div className="text-center">
                            <div className="text-3xl font-bold text-green-600 mb-2">
                                {results.correct_answers}/{results.total_questions}
                            </div>
                            <div className="text-sm text-gray-600">Correct Answers</div>
                        </div>
                        <div className="text-center">
                            <div className="text-3xl font-bold text-gray-900 mb-2">
                                {results.time_spent}
                            </div>
                            <div className="text-sm text-gray-600">Time Taken</div>
                        </div>
                    </div>

                    {/* Performance Badge */}
                    <div className="mt-6 text-center">
                        <span
                            className={`inline-block px-6 py-2 rounded-full text-lg font-semibold ${results.percentage >= 80
                                    ? "bg-green-100 text-green-800"
                                    : results.percentage >= 60
                                        ? "bg-blue-100 text-blue-800"
                                        : "bg-yellow-100 text-yellow-800"
                                }`}
                        >
                            {results.insights.overall_performance}
                        </span>
                    </div>
                </div>

                {/* Section-wise Performance */}
                <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
                    <h2 className="text-2xl font-bold text-gray-900 mb-4">
                        Section-wise Performance
                    </h2>
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b-2 border-gray-200">
                                    <th className="text-left py-3 px-4 font-semibold text-gray-700">
                                        Section
                                    </th>
                                    <th className="text-center py-3 px-4 font-semibold text-gray-700">
                                        Score
                                    </th>
                                    <th className="text-center py-3 px-4 font-semibold text-gray-700">
                                        Accuracy
                                    </th>
                                    <th className="text-center py-3 px-4 font-semibold text-gray-700">
                                        Answered
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                {results.section_performance.map((section) => (
                                    <tr key={section.section_name} className="border-b border-gray-100">
                                        <td className="py-4 px-4 font-medium text-gray-900">
                                            {section.section_name}
                                        </td>
                                        <td className="text-center py-4 px-4">
                                            <span className="font-bold text-gray-900">
                                                {section.score}/{section.total_marks}
                                            </span>
                                        </td>
                                        <td className="text-center py-4 px-4">
                                            <div className="flex items-center justify-center gap-2">
                                                <div className="w-24 bg-gray-200 rounded-full h-2">
                                                    <div
                                                        className={`h-2 rounded-full ${section.accuracy >= 80
                                                                ? "bg-green-500"
                                                                : section.accuracy >= 60
                                                                    ? "bg-blue-500"
                                                                    : "bg-yellow-500"
                                                            }`}
                                                        style={{ width: `${section.accuracy}%` }}
                                                    ></div>
                                                </div>
                                                <span className="font-semibold text-gray-700">
                                                    {section.accuracy}%
                                                </span>
                                            </div>
                                        </td>
                                        <td className="text-center py-4 px-4 text-gray-700">
                                            {section.answered}/{section.total_questions}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* Insights */}
                {(results.insights.strengths.length > 0 ||
                    results.insights.improvements.length > 0) && (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                            {results.insights.strengths.length > 0 && (
                                <div className="bg-green-50 border-2 border-green-200 rounded-xl p-6">
                                    <h3 className="text-lg font-bold text-green-800 mb-3 flex items-center gap-2">
                                        <span>💪</span> Strengths
                                    </h3>
                                    <ul className="space-y-2">
                                        {results.insights.strengths.map((strength) => (
                                            <li key={strength} className="text-green-700 flex items-center gap-2">
                                                <span className="text-green-500">✓</span>
                                                {strength}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                            {results.insights.improvements.length > 0 && (
                                <div className="bg-yellow-50 border-2 border-yellow-200 rounded-xl p-6">
                                    <h3 className="text-lg font-bold text-yellow-800 mb-3 flex items-center gap-2">
                                        <span>📈</span> Areas to Improve
                                    </h3>
                                    <ul className="space-y-2">
                                        {results.insights.improvements.map((improvement) => (
                                            <li key={improvement} className="text-yellow-700 flex items-center gap-2">
                                                <span className="text-yellow-500">!</span>
                                                {improvement}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    )}

                {/* Question Review */}
                <div className="bg-white rounded-2xl shadow-lg p-6">
                    <h2 className="text-2xl font-bold text-gray-900 mb-4">
                        Question-by-Question Review
                    </h2>

                    {/* Section Filter */}
                    <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
                        <button
                            onClick={() => setActiveSection("")}
                            className={`px-4 py-2 rounded-lg font-medium whitespace-nowrap transition-colors ${activeSection === ""
                                    ? "bg-blue-600 text-white"
                                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                                }`}
                        >
                            All Questions
                        </button>
                        {results.section_performance.map((section) => (
                            <button
                                key={section.section_name}
                                onClick={() => setActiveSection(section.section_name)}
                                className={`px-4 py-2 rounded-lg font-medium whitespace-nowrap transition-colors ${activeSection === section.section_name
                                        ? "bg-blue-600 text-white"
                                        : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                                    }`}
                            >
                                {section.section_name}
                            </button>
                        ))}
                    </div>

                    {/* Questions List */}
                    <div className="space-y-4">
                        {sectionQuestions.map((question, idx) => (
                            <div
                                key={question.question_id}
                                className={`border-2 rounded-xl p-6 ${question.is_correct
                                        ? "border-green-200 bg-green-50"
                                        : question.user_answer
                                            ? "border-red-200 bg-red-50"
                                            : "border-gray-200 bg-gray-50"
                                    }`}
                            >
                                {/* Question Header */}
                                <div className="flex justify-between items-start mb-4">
                                    <div className="flex items-center gap-3">
                                        <span className="text-sm font-bold text-gray-600">
                                            Q{question.question_number}
                                        </span>
                                        <span className="text-xs px-2 py-1 rounded bg-gray-200 text-gray-700">
                                            {question.section_name}
                                        </span>
                                        {question.is_correct ? (
                                            <span className="text-xs px-2 py-1 rounded bg-green-200 text-green-800 font-semibold">
                                                ✓ Correct
                                            </span>
                                        ) : question.user_answer ? (
                                            <span className="text-xs px-2 py-1 rounded bg-red-200 text-red-800 font-semibold">
                                                ✗ Incorrect
                                            </span>
                                        ) : (
                                            <span className="text-xs px-2 py-1 rounded bg-gray-200 text-gray-800 font-semibold">
                                                Not Answered
                                            </span>
                                        )}
                                    </div>
                                    <span className="text-sm font-semibold text-gray-600">
                                        {question.marks} {question.marks === 1 ? "Mark" : "Marks"}
                                    </span>
                                </div>

                                {/* Question Text */}
                                <div className="mb-4">
                                    <p className="text-lg text-gray-800 font-medium">
                                        <MathText text={question.question_text} />
                                    </p>
                                </div>

                                {/* Options */}
                                <div className="space-y-2">
                                    {["A", "B", "C", "D"].map((option) => {
                                        const optionText = question[`option_${option.toLowerCase()}` as keyof Question] as string;
                                        const isUserAnswer = question.user_answer === option;
                                        const isCorrectAnswer = question.correct_answer === option;

                                        return (
                                            <div
                                                key={option}
                                                className={`p-3 rounded-lg border-2 ${isCorrectAnswer
                                                        ? "border-green-500 bg-green-100"
                                                        : isUserAnswer
                                                            ? "border-red-500 bg-red-100"
                                                            : "border-gray-200 bg-white"
                                                    }`}
                                            >
                                                <div className="flex items-center gap-3">
                                                    <span className="font-bold text-gray-700">{option}.</span>
                                                    <span className="text-gray-800">
                                                        <MathText text={optionText} />
                                                    </span>
                                                    {isCorrectAnswer && (
                                                        <span className="ml-auto text-green-600 font-semibold text-sm">
                                                            ✓ Correct Answer
                                                        </span>
                                                    )}
                                                    {isUserAnswer && !isCorrectAnswer && (
                                                        <span className="ml-auto text-red-600 font-semibold text-sm">
                                                            Your Answer
                                                        </span>
                                                    )}
                                                </div>
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Actions */}
                <div className="mt-6 flex gap-4 justify-center">
                    <button
                        onClick={() => router.push("/dashboard")}
                        className="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl shadow-md transition-colors"
                    >
                        Back to Dashboard
                    </button>
                </div>
            </div>
        </div>
    );
}
