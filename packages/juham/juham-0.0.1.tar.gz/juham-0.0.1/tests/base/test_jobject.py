import unittest
from juham.base.jobject import JObject

class JObjectTest(unittest.TestCase):

    def test_constructor(self):
        ok = False
        try:
            object = JObject('foo')
            self.assertNotNull(object)
        except Exception:
            ok = True

        self.assertTrue(ok)
    
    def test_get_classid(self):
        classid = JObject.get_class_id()
        self.assertEqual('JObject', classid)
        

if __name__ == '__main__':
    unittest.main()
