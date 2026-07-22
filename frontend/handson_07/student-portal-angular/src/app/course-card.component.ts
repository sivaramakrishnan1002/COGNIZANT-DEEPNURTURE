import { Component,Input } from '@angular/core';
@Component({selector:'app-course-card',standalone:true,template:`<article><h2>{{name}}</h2><p>{{code}} · {{credits}} credits · {{grade}}</p></article>`,styles:[`article{padding:1rem;border-radius:10px;background:#f4f7fc}`]}) export class CourseCardComponent{@Input() name='';@Input() code='';@Input() credits=0;@Input() grade='Pending';}
