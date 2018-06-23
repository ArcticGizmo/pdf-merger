"""
This module is for helping with everything pdf
"""

from PyPDF2 import PdfFileMerger, PdfFileReader


def merge_all(filenames, output_path):
    """
    Merges all the passed pdf files and outputs them to the output path

    Args:
        :param filenames: a list of file paths to pdfs in the order to be merged
        :type filenames: list[str]
    """
    # merge all pdf files
    merger = PdfFileMerger()
    for filename in filenames:
        #TODO add page numbers here
        merger.append(PdfFileReader(open(filename, 'rb')))

    # merge all pdf files
    merger.write(output_path)



