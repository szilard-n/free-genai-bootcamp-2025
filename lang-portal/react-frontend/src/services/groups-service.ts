import apiClient from "@/services/api-client.ts";
import { Group, PaginationResponse } from "@/types";


export const GroupsService = {
    getGroups: (page: number = 1) =>
        apiClient.get<PaginationResponse<Group>>('/groups', { params: { page } }).then(res => res.data),

    getGroup: (id: number) =>
        apiClient.get<Group>(`/groups/${id}`).then(res => res.data),
}