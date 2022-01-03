import re

import pandas as pd

df = pd.read_hdf("./artifacts/preprocessor.hdf", "df")
templates = df["query_template"]
templates = pd.DataFrame(list(set(templates)), columns=["query_template"])
matches = templates["query_template"].str.extract(
    "(.*)(?:where)(.*)", flags=re.IGNORECASE
)
matches.dropna(inplace=True)
matches.rename(columns={0: "from", 1: "where"}, inplace=True)
matches["from"] = (
    matches["from"]
    .str.strip()
    .str.replace(r"(,|=|\(|\))", " ", regex=True)
    .str.split(" ")
    .apply(set)
)
matches["where"] = (
    matches["where"]
    .str.strip()
    .str.replace(r"(,|=|\(|\))", " ", regex=True)
    .str.split(" ")
    .apply(set)
)
print(matches)
tables = {}

# TODO(WAN): How do you aggregate with set merge in pandas?
keywords = [
    "",
    "AND",
    "FOR",
    "UPDATE",
    "ORDER",
    "BY",
    "LIKE",
    "<>",
    "ASC",
    "DESC",
    "LIMIT",
    "SET",
    "SELECT",
    "DELETE",
    "INSERT",
    "FROM",
    "OR",
    "AS",
    "<",
    ">",
    "<=",
    ">=",
    "!~",
    "=",
    "+",
    "-",
    "*",
    "/",
]


def filter(col):
    if col.startswith("$") or col.startswith("pg_"):
        return False
    return col.upper() not in keywords


for idx, row in matches.iterrows():
    for table in row["from"]:
        if not filter(table):
            continue

        columns = tables.get(table, set())
        candidates = set(col for col in row["where"] if filter(col))
        columns.update(candidates)
        tables[table] = columns

breakpoint()
