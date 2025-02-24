
def apply_modifier(query, db_obj_cls, string):
    if string.startswith('is exactly'):
        return query.filter(db_obj_cls == string[1:])
    elif string.startswith('greater than or equal to'):
        return query.filter(db_obj_cls >= string[2:])
    elif string.startswith('greater than'):
        return query.filter(db_obj_cls > string[1:])
    elif string.startswith('less than'):
        return query.filter(db_obj_cls <= string[2:])
    elif string.startswith('less than'):
        return query.filter(db_obj_cls < string[1:])
    elif string.startswith('is not'):
        return query.filter(db_obj_cls != string[2:])
    else:
        return query.filter(db_obj_cls == string)

