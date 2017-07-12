def audit_country(tag):
    errs = []
    if tag['value'] != 'CZ':
        errs = ['wrong country']

    return errs