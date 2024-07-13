from flask_security import auth_required, current_user, roles_required
from application.models import db,Section,User ,  Book, UserBook, Role
from flask_restful import Api, Resource, fields, marshal, reqparse
from application.cache_instance import cache
from datetime import  datetime,timedelta
from flask import jsonify, Response
import matplotlib.pyplot as plt
from sqlalchemy import not_
import io

api = Api(prefix="/api")

parser_section = reqparse.RequestParser()
parser_section.add_argument('name', type=str,
                    help='Section Name is Required', required=True)
parser_section.add_argument('date', type=str,
                    help='Section Created Date is Required')
parser_section.add_argument('description', type=str,
                    help='Section Description is Required', required=True)

section_field = {
    'section_id': fields.Integer,
    'name':   fields.String,
    'date': fields.DateTime(dt_format='iso8601'),
    'description':  fields.String,
}

class Username(Resource):
    @auth_required("token")
    def get(self):
        return jsonify({"User": current_user.username})

class SectionResource(Resource):
    @auth_required("token")
    @roles_required("librarian")
    @cache.cached(timeout=50, key_prefix='Section_Caching')
    def get(self):
        sec = Section.query.all()
        return marshal(sec, section_field)
    
    @auth_required("token")
    @roles_required("librarian")
    def post(self):
        args = parser_section.parse_args()
        section = Section(name=args.get("name"), description=args.get(
            "description"))
        sec = Section.query.filter_by(name=args.get("name")).all()
        if len(sec)==0:
           db.session.add(section)
           db.session.commit()
           cache.delete('Section_Caching')
           return {"message": "Section Created"},200
        return {"message": "Section Already Exist."}, 404
    
    @auth_required("token")
    @roles_required("librarian")
    def put(self, section_id):
        args = parser_section.parse_args()
        section = Section.query.filter_by(section_id=section_id).first()
        if section:
            section.name = args.get("name")
            section.description = args.get("description")
            db.session.commit()
            cache.delete('Section_Caching')
            return {"message": "Section Updated"}, 200
        return {"message": "Section not found."}, 404

    @auth_required("token")
    @roles_required("librarian")
    def delete(self, section_id):
        section = Section.query.filter_by(section_id=section_id).first()
        if section:
            for book in section.books:
                user_book = UserBook.query.filter_by(book_id = book.book_id).all()
                if user_book:
                    for b in user_book:
                        db.session.delete(b)
                db.session.delete(book)
            db.session.delete(section)
            db.session.commit()
            cache.delete('Section_Caching')
            return {"message": "Section and related books Deleted"}, 200
        return {"message": "Section not found."}, 404


parser_book = reqparse.RequestParser()
parser_book.add_argument('name', type=str,
                    help='Book Name is Required', required=True)
parser_book.add_argument('author', type=str,
                    help='Book\'s Author  is Required', required=True)
parser_book.add_argument('content', type=str,
                    help='Book Content is Required', required=True)
parser_book.add_argument('pages', type=int,
                    help='Book Pages is Required', required=True)

book_field_full = {
    'book_id': fields.Integer,
    'name':    fields.String,
    'pages':   fields.Integer,
    'author' : fields.String,
    'content': fields.String,
    'section': fields.String,
    'section_name': fields.String(attribute=lambda b: b.section.name)
}

book_field = {
    'book_id': fields.Integer,
    'name':    fields.String,
    'author' : fields.String,
    'rated' : fields.Integer,
    'section_name': fields.String(attribute=lambda b: b.section.name),
}


class BookResource(Resource):
    @auth_required("token")
    def get(self,section_id= None, book_id=None):
        if section_id:
            book = Book.query.filter_by(section_id=section_id).all()
            return marshal(book, book_field_full)
        elif book_id:
            book = Book.query.filter_by(book_id= book_id).first()
            return marshal(book, book_field_full)
        else:
            book = Book.query.filter(
            not_(Book.books.any(user_id=current_user.id))
        ).all()

        return marshal(book, book_field)
    
    @auth_required("token")
    @roles_required("librarian")
    def post(self,section_id):
        args = parser_book.parse_args()
        existing_book = Book.query.filter_by(name=args.get("name")).first()
        sec = Section.query.filter_by(section_id=section_id).first()
        if existing_book:
            return {"message": "Book Already Exist."}, 404
        book = Book(
            name=args.get("name"),
            author=args.get("author"),
            content=args.get("content"),
            pages=args.get("pages"),
            section=sec
        )
        db.session.add(book)
        db.session.commit()
        return {"message": "Book Created"},200
    
    @auth_required("token")
    @roles_required("librarian")
    def put(self, book_id):
        args = parser_book.parse_args()
        book = Book.query.filter_by(book_id=book_id).first()
        if book:
            book.name = args.get("name")
            book.author=args.get("author")
            book.content=args.get("content")
            book.pages=args.get("pages")
            db.session.commit()
            return {"message": "Book Updated"}, 200
        return {"message": "Book not found."}, 404

    @auth_required("token")
    @roles_required("librarian")
    def delete(self, book_id):
        book = Book.query.filter_by(book_id=book_id).first()
        user_book = UserBook.query.filter_by(book_id = book_id).all()
        if book:
            if user_book:
                for b in user_book:
                    db.session.delete(b)
            db.session.delete(book)
            db.session.commit()
            return {"message": "Book Deleted"}, 200
        return {"message": "Book not found."}, 404

