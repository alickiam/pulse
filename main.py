from heartrate import HeartRateManager

def run():
    hr = HeartRateManager()
    print("Press enter to read temp", end="")
    try:
        while True:
            input()
            print(f"0: {hr.read_temp(0)}, 1: {hr.read_temp(1)}", end="")
    except KeyboardInterrupt:
        pass
    print()
    hr.stop()

if __name__ == "__main__":
    run()

