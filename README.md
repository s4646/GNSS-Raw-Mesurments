# GNSS Raw Mesurments

### Authors:
- Sahar Tuvyahu
- Guy Gur-Arieh
- Yehonatan Baruchson
- Harel Gilad

## Data 
[Link](https://drive.google.com/drive/folders/1qZ8URVwwjrbTf_sDTgKoenw0OnwZKh1X)  

## Usage:
Open a terminal, clone the repo:
```bash
git clone https://github.com/s4646/GNSS-Raw-Mesurments.git
```
Extract the data into a new directiory called `data`

To create a csv file from the data, run:
```bash
python create_csv.py <path_inside_data_directory>
```
To get position (x,y,z), (lat,lon,alt) from the csv file using GPSTime, run:
```bash
python get_position.py <Unix_Time>
```
To create kml and csv files from the generated csv file, run:
```bash
python create_kml_csv.py
```

## Example Usage:
```bash
fedora@fedora:~/GNSS-Raw-Mesurments$ python create_csv.py 'fixed/gnss_log_2024_04_13_19_51_17.txt'
fedora@fedora:~/GNSS-Raw-Mesurments$ python get_position.py '2024-04-13 16:51:36.417342720+00:00'
[4436876.524074284, 3085278.6874412284, 3376310.701653478]
(32.16879873393706, 34.813661167085066, 38.137367780320346)
fedora@fedora:~/GNSS-Raw-Mesurments$ python create_kml_csv.py
fedora@fedora:~/GNSS-Raw-Mesurments$
```
