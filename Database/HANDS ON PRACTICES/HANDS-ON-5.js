//HANDS ON 5
//task 1

use college_nosql

db.createCollection("feedback")

db.feedback.insertMany([
{
student_id:1,
course_code:"CS101",
semester:"2022-ODD",
rating:5,
comments:"Excellent teaching",
tags:["challenging","well-structured"],
submitted_at:new Date(),
attachments:[{filename:"notes.pdf",size_kb:240}]
},
{
student_id:2,
course_code:"CS101",
semester:"2022-ODD",
rating:4,
comments:"Very good",
tags:["challenging","examples"],
submitted_at:new Date(),
attachments:[{filename:"lab.pdf",size_kb:120}]
},
{
student_id:3,
course_code:"CS101",
semester:"2022-ODD",
rating:5,
comments:"Best course",
tags:["challenging","good-examples"],
submitted_at:new Date(),
attachments:[{filename:"ppt.pdf",size_kb:150}]
},
{
student_id:4,
course_code:"CS102",
semester:"2022-ODD",
rating:3,
comments:"Average",
tags:["database","normalization"],
submitted_at:new Date(),
attachments:[{filename:"dbms.pdf",size_kb:180}]
},
{
student_id:5,
course_code:"CS102",
semester:"2022-ODD",
rating:2,
comments:"Needs improvement",
tags:["database"],
submitted_at:new Date(),
attachments:[{filename:"review.pdf",size_kb:100}]
},
{
student_id:6,
course_code:"EC101",
semester:"2021-EVEN",
rating:4,
comments:"Good",
tags:["electronics"],
submitted_at:new Date(),
attachments:[{filename:"ec.pdf",size_kb:120}]
},
{
student_id:7,
course_code:"ME101",
semester:"2022-ODD",
rating:5,
comments:"Interesting",
tags:["mechanical","practical"],
submitted_at:new Date(),
attachments:[{filename:"mech.pdf",size_kb:110}]
},
{
student_id:8,
course_code:"CS103",
semester:"2022-ODD",
rating:1,
comments:"Difficult",
tags:["oop","hard"],
submitted_at:new Date(),
attachments:[{filename:"oop.pdf",size_kb:130}]
},
{
student_id:9,
course_code:"CS103",
semester:"2022-ODD",
rating:3,
comments:"Okay",
tags:["oop"],
submitted_at:new Date(),
attachments:[{filename:"java.pdf",size_kb:140}]
},
{
student_id:10,
course_code:"CS101",
semester:"2022-ODD",
rating:5,
comments:"Highly recommended",
tags:["challenging","well-structured"],
submitted_at:new Date(),
attachments:[{filename:"rec.pdf",size_kb:160}]
}
])

db.feedback.insertOne({
student_id:11,
course_code:"CS102",
semester:"2022-ODD",
rating:4,
comments:"Good DBMS course",
tags:["database","sql"],
submitted_at:new Date()
})

db.feedback.countDocuments()

//Task 2 (CRUD Operations)

db.feedback.find({
rating:5
})

db.feedback.find({
course_code:"CS101",
tags:"challenging"
})

db.feedback.find(
{},
{
student_id:1,
course_code:1,
rating:1,
_id:0
}
)

db.feedback.updateMany(
{
rating:{$lt:3}
},
{
$set:{needs_review:true}
}
)

db.feedback.updateMany(
{
needs_review:true
},
{
$push:{tags:"reviewed"}
}
)

db.feedback.deleteMany({
semester:"2021-EVEN"
})

//TASK 3

db.feedback.aggregate([
{
$match:{semester:"2022-ODD"}
},
{
$group:{
_id:"$course_code",
avg_rating:{$avg:"$rating"},
feedback_count:{$sum:1}
}
},
{
$sort:{avg_rating:-1}
}
])

db.feedback.aggregate([
{
$match:{semester:"2022-ODD"}
},
{
$group:{
_id:"$course_code",
avg_rating:{$avg:"$rating"},
feedback_count:{$sum:1}
}
},
{
$project:{
course_code:"$_id",
average_rating:{
$round:["$avg_rating",1]
},
feedback_count:1,
_id:0
}
},
{
$sort:{average_rating:-1}
}
])

db.feedback.aggregate([
{
$unwind:"$tags"
},
{
$group:{
_id:"$tags",
count:{$sum:1}
}
},
{
$sort:{count:-1}
}
])

db.feedback.createIndex({
course_code:1
})

db.feedback.getIndexes()

