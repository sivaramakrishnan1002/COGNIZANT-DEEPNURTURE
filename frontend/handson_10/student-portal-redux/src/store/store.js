import {configureStore} from '@reduxjs/toolkit';import courses from './coursesSlice';export const store=configureStore({reducer:{courses}});
