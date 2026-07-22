import axios from 'axios';
const apiClient=axios.create({baseURL:'https://jsonplaceholder.typicode.com',headers:{'Content-Type':'application/json'},timeout:8000});
apiClient.interceptors.request.use(config=>{config.headers.Authorization='Bearer demo-student-token';return config});
apiClient.interceptors.response.use(response=>response.data,error=>{const standard=new Error(error.response?.data?.message||'Unable to load courses. Please try again.');standard.statusCode=error.response?.status||0;return Promise.reject(standard)});export default apiClient;
