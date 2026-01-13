export default function AuthLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="min-h-screen flex items-center justify-center relative overflow-hidden bg-background">
            {/* Background Effects */}
            <div className="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top_right,_var(--tw-gradient-stops))] from-blue-100/50 via-background to-background dark:from-blue-900/20"></div>
            <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-purple-200/30 rounded-full blur-3xl opacity-50 pointer-events-none mix-blend-multiply"></div>
            <div className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-blue-200/30 rounded-full blur-3xl opacity-50 pointer-events-none mix-blend-multiply"></div>

            <div className="w-full max-w-md px-4 sm:px-6 lg:px-8 relative z-10">
                <div className="mb-8 text-center">
                    <div className="inline-flex items-center justify-center mb-4">
                        <img src="/logo_sample.png" alt="DCEThelper Logo" className="h-24 w-auto object-contain" />
                    </div>
                </div>
                {children}
            </div>
        </div>
    );
}
