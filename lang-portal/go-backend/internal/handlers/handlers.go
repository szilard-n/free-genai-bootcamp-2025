package handlers

import (
	"encoding/json"
	"net/http"
	"strconv"

	"backend/internal/database"
	"backend/internal/dto"
	"github.com/gorilla/mux"
)

type Handler struct {
	sqlRepository *database.SQLiteRepository
}

func NewHandler(repository *database.SQLiteRepository) *Handler {
	return &Handler{sqlRepository: repository}
}

func (h *Handler) GetWords(w http.ResponseWriter, r *http.Request) {
	params := dto.PaginationParams{
		Page:   getIntQueryParam(r, "page", 1),
		SortBy: r.URL.Query().Get("sort_by"),
		Order:  r.URL.Query().Get("order"),
	}

	words, total, err := h.sqlRepository.FindAllWords(params)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	response := dto.PaginationResponse{
		Data:  words,
		Total: total,
		Page:  params.Page,
		Pages: (total + 9) / 10,
	}

	json.NewEncoder(w).Encode(response)
}

func (h *Handler) GetGroups(w http.ResponseWriter, r *http.Request) {
	params := dto.PaginationParams{
		Page:   getIntQueryParam(r, "page", 1),
		SortBy: r.URL.Query().Get("sort_by"),
		Order:  r.URL.Query().Get("order"),
	}

	groups, total, err := h.sqlRepository.FindAllGroups(params)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	response := dto.PaginationResponse{
		Data:  groups,
		Total: total,
		Page:  params.Page,
		Pages: (total + 9) / 10,
	}

	json.NewEncoder(w).Encode(response)
}

func (h *Handler) GetGroupWords(w http.ResponseWriter, r *http.Request) {
	groupID, err := strconv.Atoi(mux.Vars(r)["id"])
	if err != nil {
		http.Error(w, "Invalid group ID", http.StatusBadRequest)
		return
	}

	params := dto.PaginationParams{
		Page:   getIntQueryParam(r, "page", 1),
		SortBy: r.URL.Query().Get("sort_by"),
		Order:  r.URL.Query().Get("order"),
	}

	words, total, err := h.sqlRepository.FindGroupWords(groupID, params)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	response := dto.PaginationResponse{
		Data:  words,
		Total: total,
		Page:  params.Page,
		Pages: (total + 9) / 10,
	}

	json.NewEncoder(w).Encode(response)
}

func (h *Handler) CreateStudySession(w http.ResponseWriter, r *http.Request) {
	var req struct {
		GroupID         int `json:"group_id"`
		StudyActivityID int `json:"study_activity_id"`
	}

	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request payload", http.StatusBadRequest)
		return
	}

	session, err := h.sqlRepository.CreateStudySession(req.GroupID, req.StudyActivityID)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(session)
}

func (h *Handler) LogReview(w http.ResponseWriter, r *http.Request) {
	sessionID, err := strconv.Atoi(mux.Vars(r)["id"])
	if err != nil {
		http.Error(w, "Invalid session ID", http.StatusBadRequest)
		return
	}

	var req struct {
		WordID  int  `json:"word_id"`
		Correct bool `json:"correct"`
	}

	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request payload", http.StatusBadRequest)
		return
	}

	review, err := h.sqlRepository.CreateReview(sessionID, req.WordID, req.Correct)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(review)
}

func getIntQueryParam(r *http.Request, name string, defaultValue int) int {
	valueStr := r.URL.Query().Get(name)
	if value, err := strconv.Atoi(valueStr); err == nil {
		return value
	}
	return defaultValue
}
