package dto

type PaginationParams struct {
	Page   int    `json:"page"`
	SortBy string `json:"sort_by"`
	Order  string `json:"order"`
}

type PaginationResponse struct {
	Data  interface{} `json:"data"`
	Total int         `json:"total"`
	Page  int         `json:"page"`
	Pages int         `json:"pages"`
}
