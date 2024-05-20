import os
import sys
import re
import datetime
import subprocess
import difflib

import ipynbname
import numpy as np


def _rolling_sum(data, window):
    """Calculate the rolling sum for a given window"""
    
    return np.convolve(data, np.ones(window, dtype=int), 'valid')


def _flatten(xss):
    """Flatten a list."""

    return [x for xs in xss for x in xs]


def _bolg(filepaths, minOrphanCharacters=2):
    """
    Approximate inverse of `glob.glob`: take a sequence of `filepaths`
    and compute a glob pattern that matches them all. Only the star
    character will be used (no question marks or square brackets).

    Define an "orphan" substring as a sequence of characters, not
    including a file separator, that is sandwiched between two stars.   
    Orphan substrings shorter than `minOrphanCharacters` will be
    reduced to a star. If you don't mind having short orphan
    substrings in your result, set `minOrphanCharacters=1` or 0.
    Then you might get ugly results like '*0*2*.txt' (which contains
    two orphan substrings, both of length 1).
    
    Source: https://stackoverflow.com/questions/43808808/inverse-glob-reverse-engineer-a-wildcard-string-from-file-names
    """
    if os.path.sep == '\\':
        # On Windows, convert to forward-slashes (Python can handle
        # it, and Windows doesn't permit them in filenames anyway):
        filepaths = [filepath.replace('\\', '/') for filepath in filepaths]
    out = ''
    for filepath in filepaths:
        if not out: out = filepath; continue
        # Replace differing characters with stars:
        out = ''.join(x[-1] if x[0] == ' ' or x[-1] == '/' else '*' for x in difflib.ndiff(out, filepath))
        # Collapse multiple consecutive stars into one:
        out = re.sub(r'\*+', '*', out)
    # Deal with short orphan substrings:
    if minOrphanCharacters > 1:
        pattern = r'\*+[^/]{0,%d}\*+' % (minOrphanCharacters - 1)
        while True:
            reduced = re.sub(pattern, '*', out)
            if reduced == out: break
            out = reduced
    # Collapse any intermediate-directory globbing into a double-star:
    out = re.sub(r'(^|/).*\*.*/', r'\1**/', out)

    return out


def _insert_wildcards(input_arg_list, prefix):
    """Use wildcards to abbrevate consecutive command line args that have a common prefix (e.g. file paths)"""
    
    output_arg_list = input_arg_list.copy()
    max_consecutive_matches = 999
    while max_consecutive_matches > 1:
        prefix_matches = [prefix in arg for arg in output_arg_list]
        consecutive_matches = _rolling_sum(prefix_matches, window=2)
        max_consecutive_matches = np.max(consecutive_matches)
        if max_consecutive_matches > 1:            
            start_index = consecutive_matches.tolist().index(2)
            end_index = start_index
            while prefix_matches[end_index]:
                end_index += 1
                if end_index == len(output_arg_list):
                    break
            wildcard = _bolg(output_arg_list[start_index:end_index])
            del output_arg_list[start_index:end_index]
            output_arg_list.insert(start_index, wildcard)
    
    return output_arg_list


def _isnotebook():
    try:
        ipynbname.name()
        return True
    except FileNotFoundError:
        return False


def _get_current_entry(code_url='', wildcard_prefixes=[]):
    """Create a record of the current command line entry.
    
    Kwargs:
      code_url (str):            Where to find the code online
                                 (e.g. https://github.com/... or https://doi.org/...)
      wildcard_prexifes (list):  Use wildcards to abbreviate consecutive command
                                 arguments with these common prefixes (e.g. a file path)
                                
    Returns:
      str. Latest command line record
    
    """

    time_stamp = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
    if _isnotebook():
        exe = subprocess.run(['which', 'jupyter'], stdout=subprocess.PIPE)
        exe = exe.stdout.decode('utf-8').replace('\n','')
        args_list = ['notebook', str(ipynbname.path())]
    else:
        exe = sys.executable
        args_list = sys.argv
    
    for prefix in wildcard_prefixes:
        args_list = _insert_wildcards(args_list, prefix)
    
    args = " ".join(args_list)
    entry = f"{time_stamp}: {exe} {args}"
    if code_url:
        entry = entry + f" ({code_url})"
            
    return entry

    
def new_log(infile_logs={}, extra_notes=[], code_url='', wildcard_prefixes=[]):
    """Create a new command log/history.
    
    Kwargs:
      infile_logs (dict):        Keys are input file names
                                 Values are the logs for those files 
      extra_notes (list):        Extra information to include in new log
                                 (output is one list item per line)
      code_url (str):            Where to find the code online
                                 (e.g. https://github.com/... or https://doi.org/...) 
      wildcard_prexifes (list):  Use wildcards to abbreviate consecutive command
                                 arguments with these common prefixes (e.g. a file path)
      
    Returns:
      str. Command log
      
    """
    
    log = _get_current_entry(code_url=code_url, wildcard_prefixes=wildcard_prefixes)
    
    if extra_notes:
        assert isinstance(extra_notes, (list, tuple)), \
        "extra_notes must be a list/tuple: output is one list/tuple item per line"
        log += '\nExtra notes: '
        for line in extra_notes:
            log += '\n' + line 
    
    if infile_logs:
        assert isinstance(infile_logs, dict), \
        "infile_logs must be a dict: file names as keys and logs as values"
        nfiles = len(list(infile_logs.keys()))
        for fname, history in infile_logs.items():
            if nfiles > 1:
                log += f"\nHistory of {fname}: \n {history}"
            else:
                log += f"\n{history}"
    
    return log


def read_log(fname):
    """Read a log file.
    
    Args:
      fname (str):  Name of log file
      
    Returns:
      str. Command log
    
    """
   
    log_file = open(fname, 'r')
    log = log_file.read()
    
    return log

    
def write_log(fname, cmd_log):
    """Write an updated command log/history to a text file.
    
    Args:
      fname (str):    Name of output file
      cmd_log (str):  Command line log produced by new_log()
    
    """
   
    log_file = open(fname, 'w')
    log_file.write(cmd_log) 
    log_file.close()