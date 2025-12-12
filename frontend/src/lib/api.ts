import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use((config) => {
    // Don't attach token for public endpoints
    const publicEndpoints = [
        '/auth/login/',
        '/auth/register/',
        '/users/send-signup-otp/',
        '/users/verify-signup-otp/',
        '/users/send-password-reset-otp/',
        '/users/verify-password-reset-otp/',
        '/users/reset-password/'
    ];
    if (publicEndpoints.some(endpoint => config.url?.includes(endpoint))) {
        return config;
    }

    if (typeof window !== 'undefined') {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
    }
    return config;
});

export default api;
