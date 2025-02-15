export interface Word {
    id: number;
    german: string;
    english: string;
    correctCount: number;
    wrongCount: number;
}

export interface Group {
    id: number;
    name: string;
    wordCount: number;
    description: string;
}

export interface StudyActivity {
    id: number;
    name: string;
    url: string;
}

export interface PaginationResponse<T> {
    data: T[];
    total: number;
    page: number;
    pages: number;
}
    