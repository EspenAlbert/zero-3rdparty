from dataclasses import dataclass

from zero_3rdparty.dataclass_utils import as_dict, copy_dataclass, field_names, values


@dataclass
class MyTestClass:
    name: str
    age: int
    fictive: bool = True


def test_field_names():
    instance = MyTestClass(name="Espen", age=99)
    assert field_names(instance) == ["name", "age", "fictive"]
    assert field_names(MyTestClass) == ["name", "age", "fictive"]


def test_values():
    instance = MyTestClass(name="espen", age=99)
    assert values(instance) == ["espen", 99, True]


def test_copy_dataclass(subtests):
    instance = MyTestClass(name="name1", age=1, fictive=False)
    with subtests.test("copy no update"):
        instance2 = copy_dataclass(instance)
        assert instance == instance2
    with subtests.test("copy with update"):
        instance3 = copy_dataclass(instance, update={"fictive": True})
        assert instance3.fictive
    with subtests.test("copy with exclude"):
        instance4 = copy_dataclass(instance, exclude={"fictive"})
        assert instance4.fictive
    with subtests.test("copy with update and exclude"):
        instance5 = copy_dataclass(instance, update={"age": 2}, exclude=["fictive"])
        assert instance5 == MyTestClass(name="name1", age=2)


def test_as_dict(subtests):
    instance = MyTestClass("name2", 22)
    with subtests.test("no filter"):
        assert as_dict(instance) == {"name": "name2", "age": 22, "fictive": True}
    with subtests.test("with filter"):

        def skip_age(field_name: str) -> bool:
            return field_name != "age"

        assert as_dict(instance, filter=skip_age) == {
            "fictive": True,
            "name": "name2",
        }
