from analyze import ask_match

if __name__ == "__main__":
    convo = open("example_convo.txt", "r").read()
    result = ask_match(convo)
    print(result.explanation)
    print("\n\n\n\n")
    print(result)