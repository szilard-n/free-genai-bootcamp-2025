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

	wordHandler := handlers.NewWordHandler(dbManager.NewWordRepository())
	groupHandler := handlers.NewGroupHandler(dbManager.NewGroupRepository())
	studyHandler := handlers.NewStudyActivityHandler(dbManager.NewStudyRepository())

	r := mux.NewRouter()
	r.HandleFunc("/words", wordHandler.GetWords).Methods("GET")
	r.HandleFunc("/words/{id}", wordHandler.GetWordById).Methods("GET")

	r.HandleFunc("/groups", groupHandler.GetGroups).Methods("GET")
	r.HandleFunc("/groups/{id}", groupHandler.GetGroup).Methods("GET")
	r.HandleFunc("/groups/{id}/words", groupHandler.GetGroupWords).Methods("GET")
	r.HandleFunc("/groups/{id}/study_sessions", groupHandler.GetGroupStudySessions).Methods("GET")

	r.HandleFunc("/study_activities", studyHandler.GetStudyActivities).Methods("GET")
	r.HandleFunc("/study_activities/{id}", studyHandler.GetStudyActivity).Methods("GET")
	r.HandleFunc("/study_activities/{id}/sessions", studyHandler.GetStudyActivitySessions).Methods("GET")

	c := cors.New(cors.Options{
		AllowedOrigins: []string{"http://localhost:8080"},
		AllowedMethods: []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowedHeaders: []string{"Content-Type", "Authorization"},
	})

	corsHandler := c.Handler(r)
	log.Fatal(http.ListenAndServe(":8081", corsHandler))
}
