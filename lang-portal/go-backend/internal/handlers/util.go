package handlers

import (
	"net/http"
	"strconv"
)

func getIntQueryParam(r *http.Request, name string, defaultValue int) int {
	valueStr := r.URL.Query().Get(name)
	if value, err := strconv.Atoi(valueStr); err == nil {
		return value
	}
	return defaultValue
}