parser_user_book = reqparse.RequestParser()
parser_user_book.add_argument('issued_date', type=str,
                    help='Issued date is parameter')
parser_user_book.add_argument('return_date', type=str,
                    help='Return date is parameter')
parser_user_book.add_argument('book_status', type=str,
                    help='Book status is Required', required=True)
parser_user_book.add_argument('days', type=int,
                    help='Number of Days is Required')
parser_user_book.add_argument('rate', type=int,
                    help='Please Give Feedback')

user_book_field = {
    'book_id': fields.Integer,
    'user_id': fields.Integer,
    'book_status': fields.Integer,
    'days': fields.Integer,
    'return_date': fields.DateTime(dt_format='iso8601'),
    'book_name': fields.String(attribute=lambda b: b.book.name),
    'author': fields.String(attribute=lambda b: b.book.author),
    'user_name': fields.String(attribute=lambda b: b.user.username),
    'section_name': fields.String(attribute=lambda b: b.book.section.name)
}
user_book_completed_field = {
    'book_id': fields.Integer,
    'user_id': fields.Integer,
    'book_status': fields.Integer,
    'days': fields.Integer,
    'rate': fields.Integer,
    'issued_date': fields.DateTime(dt_format='iso8601'),
    'return_date': fields.DateTime(dt_format='iso8601'),
    'book_name': fields.String(attribute=lambda b: b.book.name),
    'author': fields.String(attribute=lambda b: b.book.author),
    'user_name': fields.String(attribute=lambda b: b.user.username),
    'section_name': fields.String(attribute=lambda b: b.book.section.name)

}
        
class UserBookResource(Resource):
    @auth_required("token")
    def get(self,user_id=None, book_status=None):
        status = {"Requested":1, "Granted":2, "Revoked":3, "Completed":4 }
        if user_id or current_user.roles[0].name=='user':
            user = current_user
            book = UserBook.query.filter_by(user_id = user.id,book_status = status[book_status] ).all()
            
            if book_status == 'Completed':
                return marshal(book, user_book_completed_field)
        else:
            book = UserBook.query.all()
        return marshal(book, user_book_completed_field)
    
    @auth_required("token")
    def post(self, book_id):
        args = parser_user_book.parse_args()
        user = current_user
        books = UserBook.query.filter_by(user_id = user.id).all()
        if len(books)>= 5:
            return {"message": "Your request limit for books has been exceeded."},404
        book = Book.query.filter_by(book_id=book_id).first()
        user_book = UserBook(
            user_id=user.id,
            book_id=book.book_id,
            days = args.get("days"),
            issued_date=args.get("issued_date"),
            return_date=args.get("return_date"),
            book_status=args.get("book_status"),
        )
        db.session.add(user_book)
        db.session.commit()
        return {"message": "Book Status Changed"},200
    
    @auth_required("token")
    # @roles_required("librarian")
    def put(self,user_id, book_id):
        args = parser_user_book.parse_args()
        user = User.query.filter_by(id=user_id).first()
        book = Book.query.filter_by(book_id=book_id).first()
        userbook = UserBook.query.filter_by(user_id = user.id, book_id=book.book_id).first()

        if userbook:
            userbook.issued_date=datetime.now().date()
            if args.get("book_status") == '4':
                userbook.return_date = datetime.now().date()
                rate = args.get("rate")
                if book.rated:
                    book.rated = (rate+book.rated)/2
                else:
                    book.rated = rate
            elif args.get("book_status") == '3':
                userbook.return_date = datetime.now().date()
            elif args.get("book_status") == '2':
                userbook.return_date = datetime.now().date() + timedelta(days=userbook.days)
            userbook.book_status=args.get("book_status")
            userbook.rate=args.get("rate")
            db.session.commit()
            return {"message": "User-Book Status Changed"}, 200
        return {"message": "User-Book not found."}, 404
    
    @auth_required("token")
    @roles_required("librarian")
    def delete(self,user_id, book_id):
        user = User.query.filter_by(id=user_id).first()
        book = Book.query.filter_by(book_id=book_id).first()
        userbook = UserBook.query.filter_by(user_id = user.id, book_id=book.book_id).first()
        if userbook:
            db.session.delete(userbook)
            db.session.commit()
            return {"message": "User-Book Rejected"}, 200
        return {"message": "User-Book not found."}, 404



