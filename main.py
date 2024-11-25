from analyze import ask_match, ask_advice

if __name__ == "__main__":
    convo = open("example_convo.txt", "r").read()
    result = ask_match(convo)
    print(result.explanation)
    print("\n\n\n\n")
    print(result)

    print("\n\n\nTips\n")
    result = ask_advice([convo])
    print(result.explanation)