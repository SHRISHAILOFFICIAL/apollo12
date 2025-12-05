import api from '../api';

export interface ExamAttempt {
    id: number;
    test_title: string;
    score: number;
    completed_at: string;
    exam: number;
}

const attemptService = {
    async getMyAttempts() {
        const response = await api.get('/attempts/my_attempts/');
        return response.data;
    },

    async startExam(examId: number) {
        const response = await api.post('/attempts/start_exam/', { exam_id: examId });
        return response.data;
    },

    async submitAnswer(attemptId: number, questionId: number, optionId: number) {
        const response = await api.post('/attempts/submit_answer/', {
            attempt_id: attemptId,
            question_id: questionId,
            selected_option_id: optionId
        });
        return response.data;
    },

    async submitExam(attemptId: number) {
        const response = await api.post(`/attempts/${attemptId}/submit_exam/`);
        return response.data;
    }
};

export default attemptService;
