import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analyze import ask_match, ask_advice

if __name__ == "__main__":
    convo = open(f"{os.path.dirname(os.path.abspath(__file__))}/example_convo.txt", "r").read()
    result = ask_match(convo)
    print(result.explanation)
    print("\n\n\n\n")
    print(result)

    print("\n\n\nTips\n")
    result = ask_advice([convo])
    print(result.explanation)
