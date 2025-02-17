package database

import (
	"backend/internal/dto"
	"backend/internal/models"
)

// StudyActivityRepository defines study-related operations
type StudyActivityRepository interface {
	CreateStudyActivitySession(groupID, studyActivityID int) (models.StudySession, error)
	FindAllStudyActivities() ([]models.StudyActivity, error)
	FindStudyActivity(studyActivityID int) (models.StudyActivity, error)
	FindStudyActivitySessions(studyActivityID int) ([]models.StudySession, error)
}

// WordRepository defines word-related operations
type WordRepository interface {
	FindAllWords(params dto.PaginationParams) ([]models.Word, int, error)
	FindWordByID(id int) (models.Word, error)
}

// GroupRepository defines group-related operations
type GroupRepository interface {
	FindAllGroups(params dto.PaginationParams) ([]models.Group, int, error)
	FindGroup(groupID int) (models.Group, error)
	FindGroupWords(groupID int) ([]models.Word, error)
	FindGroupStudySessions(groupID int) ([]models.StudySession, error)
}

type StudySessionRepository interface {
	CreateStudySession(request dto.CreateStudySessionRequest) (models.StudySession, error)
	FindAllStudySessions(params dto.PaginationParams) ([]models.StudySession, error)
	FindStudySession(studySessionID int) (models.StudySession, error)
	LogStudySessionReview(request dto.LogStudySessionReviewRequest) (models.WordReviewItem, error)
}
