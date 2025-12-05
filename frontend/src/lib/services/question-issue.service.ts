import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export const questionIssueService = {
    /**
     * Report an issue with a question
     */
    async reportIssue(data: {
        question_id: number;
        attempt_id?: number;
        issue_type: string;
        description?: string;
    }) {
        const response = await axios.post(`${API_BASE_URL}/exam/report-issue/`, data, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                'Content-Type': 'application/json',
            },
        });
        return response.data;
    },
};

