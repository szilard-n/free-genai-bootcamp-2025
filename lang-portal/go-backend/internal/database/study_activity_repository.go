package database

import (
	"database/sql"

	"backend/internal/models"
)

type SQLStudyActivityRepository struct {
	db *sql.DB
}

// CreateStudyActivitySession implements StudyActivityRepository
func (r *SQLStudyActivityRepository) CreateStudyActivitySession(groupID, studyActivityID int) (models.StudySession, error) {
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

func (r *SQLStudyActivityRepository) FindAllStudyActivities() ([]models.StudyActivity, error) {
	rows, err := r.db.Query(`
		SELECT id, name, url
		FROM study_activities`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var activities []models.StudyActivity
	for rows.Next() {
		var a models.StudyActivity
		err := rows.Scan(&a.ID, &a.Name, &a.URL)
		if err != nil {
			return nil, err
		}
		activities = append(activities, a)
	}

	return activities, nil
}

// FindStudyActivity implements StudyActivityRepository
func (r *SQLStudyActivityRepository) FindStudyActivity(studyActivityID int) (models.StudyActivity, error) {
	var activity models.StudyActivity
	err := r.db.QueryRow(`
		SELECT id, name, url
		FROM study_activities
		WHERE id = ?`, studyActivityID).Scan(
		&activity.ID,
		&activity.Name,
		&activity.URL,
	)

	return activity, err
}

func (r *SQLStudyActivityRepository) FindStudyActivitySessions(studyActivityID int) ([]models.StudySession, error) {
	query := `
		SELECT id, group_id, study_activity_id, created_at
		FROM study_sessions
		WHERE study_activity_id = ?`

	rows, err := r.db.Query(query, studyActivityID)
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
