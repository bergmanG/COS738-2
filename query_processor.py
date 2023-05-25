import os
import logging as log
import xml.etree.cElementTree as ET

logger = log.getLogger('QueryProcessor')

def load_config(config_path):
    logger.info('Reading config file')
    for line in open(config_path, 'r'):
        line = line.strip()
        if line.split('=')[0] == 'LEIA':
            leia_file = line.split('=')[1]
        elif line.split('=')[0] == 'CONSULTAS':
            consultas_file = line.split('=')[1]
        elif line.split('=')[0] == 'ESPERADOS':
            esperados_file = line.split('=')[1]
        else:
            logger.error(f'Unexepected config field {line}')
            return False

    if leia_file and consultas_file and esperados_file:
        logger.info('Finished Reading config file')
        return (leia_file, consultas_file, esperados_file)
    else:
        logger.error(f'Error reading configuration files' +
                      'LEIA: {leia_field} CONSULTAS:{consultas_field} ESPERADOS: {esperados_field}')

def read_xml(leia_file): 
    logger.info('Reading xml')
    tree = ET.parse(leia_file)
    root = tree.getroot()
    if not root:
        logger.error('Failed Reading xml')

    queries = []
    for QUERY in root.findall('QUERY'):
        query_number = int(QUERY.find('QueryNumber').text)
        query_text = ' '.join(QUERY.find('QueryText').text.split()).upper()
        query_results = int(QUERY.find('Results').text)
        query_records = {item.text: item.get('score') for item in QUERY.iter('Item')}
        queries.append((query_number,query_text,query_results,query_records))
    logger.info('Finished reading xml')
    return queries

def create_queries_file(consultas_file, queries):
    logger.info('Creating Consultas.csv')
    with open(consultas_file, 'w') as file:
        file.write('QueryNumber;QueryText\n')
        for ix,query in enumerate(queries):
            file.write(f'{ix};{query[1]}\n')
    logger.info('Fineshed creating Consultas.csv')

def create_expected_file(esperados_file, queries):
    logger.info('Creating Esperados.csv')
    with open(esperados_file, 'w') as file:
        file.write('QueryNumber;DocNumber;DocVotes\n')
        for query in queries:
            for doc,votes in query[3].items():
                file.write(f'{query[0]};{doc};{sum([int(v) for v in votes])}\n')
    logger.info('Fineshed creating Esperados.csv')

logger.info(f'Starting {__file__}')

leia_file, consultas_file, esperados_file = load_config('PC.CFG')
queries = read_xml(leia_file)
create_queries_file(consultas_file, queries)
create_expected_file(esperados_file, queries)

logger.info(f'Finished {__file__}')