from pylord.app import PyLordApp
from auth import STATIC_TOKEN, TokenMiddleware, login_required, on_exception
from storage import BookStorage

app = PyLordApp()

book_storage = BookStorage()
book_storage.create(name="Sherlock Holms", author="Arthur Conan Doyle")
app.add_middleware(TokenMiddleware)
app.add_exception_handler(on_exception)


@app.route("/", allowed_methods=["get"])
def index(req, resp):
    resp.text = "hello world"


@app.route("/index")
def work_with_templates(req, resp):
    books = book_storage.all()
    resp.html = app.template("index.html", context={"books": books})


@app.route("/login", allowed_methods=["post"])
def login(req, resp):
    resp.json = {"token": STATIC_TOKEN}


@app.route("/create", allowed_methods=["post"])
@login_required
def create(req, resp):
    book = book_storage.create(**req.POST)

    resp.status_code = 201
    resp.json = book._asdict()


@app.route("/delete/{id:d}", allowed_methods=["delete"])
@login_required
def delete(req, resp, id):
    book_storage.delete(id)

    resp.status_code = 204


@app.route("/get/{id}")
def get_book(req, resp, id):
    if id in book_storage.books:
        resp.status_code = 200
        book_storage.get(id)


    else:
        resp.text = "bunday kitob yo'q"
        resp.status_code = 404






