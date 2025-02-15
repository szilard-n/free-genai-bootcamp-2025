package database

import (
	"database/sql"
	"io/ioutil"
	"log"
	"path/filepath"

	"github.com/mattn/go-sqlite3"
)

var _ any = (*sqlite3.SQLiteDriver)(nil)

type DBConnectionManager struct {
	db *sql.DB
}

// NewDBConnectionManager creates a new database manager
func NewDBConnectionManager(dbPath string) (*DBConnectionManager, error) {
	db, err := sql.Open("sqlite3", dbPath)
	if err != nil {
		return nil, err
	}

	// Enable foreign keys
	if _, err := db.Exec("PRAGMA foreign_keys = ON"); err != nil {
		db.Close()
		return nil, err
	}

	return &DBConnectionManager{db: db}, nil
}

func (m *DBConnectionManager) NewSQLiteRepository() *SQLiteRepository {
	return &SQLiteRepository{db: m.db}
}

func (m *DBConnectionManager) RunMigrations() error {
	files, err := filepath.Glob("migration/*.sql")
	if err != nil {
		return err
	}

	for _, file := range files {
		content, err := ioutil.ReadFile(file)
		if err != nil {
			return err
		}

		if _, err := m.db.Exec(string(content)); err != nil {
			return err
		}
	}

	return nil
}

func (m *DBConnectionManager) Seed() error {
	words := []struct {
		German  string
		English string
		Class   string
	}{
		{"das Haus", "House", "noun"},
		{"der Hund", "Dog", "noun"},
		{"die Katze", "Cat", "noun"},
		{"das Buch", "Book", "noun"},
		{"der Stuhl", "Chair", "noun"},
		{"der Tisch", "Table", "noun"},
		{"das Auto", "Car", "noun"},
		{"der Baum", "Tree", "noun"},
		{"die Blume", "Flower", "noun"},
		{"der Apfel", "Apple", "noun"},
		{"die Schule", "School", "noun"},
		{"der Lehrer", "Teacher", "noun"},
		{"die Schülerin", "Student (female)", "noun"},
		{"der Schüler", "Student (male)", "noun"},
		{"das Fenster", "Window", "noun"},
		{"die Tür", "Door", "noun"},
		{"der Computer", "Computer", "noun"},
		{"das Telefon", "Phone", "noun"},
		{"die Uhr", "Clock", "noun"},
		{"der Tisch", "Desk", "noun"},
		{"das Papier", "Paper", "noun"},
		{"der Stift", "Pen", "noun"},
		{"das Heft", "Notebook", "noun"},
		{"das Bild", "Picture", "noun"},
		{"die Lampe", "Lamp", "noun"},
		{"der Teppich", "Carpet", "noun"},
		{"die Wand", "Wall", "noun"},
		{"das Dach", "Roof", "noun"},
		{"der Garten", "Garden", "noun"},
		{"die Straße", "Street", "noun"},
	}

	for _, word := range words {
		_, err := m.db.Exec("INSERT INTO words (german, english, class) VALUES (?, ?, ?)", word.German, word.English, word.Class)
		if err != nil {
			return err
		}
	}

	groups := []struct {
		Name        string
		Description string
	}{
		{"Basic Nouns", "Basic nouns for beginners"},
		{"Household Items", "Items found in a house"},
		{"Animals", "Common animals"},
	}

	for _, group := range groups {
		_, err := m.db.Exec("INSERT INTO groups (name, description) VALUES (?, ?)", group.Name, group.Description)
		if err != nil {
			return err
		}
	}

	wordGroups := []struct {
		WordID  int
		GroupID int
	}{
		{1, 1}, {2, 3}, {3, 3}, {4, 1}, {5, 2},
		{6, 2}, {7, 1}, {8, 1}, {9, 1}, {10, 1},
		{11, 1}, {12, 1}, {13, 1}, {14, 1}, {15, 2},
		{16, 2}, {17, 2}, {18, 2}, {19, 2}, {20, 2},
		{21, 2}, {22, 2}, {23, 2}, {24, 2}, {25, 2},
		{26, 2}, {27, 2}, {28, 2}, {29, 2}, {30, 2},
	}

	for _, wordGroup := range wordGroups {
		_, err := m.db.Exec("INSERT INTO word_groups (word_id, group_id) VALUES (?, ?)", wordGroup.WordID, wordGroup.GroupID)
		if err != nil {
			return err
		}
	}

	studyActivities := []struct {
		Name string
		URL  string
	}{
		{"Flashcards", "https://picsum.photos/seed/picsum/600/300"},
		{"Quizzes", "https://picsum.photos/seed/picsum/600/300"},
		{"Listening Practice", "https://picsum.photos/seed/picsum/600/300"},
	}

	for _, activity := range studyActivities {
		_, err := m.db.Exec("INSERT INTO study_activities (name, url) VALUES (?, ?)", activity.Name, activity.URL)
		if err != nil {
			return err
		}
	}

	log.Println("Database seeded successfully with words, groups, word_groups, and study_activities.")
	return nil
}

func (m *DBConnectionManager) Close() error {
	return m.db.Close()
}
