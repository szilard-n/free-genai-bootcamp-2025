export interface Word {
    id: number;
    german: string;
    english: string;
    correctCount: number;
    wrongCount: number;
}

export interface PaginationResponse<T> {
    data: T[];
    total: number;
    page: number;
    pages: number;
}
    