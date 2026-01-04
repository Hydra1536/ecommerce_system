def dfs_category_tree(category):
    result = {"id": category.id, "name": category.name, "children": []}

    for child in category.children.all():
        result["children"].append(dfs_category_tree(child))

    return result
