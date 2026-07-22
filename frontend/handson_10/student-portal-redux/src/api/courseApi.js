import client from './apiClient';
export const getAllCourses=async()=>{const posts=await client.get('/posts',{params:{_limit:5}});return posts.map((post,index)=>({id:post.id,name:post.title,code:`CS${101+index}`,credits:index%2?3:4}))};export const getCourseById=id=>client.get(`/posts/${id}`);export const enrollStudent=(studentId,courseId)=>client.post('/posts',{studentId,courseId});
