package main

import (
	"log"
	"net/http"

	"backend/internal/database"
	"backend/internal/handlers"
	"github.com/gorilla/mux"
	"github.com/rs/cors"
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
	r.HandleFunc("/words/{id}", handler.GetWordById).Methods("GET")
	r.HandleFunc("/groups", handler.GetGroups).Methods("GET")
	r.HandleFunc("/groups/{id}", handler.GetGroupWords).Methods("GET")
	r.HandleFunc("/study_sessions", handler.CreateStudySession).Methods("POST")
	r.HandleFunc("/study_sessions/{id}/review", handler.LogReview).Methods("POST")

	c := cors.New(cors.Options{
		AllowedOrigins: []string{"http://localhost:8080"},
		AllowedMethods: []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowedHeaders: []string{"Content-Type", "Authorization"},
	})

	corsHandler := c.Handler(r)
	log.Fatal(http.ListenAndServe(":8081", corsHandler))
}
