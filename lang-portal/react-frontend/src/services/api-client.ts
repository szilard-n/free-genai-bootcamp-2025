import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://localhost:8081/",
  headers: {
    "Content-Type": "application/json",
  },
  transformRequest: [(data, headers) => {
    return data;
  }],
});

apiClient.interceptors.request.use(
  (config) => {
    console.log('Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default apiClient;

