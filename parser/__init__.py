

symbols = {
    '[': 'lbracket',
    ']': 'rbracket',
}

def repo_script_to_token(xs):
    tokens = []

    max_len = len(xs)
    count = 0
    world = []
    sentence = []

    lines = xs.split("\n")

    for line in lines:
        worlds = line.split(" ")
        tokens.append(["name", worlds[0]])
        tokens.append(["link", worlds[1]])
        if len(worlds) < 3:
            tokens.append(["newline"])
            continue
        tokens.append(["hour", worlds[2]])
        tokens.append(["hour", worlds[3]])
        tokens.append(["filename", " ".join(worlds[4:])])

    return tokens


    