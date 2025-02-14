import { Word, PaginationResponse } from "@/types"
import apiClient from "./api-client"

export const WordsService = {
    getWords: (page: number = 1) => 
        apiClient.get<PaginationResponse<Word>>('/words', { params: { page } }).then(res => res.data),

    getWord: (id: number) => 
        apiClient.get<Word>(`/words/${id}`).then(res => res.data),
}