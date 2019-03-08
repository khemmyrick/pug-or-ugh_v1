def get_age_range(letter):
    """Takes a str and returns a tuple for desired age range."""
    print("Letter is " + letter)
    if all(s in letter for s in ("b", "s")):
        # check if both letters in letter
        print("Returning all ages.")
        return (1, 97)
    elif all(s in letter for s in ("b", "a")):
        print("Returning babies, youths and adults.")
        return (1, 38)
    elif all(s in letter for s in ("y", "s")):
        print("Returning youths, adults and seniors.")
        return (13, 97)
    elif all(s in letter for s in ("b", "y")):
        print("Returning babies and youths.")
        return (1, 26)
    elif all(s in letter for s in ("y", "a")):
        print("Returning youths and adults.")
        return (13, 38)
    elif all(s in letter for s in ("a", "s")):
        print("Returning adults and seniors.")
        return (25, 97)
    elif 'b' in letter:
        print("Returning babies.")
        return (1, 13)
    elif 'y' in letter:
        print("Returning youth.")
        return (13, 26)
    elif 'a' in letter:
        print("Returning adults.")
        return (25, 38)
    else:
        print("Returning seniors.")
        return (37, 97)
