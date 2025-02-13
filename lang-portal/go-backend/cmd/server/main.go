package main

import (
	"log"
	"net/http"

	"backend/internal/database"
	"backend/internal/handlers"
	"github.com/gorilla/mux"
)

func main() {
	dbManager, err := database.NewDBConnectionManager("lang_portal.db")
	if err != nil {
		log.Fatal(err)
	}
	defer dbManager.Close()

	if err := dbManager.RunMigrations(); err != nil {
		log.Fatal(err)
	}

	if err := dbManager.Seed(); err != nil {
		log.Fatal(err)
	}

	sqlRepo := dbManager.NewSQLiteRepository()
	handler := handlers.NewHandler(sqlRepo)

	r := mux.NewRouter()
	r.HandleFunc("/words", handler.GetWords).Methods("GET")
	r.HandleFunc("/groups", handler.GetGroups).Methods("GET")
	r.HandleFunc("/groups/{id}", handler.GetGroupWords).Methods("GET")
	r.HandleFunc("/study_sessions", handler.CreateStudySession).Methods("POST")
	r.HandleFunc("/study_sessions/{id}/review", handler.LogReview).Methods("POST")

	log.Fatal(http.ListenAndServe(":8080", r))
}
