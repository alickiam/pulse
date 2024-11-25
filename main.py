from heartrate import HeartRateManager
import pigpio
import matplotlib.pyplot as plt
import time
import traceback

# Enable drawing red LED data
RED_PLOT_EN = False
# Enable drawing IR LED data
SPO2_PLOT_EN = True

x = []
c = 0
ys = [[[], []] for i in range(HeartRateManager.NUM_SENSORS)]
axs = [[None, None] for i in range(HeartRateManager.NUM_SENSORS)]
lines = [[None, None] for i in range(HeartRateManager.NUM_SENSORS)]
(fig, a) = plt.subplots(1, HeartRateManager.NUM_SENSORS)
for i in range(HeartRateManager.NUM_SENSORS):
    axs[i][0] = a[i]
    axs[i][0].set_xlabel("time (s)")
    axs[i][0].set_ylabel("red")
    (lines[i][0],) = axs[i][0].plot(x, ys[i][0], "-r")
    axs[i][1] = axs[i][0].twinx()
    axs[i][1].set_ylabel("SpO2")
    (lines[i][1],) = axs[i][1].plot(x, ys[i][1], "-b")
fig.tight_layout()

def run():
    global x, c
    hr = HeartRateManager()
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
                    x.append(c / 50)
                    ys[sensor_num][0].append(data1[i])
                    ys[sensor_num][1].append(data2[i])
                    c += 1

                # Prune old data
                if len(x) > 2 * 50:
                    x = x[-2 * 50:]
                    ys[sensor_num][0] = ys[sensor_num][0][-2 * 50:]
                    ys[sensor_num][1] = ys[sensor_num][1][-2 * 50:]

                # Update plots
                if RED_PLOT_EN:
                    lines[sensor_num][0].set_xdata(x)
                    lines[sensor_num][0].set_ydata(ys[sensor_num][0])
                if SPO2_PLOT_EN:
                    lines[sensor_num][1].set_xdata(x)
                    lines[sensor_num][1].set_ydata(ys[sensor_num][1])
                axs[sensor_num][0].relim()
                axs[sensor_num][0].autoscale_view()
                axs[sensor_num][1].relim()
                axs[sensor_num][1].autoscale_view()
            plt.pause(0.01)
    except KeyboardInterrupt:
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

