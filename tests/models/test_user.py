import unittest
from models.user import User
import uuid
from models.engine.mysqldb_config import MysqlConfig

class TestUser(unittest.TestCase):
    def setUp(self):
        self.mysql = MysqlConfig()
        self.mysql.reload()
        self.session = self.mysql.get_session()

    def tearDown(self) -> None:
        self.mysql.close()

    def test_user(self):    
       user = User()
       user.id = uuid.uuid4()
       user.email = "kabiba@bib.com"
       user.phone = "345345"
       user.password = "bibia"
       user.role = "user"
       self.mysql.new(user)
       self.mysql.save()

        # fetch added user
       existin_user = self.mysql.find_one(User, condition=User.email == 'kabiba@bib.com')
       print(existin_user)
    #    self.session.close()

       self.assertIsNotNone(existin_user)
       self.assertEqual(existin_user.email, 'kabiba@bib.com')
       self.assertEqual(existin_user.phone, '345345')
       self.assertEqual(user.role, 'user')
if __name__ == '__main__':
    unittest.main()