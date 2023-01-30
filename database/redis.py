import redis

rdb = redis.StrictRedis()


def add_relation(relation: str, subject_id: int, item_id: int, unique: bool = False) -> bool:
    if unique:
        return rdb.set(f"{relation}:{subject_id}", item_id) == 1
    return rdb.sadd(f"{relation}:{subject_id}", item_id) == 1


def rem_relation(relation: str, subject_id: int, item_id: int, unique: bool = False) -> bool:
    if unique:
        return rdb.delete(f"{relation}:{subject_id}") == 1
    return rdb.srem(f"{relation}:{subject_id}", item_id) == 1


def get_relation(relation: str, subject_id: int, unique: bool = False) -> set:
    if unique:
        return rdb.get(f"{relation}:{subject_id}")
    return rdb.smembers(f"{relation}:{subject_id}")


def delete_regex(reg_expression: str) -> int:
    count: int = 0
    for key in rdb.scan_iter(reg_expression):
        rdb.delete(key)
        count += 1
    return count


def relation_to_dict(rel_name: str):
    rel_dict: dict = dict()
    rel_dict["users"] = set()
    rel_dict["items"] = set()
    rel_dict["relations"] = dict()
    for key in rdb.scan_iter(f"{rel_name}*"):
        user_id = int(str(key).split(':')[1][:-1])
        item_set: set = set(map(int, rdb.smembers(key)))
        rel_dict["users"].add(user_id)
        rel_dict["items"].update(item_set)
        rel_dict["relations"].update({user_id: item_set})
    return rel_dict
