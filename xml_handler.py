#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
xml_handler.py

Constants:
    UID_LENGTH (int): The length of the uids generated.
    OBJECT_NAME_LENGTH (int): The length of the object names generated.
    RANDOM_SEED (int): Random seed for results reproductivity.
    DATA_DIR (str): The working directory for zip files.
    NUM_ZIP (int): The number of zip files to create.
    NUM_XML (int): The number of xml files per each zip file.
"""

import multiprocessing as mp
import os
import random
import re
import string
import zipfile

UID_LENGTH = 16
OBJECT_NAME_LENGTH = 16
RANDOM_SEED = 42
DATA_DIR = './'
NUM_ZIP = 50
NUM_XML = 100


def main():
    """
    See README.md for more info.
    """
    random.seed(RANDOM_SEED)
    stage1(DATA_DIR, NUM_ZIP, NUM_XML)
    stage2(DATA_DIR)


def stage1(path='./', num_zip=50, num_xml=100):
    """
    Creates <num_zip> archives, <num_xml> xml files in each

    Args:
        path (str): Working directory.
        num_zip (int): Number of zip files to create.
        num_xml (int): Number of xml in each zip file.
    """
    uids = set()

    while len(uids) < num_zip * num_xml:
        uids.add(make_random_string(UID_LENGTH))
    
    fname_len = len(str(max(num_zip, num_xml)))

    pool = mp.Pool()
    results = []

    for i in range(num_zip):
        results.append(pool.apply_async(make_zip, 
            args=(path + str(i + 1).zfill(fname_len) + '.zip', [uids.pop() for _ in range(num_xml)], fname_len)))
    
    results = [r.get() for r in results]


def make_zip(file_name, uids, fname_len):
    """
    Creates zip archive with xml files inside.

    Args:
        file_name (str): The name of zip file to create.
        uids (list of str): List of uids.
        fname_len (int): Length of name for xml files (w/o ext).
    """
    # TODO: check if we can write to the directory
    with zipfile.ZipFile(file_name, 'w') as fzip:
        for i in range(len(uids)):
            fzip.writestr(str(i + 1).zfill(fname_len) + '.xml', make_xml(uids[i]))


def make_xml(uid):
    """
    Creates xml string according to the specified format.
    
    Args:
        uid (str): The unique string for the id tag.

    Returns:
        str: xml string created.

    Examples:
        <root>
            <var name='id' value='<random unique string value>'/>
            <var name='level' value='<random number within 1..100>'/>
            <objects>
                <object name='<random string value>'/>
                <object name='<random string value>'/>
                    The objects tag containts random number (within 1..10) of object tags.
            </objects>
        </root>
    """
    xml = ['<root>\n']
    xml.append('\t<var name=\'id\' value=\'{}\'/>\n'.format(uid))
    xml.append('\t<var name=\'level\' value=\'{}\'/>\n'.format(random.randint(1, 100)))
    xml.append('\t<objects>\n')

    for _ in range(random.randint(1, 10)):
        xml.append('\t\t<object name=\'{}\'/>\n'.format(make_random_string(OBJECT_NAME_LENGTH)))
   
    xml.append('\t</objects>\n</root>\n')

    return ''.join(xml)


def make_random_string(length):
    """
    Generates a random string.

    Args:
        length (int): Length of the string.

    Returns:
        str: The string generated.    
    """
    return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(length))


def stage2(path='./'):
    """
    Processes zip files and creates 2 csv files. For more info read README.md, please.
    
    Args:
        path (str): The working directory with zip archives.

    Examples:
        1.csv header line: 'id, level'
        2.csv header line: 'id, object_name'
    """

    regexes = [
        re.compile(r'<var name=\'id\' value=\'([^\']*)\'/>'),
        re.compile(r'<var name=\'level\' value=\'([^\']*)\'/>'),
        re.compile(r'<object name=\'([^\']*)\'/>')
        ]

    pool = mp.Pool()
    results = []

    for file_name in os.listdir(path):
        if file_name.endswith('.zip'):
            results.append(pool.apply_async(parse_zip, args=(path + file_name, regexes)))

    # TODO: check if we can write to the directory
    with open('1.csv', 'w') as fcsv:
        fcsv.write(''.join(['id, level\n'] + [r.get()[0] for r in results]))

    with open('2.csv', 'w') as fcsv:
        fcsv.write(''.join(['id, object_name\n'] + [r.get()[1] for r in results]))        


def parse_zip(file_name, regexes):
    """
    Parses zip file and returns 2 blocks of csv data.

    Args:
        file_name (str): The name of zip file to parse.
        regexes (list of RegexObject): 3 compiled regex objects.

    Returns:
        list of str: 2 blocks of csv data.
    """
    csv1, csv2 = [], []
    fzip = zipfile.ZipFile(file_name, 'r')
    # TODO: check if the zip file exists

    for file_name in fzip.namelist():
        if file_name.endswith('.xml'):
            xml = str(fzip.read(file_name))
            # TODO: check if xml has correct structure
            try:
                uid = regexes[0].findall(xml)[0]
                csv1.append('{}, {}\n'.format(uid, regexes[1].findall(xml)[0]))
                csv2.append(uid + ', ' + ('\n' + uid + ', ').join(regexes[2].findall(xml)) + '\n')
            except:
                pass
    return ''.join(csv1), ''.join(csv2)


if __name__ == '__main__':
    main()
