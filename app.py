
# WHEN RUNNING, IT'S IN JSON!
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask, jsonify, request,redirect
import json
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)


db = SQLAlchemy(app)
 
class book(db.Model):
    __tablename__ = "books"
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    author = db.Column(db.String())
    year_published = db.Column(db.String()) #might need to change to interger
    _type = db.Column("type",db.Integer())
 
    def __init__(self, name,author,year_published,_type):
        self.name = name
        self.author = author
        self.year_published = year_published
        self._type = _type

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "author": self.author,
            "year_published": self.year_published,
            "_type": self._type 
        }  

class customer(db.Model):
    __tablename__ = "customers"
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    city = db.Column(db.String(80))
    age = db.Column(db.Integer())
    
 
    def __init__(self, name,city,age):
        self.name = name
        self.city = city
        self.age = age

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'age': self.age,
        }
    
class loan(db.Model):
    __tablename__ = "loans"
 
    id = db.Column(db.Integer, primary_key=True)
    custid = db.Column(db.Integer())
    bookid = db.Column(db.Integer())
    loandate = db.Column(db.Integer())
    returndate = db.Column(db.Integer()) 
    
    #loandate- 1/2/3
    # if 1 --> up to 10 days   
    # if 2 --> up to 5 days
    # if 3 --> up to 2 days
    def __init__(self, custid,bookid,loandate,returndate):
        self.custid = custid
        self.bookid = bookid
        self.loandate = loandate
        self.returndate = returndate







@app.route("/")
def menu():
    return "this is where the menu will be"


#----------CUSTOMERS SECTION----------
@app.route("/customers/view")
def view_customer_S():
    customers_list = [customers.to_dict() for customers in customer.query.all()]
    customers_as_json_data = json.dumps(customers_list)
    return customers_as_json_data

@app.route("/customers/view/<id>")
def view_customer(id):
    this_customer = customer.query.get(id)
    customer_to_dict = this_customer.to_dict()
    return jsonify(customer_to_dict)
    


@app.route('/customers/new', methods=['POST'])
def new_customer():
    data = request.get_json()
    name = data['name']
    city = data['city']
    age = data['age']

    new_customer = customer(name, city, age)
    db.session.add(new_customer)
    db.session.commit()
    return "A new customer was added."

@app.route("/customers/del/<id>", methods=['DELETE'])
def delete_customer(id):
    customer_id = db.get_or_404(customer, id)
    print(customer_id)
    db.session.delete(customer_id)
    db.session.commit()
    return "customer deleted."


# #all of the above work as intneded
# #NEED TO FIX!!!!
# @app.route("/update/<id>", methods=['PUT','GET'])
# def upd_customer(id):
#     our_customer = customer.query.get(id)
#     data = request.get_json()
#     our_customer.name = data["name"]
#     our_customer.city = data["city"]
#     our_customer.age = data["age"]
#     db.session.commit()
#     return "made it"

    

    # user_dict = user.to_dict()
    # user_json = jsonify(user_dict)
    # print(user_json)
    # Print(user_json["id"])
    # user_json["name"] = "TOOOOOOOTMM"
    # user_json["city"] = "TIITDGDFHDH"
    # user_json["age"] = 999
#----------CUSTOMERS END----------



#----------BOOKS SECTION----------
@app.route("/books/view")
def view_book_S():
    books_list = [books.to_dict() for books in book.query.all()]
    books_as_json_data = json.dumps(books_list)
    print(books_list)
    return books_as_json_data

@app.route("/books/view/<id>")
def view_book(id):
    this_book = book.query.get(id)
    book_to_dict = this_book.to_dict()
    return jsonify(book_to_dict)
    


@app.route('/books/new', methods=['POST'])
def new_book():
    data = request.get_json()
    name = data['name']
    author = data['author']
    year_published = data['year_published']
    _type = data["book_loan"]

    new_book = book(name, author, year_published, _type)
    db.session.add(new_book)
    db.session.commit()
    return "A new book was added."

@app.route("/books/del/<id>", methods=['DELETE'])
def delete_book(id):
    book_id = db.get_or_404(book, id)
    print(book_id)
    db.session.delete(book_id)
    db.session.commit()
    return "book deleted."
#----------BOOKS END----------


#all of the above work as intneded
#NEED TO FIX!!!!
# @app.route("/update/<id>", methods=['PUT','GET'])
# def upd_customer(id):
#     our_customer = customer.query.get(id)
#     data = request.get_json()
#     our_customer.name = data["name"]
#     our_customer.city = data["city"]
#     our_customer.age = data["age"]
#     db.session.commit()
#     return "made it"
    




if __name__ == "__main__":

    with app.app_context():
        db.create_all()
        # results = db.session.query(customer).join(book)
        # for result in results:
        #     print(result)

        
    app.run(debug=True)

