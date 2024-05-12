import sys
import numpy as np
import pandas as pd
import navpy


LIGHTSPEED = 2.99792458e8

def least_squares(xs, measured_pseudorange, x0, b0):
    dx = 100*np.ones(3)
    b = b0
    # set up the G matrix with the right dimensions. We will later replace the first 3 columns
    # note that b here is the clock bias in meters equivalent, so the actual clock bias is b/LIGHTSPEED
    G = np.ones((measured_pseudorange.size, 4))
    iterations = 0
    while np.linalg.norm(dx) > 1e-3:
        # Eq. (2):
        r = np.linalg.norm(xs - x0, axis=1)
        # Eq. (1):
        phat = r + b0
        # Eq. (3):
        deltaP = measured_pseudorange - phat
        G[:, 0:3] = -(xs - x0) / r[:, None]
        # Eq. (4):
        sol = np.linalg.inv(np.transpose(G) @ G) @ np.transpose(G) @ deltaP
        # Eq. (5):
        dx = sol[0:3]
        db = sol[3]
        x0 = x0 + dx
        b0 = b0 + db
    norm_dp = np.linalg.norm(deltaP)
    return x0, b0, norm_dp
def main():
    
    # date = '2024-04-13 16:51:55.417345280+00:00'
    date = sys.argv[1]
    data = pd.read_csv('out.csv')
    data = data[data['UnixTime'] == date]
    if len(data) == 0:
        print("Invalid date")
        exit(0)

    # initial guesses of receiver clock bias and position
    b0 = 0
    x0 = np.array([0, 0, 0])
    xs = data[['x_k', 'y_k', 'z_k']].to_numpy()

    # Apply satellite clock bias to correct the measured pseudorange values
    pr = data['PrM'] + LIGHTSPEED * data['delT_sv']
    pr = pr.to_numpy()

    x, b, dp = least_squares(xs, pr, x0, b0)
    print(navpy.ecef2lla(x))
    print(b/LIGHTSPEED)
    print(dp)

if __name__ == '__main__':
    main()