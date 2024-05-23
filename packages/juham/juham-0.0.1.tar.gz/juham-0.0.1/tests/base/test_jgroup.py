import unittest
from juham.base.jobject import JObject
from juham.base.jgroup import JGroup

class JGroupTest(unittest.TestCase):

    def test_constructor(self):
        ok = False
        try:
            object = JGroup('group')
            self.assertNotNull(object)
        except Exception:
            ok = True

        self.assertTrue(ok)
    
    def test_get_classid(self):
        classid = JGroup.get_class_id()
        self.assertEqual('JGroup', classid)
        
    def test_add(self):
        group = JGroup('parent')
        child = JObject('child')
        group.add(child)
        self.assertEqual(1, len(group.children))
        

if __name__ == '__main__':
    unittest.main()
