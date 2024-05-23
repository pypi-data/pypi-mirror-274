from io import StringIO


def yaml_to_str(p):
    from convocations.base.utils import yaml_serializer
    y = yaml_serializer()
    buff = StringIO()
    y.dump(p, buff)
    buff.seek(0)
    return buff.getvalue()
