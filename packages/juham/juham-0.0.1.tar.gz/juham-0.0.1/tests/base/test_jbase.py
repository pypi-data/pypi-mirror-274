import unittest
from juham.base.jobject import JObject
from juham.base.jbase import JBase

class JBaseTest(unittest.TestCase):

    def test_constructor(self):
        ok = False
        try:
            object = JBase('base')
            self.assertNotNull(object)
        except Exception:
            ok = True

        self.assertTrue(ok)
    
    def test_get_classid(self):
        classid = JBase.get_class_id()
        self.assertEqual('JBase', classid)
        

if __name__ == '__main__':
    unittest.main()
