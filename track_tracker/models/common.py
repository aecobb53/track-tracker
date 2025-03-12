
def apply_modifier(query, db_obj_cls, string):
    if string.startswith('Is exactly'):
        return query.filter(db_obj_cls == string[10:])
    elif string.startswith('Greater than or equal to'):
        return query.filter(db_obj_cls >= string[24:])
    elif string.startswith('Greater than'):
        return query.filter(db_obj_cls > string[12:])
    elif string.startswith('Less than or equal to'):
        return query.filter(db_obj_cls <= string[21:])
    elif string.startswith('Less than'):
        return query.filter(db_obj_cls < string[9:])
    elif string.startswith('Is not'):
        return query.filter(db_obj_cls != string[6:])
    else:
        return query.filter(db_obj_cls == string)

