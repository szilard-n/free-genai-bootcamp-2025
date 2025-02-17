package database

import (
	"database/sql"

	"backend/internal/dto"
	"backend/internal/models"
)

type SQLGroupRepository struct {
	db *sql.DB
}

// FindAllGroups implements WordRepository
func (r *SQLGroupRepository) FindAllGroups(params dto.PaginationParams) ([]models.Group, int, error) {
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
        SELECT id, name, words_count, description
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
		err := rows.Scan(&g.ID, &g.Name, &g.WordsCount, &g.Description)
		if err != nil {
			return nil, 0, err
		}
		groups = append(groups, g)
	}

	return groups, total, nil
}

// FIndGroup implements WordRepository
func (r *SQLGroupRepository) FindGroup(groupID int) (models.Group, error) {
	var group models.Group
	err := r.db.QueryRow(`
		SELECT id, name, words_count, description
		FROM groups
		WHERE id = ?`, groupID).Scan(
		&group.ID,
		&group.Name,
		&group.WordsCount,
		&group.Description,
	)

	return group, err
}

// FindGroupWords implements WordRepository
func (r *SQLGroupRepository) FindGroupWords(groupID int) ([]models.Word, error) {
	query := `
		SELECT id, german, english, class
		FROM words
		WHERE group_id = ?`

	rows, err := r.db.Query(query, groupID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var words []models.Word
	for rows.Next() {
		var w models.Word
		err := rows.Scan(&w.ID, &w.German, &w.English, &w.Class)
		if err != nil {
			return nil, err
		}
		words = append(words, w)
	}

	return words, nil
}

// FindGroupStudySessions implements WordRepository
func (r *SQLGroupRepository) FindGroupStudySessions(groupID int) ([]models.StudySession, error) {
	query := `
		SELECT id, group_id, study_activity_id, created_at
		FROM study_sessions
		WHERE group_id = ?`

	rows, err := r.db.Query(query, groupID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var sessions []models.StudySession
	for rows.Next() {
		var s models.StudySession
		err := rows.Scan(&s.ID, &s.GroupID, &s.StudyActivityID, &s.CreatedAt)
		if err != nil {
			return nil, err
		}
		sessions = append(sessions, s)
	}

	return sessions, nil
}
