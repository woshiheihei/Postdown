import json
from .ctor import MDDoc


def get_rows(raw, keys):
    result = list()
    for i in raw:
        result.append([i[k] for k in keys])
    return result


def parse(in_file, out_file):
    doc = MDDoc()

    with open(in_file) as f:
        collection = json.load(f)

    # The basic info.
    doc.title(collection['info']['name'])
    doc.hr()
    doc.line(collection['info']['description'])
    doc.br()
    doc.hr()

    # API
    for api in collection['item']:
        doc.title(api['name'], 2)
        request = api['request']
        doc.code_block('{0[method]} {0[url][raw]}'.format(request))
        doc.block(request['description'])
        doc.hr()

        # Request information.
        doc.title('Request', 3)
        doc.comment_begin()
        doc.bold('Query')
        rows = get_rows(
            request['url']['query'],
            ['key', 'value', 'description']
        )
        doc.table(['Key', 'Value', 'Description'], rows)

        doc.bold('Header')
        rows = get_rows(
            request['header'],
            ['key', 'value', 'description']
        )
        doc.table(['Key', 'Value', 'Description'], rows)

        if request['body']:
            doc.bold('Body')
            if request['body']['mode'] in ['formdata', 'urlencoded']:
                rows = get_rows(
                    request['body'][request['body']['mode']],
                    ['key', 'value', 'type', 'description']
                )
                doc.table(['Key', 'Value', 'Type', 'Description'], rows)
            elif request['body']['mode'] == 'raw':
                doc.code_block(request['body']['raw'])
            elif request['body']['mode'] == 'file':
                doc.text(request['body']['file']['src'])

        doc.comment_end()

        # Response example.
        doc.title('Examples:', 3)
        doc.comment_begin()
        for response in api['response']:
            doc.bold('Example: {0}'.format(response['name']))
            doc.comment_begin()

            # Original Request
            request = response['originalRequest']
            doc.bold('Request')
            doc.comment_begin()
            doc.bold('Query')
            rows = get_rows(
                request['url']['query'],
                ['key', 'value', 'description']
            )
            doc.table(['Key', 'Value', 'Description'], rows)

            doc.bold('Header')
            rows = get_rows(
                request['header'],
                ['key', 'value', 'description']
            )
            doc.table(['Key', 'Value', 'Description'], rows)

            if request['body']:
                doc.bold('Body')
                if request['body']['mode'] in ['formdata', 'urlencoded']:
                    rows = get_rows(
                        request['body'][request['body']['mode']],
                        ['key', 'value', 'type', 'description']
                    )
                    doc.table(['Key', 'Value', 'Type', 'Description'], rows)
                elif request['body']['mode'] == 'raw':
                    doc.code_block(request['body']['raw'])
                elif request['body']['mode'] == 'file':
                    doc.text(request['body']['file']['src'])

            doc.comment_end()

            # Response
            doc.bold('Response')
            doc.comment_begin()
            doc.bold('Header')
            header_rows = [[i['key'], i['value']] for i in response['header']]
            doc.table(['Key', 'Value'], header_rows)
            doc.bold('Body')
            doc.code_block(json.dumps(json.loads(response['body']), indent=2))
            doc.comment_end()

            doc.comment_end()
        doc.comment_end()
        doc.hr()

    with open(out_file, 'w+') as f:
        f.write(doc.output())
