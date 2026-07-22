import { configureStore, createSlice } from '@reduxjs/toolkit';
const enrollment = createSlice({ name: 'enrollment', initialState: { enrolledCourses: [] }, reducers: {
  enroll: (state, { payload }) => { if (!state.enrolledCourses.some(course => course.id === payload.id)) state.enrolledCourses.push(payload); },
  unenroll: (state, { payload }) => { state.enrolledCourses = state.enrolledCourses.filter(course => course.id !== payload); }
}});
export const { enroll, unenroll } = enrollment.actions;
export const store = configureStore({ reducer: { enrollment: enrollment.reducer } });
