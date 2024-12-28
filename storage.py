from models import Book


class BookStorage:
    id = 0

    def __init__(self):
        self.books = []

    def all(self):
        return [book._asdict() for book in self.books]

    def get(self, id):
        for book in self.books:
            if book.id == id:
                return book

        return None

    def delete(self, id):
        for ind, book in enumerate(self.books):
            if book.id == id:
                del self.books[ind]

    def create(self, **kwargs):
        self.id += 1
        kwargs['id'] = self.id
        book = Book(**kwargs)
        self.books.append(book)
        return book

    def put(self, id, **kwargs):
        book = self.get(id)  # Find the book by ID

        if book:
            index = self.books.index(book)

            updated_book = book._replace(**kwargs)
            self.books[index] = updated_book

            return updated_book

        return None
