package handlers

import (
	"encoding/json"
	"net/http"
	"strconv"

	"backend/internal/database"
)

type StudyActivityHandler struct {
	repo database.StudyActivityRepository
}

func NewStudyActivityHandler(repo database.StudyActivityRepository) *StudyActivityHandler {
	return &StudyActivityHandler{repo: repo}
}

func (h *StudyActivityHandler) CreateStudySession(w http.ResponseWriter, r *http.Request) {
	var req struct {
		GroupID         int `json:"group_id"`
		StudyActivityID int `json:"study_activity_id"`
	}

	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request payload", http.StatusBadRequest)
		return
	}

	session, err := h.repo.CreateStudyActivitySession(req.GroupID, req.StudyActivityID)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(session)
}

func (h *StudyActivityHandler) GetStudyActivities(w http.ResponseWriter, r *http.Request) {
	activities, err := h.repo.FindAllStudyActivities()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	json.NewEncoder(w).Encode(activities)
}

func (h *StudyActivityHandler) GetStudyActivity(w http.ResponseWriter, r *http.Request) {
	activityID, err := strconv.Atoi(r.URL.Query().Get("id"))
	if err != nil {
		http.Error(w, "Invalid activity ID", http.StatusBadRequest)
		return
	}

	sessions, err := h.repo.FindStudyActivity(activityID)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	json.NewEncoder(w).Encode(sessions)
}

func (h *StudyActivityHandler) GetStudyActivitySessions(w http.ResponseWriter, r *http.Request) {
	activityID, err := strconv.Atoi(r.URL.Query().Get("id"))
	if err != nil {
		http.Error(w, "Invalid activity ID", http.StatusBadRequest)
		return
	}

	sessions, err := h.repo.FindStudyActivitySessions(activityID)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	json.NewEncoder(w).Encode(sessions)
}
