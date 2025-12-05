import api from '../api';

export interface Exam {
    id: number;
    title: string;
    description: string;
    duration_minutes: number;
    total_marks: number;
    is_published: boolean;
}

const examService = {
    async getExams(params?: any) {
        const response = await api.get('/exams/', { params });
        return response.data;
    },

    async getExam(id: number) {
        const response = await api.get(`/exams/${id}/`);
        return response.data;
    }
};

export default examService;
