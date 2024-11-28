from heartrate import HeartRateManager, BeatFinder
import analyze
import pulsedb
import matching

import pigpio
import matplotlib.pyplot as plt
import time
import traceback
import subprocess
import signal
from random import random

# Enable drawing red LED data
RED_PLOT_EN = False
# Enable drawing IR LED data
SPO2_PLOT_EN = True
# Enable drawing heartbeat detection data
BEAT_PLOT_EN = False

xs = [[] for i in range(HeartRateManager.NUM_SENSORS)]
cs = [0 for i in range(HeartRateManager.NUM_SENSORS)]
ys = [[[], [], []] for i in range(HeartRateManager.NUM_SENSORS)]
axs = [[None, None, None] for i in range(HeartRateManager.NUM_SENSORS)]
lines = [[None, None, None] for i in range(HeartRateManager.NUM_SENSORS)]
(fig, a) = plt.subplots(1, HeartRateManager.NUM_SENSORS)
for i in range(HeartRateManager.NUM_SENSORS):
    axs[i][0] = a[i]
    axs[i][0].set_xlabel("time (s)")
    axs[i][0].set_ylabel("red")
    (lines[i][0],) = axs[i][0].plot(xs[i], ys[i][0], "-r")
    axs[i][1] = axs[i][0].twinx()
    axs[i][1].set_ylabel("SpO2")
    (lines[i][1],) = axs[i][1].plot(xs[i], ys[i][1], "-b")
    axs[i][2] = axs[i][0].twinx()
    axs[i][2].set_ylabel("beat")
    (lines[i][2],) = axs[i][2].plot(xs[i], ys[i][2], "-g")
fig.tight_layout()

beat_times = [[] for i in range(HeartRateManager.NUM_SENSORS)]
beat_lines = [[] for i in range(HeartRateManager.NUM_SENSORS)]
beat_finders = [BeatFinder() for i in range(HeartRateManager.NUM_SENSORS)]

def run():
    while True:
        try:
            hr = HeartRateManager()
            break
        except pigpio.error as e:
            print(e)
            continue

    audio_filename = f"pulse-{time.time()}.wav"
    print(f"Starting recording {audio_filename}")
    record_process = subprocess.Popen(f"exec ssh pi@pulse.local arecord -D dmic_sv -c2 -r 48000 -f S32_LE -t wav -V mono -v {audio_filename}", stdout=subprocess.PIPE, shell=True)

    try:
        while True:
            for sensor_num in range(HeartRateManager.NUM_SENSORS):
                # Get data
                try:
                    (count, data1, data2) = hr.read_hr(sensor_num)
                except pigpio.error:
                    continue
                if count <= 0:
                    continue

                # Update lists
                for i in range(count):
                    xs[sensor_num].append(cs[sensor_num] / 50)
                    ys[sensor_num][0].append(data1[i])
                    ys[sensor_num][1].append(data2[i])

                    # Add heartbeat detection lines
                    if beat_finders[sensor_num].check_for_beat(data2[i]):
                        beat_times[sensor_num].append(cs[sensor_num] / 50)
                        beat_lines[sensor_num].append(axs[sensor_num][1].axvline(cs[sensor_num] / 50, color="black"))
                    ys[sensor_num][2].append(beat_finders[sensor_num].get_cur())

                    cs[sensor_num] += 1

                # Prune old data
                if len(xs[sensor_num]) > 2 * 50:
                    xs[sensor_num] = xs[sensor_num][-2 * 50:]
                    ys[sensor_num][0] = ys[sensor_num][0][-2 * 50:]
                    ys[sensor_num][1] = ys[sensor_num][1][-2 * 50:]
                    ys[sensor_num][2] = ys[sensor_num][2][-2 * 50:]
                # Prune old heartbeat lines
                for line in beat_lines[sensor_num]:
                    if line.get_xdata()[0] < cs[sensor_num] / 50 - 2:
                        line.remove()
                        beat_lines[sensor_num].remove(line)

                # Update plots
                if RED_PLOT_EN:
                    lines[sensor_num][0].set_data(xs[sensor_num], ys[sensor_num][0])
                if SPO2_PLOT_EN:
                    lines[sensor_num][1].set_data(xs[sensor_num], ys[sensor_num][1])
                if BEAT_PLOT_EN:
                    lines[sensor_num][2].set_data(xs[sensor_num], ys[sensor_num][2])

                for ax in axs[sensor_num]:
                    ax.relim()
                    ax.autoscale_view()
            plt.pause(0.01)
    except KeyboardInterrupt:
        print("\nSending SIGINT to ssh recording process")
        record_process.send_signal(signal.SIGINT)
        print(f"Running scp for {audio_filename}")
        subprocess.run(["scp", f"pi@pulse.local:{audio_filename}", audio_filename])
        print(f"Running ffmpeg")
        subprocess.run(["ffmpeg", "-i", audio_filename, "-ac", "1", f"mono-{audio_filename}"])
        command = input("Command (q for force quit, enter for analyze): ")
        if command == "q":
            return

        for i in range(HeartRateManager.NUM_SENSORS):
            score = analyze.get_heartrate_score(beat_times[i])
            print(f"score {i}: {score}")
        pulsedb.addUserPair(f"jim{random()}", f"pam{random()}")
        id = pulsedb.getID()
        convo = open("example_convo.txt", "r").read()
        result = analyze.ask_match(convo)
        convo_score = analyze.get_overall_conversation_score(result)
        heart_score = min(analyze.get_heartrate_score(beat_times[0]),
                          analyze.get_heartrate_score(beat_times[1]))
        pulsedb.updateScores(result.affection, result.vulnerability, result.kindness,
                             result.other, result.negative, result.explanation,
                             heart_score, convo_score, (convo_score + heart_score) / 2, id)
        print(f"Matching results: {matching.perform_matching()}")

        print("Trying to clean up...", end="")
        while True:
            try:
                hr.stop()
            except:
                print(" failed:")
                traceback.print_exc()
                time.sleep(1)
                print("Trying again...", end="")
                continue
            break
        print(" done!")
        return

if __name__ == "__main__":
    run()

