import os
import platform
import string
import subprocess


def sanitize_string(string_to_sanitize):
    """
    Sanitize a string to prevent SQL injections

    Arguments:
    string_to_sanitize      - the string that has to be sanitized

    Returns:
    A sanitized string
    """
    # TODO: A whitelist approach has to be added
    # something like, the string is good only when it contains
    # ASCII characters + digits after the removal of punctuation
    for i in string.punctuation:
        string_to_sanitize = string_to_sanitize.replace(i, '')
    return string_to_sanitize


def open_non_text_file(filename):
    """
    Open a non-text file
    """
    if platform.system() == 'Darwin':
        subprocess.call(('open', filename))
    elif platform.system() == 'Windows':
        os.startfile(filename)
    else:
        subprocess.call(('xdg-open', filename))


def get_os():
    """
    Get Operating System of current machine as a string.
    """
    if platform.system() == 'Darwin':
        return "macos"
    if platform.system() == 'Windows':
        return "windows"
    else:
        return "linux"
