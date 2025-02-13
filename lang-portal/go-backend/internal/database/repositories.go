package database

import (
	"backend/internal/dto"
	"backend/internal/models"
)

// StudyRepository defines study-related operations
type StudyRepository interface {
	CreateStudySession(groupID, studyActivityID int) (models.StudySession, error)
	CreateReview(sessionID, wordID int, correct bool) (models.WordReviewItem, error)
}

// WordRepository defines word-related operations
type WordRepository interface {
	FindAllWords(params dto.PaginationParams) ([]models.Word, int, error)
	FindAllGroups(params dto.PaginationParams) ([]models.Group, int, error)
	FindGroupWords(groupID int, params dto.PaginationParams) ([]models.Word, int, error)
}
