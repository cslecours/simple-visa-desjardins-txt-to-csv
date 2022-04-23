def extract_transactions(file: str):
    with open(file, 'r', encoding='UTF-8') as content:
        lines = content.read()

    transactions = lines.split('Détail des transactions du mois courant\n\n')[
        1].split('\n\n')[0].split('\n')
    transactions = transactions[2:-1]

    id_start: str = file.split('_')[1].split('.')[0]

    transactions = [transform_line(
        line, id_start) for line in transactions]

    return transactions

def transform_line(line: str, id_start: str):
    transformed_line = line

    transformed_line = transformed_line[:57]+'\t\t' + \
        transformed_line[57:70]+'\t\t\t\t'+transformed_line[70:]
    transformed_line = transformed_line.replace('\t\t', '\t')
    transformed_line = transformed_line.replace('\t\t', '\t')

    transformed_cells = transformed_line.split('\t')

    transformed_cells = [cell.strip() for cell in transformed_cells]

    transformed_cells[0] = transform_date(transformed_cells[0])
    transformed_cells[1] = transform_date(transformed_cells[1])

    metadata = extract_metadata(transformed_cells, id_start)

    return metadata


def extract_metadata(cells: list, id_start: str):

    return dict({
        "@id": "%s_%s" % (id_start, cells[2]),
        "transaction_date": cells[0],
        "inscription_date": cells[1],
        "transaction_number": cells[2],
        "description": cells[3],
        "city": cells[4],
        "province": cells[5],
        "amount": float(cells[6].replace(',', '.').replace('CR ','-')),
    })



def transform_date(d: str):
    dateParts = d.split(' ')
    dateParts[1] = transform_month(dateParts[1])
    return '-'.join(reversed(dateParts))


def transform_month(month: str):
    map = {
        'JAN': '01',
        'FÉV': '02',
        'MAR': '03',
        'AVR': '04',
        'MAI': '05',
        'JUN': '06',
        'JUI': '07',
        'AOÛ': '08',
        'SEP': '09',
        'OCT': '10',
        'NOV': '11',
        'DÉC': '12'
    }
    return map[month]
