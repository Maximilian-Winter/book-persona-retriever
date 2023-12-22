from math import ceil


def chunk_into_n(lst, n):
    size = ceil(len(lst) / n)
    return list(
      map(lambda x: lst[x * size:x * size + size],
      list(range(n)))
    )


def filter_whitespaces(terms):
    return [term.strip() for term in terms if term.strip()]
