import api from '../api';
import { jwtDecode } from "jwt-decode";

export const authService = {
    async register(userData: any) {
        const response = await api.post('/auth/register/', userData);
        return response.data;
    },

    async login(credentials: any) {
        const response = await api.post('/auth/login/', credentials);
        if (response.data.access) {
            localStorage.setItem('access_token', response.data.access);
            localStorage.setItem('refresh_token', response.data.refresh);
        }
        return response.data;
    },

    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    },

    isAuthenticated() {
        if (typeof window === 'undefined') return false;
        const token = localStorage.getItem('access_token');
        if (!token) return false;
        try {
            const decoded: any = jwtDecode(token);
            const currentTime = Date.now() / 1000;
            if (decoded.exp < currentTime) {
                this.logout();
                return false;
            }
            return true;
        } catch (e) {
            return false;
        }
    },

    getUser() {
        if (typeof window === 'undefined') return null;
        const token = localStorage.getItem('access_token');
        if (!token) return null;
        try {
            return jwtDecode(token);
        } catch (e) {
            return null;
        }
    }
};
