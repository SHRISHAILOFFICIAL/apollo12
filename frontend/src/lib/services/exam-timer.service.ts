import api from '../api';

export const examTimerService = {
    // Start exam and get initial timer state
    async startExam(examId: number) {
        // Backend expects exam_id in URL, not body
        const response = await api.post(`/exam/timer/start/${examId}/`);
        return response.data;
    },

    // Get questions for the attempt
    async getExamQuestions(attemptId: number) {
        const response = await api.get(`/exam/timer/questions/${attemptId}/`);
        return response.data;
    },

    // Get remaining time from server (source of truth)
    async getRemainingTime(attemptId: number) {
        const response = await api.get(`/exam/timer/remaining/${attemptId}/`);
        return response.data;
    },

    // Submit an answer
    async submitAnswer(data: { attempt_id: number; question_id: number; selected_option: string }) {
        const response = await api.post('/exam/timer/submit-answer/', data);
        return response.data;
    },

    // Submit the entire exam
    async submitExam(attemptId: number) {
        const response = await api.post(`/exam/timer/submit/${attemptId}/`);
        return response.data;
    },

    // Helper: Format seconds to MM:SS
    formatTime(seconds: number): string {
        if (seconds <= 0) return "00:00";
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
    },

    // Helper: Check if time is critical (< 1 min)
    isTimeCritical(seconds: number): boolean {
        return seconds > 0 && seconds < 60;
    },

    // Helper: Check if time is warning (< 5 mins)
    isTimeWarning(seconds: number): boolean {
        return seconds >= 60 && seconds < 300;
    }
};
