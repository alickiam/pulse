import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analyze import get_heartrate_score, get_rates, get_absolute_score

runs = (
    # Regular resting
    [4.3, 5.0, 5.72, 6.48, 7.24, 7.98, 8.76, 9.5, 10.26, 11.0, 11.78, 12.58, 13.4, 14.22, 15.02, 15.82, 16.64, 17.46, 18.26, 19.02, 19.82, 20.68, 21.48, 22.3, 23.14, 23.96, 24.76, 25.6, 26.42, 27.2, 28.0, 28.84, 29.72, 30.52, 31.36, 32.18, 32.96, 33.72, 34.5, 35.26, 36.0, 36.8, 37.64, 38.46, 39.28, 40.18, 41.04, 41.86, 42.7, 43.48, 44.24, 45.0, 45.82, 46.62, 47.42, 48.24, 49.06, 49.84, 50.66, 51.5, 52.3, 53.06, 53.88, 54.74, 55.54, 56.34, 57.18, 57.98, 58.78, 59.62, 60.46, 61.24, 62.02, 62.8, 63.56, 64.3, 65.06, 65.86, 66.62, 67.42, 68.24, 69.04, 69.82, 70.64, 71.4, 72.14, 72.9, 73.64, 74.38, 75.14, 75.94, 76.7, 77.46, 78.24, 79.04, 79.8, 80.58, 81.42, 82.24, 83.02, 83.78, 84.54, 85.32, 86.02, 86.8, 87.6, 88.34, 89.08, 89.84, 90.6, 91.34, 92.04, 92.82, 93.62, 94.4, 95.16, 95.94, 96.72, 97.56, 98.32, 99.04, 99.78, 100.56, 101.3, 101.96, 102.6, 103.3, 104.02, 104.68, 105.4, 106.16, 106.92, 107.66, 108.4, 109.18, 109.9, 110.64, 111.38, 112.1, 112.8, 113.5, 114.18, 114.92, 115.62, 116.34, 117.02, 117.7, 118.42, 119.16, 119.86, 120.62, 121.4, 122.16, 122.9, 123.56, 124.3, 125.02, 125.74, 126.42, 127.12, 127.86, 128.6, 129.3, 130.04, 130.78, 131.52, 132.2, 132.92, 133.64, 134.42, 135.14, 135.92, 136.72, 137.48, 138.22, 138.94, 139.7, 140.42, 141.16, 141.9, 142.66, 143.38, 144.1, 144.86, 145.62, 146.36, 147.12, 147.88, 148.7, 149.44, 150.22, 151.0, 151.76, 152.5, 153.24, 154.0, 154.72, 155.46, 156.2, 157.3, 158.06, 158.8, 159.54, 160.32, 161.16, 161.96, 162.72, 163.5, 164.28, 165.0, 165.68, 166.36, 166.88, 167.76, 168.64],
    # Recorded same time as above (other hand), but with some dropped heart beats
    [4.46, 5.3, 5.96, 6.7, 7.24, 8.04, 8.32, 8.9, 9.7, 10.46, 11.2, 11.96, 12.74, 13.64, 14.48, 15.26, 16.1, 16.88, 17.72, 18.46, 19.24, 19.6, 20.04, 21.04, 21.82, 22.56, 23.4, 24.24, 25.1, 25.88, 26.64, 27.42, 28.22, 29.26, 30.04, 30.8, 31.64, 32.5, 33.24, 33.6, 34.0, 34.84, 35.58, 36.32, 37.1, 41.34, 42.16, 42.96, 43.78, 44.56, 45.3, 46.14, 46.92, 47.7, 48.58, 49.32, 50.12, 50.94, 51.8, 52.04, 52.58, 53.34, 54.28, 55.16, 55.9, 56.38, 56.64, 57.54, 58.36, 59.14, 59.96, 60.86, 61.58, 62.36, 63.16, 63.94, 64.62, 65.42, 66.24, 66.98, 67.78, 68.62, 69.38, 70.2, 71.04, 71.82, 72.5, 73.28, 74.04, 74.8, 75.54, 76.34, 77.1, 77.84, 78.64, 79.46, 80.24, 81.0, 84.98, 85.76, 86.48, 87.24, 88.0, 88.8, 89.52, 90.28, 91.04, 91.78, 92.5, 93.28, 94.06, 94.86, 95.62, 96.4, 97.2, 98.0, 98.8, 99.5, 100.26, 101.02, 101.8, 102.42, 103.12, 103.82, 104.54, 105.18, 106.0, 106.74, 107.48, 108.26, 109.02, 109.74, 110.48, 111.26, 111.98, 112.66, 113.4, 114.1, 114.8, 115.5, 116.24, 116.9, 117.58, 118.3, 119.06, 119.78, 120.52, 121.28, 122.08, 122.82, 123.48, 124.2, 124.94, 125.7, 126.34, 127.08, 127.8, 128.58, 129.26, 129.98, 130.74, 131.46, 132.12, 132.9, 133.6, 134.38, 135.1, 135.88, 136.64, 137.46, 138.18, 138.9, 139.68, 140.38, 141.12, 141.86, 142.64, 143.34, 144.06, 144.84, 145.6, 146.34, 147.08, 147.86, 148.68, 149.46, 150.22, 151.0, 151.8, 152.48, 153.28, 154.02, 154.74, 155.48, 156.24, 156.9, 157.58, 158.28, 159.04, 159.78, 160.58, 161.42, 162.24, 163.0, 163.74, 164.56, 165.28, 165.96, 167.42, 168.32],
    # Resting start and excited end
    [4.18, 4.84, 5.5, 6.24, 7.0, 7.72, 8.48, 9.22, 9.96, 10.7, 11.46, 12.26, 13.12, 13.98, 14.86, 15.68, 16.52, 17.36, 18.2, 19.02, 19.7, 20.4, 21.16, 21.92, 22.6, 23.38, 24.08, 24.8, 25.58, 26.34, 27.06, 27.84, 28.6, 29.32, 30.08, 30.86, 31.68, 32.46, 33.26, 34.08, 34.86, 35.62, 36.32, 36.98, 37.62, 38.26, 38.88, 39.44, 40.04, 40.66, 41.3, 41.94, 42.62, 43.24, 43.82, 44.38, 44.98, 45.58, 46.12, 46.68, 47.26, 47.86, 48.46, 49.06, 49.66, 50.22, 50.76, 51.32, 51.88, 52.44, 52.98, 53.46, 53.98, 54.52, 55.04, 55.56, 56.0, 56.5, 57.02, 57.54, 58.02, 58.52, 58.96, 59.44, 59.96, 60.42, 60.88, 61.38, 61.86, 62.28, 62.8, 63.32, 63.66, 64.12, 64.6, 65.04, 65.5, 65.98, 66.44, 66.88, 67.34, 67.82, 68.26, 68.7, 69.18, 69.64, 70.4, 70.92, 71.4, 71.84, 72.3, 72.78, 73.26, 73.7, 74.16, 74.64, 75.12, 75.58, 76.06, 76.5, 77.0, 77.5, 77.92, 78.42, 78.9, 79.36, 79.84, 80.3, 80.78, 81.28, 81.74, 82.2, 82.64, 83.12, 83.6, 84.08, 84.52, 84.98, 85.46, 85.94, 86.38, 86.84, 87.3, 87.78, 88.24, 88.68, 89.16, 89.64, 90.1, 90.54, 91.0, 91.46, 91.9, 92.34, 92.76, 93.24, 93.7, 94.14, 94.58, 95.02, 95.5, 95.94, 96.38, 96.84, 97.34, 97.74, 98.18, 98.64, 99.12, 99.58, 100.06, 100.84, 101.32, 101.84, 102.36, 102.86, 103.38, 103.88, 104.38, 104.88, 105.4, 105.94, 106.46, 106.96, 107.46, 107.94, 108.44, 108.96, 109.46, 109.96, 110.48, 110.94, 111.44, 111.96],
    # Excited start and resting end
    [3.84, 4.42, 4.94, 5.48, 6.08, 6.66, 7.28, 7.86, 8.4, 9.0, 9.64, 10.28, 10.98, 11.64, 12.24, 12.86, 13.46, 14.1, 14.62, 15.16, 15.8, 16.46, 17.14, 17.88, 18.62, 19.36, 20.18, 21.06, 21.74, 22.56, 23.34, 24.1, 24.92, 25.7, 26.5, 27.36, 28.2, 29.12, 29.98, 30.76, 31.6, 32.36, 33.08, 33.92, 34.74, 35.58, 36.34, 37.18, 38.04, 38.86, 39.6, 40.4, 41.24, 42.0, 42.76, 43.58, 44.46, 45.24, 46.1, 47.06, 47.96, 48.86, 49.78, 50.66, 51.46, 52.32, 53.24, 54.1, 54.88, 55.8, 56.64, 57.42, 58.24, 59.12, 60.0, 60.78, 61.46, 62.12, 62.78, 63.52, 64.58, 65.68, 66.72, 67.78, 68.76, 69.68, 70.58, 71.36, 72.1, 72.76, 73.42, 74.12, 74.78, 75.68, 76.7, 77.72, 78.7, 79.66, 80.6, 81.48, 82.32, 83.04, 83.74, 84.42, 85.12, 85.82, 86.74, 87.74, 88.68, 89.62, 90.58, 91.48, 92.38, 93.22, 93.94, 94.66, 95.36, 96.06, 96.78, 97.7, 98.62, 99.6, 100.56, 101.48, 102.34, 103.16, 103.94, 104.74, 105.54, 106.4, 107.26, 108.12, 109.02, 109.82, 110.68, 111.4, 112.12, 112.78, 113.44, 114.08, 114.8, 115.68, 116.6, 117.54, 118.46, 119.36, 120.28, 121.16, 122.0, 122.82, 123.66, 124.48, 125.24, 125.98, 126.66, 127.34, 128.0, 128.68, 129.5, 130.42, 131.3, 132.2, 133.06, 133.92, 134.68, 135.5, 136.32, 137.16, 138.04, 138.96, 139.82, 140.68, 141.56, 142.38, 143.26, 144.12, 145.02, 145.84, 146.68, 147.58, 148.42, 149.32, 150.12, 150.94, 151.68, 152.4, 153.18, 154.0, 154.86, 155.74, 156.56, 157.38, 158.22, 159.06, 159.92, 160.76, 161.62, 162.48, 163.32, 164.18, 165.04, 165.88, 166.74, 167.64, 168.58, 169.4, 170.34],
    # Resting with inconsistencies
    [12.5, 13.44, 14.38, 15.26, 16.24, 17.16, 18.1, 19.02, 19.94, 20.84, 21.7, 22.5, 23.38, 24.28, 25.08, 26.06, 27.0, 27.94, 28.88, 29.8, 30.66, 31.44, 32.1, 32.74, 34.48, 36.54, 37.56, 38.68, 39.7, 40.78, 41.82, 42.86, 43.86, 44.86, 45.76, 46.74, 54.5, 58.24, 59.18, 62.8, 66.74, 67.82, 68.5, 69.6, 70.42, 71.3, 72.32, 73.3, 74.06, 75.04, 75.9, 76.78, 77.76, 78.58, 79.92, 80.7, 81.72, 82.68, 83.48, 84.44, 85.4, 86.24, 86.92, 87.72, 88.64, 89.66, 90.42, 91.32, 92.3, 93.82, 94.56, 97.82, 98.78, 99.82, 100.66, 101.62, 102.58, 103.34, 104.2, 105.1, 105.88, 106.78, 107.72, 108.54, 109.48, 110.38, 111.2, 112.1, 113.0, 113.86, 114.78, 115.62, 116.5, 117.4, 118.22, 119.1, 120.12, 121.08, 121.96, 122.86, 123.84, 124.68, 125.58, 126.56, 127.4, 128.36, 129.28, 130.12, 131.04, 131.96, 132.82, 133.6, 134.08],
    # Increase and then decrease in heart rate
    [3.72, 4.66, 5.7, 6.6, 7.42, 8.14, 8.98, 9.7, 10.5, 11.3, 11.96, 12.76, 13.6, 14.24, 14.96, 15.76, 16.5, 17.16, 17.92, 18.54, 19.22, 19.94, 20.56, 21.36, 22.04, 22.7, 23.48, 24.06, 24.76, 25.52, 26.14, 26.72, 27.36, 28.02, 28.62, 29.2, 29.8, 30.4, 30.96, 31.52, 32.12, 32.7, 33.26, 33.84, 34.46, 35.0, 35.54, 36.14, 36.58, 37.2, 37.8, 38.36, 38.9, 39.46, 39.98, 40.54, 41.12, 41.64, 42.18, 42.74, 43.28, 43.8, 44.32, 44.9, 45.38, 45.92, 46.48, 46.98, 47.58, 48.14, 48.64, 49.22, 49.78, 50.32, 50.88, 51.48, 52.04, 52.58, 53.18, 53.7, 54.28, 54.76, 55.38, 55.96, 56.58, 56.94, 57.48, 58.06, 58.64, 59.18, 59.66, 60.14, 60.64, 61.2, 61.74, 62.28, 62.8, 63.34, 63.9, 64.48, 65.04, 65.58, 66.16, 66.7, 67.3, 67.9, 68.5, 69.08, 69.72, 70.32, 70.94, 71.58, 72.16, 72.78, 73.4, 74.04, 74.7, 75.38, 76.06, 76.76, 77.46, 78.12, 78.84, 79.54, 80.22, 80.88, 81.54, 82.24, 82.96, 83.66, 84.38, 85.22, 86.06, 86.92, 87.78, 88.66, 89.52, 90.44, 91.34, 92.24, 93.12, 94.02, 94.88, 95.78, 96.68, 97.62, 98.5, 99.38, 100.28, 101.2, 102.12, 103.0, 103.9, 104.78, 105.66, 106.54, 107.4, 108.3, 109.14, 109.94, 110.68, 111.52, 112.34, 113.2, 114.06, 114.82, 115.54, 116.2, 116.88],
    # Moderate increase in heart rate from resting
    [4.1, 4.9, 5.68, 6.44, 7.2, 7.98, 8.76, 9.6, 10.42, 11.24, 12.08, 12.94, 13.8, 14.66, 15.5, 16.32, 17.04, 17.76, 18.56, 19.32, 20.12, 20.94, 21.7, 22.5, 23.36, 24.22, 25.02, 25.82, 26.64, 27.36, 28.16, 28.94, 29.72, 30.44, 31.24, 32.08, 32.88, 33.7, 34.58, 35.06, 35.74, 36.56, 37.44, 38.2, 38.96, 39.74, 40.6, 41.38, 42.14, 43.0, 43.84, 44.68, 45.52, 46.36, 47.1, 47.82, 48.64, 49.5, 50.32, 51.22, 52.1, 52.96, 53.82, 54.7, 55.5, 56.32, 57.16, 57.94, 58.62, 59.24, 59.92, 60.84, 61.6, 62.5, 63.38, 64.28, 65.2, 65.86, 66.66, 67.42, 68.06, 68.8, 69.6, 70.28, 70.92, 71.72, 72.52, 73.16, 73.92, 74.68, 75.44, 76.1, 76.8, 77.4, 78.04, 78.74, 79.32, 80.02, 80.68, 81.4, 82.1, 82.72, 83.36, 84.04, 84.64, 85.28, 85.92, 86.54, 87.18, 87.86, 88.5, 89.2, 89.92, 90.62, 91.32, 91.96, 92.6, 93.24, 93.86, 94.48, 95.1, 95.7, 96.28, 96.94, 97.68, 98.48, 99.3, 100.1, 100.9, 101.72, 102.5, 103.26, 104.06, 104.8],
    # Garbage (no person to read)
    [7.14, 37.56, 39.32, 49.96, 71.58, 72.98, 106.34],
    # Resting with large movement in the middle
    [4.64, 5.46, 6.26, 7.12, 7.92, 8.7, 9.5, 10.3, 11.1, 11.86, 12.62, 13.38, 14.12, 14.9, 19.3, 20.02, 20.76, 21.48, 22.22, 22.96, 23.68, 24.38, 25.06, 25.72, 26.4, 27.12, 27.74, 28.38, 29.04, 29.72, 30.4, 31.18, 31.92, 32.74, 33.52],
)

if __name__ == "__main__":
    for i, run in enumerate(runs):
        #print(get_rates(run))
        #print(f"abs score {i}: {get_absolute_score(run)}")
        print(f"score {i}: {get_heartrate_score(run)}")