class Stats(Resource):
    @auth_required("token")
    @roles_required("librarian")
    @cache.cached(timeout=10)
    def get(self):
        n_users = User.query.join(User.roles).filter(Role.name == 'user').all()
        n_book = Book.query.all()
        n_sec = Section.query.all()
            
        return jsonify({"users": len(n_users), "books":len(n_book), "sections":len(n_sec)})

class UserStats(Resource):
    @auth_required("token")
    @roles_required("user")
    @cache.cached(timeout=10)
    def get(self):
        user = current_user
        c_book = UserBook.query.filter_by(user_id = user.id, book_status = 2).all()
        cmpt_book = UserBook.query.filter_by(user_id = user.id, book_status = 4).all()
            
        return jsonify({"c_book": len(c_book), "cmpt_book":len(cmpt_book)})


class Dist(Resource):
    @auth_required("token")
    @roles_required("librarian")
    @cache.cached(timeout=10)
    def get(self):
        n_sec = Section.query.all()
        book_dist = {}
        for sec in n_sec:
            books = Book.query.filter_by(section_id = sec.section_id).all()
            book_dist[sec.name]= len(books)
            
        books = Book.query.order_by(Book.rated.desc()).all()
        top_book = {}
        for book in books:
            if book.rated:
             top_book[book.name]= book.rated
        
        x = list(top_book.keys())
        y = list(top_book.values())
                
        labels = list(book_dist.keys())
        sizes = list(book_dist.values())
        
        
        fig, ax = plt.subplots(2, figsize=(8, 8))
        ax[0].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax[0].axis('equal') 
        ax[0].set_title("Books Distribution section wise", color='green')
        
        ax[1].bar(x, y, color='blue', width=0.4)
        ax[1].set_xlabel("Book Name")  
        ax[1].set_ylabel("Rating") 
        ax[1].set_title("Top Rated Books", color='green')
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        
      
        response = Response(img_buffer.read())
        response.headers['Content-Type'] = 'image/png'
        return response
 
class UserDist(Resource):
    @auth_required("token")
    @roles_required("user")
    @cache.cached(timeout=10)
    def get(self):
        user = current_user
        user_books = UserBook.query.filter_by(user_id = user.id).all()
        book_dist = {}
        for user_book in user_books:
            book = Book.query.filter_by(book_id = user_book.book_id).first()
            if book and book.section:
                section_name = book.section.name
                book_dist[section_name] = book_dist.get(section_name, 0) + 1
         
        
        books = UserBook.query.filter_by(user_id=user.id).order_by(UserBook.rate.desc()).all()
        top_book = {}
        for book in books:
            if book.rate:
             top_book[book.book.name]= book.rate
        
        x = list(top_book.keys())
        y = list(top_book.values())
        labels = list(book_dist.keys())
        sizes = list(book_dist.values())
        

        fig, ax = plt.subplots(2, figsize=(8, 8))
        ax[0].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax[0].axis('equal') 
        ax[0].set_title("Your Books Distribution section wise", color='green')
        
        ax[1].bar(x, y, color='blue', width=0.4)
        ax[1].set_xlabel("Book Name")  
        ax[1].set_ylabel("Rating") 
        ax[1].set_title("Top Favorite Books", color='green')
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        
      
        response = Response(img_buffer.read())
        response.headers['Content-Type'] = 'image/png'
        return response


api.add_resource(Username,'/current_profile')
api.add_resource(Stats,'/stats')
api.add_resource(UserStats,'/userstats')
api.add_resource(Dist,'/dist')
api.add_resource(UserDist,'/userdist')
api.add_resource(BookResource,'/book','/book/<int:book_id>' ,'/book_section/<int:section_id>')
api.add_resource(SectionResource, '/section','/section/<int:section_id>')
api.add_resource(UserBookResource,'/user_book' ,'/user_book/<int:book_id>','/user_book/<int:user_id>/<int:book_id>','/user_book/<string:book_status>')