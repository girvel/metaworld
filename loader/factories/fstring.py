def fstring(source):
    return eval(f'rf"""{source}"""')

fstring.implicit_resolver =  r".*{.*"
