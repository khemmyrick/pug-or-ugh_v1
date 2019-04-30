def get_age_range(letter):
    """Takes a str and returns a tuple for desired age range."""
    if all(s in letter for s in ("b", "s")):
        return (1, 97)
    elif all(s in letter for s in ("b", "a")):
        return (1, 38)
    elif all(s in letter for s in ("y", "s")):
        return (13, 97)
    elif all(s in letter for s in ("b", "y")):
        return (1, 26)
    elif all(s in letter for s in ("y", "a")):
        return (13, 38)
    elif all(s in letter for s in ("a", "s")):
        return (25, 97)
    elif 'b' in letter:
        return (1, 13)
    elif 'y' in letter:
        return (13, 26)
    elif 'a' in letter:
        return (25, 38)
    else:
        return (37, 97)
