# DM Digital Marker Creation

The DM program creates behavioral digital markers from activity-labeled mobile
sensor data. The markers can be used to quantify changes in behavior between
time points or between multiple people/groups.

To create the markers, DM first downsamples the sensor data if needed, to
meet the target rate of one data point per minute. Next, DM imputes missing
values so there is one set of values for each data of collected data.
From the complete data, DM generates
1) a set of daily behavior markers
2) a set of hourly behavior markers
3) a set of overall behavior markers

Author: Dr. Diane J. Cook, School of Electrical Engineering and
Computer Science, Washington State University, email: djcook@wsu.edu.

Support: This material is based on upon work supported by the National Science
Foundation under Grant Nos. 1954372 and 1543656 and by the National Institutes
of Health under Grant No. R41EB029774.


# Running DM

DM requires packages `geopy`, `numpy`, `pandas`, `requests`, and `scikit-learn`.  To install the
packages for your environment, run:
```
pip intall geopy numpy pandas requests scikit-learn
```

DM is run using the following command-line format (requires Python 3):
```
python dm.py [options] <inputfile>
```
The options, input file format, and output are described below.


# Options

The following DM options are currently available.

```
--datapath <path_string>
```
Specification of the location for the data files.
The default value is `./data/`.

```
--activity_list <list>
```
Specify list of overall (primary) activities to learn with a single
multi-class classifier. There should be at least one occurrence of each
activity in the training data. The default value is the list
`['Chores','Eat','Entertainment','Errands','Exercise','Hobby','Hygiene','Relax',
'School','Sleep','Travel','Work']`.

```
--translate
```
If this option is provided, then location names will be mapped from their
original values to a different (typically smaller) set of values.
DM will look in file `loc.translate` for a set of location mappings,
one per line. Each line contains the original activity label and the
new mapped label, separated by a space. Examples are
```
office work
park service
parking road
```
When the open street map returns type `office` this will be mapped to `work`,
`park` will be mapped to `service`, and `parking` will be mapped to `road`.


# Input File(s)

The input file contains time-stamped sensor readings with associated activity
labels. This activity-labeled data can be generated by the AL activity learning
program or another external program. An example input file is in the
file data. The file is in csv format, where each line contains a set of values
for a single timestamp. The format of the input is
`day,time,<sensor values>,<activity labels>`.
The current version of DM assumes that there are 16 sensors with associated
values, 33 one-class activity categories with associated 0 or 1 values, and
one overall activity value. Thus there should be 51 entries on each line
of the input file.


# Output files

DM generates two files. The first has the same name as the input file with the
suffix .bm, this is the behavior marker file. The second has the same name as
the input file with the suffix .bcd, this is the behavior change score file.
The behavior marker file contains a single line of 952 csv behavior markers.
A description of these markers is found in the `behaviormarkers.docx` file.
The behavior change score file contains `n-1` lines corresponding to `n` weeks of
data collection. Each line lists a score representing the amount of behavior
change that occurred between the corresponding week and baseline (the first
week of data collection) and a value indicating the statistical significance
of the change (0=not significant, 1=significant).


# Features

AL extract a vector of features for each non-overlapping sensor sequence of
length `windowsize` (`windowsize` indicates the number of distinct time stamps that
are included in the sequence). A random forest classifier maps the feature
vector to the activity label(s).

The first set of features AL extracts are person-specific features related to
location. Specific <`latitude`, `longitude`, `altitude`> values do not generalize
well to multiple people, so more abstract features are used. Before activity
models are learned, each input file is processed separately to construct
person-specific information. The information includes the person's mean
location (`latitude` and `longitude`) and the span of their visited locations
(`latitude` and `longitude`). To identify frequent locations, k-means clustering
is applied to determine the overall top location clusters and top location
clusters by time of day. The learned cluster models are stored in the clusters
directory and the person-specific features are stored in a file with the
same root name as the input file and a .person suffix. Based on this stored
information, person-specific features are extracted which include the
normalized distance of the current sequence from the user's mean location and
whether the last location in the current sequence belongs to any of the
learned clusters.

Additional statistical features are applied to each non-location sensor
including max, min, sum, mean, median, mean/median absolute value, standard
deviation, mean/median absolute deviation, moments, fft features (ceps, entropy,
energy, msignal, and vsignal), coefficient of variation, skewness, kurtosis,
signal energy, log signal energy, power, autocorrelation, the absolute
differences between successive values in the sequence, and time between peaks.
For sensors with multiple axes (e.g., acceleration, rotation), correlations
between the axes are added to the feature vector. Before extracting these
features, a lowpass filter is applied to remove signal noise.

For the location values, features further include the heading change rate
(number of orientation changes within the sequence), stop rate (number of
movement stops/starts within the sequence), and overall trajectory in
the sequence. Additionally, reverse geocoding with an open street map
and the `loc.translate` file is used to add the location type to the feature list.
