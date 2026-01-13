"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import { motion } from "framer-motion";
import { Check, Shield, Zap, RefreshCw, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

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
  const [userData, setUserData] = useState<any>(null);

  useEffect(() => {
    fetchPlans();
    fetchUserProfile();
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

  const fetchUserProfile = async () => {
    try {
      const token = localStorage.getItem("access_token");
      if (!token) return;

      const response = await axios.get(`${API_BASE_URL}/users/auth/me/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUserData(response.data);
    } catch (error) {
      console.error("Failed to fetch user profile", error);
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
          name: userData?.username || "",
          email: userData?.email || "",
          contact: userData?.phone || "",
        },
        theme: {
          color: "#3b82f6",
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
      <div className="flex min-h-screen items-center justify-center bg-background">
        <div className="text-center">
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-primary border-t-transparent mx-auto mb-4"></div>
          <p className="text-muted-foreground font-medium">
            Loading available plans...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background text-foreground bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-100/50 via-background to-background">
      {/* Header */}
      <header className="glass fixed top-0 w-full z-50 border-b border-white/20">
        <div className="container mx-auto px-6 h-16 flex justify-between items-center">
          <div
            className="flex items-center gap-3 cursor-pointer"
            onClick={() => router.push("/dashboard")}
          >
            <img
              src="/logo_sample.png"
              alt="DCEThelper Logo"
              className="h-20 w-auto object-contain"
            />
          </div>
          <Button
            variant="ghost"
            onClick={() => router.push("/dashboard")}
            className="gap-2"
          >
            <ArrowLeft className="w-4 h-4" /> Back to Dashboard
          </Button>
        </div>
      </header>

      {/* Hero Section */}
      <div className="container mx-auto px-6 py-32 text-center max-w-4xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1 className="text-4xl md:text-6xl font-heading font-bold mb-6">
            Invest in Your <span className="text-primary">Future</span>
          </h1>
          <p className="text-xl text-muted-foreground mb-4 max-w-2xl mx-auto">
            Unlock unlimited possibilities with our PRO plan. Practice more,
            score better.
          </p>
          <p className="text-lg font-medium text-foreground/80">
            One-time payment • No recurring charges • 1 year access
          </p>
        </motion.div>
      </div>

      {/* Pricing Cards */}
      <div className="container mx-auto px-6 pb-20 max-w-6xl">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* FREE Plan */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0 }}
            className="relative bg-card rounded-3xl shadow-lg border border-border overflow-hidden hover:shadow-xl transition-all duration-300"
          >
            <div className="p-8">
              {/* Plan Info */}
              <div className="text-center mb-6">
                <h3 className="text-3xl font-bold font-heading mb-2">
                  FREE Plan
                </h3>
                <div className="flex items-baseline justify-center gap-2 mb-4">
                  <span className="text-5xl font-extrabold text-foreground">
                    ₹0
                  </span>
                  <span className="text-muted-foreground text-lg">forever</span>
                </div>
                <p className="text-sm text-muted-foreground">
                  Get started with basics
                </p>
              </div>

              {/* Features */}
              <div className="space-y-3 mb-8">
                <div className="flex items-start gap-3">
                  <div className="mt-1 bg-green-100 p-1 rounded-full">
                    <Check className="w-4 h-4 text-green-600" />
                  </div>
                  <span className="text-foreground/90">
                    1 Previous Year Question Paper
                  </span>
                </div>
                <div className="flex items-start gap-3">
                  <div className="mt-1 bg-green-100 p-1 rounded-full">
                    <Check className="w-4 h-4 text-green-600" />
                  </div>
                  <span className="text-foreground/90">
                    Basic performance tracking
                  </span>
                </div>
                <div className="flex items-start gap-3">
                  <div className="mt-1 bg-green-100 p-1 rounded-full">
                    <Check className="w-4 h-4 text-green-600" />
                  </div>
                  <span className="text-foreground/90">
                    Limited attempts per exam
                  </span>
                </div>
                <div className="flex items-start gap-3 opacity-40">
                  <div className="mt-1 bg-gray-100 p-1 rounded-full">
                    <span className="w-4 h-4 block text-gray-400">✕</span>
                  </div>
                  <span className="text-foreground/50 line-through">
                    Mock Tests
                  </span>
                </div>
                <div className="flex items-start gap-3 opacity-40">
                  <div className="mt-1 bg-gray-100 p-1 rounded-full">
                    <span className="w-4 h-4 block text-gray-400">✕</span>
                  </div>
                  <span className="text-foreground/50 line-through">
                    Video Solutions
                  </span>
                </div>
                <div className="flex items-start gap-3 opacity-40">
                  <div className="mt-1 bg-gray-100 p-1 rounded-full">
                    <span className="w-4 h-4 block text-gray-400">✕</span>
                  </div>
                  <span className="text-foreground/50 line-through">
                    Detailed Analytics
                  </span>
                </div>
              </div>

              <Button
                onClick={() => router.push("/dashboard")}
                variant="outline"
                size="lg"
                className="w-full h-14 text-lg font-semibold rounded-xl"
              >
                Current Plan
              </Button>
            </div>
          </motion.div>

          {/* PRO Plan */}
          {plans.map((plan, index) => (
            <motion.div
              key={plan.id}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.1 }}
              className="relative bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-950/30 dark:to-purple-950/30 rounded-3xl shadow-2xl border-2 border-primary/50 overflow-hidden hover:border-primary transition-all duration-300 hover:scale-[1.02]"
            >
              {/* Recommended Badge */}
              <div className="absolute top-0 right-0 bg-primary text-primary-foreground px-6 py-2 rounded-bl-2xl font-bold text-sm tracking-wide shadow-lg">
                ⭐ MOST POPULAR
              </div>

              <div className="p-8">
                {/* Plan Info */}
                <div className="text-center mb-6">
                  <h3 className="text-3xl font-bold font-heading mb-2">
                    {plan.name}
                  </h3>
                  <div className="flex items-baseline justify-center gap-2 mb-4">
                    <span className="text-5xl font-extrabold text-primary">
                      ₹{plan.price_in_rupees}
                    </span>
                    <span className="text-muted-foreground text-lg">
                      / {plan.duration_days} days
                    </span>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Secure payment via Razorpay • Instant Activation
                  </p>
                </div>

                {/* Features */}
                <div className="space-y-3 mb-8">
                  {plan.features.map((feature, i) => (
                    <div key={i} className="flex items-start gap-3">
                      <div className="mt-1 bg-green-100 p-1 rounded-full">
                        <Check className="w-4 h-4 text-green-600" />
                      </div>
                      <span className="text-foreground/90 font-medium">
                        {feature}
                      </span>
                    </div>
                  ))}
                </div>

                <Button
                  onClick={() => handleBuyNow(plan)}
                  disabled={processing}
                  size="lg"
                  className="w-full h-14 text-lg font-bold rounded-xl shadow-xl shadow-primary/20 hover:shadow-primary/40"
                >
                  {processing ? "Processing Request..." : " Upgrade to PRO Now"}
                </Button>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Trust Indicators */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-20 flex flex-wrap justify-center gap-8 md:gap-16 opacity-80"
        >
          <div className="flex items-center gap-3 text-muted-foreground">
            <Shield className="w-6 h-6 text-primary" />
            <span className="font-semibold">Secure Payment</span>
          </div>
          <div className="flex items-center gap-3 text-muted-foreground">
            <Zap className="w-6 h-6 text-yellow-500" />
            <span className="font-semibold">Instant Access</span>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
