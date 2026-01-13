"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Mail,
  Phone,
  User,
  MessageSquare,
  CheckCircle,
  AlertCircle,
  ArrowLeft,
} from "lucide-react";
import Link from "next/link";

export default function ContactPage() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    mobile: "",
    query: "",
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState<
    "idle" | "success" | "error"
  >("idle");
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem("access_token");
    setIsAuthenticated(!!token);
  }, []);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitStatus("idle");
    setErrorMessage("");

    try {
      const response = await fetch(
        `${
          process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api"
        }/users/submit-query/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        }
      );

      const data = await response.json();

      if (response.ok) {
        setSubmitStatus("success");
        setFormData({ username: "", email: "", mobile: "", query: "" });
      } else {
        setSubmitStatus("error");
        // Handle validation errors
        if (data.mobile) {
          setErrorMessage(data.mobile[0]);
        } else if (data.query) {
          setErrorMessage(data.query[0]);
        } else if (data.email) {
          setErrorMessage(data.email[0]);
        } else {
          setErrorMessage("Failed to submit query. Please try again.");
        }
      }
    } catch (error) {
      setSubmitStatus("error");
      setErrorMessage(
        "Network error. Please check your connection and try again."
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Navbar */}
      <nav className="fixed top-0 w-full z-50 glass border-b border-white/20">
        <div className="container mx-auto px-6 h-16 flex items-center justify-between">
          <Link
            href={isAuthenticated ? "/dashboard" : "/"}
            className="flex items-center gap-2"
          >
            <img
              src="/logo_sample.png"
              alt="DCEThelper Logo"
              className="h-20 w-auto object-contain"
            />
          </Link>
          <div className="flex gap-4">
            {isAuthenticated ? (
              <Button
                variant="ghost"
                onClick={() => router.push("/dashboard")}
                className="gap-2"
              >
                <ArrowLeft className="w-4 h-4" /> Back to Dashboard
              </Button>
            ) : (
              <>
                <Link href="/auth/login">
                  <Button
                    variant="ghost"
                    className="font-medium text-muted-foreground hover:text-primary"
                  >
                    Login
                  </Button>
                </Link>
                <Link href="/auth/signup">
                  <Button className="rounded-full px-6 shadow-lg shadow-primary/25">
                    Get Started
                  </Button>
                </Link>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* Contact Form Section */}
      <div className="pt-32 pb-20 px-6">
        <div className="container mx-auto max-w-2xl">
          <div className="text-center mb-10">
            <h1 className="text-4xl md:text-5xl font-heading font-bold mb-4 text-foreground">
              Get in Touch
            </h1>
            <p className="text-xl text-muted-foreground">
              Have a question or need help? We're here to assist you!
            </p>
          </div>

          <Card className="shadow-xl border-2">
            <CardHeader>
              <CardTitle className="text-2xl">Send us a Message</CardTitle>
              <CardDescription>
                Fill out the form below and we'll get back to you as soon as
                possible.
              </CardDescription>
            </CardHeader>
            <CardContent>
              {submitStatus === "success" && (
                <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="font-semibold text-green-900">
                      Query Submitted Successfully!
                    </p>
                    <p className="text-sm text-green-700">
                      We'll get back to you soon.
                    </p>
                  </div>
                </div>
              )}

              {submitStatus === "error" && (
                <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
                  <AlertCircle className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="font-semibold text-red-900">
                      Submission Failed
                    </p>
                    <p className="text-sm text-red-700">{errorMessage}</p>
                  </div>
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-2">
                  <label
                    htmlFor="username"
                    className="text-sm font-medium flex items-center gap-2"
                  >
                    <User className="w-4 h-4" />
                    Your Name
                  </label>
                  <Input
                    id="username"
                    name="username"
                    type="text"
                    placeholder="Enter your name"
                    value={formData.username}
                    onChange={handleChange}
                    required
                    className="h-12"
                  />
                </div>

                <div className="space-y-2">
                  <label
                    htmlFor="email"
                    className="text-sm font-medium flex items-center gap-2"
                  >
                    <Mail className="w-4 h-4" />
                    Email Address
                  </label>
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    placeholder="your.email@example.com"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    className="h-12"
                  />
                </div>

                <div className="space-y-2">
                  <label
                    htmlFor="mobile"
                    className="text-sm font-medium flex items-center gap-2"
                  >
                    <Phone className="w-4 h-4" />
                    Mobile Number
                  </label>
                  <Input
                    id="mobile"
                    name="mobile"
                    type="tel"
                    placeholder="10-digit mobile number"
                    value={formData.mobile}
                    onChange={handleChange}
                    required
                    className="h-12"
                  />
                </div>

                <div className="space-y-2">
                  <label
                    htmlFor="query"
                    className="text-sm font-medium flex items-center gap-2"
                  >
                    <MessageSquare className="w-4 h-4" />
                    Your Query
                  </label>
                  <Textarea
                    id="query"
                    name="query"
                    placeholder="Please describe your question or concern in detail (minimum 10 characters)"
                    value={formData.query}
                    onChange={handleChange}
                    required
                    rows={6}
                    className="resize-none"
                  />
                </div>

                <Button
                  type="submit"
                  className="w-full h-12 text-lg rounded-full shadow-lg shadow-primary/20"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? "Submitting..." : "Submit Query"}
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Footer */}
      <footer className="py-12 bg-slate-50 border-t border-border">
        <div className="container mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-2">
            <img
              src="/logo_sample.png"
              alt="DCEThelper Logo"
              className="h-16 w-auto object-contain"
            />
          </div>
          <div className="text-sm text-muted-foreground">
            © 2025 Apollo11 EdTech. All rights reserved.
          </div>
          <div className="flex gap-6 text-sm text-muted-foreground">
            <Link href="/" className="hover:text-primary transition-colors">
              Home
            </Link>
            <Link
              href="/contact"
              className="hover:text-primary transition-colors"
            >
              Contact
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
