import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import subprocess
import simplekml
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

def create_kml(data):
    dates = data['UnixTime'].unique()
    kml = simplekml.Kml()

    for date in dates:
        b0 = 0
        x0 = np.array([0, 0, 0])
        temp = data[data['UnixTime'] == date]
        xs = temp[['x_k', 'y_k', 'z_k']].to_numpy()
        # Apply satellite clock bias to correct the measured pseudorange values
        pr = temp['PrM'] + LIGHTSPEED * temp['delT_sv']
        pr = pr.to_numpy()

        x, b, dp = least_squares(xs, pr, x0, b0)
        lla = navpy.ecef2lla(x)
        kml.newpoint(name = date, coords = [[lla[1], lla[0], lla[2]]])

    kml.save('out.kml')

def create_csv(data):
    df: pd.DataFrame = data
    dates = df['UnixTime'].unique()
    df['x'] = None
    df['y'] = None
    df['z'] = None
    df['lat'] = None
    df['lon'] = None
    df['alt'] = None

    for date in dates:
        b0 = 0
        x0 = np.array([0, 0, 0])
        temp = data[data['UnixTime'] == date]
        xs = temp[['x_k', 'y_k', 'z_k']].to_numpy()
        # Apply satellite clock bias to correct the measured pseudorange values
        pr = temp['PrM'] + LIGHTSPEED * temp['delT_sv']
        pr = pr.to_numpy()

        xyz, b, dp = least_squares(xs, pr, x0, b0)
        lla = navpy.ecef2lla(xyz)

        df.loc[df['UnixTime'] == date, 'x'] = xyz[0]
        df.loc[df['UnixTime'] == date, 'y'] = xyz[1]
        df.loc[df['UnixTime'] == date, 'z'] = xyz[2]
        df.loc[df['UnixTime'] == date, 'lat'] = lla[0]
        df.loc[df['UnixTime'] == date, 'lon'] = lla[1]
        df.loc[df['UnixTime'] == date, 'alt'] = lla[2]

    df.to_csv('out.csv', index=False)


def main():
    data = pd.read_csv('data.csv')
    create_kml(data)
    create_csv(data)

if __name__ == '__main__':
    main()

#     # CSV
# result = subprocess.run(['/usr/bin/python', 'get_position.py', date], stdout=subprocess.PIPE)
# result = result.stdout.decode('utf-8')