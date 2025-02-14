package database

import (
	"database/sql"

	"backend/internal/dto"
	"backend/internal/models"
)

type SQLiteRepository struct {
	db *sql.DB
}

// FindAllWords implements WordRepository
func (r *SQLiteRepository) FindAllWords(params dto.PaginationParams) ([]models.Word, int, error) {
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
func (r *SQLiteRepository) FindWordByID(id int) (models.Word, error) {
	var word models.Word
	err := r.db.QueryRow(`
		SELECT id, german, english, class
		FROM words
		WHERE id = ?`, id).Scan(&word.ID, &word.German, &word.English, &word.Class)

	return word, err
}

// FindAllGroups implements WordRepository
func (r *SQLiteRepository) FindAllGroups(params dto.PaginationParams) ([]models.Group, int, error) {
	// Get total count
	var total int
	err := r.db.QueryRow("SELECT COUNT(*) FROM groups").Scan(&total)
	if err != nil {
		return nil, 0, err
	}

	// Calculate pagination
	limit := 10
	offset := (params.Page - 1) * limit

	query := `
        SELECT id, name, words_count
        FROM groups
        LIMIT ? OFFSET ?`

	rows, err := r.db.Query(query, limit, offset)
	if err != nil {
		return nil, 0, err
	}
	defer rows.Close()

	var groups []models.Group
	for rows.Next() {
		var g models.Group
		err := rows.Scan(&g.ID, &g.Name, &g.WordsCount)
		if err != nil {
			return nil, 0, err
		}
		groups = append(groups, g)
	}

	return groups, total, nil
}

// FindGroupWords implements WordRepository
func (r *SQLiteRepository) FindGroupWords(groupID int, params dto.PaginationParams) ([]models.Word, int, error) {
	var total int
	err := r.db.QueryRow(`
		SELECT COUNT(*)
		FROM words w
		JOIN word_groups wg ON w.id = wg.word_id
		WHERE wg.group_id = ?`, groupID).Scan(&total)
	if err != nil {
		return nil, 0, err
	}

	if params.SortBy == "" {
		params.SortBy = "german"
	}
	if params.Order != "desc" {
		params.Order = "asc"
	}

	limit := 10
	offset := (params.Page - 1) * limit

	query := `
		SELECT w.id, w.german, w.english, w.class
		FROM words w
		JOIN word_groups wg ON w.id = wg.word_id
		WHERE wg.group_id = ?
		ORDER BY w.` + params.SortBy + ` ` + params.Order + `
		LIMIT ? OFFSET ?`

	rows, err := r.db.Query(query, groupID, limit, offset)
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

// CreateStudySession implements StudyRepository
func (r *SQLiteRepository) CreateStudySession(groupID, studyActivityID int) (models.StudySession, error) {
	query := `
		INSERT INTO study_sessions (group_id, study_activity_id)
		VALUES (?, ?)`

	result, err := r.db.Exec(query, groupID, studyActivityID)
	if err != nil {
		return models.StudySession{}, err
	}

	id, err := result.LastInsertId()
	if err != nil {
		return models.StudySession{}, err
	}

	var session models.StudySession
	err = r.db.QueryRow(`
		SELECT id, group_id, study_activity_id, created_at
		FROM study_sessions
		WHERE id = ?`, id).Scan(
		&session.ID,
		&session.GroupID,
		&session.StudyActivityID,
		&session.CreatedAt,
	)

	return session, err
}

// CreateReview implements StudyRepository
func (r *SQLiteRepository) CreateReview(sessionID, wordID int, correct bool) (models.WordReviewItem, error) {
	query := `
		INSERT INTO word_review_items (study_session_id, word_id, correct)
		VALUES (?, ?, ?)`

	result, err := r.db.Exec(query, sessionID, wordID, correct)
	if err != nil {
		return models.WordReviewItem{}, err
	}

	id, err := result.LastInsertId()
	if err != nil {
		return models.WordReviewItem{}, err
	}

	var review models.WordReviewItem
	err = r.db.QueryRow(`
		SELECT id, word_id, study_session_id, correct, created_at
		FROM word_review_items
		WHERE id = ?`, id).Scan(
		&review.ID,
		&review.WordID,
		&review.StudySessionID,
		&review.Correct,
		&review.CreatedAt,
	)

	return review, err
}
