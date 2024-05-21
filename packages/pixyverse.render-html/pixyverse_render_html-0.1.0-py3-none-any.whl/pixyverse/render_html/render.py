from typing import Iterable, List

safeKeyNames = {"class_name": "class"}


def map_prop_name(name: str):
    if name in safeKeyNames.keys():
        return safeKeyNames[name]
    return name


id = lambda x: x


def flat_map(f, xs: Iterable):
    ys: List = []
    for x in xs:
        ys.extend(f(x))
    return ys


def underscoreToHyphen(input: str) -> str:
    return input.replace("_", "-")


def create_element(
    elem: str,
    props: dict[str, str] = {},
    children: Iterable[str] | Iterable[Iterable[str]] = [],
):
    render_children = "".join(flat_map(id, children))
    return f"""<{elem}{''.join(f' {underscoreToHyphen(map_prop_name(key))}={value}' for key, value in props.items())}>{render_children}</{elem}>"""
