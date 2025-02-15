import apiClient from "@/services/api-client.ts";
import { StudyActivity } from "@/types";

export const StudyActivitiesService = {
    getStudyActivities: () =>
        apiClient.get<StudyActivity[]>('/study_activities').then(res => res.data),
}