package database

import (
	"database/sql"

	"backend/internal/dto"
	"backend/internal/models"
)

type SQLWordRepository struct {
	db *sql.DB
}

// FindAllWords implements WordRepository
func (r *SQLWordRepository) FindAllWords(params dto.PaginationParams) ([]models.Word, int, error) {
	// Get total count
	var total int
	err := r.db.QueryRow("SELECT COUNT(*) FROM words").Scan(&total)
	if err != nil {
		return nil, 0, err
	}

	// Validate and set default sorting
	if params.SortBy == "" {
		params.SortBy = "german"
	}
	if params.Order != "desc" {
		params.Order = "asc"
	}

	// Calculate pagination
	limit := 10
	offset := (params.Page - 1) * limit

	query := `
		SELECT id, german, english, class
		FROM words
		ORDER BY ` + params.SortBy + ` ` + params.Order + `
		LIMIT ? OFFSET ?`

	rows, err := r.db.Query(query, limit, offset)
	if err != nil {
		return nil, 0, err
	}
	defer rows.Close()

	var words []models.Word
	for rows.Next() {
		var w models.Word
		err := rows.Scan(&w.ID, &w.German, &w.English, &w.Class)
		if err != nil {
			return nil, 0, err
		}
		words = append(words, w)
	}

	return words, total, nil
}

// FindWordByID implements WordRepository
func (r *SQLWordRepository) FindWordByID(id int) (models.Word, error) {
	var word models.Word
	err := r.db.QueryRow(`
		SELECT id, german, english, class
		FROM words
		WHERE id = ?`, id).Scan(&word.ID, &word.German, &word.English, &word.Class)

	return word, err
}
