package handlers

import (
	"encoding/json"
	"log"
	"net/http"
	"strconv"

	"backend/internal/database"
	"backend/internal/dto"
	"github.com/gorilla/mux"
)

type GroupHandler struct {
	repo database.GroupRepository
}

func NewGroupHandler(repo database.GroupRepository) *GroupHandler {
	return &GroupHandler{repo: repo}
}

func (h *GroupHandler) GetGroups(w http.ResponseWriter, r *http.Request) {
	params := dto.PaginationParams{
		Page:   getIntQueryParam(r, "page", 1),
		SortBy: r.URL.Query().Get("sort_by"),
		Order:  r.URL.Query().Get("order"),
	}

	groups, total, err := h.repo.FindAllGroups(params)
	if err != nil {
		log.Printf("Error: %v", err)
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

func (h *GroupHandler) GetGroup(w http.ResponseWriter, r *http.Request) {
	groupID, err := strconv.Atoi(mux.Vars(r)["id"])
	if err != nil {
		http.Error(w, "Invalid group ID", http.StatusBadRequest)
		return
	}

	word, err := h.repo.FindGroup(groupID)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	json.NewEncoder(w).Encode(word)
}

func (h *GroupHandler) GetGroupWords(w http.ResponseWriter, r *http.Request) {
	groupID, err := strconv.Atoi(mux.Vars(r)["id"])
	if err != nil {
		http.Error(w, "Invalid group ID", http.StatusBadRequest)
		return
	}

	words, err := h.repo.FindGroupWords(groupID)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	json.NewEncoder(w).Encode(words)
}

func (h *GroupHandler) GetGroupStudySessions(w http.ResponseWriter, r *http.Request) {
	groupID, err := strconv.Atoi(mux.Vars(r)["id"])
	if err != nil {
		http.Error(w, "Invalid group ID", http.StatusBadRequest)
		return
	}

	sessions, err := h.repo.FindGroupStudySessions(groupID)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	json.NewEncoder(w).Encode(sessions)
}
