import pytest

from fe.access.new_seller import register_new_seller
from fe.access import book
from fe.access.search import Search
from fe import conf
import uuid


class TestQueryBook:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        # do before test
        self.seller_id = "test_query_books_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_query_books_store_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        self.seller = register_new_seller(self.seller_id, self.password)

        code = self.seller.create_store(self.store_id)
        assert code == 200
        book_db = book.BookDB()
        self.books = book_db.get_book_info(0, 2)
        self.search = Search(conf.URL)
        yield
        # do after test

    def test_ok(self):
        for b in self.books:
            code = self.seller.add_book(self.store_id, 0, b)
            assert code == 200
        for b in self.books:
            code , result = self.search.query_book(store_id = self.store_id, id = b.id)
            assert code == 200
            assert result != None and len(result) == 1
    
    def test_book_not_exist(self):
        for b in self.books:
            code = self.seller.add_book(self.store_id, 0, b)
            assert code == 200
        
        for b in self.books:
            code , result = self.search.query_book(store_id = self.store_id+'x', id = b.id)
            assert code == 200
            assert result != None and len(result) == 0


