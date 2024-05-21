#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purpose
-------

This module contains functions used to cluster sequences with MMseqs2.

Code documentation
------------------
"""


import subprocess


def create_mmseqs_db(input_file, output_db):
    """Create a MMseqs2 database from a FASTA file.

	Parameters
	----------
	input_file : str
		Path to a FASTA file with DNA sequences.
	output_db : str
		Full path that includes prefix used for
		all database files that are created.

	Returns
	-------
	db_stdout : list
		List with the stdout from MMseqs2 in bytes.
	db_stderr : list
		List with the stderr from MMseqs2 in bytes.
    """
    mmseqs_args = ['mmseqs', 'createdb', input_file, output_db]

    mmseqs_proc = subprocess.Popen(mmseqs_args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

    db_stderr = mmseqs_proc.stderr.readlines()
    db_stdout = mmseqs_proc.stdout.readlines()

    return [db_stdout, db_stderr]


def cluster_baits(database, cluster_db, temp_directory, threads):
    """Cluster sequences in a MMseqs2 database.

    Parameters
    ----------
    database : str
        Full path that includes prefix used for
        database files.
    cluster_db : str
        Full path that includes prefix used for
        files with clustering results.
    temp_directory : str
        Path to te temporary directory used to
        store intermediate files.
    threads : int
        Number of threads used in the clustering
        process.

    Returns
    -------
    stdout : list
        List with the stdout from MMseqs2 in bytes.
    stderr : list
        List with the stderr from MMseqs2 in bytes.
    """
    mmseqs_args = ['mmseqs', 'cluster', '--cov-mode', '0', '-c',
                   '0.8', '--threads', str(threads), database,
                   cluster_db, temp_directory]

    mmseqs_proc = subprocess.Popen(mmseqs_args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

    cluster_stderr = mmseqs_proc.stderr.readlines()
    cluster_stdout = mmseqs_proc.stdout.readlines()

    return [cluster_stdout, cluster_stderr]


def align_clusters(database, cluster_db, align_db, threads):
    """Align sequences in a MMseqs2 database against clustering results.

    Parameters
    ----------
    database : str
        Full path that includes prefix used for
        database files.
    cluster_db : str
        Full path that includes prefix used for
        files with clustering results.
    align_db : str
        Full path that includes prefix used for
        files with alignment results.
    threads : int
        Number of threads used in the clustering
        process.

    Returns
    -------
    List with following elements:
        align_stdout : list
            List with the stdout from MMseqs2 in bytes.
        align_stderr : list
            List with the stderr from MMseqs2 in bytes.
    """
    align_args = ['mmseqs', 'align', '--cov-mode', '0', '-c',
                  '0.8', '--threads', str(threads), database,
                  database, cluster_db, align_db, '-a']

    align_proc = subprocess.Popen(align_args,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)

    align_stderr = align_proc.stderr.readlines()
    align_stdout = align_proc.stdout.readlines()

    return [align_stdout, align_stderr]


def convert_alignmentDB(database, align_db, align_out):
    """Convert a MMseqs2 alignment to tabular format.

    Parameters
    ----------
    database : str
        Full path that includes prefix used for
        database files.
    align_db : str
        Full path that includes prefix used for
        files with alignment results.
    align_out : str
        Path to the output file with the clustering
        results in tabular format.

    Returns
    -------
    List with following elements:
        convert_stdout : list
            List with the stdout from MMseqs2 in bytes.
        convert_stderr : list
            List with the stderr from MMseqs2 in bytes.
    """
    convert_args = ['mmseqs', 'convertalis', database, database,
                    align_db, align_out]

    convert_proc = subprocess.Popen(convert_args,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)

    convert_stderr = convert_proc.stderr.readlines()
    convert_stdout = convert_proc.stdout.readlines()

    return [convert_stdout, convert_stderr]
