#!/usr/bin/env python3
"""Filter and sanitize a bibtex file for an article:
* Remove all uncited entries,
* Remove all annotations and comments.
"""
import sys
import argparse
import os
from pybtex.database import BibliographyData
from pybtex.database.input import bibtex as bibtex_input
from pybtex.database.output import bibtex as bibtex_output
from time import strptime
from collections import OrderedDict
import re


class Parser(bibtex_input.Parser):
    """Override the default implementation to do some preprocessing"""
    def parse_stream(self, stream):
        self.unnamed_entry_counter = 1
        text = stream.read()
        text = text.replace(r'\o ','ø')
        self.command_start = 0

        entry_iterator = bibtex_input.BibTeXEntryIterator(
            text,
            keyless_entries=self.keyless_entries,
            handle_error=self.handle_error,
            want_entry=self.data.want_entry,
            filename=self.filename,
            macros=self.macros,
        )
        for entry in entry_iterator:
            entry_type = entry[0]
            if entry_type == 'string':
                pass
            elif entry_type == 'preamble':
                self.process_preamble(*entry[1])
            else:
                self.process_entry(entry_type, *entry[1])
        return self.data



def parse_aux(args):
    wanted = set()
    with open(args.input_aux) as f:
        for line in f:
            line = line.strip()
            m = re.match(r'^\\citation\{([a-zA-Z0-9-.]+)\}$', line)
            if m:
                wanted.add(m.group(1))
    return wanted


def input_bibtex_filenames(args):
    # In order: later files take precedence.
    filenames = []
    if args.input_bibtex_directory:
        for bibfile in os.listdir(args.input_bibtex_directory):
            if args.include_reading_group or not bibfile.startswith('Reading group'):
                filenames.append(os.path.join(args.input_bibtex_directory, bibfile))
    if args.input_bibtex:
        filenames.append(args.input_bibtex)
    return filenames


def parse_bibtex(args, wanted):
    if wanted != None:
        bibs = BibliographyData(wanted_entries=wanted)
    else:# Because Ubuntu/Debian doesn't have a new enough pybtex for wanted_entries
        bibs = BibliographyData()
    parser = Parser()
    for filename in input_bibtex_filenames(args):
        filebibs = parser.parse_file(filename)
        bibs.add_entries(iter(filebibs.entries.items()))
    # Sort the entries to ensure a consistent ordering of the output so that adding
    # one new citation doesn't alter the whole file
    bibs.entries = OrderedDict(sorted(bibs.entries.items(),key=lambda x : x[0]))
    return bibs


def delete_notes(bibs):
    for entry in bibs.entries.values():
        if 'annote' in entry.fields:
            del entry.fields['annote']


def make_online(bibs):
     """Mendeley does not support @online entries but biblatex does
        So if an entry is @misc and has a url then make it @online
     """
     for entry in bibs.entries.values():
         if (entry.type == 'misc' and 'url' in entry.fields):
             entry.type = 'online'


def fix_months(bibs):
    """The 'month' field must be specified as a numeric value not as say 'May'
    """
    for entry in bibs.entries.values():
        if 'month' in entry.fields:
            month = entry.fields['month']
            if not month.isdigit():
                try:  # Try month full name and then abbreviation
                    month = str(strptime(month,'%B').tm_mon)
                except ValueError:
                    month = str(strptime(month,'%b').tm_mon)
                entry.fields['month'] = month


def fix_doi(bibs):
    """Some DOIs contain _s and mendeley escapes them with \ but this is
    unnecessary.
    """
    for entry in bibs.entries.values():
        if 'doi' in entry.fields:
            # If not present, does nothing.
            entry.fields['doi'] = entry.fields['doi'].replace(r'{\_}', '_')
            entry.fields['doi'] = entry.fields['doi'].replace(r'\_', '_')

def fix_url(bibs):
    """Some URLs contain _s and mendeley escapes them with \ but this is
    unnecessary. Fortunately \ is an invalid character in a URL.
    """
    for entry in bibs.entries.values():
        if 'url' in entry.fields:
            # If not present, does nothing.
            entry.fields['url'] = entry.fields['url'].replace(r'{\_}', '_')
            entry.fields['url'] = entry.fields['url'].replace(r'\_', '_')
            entry.fields['url'] = entry.fields['url'].replace(r'{\&}', '&')
            if ' http' in entry.fields['url']:
                entry.fields['url'] = entry.fields['url'].replace(' http', '| http')


def sort_fields(bibs):
    """Sort the fields and preserve the ordering so that they don't jiggle around"""
    for entry in bibs.entries.values():
        entry.persons = OrderedDict(sorted(entry.persons.items(), key=lambda x : x[0]))
        entry.fields = OrderedDict(sorted(entry.fields.items(), key=lambda x : x[0]))


def write_output(args, bibs):
    writer = bibtex_output.Writer()
    writer.write_file(bibs, args.output_bibtex)


def main(args):
    if args.input_aux:
        wanted = parse_aux(args)
        print('Looking for {} citations: {}'.format(len(wanted), ', '.join(sorted(wanted))), file=sys.stderr)
    else:
        wanted = None # This means wanted = All
        print('Keeping all citations as --input-aux not specified', file=sys.stderr)
    bibs = parse_bibtex(args, wanted)
    delete_notes(bibs)
    make_online(bibs)
    fix_months(bibs)
    fix_doi(bibs)
    fix_url(bibs)
    sort_fields(bibs)
    write_output(args, bibs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-bibtex-directory', help='Directory with .bib files generated by Mendeley.')
    parser.add_argument('--input-bibtex', help='A single .bib file generated by Mendeley.')
    parser.add_argument('--include-reading-group', action='store_true', help='Include files generated by Reading Group in Mendeley.')
    parser.add_argument('--input-aux', help='Latex .aux file of the article (it contains required citations).')
    parser.add_argument('--output-bibtex', help='Output file where to write filtered entries.', required=True)
    args = parser.parse_args()

    if not args.input_bibtex_directory and not args.input_bibtex:
        parser.error('Either --input-bibtex or --input-bibtex-directory (or both) is required.')

    if ((args.input_bibtex and args.input_bibtex == args.output_bibtex) or
        (args.input_bibtex_directory and args.output_bibtex.startswith(args.input_bibtex_directory))):
        parser.error('Output file must not be the same as any of the input files.')

    main(args)

