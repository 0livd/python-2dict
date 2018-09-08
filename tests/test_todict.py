import os
from unittest import TestCase

from todict.mixins import ToDictMixin, FromDictMixin


class Serializable(ToDictMixin, FromDictMixin):
    TO_SERIALIZE = ["attr1", "attr2", "obj_attr"]

    def __init__(self):
        self.attr1 = "attr1_init_data"
        self.attr2 = "attr2_init_data"
        self.obj_attr = Serializable2("attr_test_init_data")
        self.no_serialize = "no_serialize"


class SerializableNestedList(Serializable, ToDictMixin, FromDictMixin):
    def __init__(self):
        super().__init__()
        self.attr1 = ["attr1_data", Serializable2("nested_list")]


class SerializableNestedDict(Serializable, ToDictMixin, FromDictMixin):
    def __init__(self):
        super().__init__()
        self.attr1 = {"sub_attr1": Serializable2("nested_dict"), "sub_attr2": 2}


class Serializable2(ToDictMixin, FromDictMixin):
    TO_SERIALIZE = ["attr_test"]

    def __init__(self, attr_test):
        self.attr_test = attr_test


class TestToDictMixin(TestCase):
    def test_to_dict(self):
        obj = Serializable()
        to_dict = obj.to_dict()
        self.assertEqual(
            to_dict,
            {
                "attr1": "attr1_init_data",
                "attr2": "attr2_init_data",
                "obj_attr": {"attr_test": "attr_test_init_data"},
            },
        )

    def test_to_dict_to_serialize(self):
        obj = Serializable()
        to_dict = obj.to_dict(to_serialize=["attr1", "attr2"])
        self.assertEqual(
            to_dict, {"attr1": "attr1_init_data", "attr2": "attr2_init_data"}
        )

    def test_nested_list_to_dict(self):
        obj = SerializableNestedList()
        to_dict = obj.to_dict()
        self.assertEqual(
            to_dict,
            {
                "attr1": ["attr1_data", {"attr_test": "nested_list"}],
                "attr2": "attr2_init_data",
                "obj_attr": {"attr_test": "attr_test_init_data"},
            },
        )

    def test_nested_tuple_to_dict(self):
        obj = SerializableNestedList()
        obj.attr1 = ("attr1_data", Serializable2("nested_tuple"))
        to_dict = obj.to_dict()
        self.assertEqual(
            to_dict,
            {
                "attr1": ["attr1_data", {"attr_test": "nested_tuple"}],
                "attr2": "attr2_init_data",
                "obj_attr": {"attr_test": "attr_test_init_data"},
            },
        )

    def test_nested_set_to_dict(self):
        obj = SerializableNestedList()
        obj.attr1 = {"attr1_data", Serializable2("nested_set")}
        to_dict = obj.to_dict()
        self.assertEqual(to_dict["attr2"], "attr2_init_data")
        self.assertEqual(to_dict["obj_attr"], {"attr_test": "attr_test_init_data"})
        self.assertIn("attr1_data", to_dict["attr1"])
        self.assertIn({"attr_test": "nested_set"}, to_dict["attr1"])

    def test_nested_dict_to_dict(self):
        obj = SerializableNestedDict()
        to_dict = obj.to_dict()
        self.assertEqual(
            to_dict,
            {
                "attr1": {"sub_attr1": {"attr_test": "nested_dict"}, "sub_attr2": 2},
                "attr2": "attr2_init_data",
                "obj_attr": {"attr_test": "attr_test_init_data"},
            },
        )


class TestFromDictMixin(TestCase):
    def test_from_dict(self):
        from_dict = {
            "attr1": "attr1_data",
            "attr2": "attr2_data",
            "obj_attr": {"attr_test": "attr_test_data"},
        }
        obj = Serializable.from_dict(from_dict)
        self.assertEqual(obj.attr1, from_dict["attr1"])
        self.assertEqual(obj.attr2, from_dict["attr2"])
        self.assertEqual(obj.obj_attr.attr_test, "attr_test_data")

    def test_from_dict_to_serialize(self):
        from_dict = {
            "attr1": "attr1_data",
            "attr2": "attr2_data",
            "obj_attr": {"attr_test": "attr_test_data"},
        }
        obj = Serializable.from_dict(from_dict, to_serialize=["attr1", "attr2"])
        self.assertEqual(obj.attr1, from_dict["attr1"])
        self.assertEqual(obj.attr2, from_dict["attr2"])
        self.assertEqual(obj.obj_attr.attr_test, "attr_test_init_data")

    def test_nested_list_from_dict(self):
        from_dict = {
            "attr1": ["attr1_data", {"attr_test": "nested_list"}],
            "attr2": "attr2_init_data",
            "obj_attr": {"attr_test": "attr_test_init_data"},
        }
        obj = SerializableNestedList.from_dict(from_dict)
        self.assertEqual(obj.attr1[0], from_dict["attr1"][0])
        self.assertEqual(obj.attr1[1].attr_test, from_dict["attr1"][1]["attr_test"])
        self.assertEqual(obj.attr2, from_dict["attr2"])
        self.assertEqual(obj.obj_attr.attr_test, from_dict["obj_attr"]["attr_test"])

    def test_nested_dict_from_dict(self):
        from_dict = {
            "attr1": {"sub_attr1": {"attr_test": "nested_dict"}, "sub_attr2": 2},
            "attr2": "attr2_init_data",
            "obj_attr": {"attr_test": "attr_test_init_data"},
        }
        obj = SerializableNestedDict.from_dict(from_dict)
        self.assertEqual(
            obj.attr1["sub_attr1"].attr_test,
            from_dict["attr1"]["sub_attr1"]["attr_test"],
        )
        self.assertEqual(obj.attr1["sub_attr2"], from_dict["attr1"]["sub_attr2"])
        self.assertEqual(obj.attr2, from_dict["attr2"])
        self.assertEqual(obj.obj_attr.attr_test, from_dict["obj_attr"]["attr_test"])

    def test_from_bad_dict(self):
        from_dict = {"bad1": "baaaaad", "bad2": "baaaaad"}
        obj = Serializable.from_dict(from_dict)
        self.assertEqual(obj.attr1, "attr1_init_data")
        self.assertEqual(obj.attr2, "attr2_init_data")
        self.assertEqual(obj.obj_attr.attr_test, "attr_test_init_data")
