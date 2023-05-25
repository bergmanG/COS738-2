import os
import math
import logging as log
import pickle

logger = log.getLogger('Indexer')

def load_config(config_path):
    logger.info('Reading config file')
    for line in open(config_path, 'r'):
        line = line.strip()
        if line.split('=')[0] == 'LEIA':
            leia_file = line.split('=')[1]
        elif line.split('=')[0] == 'ESCREVA':
            escreva_file = line.split('=')[1]
        else:
            logger.error(f'Unexepected config field {line}')
            return False

    if leia_file and escreva_file:
        logger.info('Finished Reading config file')
        return (leia_file, escreva_file)
    else:
        logger.error(f'Error reading configuration files' +
                      'LEIA: {leia_field} ESCREVA:{escreva_file}')


def create_VSM():
    logger.info('Creating Vector Space Model')
    tf = vsm.read_inverse_index_to_tf(f_leia, SEP, MIN_WORD_LENGTH)
    # print(tf)
    # print(len(tf))
    tf_norm = vsm.normalize_tf(tf, norm = 'max', weight = 0.6)
    # pprint(tf_norm)
    # pprint(len(tf_norm))
    logger.info('Evaluating ni...')
    inv_tf = vsm.tf_to_itf(tf)
    ni = {}
    for word in inv_tf:
        ni[word] = len(inv_tf[word])
    # print(ni)
    # print(len(ni))
    logger.info('Evaluated ni for %d terms' % len(ni))
    logger.info('Building idf...')
    idf = {}
    N = len(tf_norm)
    for word in ni:
        idf[word] = math.log(N/ni[word])
    # print(idf)
    # print(len(idf))
    logger.info('idf built for %d terms' % len(idf))
    logger.info('Creating VSM (w_ij) from inverse index at %s...' % f_leia)
    w_ij = {}
    for doc, words in tf_norm.items():
        for word in words:
            if doc not in w_ij:
                w_ij[doc] = {}
            if word not in w_ij[doc]:
                w_ij[doc][word] = {}
            w_ij[doc][word] = tf_norm[doc][word]*idf[word]
    # print(w_ij)
    # print(len(w_ij))
    logger.info('w_ij built with %d corpus.' % len(w_ij))
    logger.info('Creating VSM (tf_idf) from corpora at %s...' % CORPORA_FILE)
    corpora = vsm.get_corpora(CORPORA_FILE, SEP, ENCOD)
    tf_idf = vsm.tf_idf(corpora, mode = 'dense', norm = 'max')
    # print(tf_idf)
    # print(len(tf_idf))
    logger.info('tf_idf built with %d corpus.' % len(tf_idf))
    logger.info('Vector Space Model created!')
    logger.info('Saving VSM (w_ij & tf_idf)')
    pickle_out = open(f_escreva,'wb')
    pickle.dump([w_ij, tf_idf], pickle_out)
    pickle_out.close()
    logger.info(('VSM (w_ij & tf_idf) saved at %s.' % f_escreva))





logger.info(f'Starting {__file__}')



logger.info(f'Finished {__file__}')






logger.info('Creating Vector Space Model...')
tf = vsm.read_inverse_index_to_tf(f_leia, SEP, MIN_WORD_LENGTH)
# print(tf)
# print(len(tf))
tf_norm = vsm.normalize_tf(tf, norm = 'max', weight = 0.6)
# pprint(tf_norm)
# pprint(len(tf_norm))
logger.info('Evaluating ni...')
inv_tf = vsm.tf_to_itf(tf)
ni = {}
for word in inv_tf:
    ni[word] = len(inv_tf[word])
# print(ni)
# print(len(ni))
logger.info('Evaluated ni for %d terms' % len(ni))
logger.info('Building idf...')
idf = {}
N = len(tf_norm)
for word in ni:
    idf[word] = math.log(N/ni[word])
# print(idf)
# print(len(idf))
logger.info('idf built for %d terms' % len(idf))
logger.info('Creating VSM (w_ij) from inverse index at %s...' % f_leia)
w_ij = {}
for doc, words in tf_norm.items():
    for word in words:
        if doc not in w_ij:
            w_ij[doc] = {}
        if word not in w_ij[doc]:
            w_ij[doc][word] = {}
        w_ij[doc][word] = tf_norm[doc][word]*idf[word]
# print(w_ij)
# print(len(w_ij))
logger.info('w_ij built with %d corpus.' % len(w_ij))
logger.info('Creating VSM (tf_idf) from corpora at %s...' % CORPORA_FILE)
corpora = vsm.get_corpora(CORPORA_FILE, SEP, ENCOD)
tf_idf = vsm.tf_idf(corpora, mode = 'dense', norm = 'max')
# print(tf_idf)
# print(len(tf_idf))
logger.info('tf_idf built with %d corpus.' % len(tf_idf))
logger.info('Vector Space Model created!')
logger.info('Saving VSM (w_ij & tf_idf)')
pickle_out = open(f_escreva,'wb')
pickle.dump([w_ij, tf_idf], pickle_out)
pickle_out.close()
logger.info(('VSM (w_ij & tf_idf) saved at %s.' % f_escreva))