package handlers

import (
	"encoding/json"
	"net/http"
	"strconv"

	"backend/internal/database"
	"backend/internal/dto"
	"github.com/gorilla/mux"
)

type WordHandler struct {
	repo database.WordRepository
}

func NewWordHandler(repo database.WordRepository) *WordHandler {
	return &WordHandler{repo: repo}
}

func (h *WordHandler) GetWords(w http.ResponseWriter, r *http.Request) {
	params := dto.PaginationParams{
		Page:   getIntQueryParam(r, "page", 1),
		SortBy: r.URL.Query().Get("sort_by"),
		Order:  r.URL.Query().Get("order"),
	}

	words, total, err := h.repo.FindAllWords(params)
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

func (h *WordHandler) GetWordById(w http.ResponseWriter, r *http.Request) {
	wordID, err := strconv.Atoi(mux.Vars(r)["id"])
	if err != nil {
		http.Error(w, "Invalid word ID", http.StatusBadRequest)
		return
	}

	word, err := h.repo.FindWordByID(wordID)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	json.NewEncoder(w).Encode(word)
}
