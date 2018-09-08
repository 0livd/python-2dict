# SERIALIZE_KEYWORD is the name of the class variable that a class should implement to be considered serializable.
# It is a list of the arguments to serialize.
SERIALIZE_KEYWORD = "TO_SERIALIZE"


class ToDictMixin:
    """
    Will serialize all attributes that are specified in the TO_SERIALIZE class variable.
    If an attribute has a TO_SERIALIZE class attribute, it will also be serialized.
    Lists and dictionnaries attributes are handled. Sets and tuples are turned into lists.
    """

    def to_dict(self, to_serialize=None):
        if to_serialize is None:
            to_serialize = getattr(self, SERIALIZE_KEYWORD, [])
        output_dict = {}
        for attr in to_serialize:
            attr_to_serialize = getattr(self, attr)
            if hasattr(attr_to_serialize, SERIALIZE_KEYWORD):
                attr_to_serialize = attr_to_serialize.to_dict()
            elif isinstance(attr_to_serialize, (list, set, tuple)):
                final_attr = []
                for a in attr_to_serialize:
                    if hasattr(a, SERIALIZE_KEYWORD):
                        a = a.to_dict()
                    final_attr.append(a)
                attr_to_serialize = final_attr
            elif isinstance(attr_to_serialize, dict):
                final_attr = {}
                for k, v in attr_to_serialize.items():
                    if hasattr(v, SERIALIZE_KEYWORD):
                        v = v.to_dict()
                    final_attr[k] = v
                attr_to_serialize = final_attr
            output_dict[attr] = attr_to_serialize
        return output_dict


class FromDictMixin:
    """
    Create an object from a dictionnary of attributes and object attributes.
    All attributes listed in the TO_SERIALIZE class attribute are restored.
    If an attribute has a TO_SERIALIZE class attribute, the from_dict method of this attribute will be called.
    """

    @classmethod
    def from_dict(cls, input_dict, to_serialize=None):
        if to_serialize is None:
            to_serialize = getattr(cls, SERIALIZE_KEYWORD, [])
        out_obj = cls()
        for attr in to_serialize:
            input_attr = input_dict.get(attr)
            if not input_attr:
                continue
            sub_attr = getattr(out_obj, attr)
            if hasattr(sub_attr, SERIALIZE_KEYWORD):
                sub_attr.from_dict(input_attr)
            elif isinstance(sub_attr, list):
                final_attr = []
                for i, a in enumerate(sub_attr):
                    if hasattr(a, SERIALIZE_KEYWORD):
                        a = a.from_dict(input_attr[i])
                    final_attr.append(a)
                sub_attr = final_attr
            elif isinstance(sub_attr, dict):
                final_attr = {}
                for k, v in sub_attr.items():
                    if hasattr(v, SERIALIZE_KEYWORD):
                        v = v.from_dict(input_attr[k])
                    final_attr[k] = v
                sub_attr = final_attr
            else:
                setattr(out_obj, attr, input_attr)
        return out_obj
