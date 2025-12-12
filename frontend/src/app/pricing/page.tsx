"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

interface Plan {
    id: number;
    key: string;
    name: string;
    price_in_paisa: number;
    price_in_rupees: number;
    duration_days: number;
    features: string[];
    is_active: boolean;
}

export default function PricingPage() {
    const router = useRouter();
    const [plans, setPlans] = useState<Plan[]>([]);
    const [loading, setLoading] = useState(true);
    const [processing, setProcessing] = useState(false);

    useEffect(() => {
        fetchPlans();
        loadRazorpayScript();
    }, []);

    const fetchPlans = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/payments/plans/`);
            if (response.data.success) {
                setPlans(response.data.plans);
            }
            setLoading(false);
        } catch (error) {
            console.error("Failed to fetch plans", error);
            setLoading(false);
        }
    };

    const loadRazorpayScript = () => {
        return new Promise((resolve) => {
            const script = document.createElement("script");
            script.src = "https://checkout.razorpay.com/v1/checkout.js";
            script.onload = () => resolve(true);
            script.onerror = () => resolve(false);
            document.body.appendChild(script);
        });
    };

    const handleBuyNow = async (plan: Plan) => {
        const token = localStorage.getItem("access_token");
        if (!token) {
            router.push("/auth/login");
            return;
        }

        setProcessing(true);

        try {
            // Step 1: Create order
            const orderResponse = await axios.post(
                `${API_BASE_URL}/payments/create-order/`,
                { plan_id: plan.id },
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );

            if (!orderResponse.data.success) {
                alert("Failed to create order");
                setProcessing(false);
                return;
            }

            const { order, razorpay_key_id } = orderResponse.data;

            // Step 2: Open Razorpay checkout
            const options = {
                key: razorpay_key_id,
                amount: order.amount,
                currency: order.currency,
                name: "DCET Platform",
                description: `${plan.name} - ${plan.duration_days} days`,
                order_id: order.id,
                handler: async function (response: any) {
                    // Step 3: Verify payment
                    try {
                        const verifyResponse = await axios.post(
                            `${API_BASE_URL}/payments/verify-payment/`,
                            {
                                razorpay_order_id: response.razorpay_order_id,
                                razorpay_payment_id: response.razorpay_payment_id,
                                razorpay_signature: response.razorpay_signature,
                                plan_id: plan.id,
                            },
                            {
                                headers: { Authorization: `Bearer ${token}` },
                            }
                        );

                        if (verifyResponse.data.success) {
                            alert("🎉 Payment successful! You are now a PRO user!");
                            router.push("/dashboard");
                        } else {
                            alert("Payment verification failed");
                        }
                    } catch (error) {
                        console.error("Payment verification error", error);
                        alert("Payment verification failed");
                    } finally {
                        setProcessing(false);
                    }
                },
                prefill: {
                    name: "",
                    email: "",
                    contact: "",
                },
                theme: {
                    color: "#2563eb",
                },
                modal: {
                    ondismiss: function () {
                        setProcessing(false);
                    },
                },
            };

            const razorpay = new (window as any).Razorpay(options);
            razorpay.open();
        } catch (error) {
            console.error("Payment error", error);
            alert("Failed to initiate payment");
            setProcessing(false);
        }
    };

    if (loading) {
        return (
            <div className="flex min-h-screen items-center justify-center bg-gray-50">
                <div className="text-center">
                    <div className="h-12 w-12 animate-spin rounded-full border-4 border-blue-600 border-t-transparent mx-auto mb-4"></div>
                    <p className="text-gray-500 font-medium">Loading plans...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
            {/* Header */}
            <header className="bg-white shadow-sm">
                <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
                    <div className="flex items-center gap-3 cursor-pointer" onClick={() => router.push("/dashboard")}>
                        <img
                            src="/logo.jpg"
                            alt="DCET Platform Logo"
                            className="h-10 w-10 rounded-lg object-cover"
                        />
                        <h1 className="text-xl font-bold text-gray-900">DCET Platform</h1>
                    </div>
                    <button
                        onClick={() => router.push("/dashboard")}
                        className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
                    >
                        ← Back to Dashboard
                    </button>
                </div>
            </header>

            {/* Hero Section */}
            <div className="max-w-7xl mx-auto px-4 py-16 text-center">
                <h1 className="text-5xl font-bold text-gray-900 mb-4">
                    Upgrade to <span className="text-blue-600">PRO</span>
                </h1>
                <p className="text-xl text-gray-600 mb-2">
                    Get unlimited access to all exams, mock tests, and video solutions
                </p>
                <p className="text-lg text-gray-500">
                    One-time payment. No recurring charges. 1 year access.
                </p>
            </div>

            {/* Pricing Cards */}
            <div className="max-w-4xl mx-auto px-4 pb-20">
                <div className="grid grid-cols-1 md:grid-cols-1 gap-8">
                    {plans.map((plan) => (
                        <div
                            key={plan.id}
                            className="relative bg-white rounded-2xl shadow-2xl border-4 border-blue-500 overflow-hidden transform hover:scale-105 transition-transform duration-300"
                        >
                            {/* Recommended Badge */}
                            <div className="absolute top-0 right-0 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-2 rounded-bl-2xl font-bold text-sm">
                                ⭐ RECOMMENDED
                            </div>

                            <div className="p-8">
                                {/* Plan Header */}
                                <div className="text-center mb-8">
                                    <h3 className="text-3xl font-bold text-gray-900 mb-2">{plan.name}</h3>
                                    <div className="flex items-baseline justify-center gap-2">
                                        <span className="text-5xl font-bold text-blue-600">₹{plan.price_in_rupees}</span>
                                        <span className="text-gray-500 text-lg">/ {plan.duration_days} days</span>
                                    </div>
                                    <p className="text-sm text-gray-500 mt-2">One-time payment • No hidden charges</p>
                                </div>

                                {/* Features */}
                                <div className="space-y-4 mb-8">
                                    {plan.features.map((feature, index) => (
                                        <div key={index} className="flex items-start gap-3">
                                            <svg
                                                className="w-6 h-6 text-green-500 flex-shrink-0 mt-0.5"
                                                fill="none"
                                                stroke="currentColor"
                                                viewBox="0 0 24 24"
                                            >
                                                <path
                                                    strokeLinecap="round"
                                                    strokeLinejoin="round"
                                                    strokeWidth={2}
                                                    d="M5 13l4 4L19 7"
                                                />
                                            </svg>
                                            <span className="text-gray-700 text-lg">{feature}</span>
                                        </div>
                                    ))}
                                </div>

                                {/* CTA Button */}
                                <button
                                    onClick={() => handleBuyNow(plan)}
                                    disabled={processing}
                                    className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold py-4 px-8 rounded-xl shadow-lg transform hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed text-lg"
                                >
                                    {processing ? "Processing..." : "🚀 Buy Now"}
                                </button>

                                <p className="text-center text-sm text-gray-500 mt-4">
                                    Secure payment powered by Razorpay
                                </p>
                            </div>
                        </div>
                    ))}
                </div>

                {/* Trust Indicators */}
                <div className="mt-16 text-center">
                    <p className="text-gray-600 mb-4">Trusted by thousands of DCET aspirants</p>
                    <div className="flex justify-center gap-8 text-sm text-gray-500">
                        <div className="flex items-center gap-2">
                            <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                                <path
                                    fillRule="evenodd"
                                    d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                    clipRule="evenodd"
                                />
                            </svg>
                            <span>Secure Payment</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <svg className="w-5 h-5 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                                <path
                                    fillRule="evenodd"
                                    d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z"
                                    clipRule="evenodd"
                                />
                            </svg>
                            <span>Instant Activation</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <svg className="w-5 h-5 text-purple-500" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
                            </svg>
                            <span>Money-back Guarantee</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
