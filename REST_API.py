from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studentsinfo.db'
db = SQLAlchemy(app)

class StudentModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200))
	surname = db.Column(db.String(200))
	gender = db.Column(db.String(50))
	id_num = db.Column(db.String(13))
	contact_num = db.Column(db.String(10))
	email_address = db.Column(db.String(300))
	home_address = db.Column(db.String(300))
	course_name = db.Column(db.String(300))

db.create_all()

task_post_args = reqparse.RequestParser()
task_post_args.add_argument('name', type=str, help="Name is required", required=True)
task_post_args.add_argument('surname', type=str, help="Surname is required", required=True)
task_post_args.add_argument('gender', type=str, help="Gender is required", required=True)
task_post_args.add_argument('id_num', type=str, help="ID is required", required=True)
task_post_args.add_argument('contact_num', type=str, help="Contact number is required", required=True)
task_post_args.add_argument('email_address', type=str, help="Email address is required", required=True)
task_post_args.add_argument('home_address', type=str, help="Home address is required", required=True)
task_post_args.add_argument('course_name', type=str, help="Course Name is required", required=True)

task_update_args = reqparse.RequestParser()
task_update_args.add_argument('name', type=str)
task_update_args.add_argument('surname', type=str)
task_update_args.add_argument('gender', type=str)
task_update_args.add_argument('id_num', type=str)
task_update_args.add_argument('contact_num', type=str)
task_update_args.add_argument('email_address', type=str)
task_update_args.add_argument('home_address', type=str)
task_update_args.add_argument('course_name', type=str)

resource_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'surname': fields.String,
	'gender': fields.String,
	'id_num': fields.String,
	'contact_num': fields.String,
	'email_address': fields.String,
	'home_address': fields.String,
	'course_name': fields.String,
}

#Endpoint to Retrieve and list all students
class StudentList(Resource):
	def get(self):
		tasks = StudentModel.query.all()
		students = {}
		for task in tasks:
			students[task.id] = {"name": task.name, 
			"surname": task.surname, 
			"gender": task.gender, 
			"id_num": task.id_num, 
			"contact_num": task.contact_num, 
			"email_address": task.email_address, 
			"home_address": task.home_address,
			"course_name": task.course_name}
		return students


class Student(Resource):
	#Endpoint to Retrieve a student's information
	@marshal_with(resource_fields)
	def get(self, student_id):
		task = StudentModel.query.filter_by(id=student_id).first()
		if not task:
			abort(404, message="Error 404: The student for whom you are searching for, does not exist. Please try again")
		return task

	#Endpoint to Create a new student
	@marshal_with(resource_fields)
	def post(self, student_id):
		args = task_post_args.parse_args()
		task = StudentModel.query.filter_by(id=student_id).first()
		if task:
			abort(409, message="Error 409: This student id aready exists. Please use a new student Id")

		student = StudentModel(id=student_id, 
			name=args['name'], 
			surname=args['surname'], 
			gender=args['gender'], 
			id_num=args['id_num'], 
			contact_num=args['contact_num'], 
			email_address=args['email_address'], 
			home_address=args['home_address'],
			course_name=args['course_name'])

		db.session.add(student)
		db.session.commit()
		return student, 201

	#Endpoint to Edit a particular student's information
	@marshal_with(resource_fields)
	def put(self, student_id):
		args = task_update_args.parse_args()
		task = StudentModel.query.filter_by(id=student_id).first()
		if not task:
			abort(404, message="This field cannot be updated, please enter the correct information")
		if args['name']:
			task.name = args['name']
		if args['surname']:
			task.surname = args['surname']
		if args['gender']:
			task.gender = args['gender']
		if args['id_num']:
			task.id_num = args['id_num']
		if args['contact_num']:
			task.contact_num = args['contact_num']
		if args['email_address']:
			task.email_address = args['email_address']
		if args['home_address']:
			task.home_address = args['home_address']
		if args['course_name']:
			task.course_name = args['course_name']
		db.session.commit()
		return task

	#Endpoint to Delete a student
	def delete(self, student_id):
		task = StudentModel.query.filter_by(id=student_id).first()
		db.session.delete(task)
		db.session.commit()
		return 'Student Deleted', 204


api.add_resource(Student, '/students/<int:student_id>')
api.add_resource(StudentList, '/students')


if __name__ == '__main__':
	app.run(debug=True)