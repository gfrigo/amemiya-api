from pypika import Table
from functools import reduce
from operator import and_

def assemble_individual_condition(label, specs):
    element_type = specs.get("type")
    element_value = specs.get("value")
    element_table = Table(specs.get("table"))

    if element_type == "index":
        return getattr(element_table, label) == element_value

    elif element_type == "date_range":
        start, end = element_value
        return getattr(element_table, label).between(start, end)


def assemble_condition(query_filter: dict):
    conditions = []

    for k, v in query_filter.items():
        stmt = assemble_individual_condition(k, v)

        if stmt is not None:
            conditions.append(stmt)

    if not conditions:
        return None

    return reduce(and_, conditions)

