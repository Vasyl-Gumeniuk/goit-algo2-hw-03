import csv
import timeit
from typing import List, Dict, Tuple
from BTrees.OOBTree import OOBTree


def load_data(file_path: str) -> List[Dict[str, str]]:
    """
    Функція завантажує дані з CSV файлу.
    """
    data = []
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["ID"] = int(row["ID"])
            row["Price"] = float(row["Price"])
            data.append(row)
    return data


def add_item_to_tree(tree: OOBTree, item: Dict[str, str]) -> None:
    """
    Додає товар у OOBTree.
    """
    tree[item["ID"]] = {
        "Name": item["Name"],
        "Category": item["Category"],
        "Price": item["Price"]
    }


def add_item_to_dict(dictionary: Dict[int, Dict[str, str]], item: Dict[str, str]) -> None:
    """
    Додає товар у словник dict.
    """
    dictionary[item["ID"]] = {
        "Name": item["Name"],
        "Category": item["Category"],
        "Price": item["Price"]
    }


def range_query_tree(tree: OOBTree, min_price: float, max_price: float) -> List[Tuple[int, Dict[str, str]]]:
    """
    Виконує діапазонний запит у OOBTree.
    """
    return list(tree.items(min=min_price, max=max_price))


def range_query_dict(dictionary: Dict[int, Dict[str, str]], min_price: float, max_price: float) -> List[Tuple[int, Dict[str, str]]]:
    """
    Виконує діапазонний запит у стандартному словнику dict.
    """
    return [item for item in dictionary.items() if min_price <= item[1]["Price"] <= max_price]


if __name__ == "__main__":
    # Завантаження даних з файлу
    file_path = "data/generated_items_data.csv"
    items = load_data(file_path)

    # Ініціалізація структур даних
    tree = OOBTree()
    dictionary = {}

    # Додавання даних у структури
    for item in items:
        add_item_to_tree(tree, item)
        add_item_to_dict(dictionary, item)

    # Параметри для діапазонного запиту
    min_price = 10.0
    max_price = 100.0

    # Вимірювання часу для OOBTree
    tree_time = timeit.timeit(lambda: range_query_tree(tree, min_price, max_price), number=100)

    # Вимірювання часу для dict
    dict_time = timeit.timeit(lambda: range_query_dict(dictionary, min_price, max_price), number=100)

    # Вивід результатів
    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")