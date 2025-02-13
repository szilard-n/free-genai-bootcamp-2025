package models

import (
	"time"
)

// Word represents the base vocabulary entity
type Word struct {
	ID      int    `json:"id"`
	German  string `json:"german"`
	English string `json:"english"`
	Class   string `json:"class"`
}

// Group represents a collection of words
type Group struct {
	ID         int    `json:"id"`
	Name       string `json:"name"`
	WordsCount int    `json:"words_count"`
}

// WordGroup represents the join table between words and groups
type WordGroup struct {
	WordID  int `json:"word_id"`
	GroupID int `json:"group_id"`
}

// StudyActivity represents available study methods
type StudyActivity struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
	URL  string `json:"url"`
}

// StudySession represents a study session instance
type StudySession struct {
	ID              int       `json:"id"`
	GroupID         int       `json:"group_id"`
	StudyActivityID int       `json:"study_activity_id"`
	CreatedAt       time.Time `json:"created_at"`
}

// WordReviewItem represents individual word review attempts
type WordReviewItem struct {
	ID             int       `json:"id"`
	WordID         int       `json:"word_id"`
	StudySessionID int       `json:"study_session_id"`
	Correct        bool      `json:"correct"`
	CreatedAt      time.Time `json:"created_at"`
}
