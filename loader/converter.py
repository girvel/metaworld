def convert(convertee, path, conversion, expected_type=None):
    return _convert(
        convertee,
        path.split('.'),
        lambda x:
            conversion(x)
            if expected_type is None or isinstance(x, expected_type)
            else x
    )


def _convert(convertee, path, conversion):
    match path:
        case ['*']:
            assert isinstance(convertee, dict | list), \
                "Can iterate only through dict or list, sorry."

            for key, value in (
                convertee.items()
                if isinstance(convertee, dict)
                else enumerate(convertee)
            ):
                convertee[key] = conversion(value)

        case [head]:
            assert not isinstance(head, list)
            if head in convertee:
                convertee[head] = conversion(convertee[head])

        case ['*', *tail]:
            assert isinstance(convertee, dict | list), \
                "Can iterate only through dict or list, sorry."

            for value in (
                convertee.values()
                if isinstance(convertee, dict)
                else convertee
            ):
                _convert(value, tail, conversion)

        case [head, *tail]:
            assert not isinstance(head, list)
            if head in convertee:
                _convert(convertee[head], tail, conversion)