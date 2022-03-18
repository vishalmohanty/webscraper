import csv
import math

import matplotlib.lines as mlines
from matplotlib.ticker import MaxNLocator
import matplotlib.pylab as plt
import numpy as np
from matplotlib import rcParams

rcParams['font.family'] = 'Times New Roman'

weighted = {
    'Montgomery, AL': -0.03918335016516895,
    'Juneau, AK': -0.04819714984707875,
    'Phoenix, AZ': -0.04127845221123429,
    'Little Rock, AR': -0.043208189240339485,
    'Sacramento, CA': -0.0447932962175611,
    'Denver, CO': -0.03534568725038026,
    'Hartford, CT': -0.051318345269589304,
    'Dover, DE': -0.04410079817485979,
    'Tallahassee, FL': -0.04904944079404738,
    'Atlanta, GA': -0.03835455112072264,
    'Honolulu, HI': -0.04430356055903157,
    'Boise, ID': -0.04429277255559287,
    'Springfield, IL': -0.049079223899573546,
    'Indianapolis, IN': -0.04045169826106026,
    'Des Moines, IA': -0.04411556134405065,
    'Topeka, KS': -0.05086811538147495,
    'Frankfort, KY': -0.042184825476727035,
    'Baton Rouge, LA': -0.04389737416132434,
    'Augusta, ME': -0.04212128299879622,
    'Annapolis, MD': -0.04388988333076714,
    'Boston, MA': -0.0383121150700335,
    'Lansing, MI': -0.04572841478868638,
    'St. Paul, MN': -0.04296604818535782,
    'Jackson, MS': -0.04470627813704356,
    'Jefferson City, MO': -0.03657775051265361,
    'Helena, MT': -0.04413495825518135,
    'Lincoln, NE': -0.03617707893524351,
    'Carson City, NV': -0.03583424627844964,
    'Concord, NH': -0.04914145723628957,
    'Trenton, NJ': -0.041852742656047326,
    'Santa Fe, NM': -0.04794226779065536,
    'Albany, NY': -0.0439948548029637,
    'Raleigh, NC': -0.037781209393634,
    'Bismarck, ND': -0.038778420835549575,
    'Oklahoma City, OH': -0.04361796312801526,
    'Salem, OR': -0.039538993616616745,
    'Harrisburg, PA': -0.04214384792617321,
    'Providence, RI': -0.04021977341993038,
    'Columbia, SC': -0.04350047974814068,
    'Pierre, SD': -0.040579818043541147,
    'Nashville, TN': -0.0466268401751304,
    'Austin, TX': -0.04279195547437081,
    'Salt Lake City, UT': -0.042489828172970145,
    'Montpelier, VT': -0.03809070731910734,
    'Richmond, VA': -0.046323110278850894,
    'Olympia, WA': -0.04694064637514814,
    'Charleston, WV': -0.04706013948669316,
    'Madison, WI': -0.03517318797591053,
    'Cheyenne, WY': -0.04127756238860428
}
unweighted = {
    'AL': -0.071806,
    'AK': -0.082814,
    'AZ': -0.083603,
    'AR': -0.085412,
    'CA': -0.064396,
    'CO': -0.064324,
    'CT': -0.057863,
    'DE': -0.075264,
    'FL': -0.057875,
    'GA': -0.090823,
    'HI': -0.080613,
    'ID': -0.080004,
    'IL': -0.062313,
    'IN': -0.064927,
    'IA': -0.080639,
    'KS': -0.089863,
    'KY': -0.068951,
    'LA': -0.073592,
    'ME': -0.059620,
    'MD': -0.062009,
    'MA': -0.053489,
    'MI': -0.077970,
    'MN': -0.068342,
    'MS': -0.065541,
    'MO': -0.069612,
    'MT': -0.075233,
    'NE': -0.061198,
    'NV': -0.050031,
    'NH': -0.068559,
    'NJ': -0.075672,
    'NM': -0.082795,
    'NY': -0.069741,
    'NC': -0.052452,
    'ND': -0.066142,
    'OH': -0.073240,
    'OR': -0.053687,
    'PA': -0.102050,
    'RI': -0.058951,
    'SC': -0.067755,
    'SD': -0.074587,
    'TN': -0.083953,
    'TX': -0.068249,
    'UT': -0.063682,
    'VT': -0.060763,
    'VA': -0.064583,
    'WA': -0.083202,
    'WV': -0.100591,
    'WI': -0.075631,
    'WY': -0.089318
}

google_weighted = {
    'Montgomery,Alabama': -0.052620,
    'Juneau,Juneau,Alaska': -0.051601,
    'Phoenix,Arizona': -0.055961,
    'Little Rock,Arkansas': -0.052230,
    'Sacramento,California': -0.057171,
    'Denver,Colorado': -0.057646,
    'Hartford,Connecticut': -0.055862,
    'Dover,Delaware': -0.057227,
    'Tallahassee,Florida': -0.052155022000576014,
    'Atlanta,Georgia': -0.05557964076252149,
    'Honolulu,Hawaii': -0.05468414854474025,
    'Boise,Idaho': -0.053364660804897476,
    'Springfield,Illinois': -0.0525578252727048,
    'Indianapolis,Indiana': -0.050825842137306974,
    'Des Moines,New Mexico': -0.04908492404672618,
    'Topeka,Indiana': -0.04693345961806908,
    'Frankfort,Kansas': -0.05178464198623083,
    'Baton Rouge,Louisiana': -0.05996784543835305,
    'Augusta,Maine': -0.05777312624740943,
    'Annapolis,Missouri': -0.06305408946402166,
    'Boston,Massachusetts': -0.05599401243072362,
    'Lansing,Michigan': -0.05363612221065318,
    'Saint Paul,Minnesota': -0.05483828005945487,
    'Jackson,Missouri': -0.05363580468681736,
    'Jefferson City,Missouri': -0.057585290175204626,
    'Helena,Montana': -0.05282379169593389,
    'Lincoln,Montana': -0.05518281865916025,
    'Carson City,Nevada': -0.057819502850532285,
    'Concord,New Hampshire': -0.056172768550330716,
    'Trenton,New Jersey': -0.050565,
    'Santa Fe,New Mexico': -0.054469,
    'Albany,New York': -0.056666,
    'Raleigh,North Carolina': -0.057353,
    'Columbus,Ohio': -0.053442,
    'Oklahoma City,Oklahoma': -0.056267,
    'Salem,Oregon': -0.053718,
    'Harrisburg,Pennsylvania': -0.055401,
    'Columbia,South Carolina': -0.054451,
    'Pierre,South Dakota': -0.052940,
    'Nashville,Tennessee': -0.055467,
    'Austin,Texas': -0.057399,
    'Montpelier,Vermont': -0.057246,
    'Richmond County,Virginia': -0.055788,
    'Olympia,Washington': -0.058078,
    'Charleston,West Virginia': -0.056183,
    'Cheyenne,Wyoming': -0.051547,
    'Bismarck,North Dakota': -0.053327,
    'Salt Lake City,Utah': -0.049546,
    'Madison,Wisconsin': -0.052086
}

ddg_weighted = {
    'California': -0.005289,
    'New York': -0.004873,
    'Florida': -0.004223,
    'DC': -0.006426,
    'Illinois': -0.003186
}

google_selected_weighted = {
    'California': -0.057171,
    'New York': -0.056666,
    'Florida': -0.052155022000576014,

    'Illinois': -0.0525578252727048
}

bing_selected_weighted = {
    'California': -0.0447932962175611,
    'New York': -0.0439948548029637,
    'Florida': -0.04904944079404738,
    'Illinois': -0.049079223899573546
}

ddg_lists = sorted(ddg_weighted.items())
ddg_x, ddg_y = zip(*ddg_lists)

g_select_lists = sorted(google_selected_weighted.items())
g_select_x, g_select_y = zip(*g_select_lists)

b_select_lists = sorted(bing_selected_weighted.items())
b_select_x, b_select_y = zip(*b_select_lists)

google_weighted_keys = list(google_weighted.keys())
counter = 1
for old_key in google_weighted_keys:
    # print(old_key)
    google_weighted[counter] = google_weighted[old_key]
    google_weighted.pop(old_key, None)
    counter += 1
lists = sorted(google_weighted.items())
google_x, google_y = zip(*lists)

four_am_weighted = {'Montgomery, AL': -0.04106160563522392,
                    'Juneau, AK': -0.04064849660680458,
                    'Phoenix, AZ': -0.04265279814978116,
                    'Little Rock, AR': -0.03930308863192053,
                    'Sacramento, CA': -0.040419826241333286,
                    'Denver, CO': -0.03904982615326652,
                    'Hartford, CT': -0.035606543448998246,
                    'Dover, DE': -0.04090555998222333,
                    'Tallahassee, FL': -0.050915518569258966,
                    'Atlanta, GA': -0.049727090576971514,
                    'Honolulu, HI': -0.04783970951436129,
                    'Boise, ID': -0.035020529725744896,
                    'Springfield, IL': -0.03746684172767187,
                    'Indianapolis, IN': -0.04756033710095835,
                    'Des Moines, IA': -0.034563683837355245,
                    'Topeka, KS': -0.04550256955292404,
                    'Frankfort, KY': -0.038019192506392144,
                    'Baton Rouge, LA': -0.053615543995478854,
                    'Augusta, ME': -0.03942428338139096,
                    'Annapolis, MD': -0.03439317053285649,
                    'Boston, MA': -0.031500983803294975,
                    'Lansing, MI': -0.04350563944003527,
                    'St. Paul, MN': -0.046485900079785,
                    'Jackson, MS': -0.04553522749514757,
                    'Jefferson City, MO': -0.046350631481364826,
                    'Helena, MT': -0.04677409953353769,
                    'Lincoln, NE': -0.044588639757308965,
                    'Carson City, NV': -0.04534741177225348,
                    'Concord, NH': -0.03931576946625701,
                    'Trenton, NJ': -0.050834531983403784,
                    'Santa Fe, NM': -0.040076032039976485,
                    'Albany, NY': -0.05177463857044876,
                    'Raleigh, NC': -0.042098743463228915,
                    'Bismarck, ND': -0.04537421959771563,
                    'Oklahoma City, OH': -0.05003428665152617,
                    'Salem, OR': -0.047811487222152234,
                    'Harrisburg, PA': -0.04427963014170003,
                    'Providence, RI': -0.047955175091332826,
                    'Columbia, SC': -0.04848707708409153,
                    'Pierre, SD': -0.03970123649428907,
                    'Nashville, TN': -0.041485485981635456,
                    'Austin, TX': -0.045247370591412144,
                    'Salt Lake City, UT': -0.03710654358663904,
                    'Montpelier, VT': -0.04443400320248127,
                    'Richmond, VA': -0.04212392927304667,
                    'Olympia, WA': -0.05046484392817484,
                    'Charleston, WV': -0.05307760559381502,
                    'Madison, WI': -0.044838417680892646,
                    'Cheyenne, WY': -0.03900113811728395}

google_ac_scores = [{'U': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US': [0, 0, 0.0, 0.0, 0,
                                                                   0, 0.0, 0.0],
                     'US ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US E': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US El': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Ele': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Elec': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Elect': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Electi': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Electio': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Election': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Election ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Election D': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Election De': [1, 0, 0.25, 0.0, 512, 0, 51.2, 0.0], 'US Election Dem': [1, 0, 0.5, 0.0, 512, 0, 85.33333333333333, 0.0], 'US Election Demo': [1, 0, 0.5, 0.0, 512, 0, 85.33333333333333, 0.0], 'US Election Democ': [2, 0, 1.3333333333333333, 0.0, 534, 0, 178.0, 0.0], 'US Election Democr': [2, 0, 1.3333333333333333, 0.0, 534, 0, 178.0, 0.0], 'US Election Democra': [2, 0, 1.3333333333333333, 0.0, 534, 0, 178.0, 0.0], 'US Election Democrat': [3, 0, 1.8333333333333333, 0.0, 556, 0, 185.33333333333334, 0.0], 'US Election Democrati': [4, 0, 2.083333333333333, 0.0, 578, 0, 144.5, 0.0], 'US Election Democratic': [4, 0, 2.083333333333333, 0.0, 578, 0, 144.5, 0.0]}, {'U': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US E': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US El': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Ele': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Elec': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Elect': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Electi': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Electio': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Election': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Election ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Election R': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Election Re': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Election Rep': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Election Repu': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Election Repub': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Election Republ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Election Republi': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Election Republic': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Election Republica': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Election Republican': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0]}, {'U': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US P': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Po': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Pol': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Poli': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Polit': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Politi': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Politic': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Politica': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political P': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Pa': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Par': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Part': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Party': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Party ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Party D': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Party De': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Party Dem': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Party Demo': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Party Democ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Party Democr': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Party Democra': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Party Democrat': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Party Democrati': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Party Democratic': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0]}, {'U': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US P': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Po': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Pol': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Poli': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Polit': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Politi': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Politic': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Politica': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political P': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Pa': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Par': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Part': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Party': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Party ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Party R': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Party Re': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Party Rep': [1, 1, 1.0, 1.0, 22, 22, 4.4, 4.4], 'US Political Party Repu': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Party Repub': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Party Republ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Party Republi': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Party Republic': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'US Political Party Republica': [1, 1, 1.0, 1.0, 22, 22, 22.0, 22.0], 'US Political Party Republican': [1, 1, 1.0, 1.0, 22, 22, 22.0, 22.0]}, {'P': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Pa': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Par': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Part': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Party': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Party ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Party D': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Party De': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Party Dem': [2, 0, 0.225, 0.0, 1024, 0, 102.4, 0.0], 'Party Demo': [3, 0, 0.44285714285714284, 0.0, 1046, 0, 104.6, 0.0], 'Party Democ': [9, 0, 1.928968253968254, 0.0, 1178, 0, 117.8, 0.0], 'Party Democr': [9, 0, 1.928968253968254, 0.0, 1178, 0, 117.8, 0.0], 'Party Democra': [9, 0, 1.928968253968254, 0.0, 1178, 0, 117.8, 0.0], 'Party Democrat': [10, 0, 2.9289682539682538, 0.0, 1200, 0, 120.0, 0.0], 'Party Democrati': [10, 0, 2.9289682539682538, 0.0, 1200, 0, 120.0, 0.0], 'Party Democratic': [10, 0, 2.9289682539682538, 0.0, 1200, 0, 120.0, 0.0]}, {'P': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Pa': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Par': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Part': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Party': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Party ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Party R': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Party Re': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Party Rep': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Party Repu': [0, 7, 0.0, 1.0956349206349207, 0, 154, 0.0, 15.4], 'Party Repub': [0, 9, 0.0, 1.928968253968254, 0, 633, 0.0, 63.3], 'Party Republ': [0, 9, 0.0, 1.928968253968254, 0, 633, 0.0, 63.3], 'Party Republi': [0, 9, 0.0, 1.928968253968254, 0, 633, 0.0, 63.3], 'Party Republic': [0, 9, 0.0, 1.928968253968254, 0, 633, 0.0, 63.3], 'Party Republica': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Party Republican': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0]}, {'C': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Ca': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Can': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Cand': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candi': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candid': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candida': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candidat': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candidate': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candidate ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candidate D': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candidate De': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candidate Dem': [3, 0, 0.43452380952380953, 0.0, 66, 0, 7.333333333333333, 0.0], 'Candidate Demo': [3, 0, 0.6166666666666667, 0.0, 66, 0, 11.0, 0.0], 'Candidate Democ': [3, 0, 1.8333333333333333, 0.0, 66, 0, 22.0, 0.0], 'Candidate Democr': [2, 0, 1.5, 0.0, 44, 0, 22.0, 0.0], 'Candidate Democra': [3, 0, 1.8333333333333333, 0.0, 66, 0, 22.0, 0.0], 'Candidate Democrat': [3, 0, 1.8333333333333333, 0.0, 66, 0, 22.0, 0.0], 'Candidate Democrati': [3, 0, 1.8333333333333333, 0.0, 57, 0, 19.0, 0.0], 'Candidate Democratic': [3, 0, 1.8333333333333333, 0.0, 66, 0, 22.0, 0.0]}, {'C': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Ca': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Can': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Cand': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candi': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candid': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candida': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candidat': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candidate': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candidate ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candidate R': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candidate Re': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candidate Rep': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candidate Repu': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candidate Repub': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candidate Republ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candidate Republi': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candidate Republic': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candidate Republica': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Candidate Republican': [0, 2, 0.0, 1.5, 0, 44, 0.0, 22.0]}, {'P': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Po': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Pol': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Poli': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Polit': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politi': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politic': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politics': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politics ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politics D': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politics De': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politics Dem': [3, 0, 0.33611111111111114, 0.0, 66, 0, 6.6, 0.0], 'Politics Demo': [4, 0, 0.47896825396825393, 0.0, 88, 0, 8.8, 0.0], 'Politics Democ': [6, 0, 0.8456349206349206, 0.0, 132, 0, 13.2, 0.0], 'Politics Democr': [6, 0, 0.8456349206349206, 0.0, 132, 0, 13.2, 0.0], 'Politics Democra': [6, 0, 0.8456349206349206, 0.0, 132, 0, 13.2, 0.0], 'Politics Democrat': [10, 1, 2.9289682539682538, 1.0, 220, 22, 22.0, 2.2], 'Politics Democrati': [10, 1, 2.9289682539682538, 1.0, 211, 13, 21.1, 1.3], 'Politics Democratic': [10, 1, 2.9289682539682538, 1.0, 220, 22, 22.0, 2.2]}, {'P': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Po': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Pol': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Poli': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Polit': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politi': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politic': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politics': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politics ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politics R': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politics Re': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politics Rep': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politics Repu': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politics Repub': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politics Republ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politics Republi': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politics Republic': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politics Republica': [1, 1, 1.0, 1.0, 22, 22, 22.0, 22.0], 'Politics Republican': [1, 1, 1.0, 1.0, 22, 22, 22.0, 22.0]}, {'P': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Po': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Pol': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Poli': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Polit': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politi': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politic': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politica': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political N': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political Ne': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political New': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political News': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political News ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political News D': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political News De': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political News Dem': [1, 0, 0.5, 0.0, 22, 0, 11.0, 0.0], 'Political News Demo': [1, 0, 0.5, 0.0, 22, 0, 11.0, 0.0], 'Political News Democ': [1, 0, 1.0, 0.0, 22, 0, 22.0, 0.0], 'Political News Democr': [1, 0, 1.0, 0.0, 22, 0, 22.0, 0.0], 'Political News Democra': [1, 0, 1.0, 0.0, 22, 0, 22.0, 0.0], 'Political News Democrat': [1, 0, 1.0, 0.0, 22, 0, 22.0, 0.0], 'Political News Democrati': [1, 0, 1.0, 0.0, 22, 0, 22.0, 0.0], 'Political News Democratic': [1, 0, 1.0, 0.0, 22, 0, 22.0, 0.0]}, {'P': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Po': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Pol': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Poli': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Polit': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politi': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politic': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Politica': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political N': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political Ne': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political New': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political News': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political News ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political News R': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political News Re': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political News Rep': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political News Repu': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political News Repub': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political News Republ': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political News Republi': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political News Republic': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political News Republica': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0], 'Political News Republican': [0, 0, 0.0, 0.0, 0, 0, 0.0, 0.0]}]

ddg_ac_scores = [{'U': [0, 0, 0.0, 0.0], 'US': [0, 0, 0.0, 0.0], 'US ': [0, 0, 0.0, 0.0], 'US E':[0, 0, 0.0, 0.0], 'US El': [0, 0, 0.0, 0.0], 'US Ele': [0, 0, 0.0, 0.0], 'US Elec': [0, 0, 0.0, 0.0], 'US Elect': [0, 0, 0.0, 0.0], 'US Electi': [0, 0, 0.0, 0.0], 'US Electio': [0, 0, 0.0, 0.0], 'US Election': [0, 0, 0.0, 0.0], 'US Election ': [0, 0, 0.0, 0.0], 'US Election D': [0, 0, 0.0, 0.0], 'US Election De': [0, 0, 0.0, 0.0], 'US Election Dem': [1, 0, 0.5, 0.0], 'US Election Demo': [1, 0, 0.5, 0.0], 'US Election Democ': [1, 0, 1.0, 0.0], 'US Election Democr': [1, 0, 1.0, 0.0], 'US Election Democra': [1, 0, 1.0, 0.0], 'US Election Democrat': [1, 0, 1.0, 0.0], 'US Election Democrati': [1, 0, 1.0, 0.0], 'US Election Democratic': [3, 0, 1.5833333333333333, 0.0]},
{'U': [0, 0, 0.0, 0.0], 'US': [0, 0, 0.0, 0.0], 'US ': [0, 0, 0.0, 0.0], 'US E': [0, 0, 0.0, 0.0], 'US El': [0, 0, 0.0, 0.0], 'US Ele': [0, 0, 0.0, 0.0], 'US Elec': [0, 0, 0.0, 0.0], 'US Elect': [0, 0, 0.0, 0.0], 'US Electi': [0, 0, 0.0, 0.0], 'US Electio': [0, 0, 0.0, 0.0], 'US Election': [0, 0, 0.0, 0.0], 'US Election ': [0, 0, 0.0, 0.0], 'US Election R': [0, 0, 0.0, 0.0], 'US Election Re': [0, 0, 0.0, 0.0], 'US Election Rep': [0, 2, 0.0, 0.5833333333333333], 'US Election Repu': [0, 2, 0.0, 1.5], 'US Election Repub': [0, 3, 0.0, 1.75], 'US Election Republ': [0, 3, 0.0, 1.75], 'US Election Republi': [0, 3, 0.0, 1.75], 'US Election Republic': [0, 3, 0.0, 1.75], 'US Election Republica': [0, 3, 0.0, 1.8333333333333333], 'US Election Republican': [0, 5, 0.0, 2.283333333333333]},
{'U': [0, 0, 0.0, 0.0], 'US': [0, 0, 0.0, 0.0], 'US ': [0, 0, 0.0, 0.0], 'US P': [0, 0, 0.0, 0.0], 'US Po': [0, 0, 0.0, 0.0], 'US Pol': [0, 0, 0.0, 0.0], 'US Poli': [0, 0, 0.0, 0.0], 'US Polit': [0, 0, 0.0, 0.0], 'US Politi': [0, 0, 0.0, 0.0], 'US Politic': [0, 0, 0.0, 0.0], 'US Politica': [0, 0, 0.0, 0.0], 'US Political': [0, 0, 0.0, 0.0], 'US Political ': [0, 0, 0.0, 0.0], 'US Political P': [0, 0, 0.0, 0.0], 'US Political Pa': [0, 0, 0.0, 0.0], 'US Political Par': [0, 0, 0.0, 0.0], 'US Political Part': [0, 0, 0.0, 0.0], 'US Political Party': [0, 0, 0.0, 0.0], 'US Political Party ': [0, 0, 0.0, 0.0], 'US Political Party D': [0, 0, 0.0, 0.0], 'US Political Party De': [0, 0, 0.0, 0.0], 'US Political Party Dem': [1, 0, 0.2, 0.0], 'US Political Party Demo': [1, 0, 0.25, 0.0], 'US Political Party Democ': [1, 0, 0.5, 0.0], 'US Political Party Democr': [1, 0, 0.5, 0.0], 'US Political Party Democra': [1, 0, 0.5, 0.0], 'US Political Party Democrat': [1, 0, 1.0, 0.0], 'US Political Party Democrati': [1, 0, 1.0, 0.0], 'US Political Party Democratic': [1, 0, 1.0, 0.0]},
{'U': [0, 0, 0.0, 0.0], 'US': [0, 0, 0.0, 0.0], 'US ': [0, 0, 0.0, 0.0], 'US P': [0, 0, 0.0, 0.0], 'US Po': [0, 0, 0.0, 0.0], 'US Pol': [0, 0, 0.0, 0.0], 'US Poli': [0, 0, 0.0, 0.0], 'US Polit': [0, 0, 0.0, 0.0], 'US Politi': [0, 0, 0.0, 0.0], 'US Politic': [0, 0, 0.0, 0.0], 'US Politica': [0, 0, 0.0, 0.0], 'US Political': [0, 0, 0.0, 0.0], 'US Political ': [0, 0, 0.0, 0.0], 'US Political P': [0, 0, 0.0, 0.0], 'US Political Pa': [0, 0, 0.0, 0.0], 'US Political Par': [0, 0, 0.0, 0.0], 'US Political Part': [0, 0, 0.0, 0.0], 'US Political Party': [0, 0, 0.0, 0.0], 'US Political Party ': [0, 0, 0.0, 0.0], 'US Political Party R': [0, 0, 0.0, 0.0], 'US Political Party Re': [0, 1, 0.0, 0.14285714285714285], 'US Political Party Rep': [0, 1, 0.0, 0.16666666666666666], 'US Political Party Repu': [0, 1, 0.0, 0.5], 'US Political Party Repub': [0, 1, 0.0, 0.2], 'US Political Party Republ': [0, 1, 0.0, 1.0], 'US Political Party Republi': [0, 1, 0.0, 1.0], 'US Political Party Republic': [0, 1, 0.0, 1.0], 'US Political Party Republica': [0, 1, 0.0, 1.0], 'US Political Party Republican': [0, 0, 0.0, 0.0]},
{'P': [0, 0, 0.0, 0.0], 'Pa': [0, 0, 0.0, 0.0], 'Par': [0, 0, 0.0, 0.0], 'Part': [0, 0, 0.0, 0.0], 'Party': [0, 0, 0.0, 0.0], 'Party ': [0, 0, 0.0, 0.0], 'Party D': [0, 0, 0.0, 0.0], 'Party De': [0, 0, 0.0, 0.0], 'Party Dem': [2, 0, 0.45, 0.0], 'Party Demo': [2, 0, 0.45, 0.0], 'Party Democ': [5, 0, 1.2678571428571428, 0.0], 'Party Democr': [5, 0, 1.2678571428571428, 0.0], 'Party Democra': [5, 0, 1.2678571428571428, 0.0], 'Party Democrat': [7, 0, 2.3845238095238095, 0.0], 'Party Democrati': [2, 0, 1.5, 0.0], 'Party Democratic': [2, 0, 1.5, 0.0]},
{'P': [0, 0, 0.0, 0.0], 'Pa': [0, 0, 0.0, 0.0], 'Par': [0, 0, 0.0, 0.0], 'Part': [0, 0, 0.0, 0.0], 'Party': [0, 0, 0.0, 0.0], 'Party ': [0, 0, 0.0, 0.0], 'Party R': [0, 0, 0.0, 0.0], 'Party Re': [0, 0, 0.0, 0.0], 'Party Rep': [0, 1, 0.0, 0.2], 'Party Repu': [1, 8, 0.125, 2.7178571428571425], 'Party Repub': [1, 8, 0.125, 2.7178571428571425], 'Party Republ': [1, 8, 0.125, 2.7178571428571425], 'Party Republi': [1, 8, 0.125, 2.7178571428571425], 'Party Republic': [0, 7, 0.0, 2.217857142857143], 'Party Republica': [1, 8, 0.125, 2.7178571428571425], 'Party Republican': [1, 8, 0.125, 2.7178571428571425]},
{'C': [0, 0, 0.0, 0.0], 'Ca': [0, 0, 0.0, 0.0], 'Can': [0, 0, 0.0, 0.0], 'Cand': [0, 0, 0.0, 0.0], 'Candi': [0, 0, 0.0, 0.0], 'Candid': [0, 0, 0.0, 0.0], 'Candida': [0, 0, 0.0, 0.0], 'Candidat': [0, 0, 0.0, 0.0], 'Candidate': [0, 0, 0.0, 0.0], 'Candidate ': [0, 0, 0.0, 0.0], 'Candidate D': [0, 0, 0.0, 0.0], 'Candidate De': [0, 0, 0.0, 0.0], 'Candidate Dem': [2, 0, 0.29166666666666663, 0.0], 'Candidate Demo': [3, 0, 0.46785714285714286, 0.0], 'Candidate Democ': [3, 0, 0.726190476190476, 0.0], 'Candidate Democr': [3, 0, 0.726190476190476, 0.0], 'Candidate Democra': [3, 0, 0.726190476190476, 0.0], 'Candidate Democrat': [3, 0, 0.7499999999999999, 0.0], 'Candidate Democrati': [7, 0, 2.4678571428571425, 0.0], 'Candidate Democratic': [7, 0, 2.4678571428571425, 0.0]},
{'C': [0, 0, 0.0, 0.0], 'Ca': [0, 0, 0.0, 0.0], 'Can': [0, 0, 0.0, 0.0], 'Cand': [0, 0, 0.0, 0.0], 'Candi': [0, 0, 0.0, 0.0], 'Candid': [0, 0, 0.0, 0.0], 'Candida': [0, 0, 0.0, 0.0], 'Candidat': [0, 0, 0.0, 0.0], 'Candidate': [0, 0, 0.0, 0.0], 'Candidate ': [0, 0, 0.0, 0.0], 'Candidate R': [0, 0, 0.0, 0.0], 'Candidate Re': [0, 0, 0.0, 0.0], 'Candidate Rep': [0, 1, 0.0, 0.5], 'Candidate Repu': [0, 8, 0.0, 2.7178571428571425], 'Candidate Repub': [0, 8, 0.0, 2.7178571428571425], 'Candidate Republ': [0, 8, 0.0, 2.7178571428571425], 'Candidate Republi': [0, 8, 0.0, 2.7178571428571425], 'Candidate Republic': [0, 8, 0.0, 2.7178571428571425], 'Candidate Republica': [0, 8, 0.0, 2.7178571428571425], 'Candidate Republican': [0, 8, 0.0, 2.7178571428571425]},
{'P': [0, 0, 0.0, 0.0], 'Po': [0, 0, 0.0, 0.0], 'Pol': [0, 0, 0.0, 0.0], 'Poli': [0, 0, 0.0, 0.0], 'Polit': [0, 0, 0.0, 0.0], 'Politi': [0, 0, 0.0, 0.0], 'Politic': [0, 0, 0.0, 0.0], 'Politics': [0, 0, 0.0, 0.0], 'Politics ': [0, 0, 0.0, 0.0], 'Politics D': [0, 0, 0.0, 0.0], 'Politics De': [0, 0, 0.0, 0.0], 'Politics Dem': [1, 2, 0.14285714285714285, 0.34285714285714286], 'Politics Demo': [1, 2, 0.14285714285714285, 0.34285714285714286], 'Politics Democ': [1, 2, 0.16666666666666666, 0.3666666666666667], 'Politics Democr': [1, 2, 0.16666666666666666, 0.3666666666666667], 'Politics Democra': [1, 2, 0.16666666666666666, 0.3666666666666667], 'Politics Democrat': [6, 2, 1.2178571428571427, 0.8333333333333333], 'Politics Democrati': [3, 2, 1.5833333333333333, 1.1666666666666667], 'Politics Democratic': [3, 2, 1.75, 1.2]},
{'P': [0, 0, 0.0, 0.0], 'Po': [0, 0, 0.0, 0.0], 'Pol': [0, 0, 0.0, 0.0], 'Poli': [0, 0, 0.0, 0.0], 'Polit': [0, 0, 0.0, 0.0], 'Politi': [0, 0, 0.0, 0.0], 'Politic': [0, 0, 0.0, 0.0], 'Politics': [0, 0, 0.0, 0.0], 'Politics ': [0, 0, 0.0, 0.0], 'Politics R': [0, 0, 0.0, 0.0], 'Politics Re': [0, 0, 0.0, 0.0], 'Politics Rep': [0, 2, 0.0, 0.29166666666666663], 'Politics Repu': [0, 4, 0.0, 2.083333333333333], 'Politics Repub': [0, 4, 0.0, 2.083333333333333], 'Politics Republ': [0, 4, 0.0, 2.083333333333333], 'Politics Republi': [0, 4, 0.0, 2.083333333333333], 'Politics Republic': [0, 4, 0.0, 2.083333333333333], 'Politics Republica': [0, 5, 0.0, 2.283333333333333], 'Politics Republican': [0, 8, 0.0, 2.7178571428571425]},
{'P': [0, 0, 0.0, 0.0], 'Po': [0, 0, 0.0, 0.0], 'Pol': [0, 0, 0.0, 0.0], 'Poli': [0, 0, 0.0, 0.0], 'Polit': [0, 0, 0.0, 0.0], 'Politi': [0, 0, 0.0, 0.0], 'Politic': [0, 0, 0.0, 0.0], 'Politica': [0, 0, 0.0, 0.0], 'Political': [0, 0, 0.0, 0.0], 'Political ': [0, 0, 0.0, 0.0], 'Political N': [0, 0, 0.0, 0.0], 'Political Ne': [0, 0, 0.0, 0.0], 'Political New': [0, 0, 0.0, 0.0], 'Political News': [0, 0, 0.0, 0.0], 'Political News ': [0, 0, 0.0, 0.0], 'Political News D': [0, 0, 0.0, 0.0], 'Political News De': [0, 0, 0.0, 0.0], 'Political News Dem': [0, 0, 0.0, 0.0], 'Political News Demo': [0, 0, 0.0, 0.0], 'Political News Democ': [0, 0, 0.0, 0.0], 'Political News Democr': [0, 0, 0.0, 0.0], 'Political News Democra': [0, 0, 0.0, 0.0], 'Political News Democrat': [0, 0, 0.0, 0.0], 'Political News Democrati': [0, 0, 0.0, 0.0], 'Political News Democratic': [0, 0, 0.0, 0.0]},
{'P': [0, 0, 0.0, 0.0], 'Po': [0, 0, 0.0, 0.0], 'Pol': [0, 0, 0.0, 0.0], 'Poli': [0, 0, 0.0, 0.0], 'Polit': [0, 0, 0.0, 0.0], 'Politi': [0, 0, 0.0, 0.0], 'Politic': [0, 0, 0.0, 0.0], 'Politica': [0, 0, 0.0, 0.0], 'Political': [0, 0, 0.0, 0.0], 'Political ': [0, 0, 0.0, 0.0], 'Political N': [0, 0, 0.0, 0.0], 'Political Ne': [0, 0, 0.0, 0.0], 'Political New': [0, 0, 0.0, 0.0], 'Political News': [0, 0, 0.0, 0.0], 'Political News ': [0, 0, 0.0, 0.0], 'Political News R': [0, 0, 0.0, 0.0], 'Political News Re': [0, 1, 0.0, 0.125], 'Political News Rep': [0, 1, 0.0, 0.25], 'Political News Repu': [0, 1, 0.0, 1.0], 'Political News Repub': [0, 1, 0.0, 1.0], 'Political News Republ': [0, 1, 0.0, 1.0], 'Political News Republi': [0, 1, 0.0, 1.0], 'Political News Republic': [0, 1, 0.0, 1.0], 'Political News Republica': [0, 1, 0.0, 1.0], 'Political News Republican': [0, 1, 0.0, 1.0]}]

# unweighted_keys = list(unweighted.keys())
# counter = 1
# for old_key in unweighted_keys:
#     print(old_key)
#     unweighted[counter] = unweighted[old_key]
#     unweighted.pop(old_key, None)
#     counter += 1
#
# lists = sorted(unweighted.items())
# x, y = zip(*lists)  # unpack a list of pairs into two tuples
#
# weighted_keys = list(weighted.keys())
# counter = 1
# for old_key in weighted_keys:
#     print(old_key)
#     weighted[counter] = weighted[old_key]
#     weighted.pop(old_key, None)
#     counter += 1
#
# for key in weighted_keys:
#     if key[-2:] not in unweighted_keys:
#         print("*found: %s" % key)
#
# lists1 = sorted(weighted.items())
# x1, y1 = zip(*lists1)
#
# weighted_keys = list(four_am_weighted.keys())
# counter = 1
# for old_key in weighted_keys:
#     print(old_key)
#     four_am_weighted[counter] = four_am_weighted[old_key]
#     four_am_weighted.pop(old_key, None)
#     counter += 1
#
# for key in weighted_keys:
#     if key[-2:] not in unweighted_keys:
#         print("*found: %s" % key)
#
# lists2 = sorted(four_am_weighted.items())
# x2, y2 = zip(*lists2)
#
# plt.xticks(rotation=90)
# plt.ylim([-0.07, 0.01])
# plt.axhline(y=0.0, color='grey', linestyle=':')
# plt.xlabel("States")
# plt.ylabel("Search Engine Bias")
#
#
# def newline(p1, p2, color='skyblue'):
#     ax = plt.gca()
#     if p1[1] < p2[1]:
#         color = 'lightsalmon'
#     l = mlines.Line2D([p1[0], p2[0]], [p1[1], p2[1]], color=color)
#     ax.add_line(l)
#     return l


# fig, ax = plt.subplots(1,1,figsize=(14,14))
# ax.scatter(y=y1, x=x1, s=50, color='blue', alpha=0.7, label='8pm')
# ax.scatter(y=y2, x=x1, s=50, color='red', alpha=0.7, label='4am')
# ax.set_ylim([-0.06, -0.02])
# ax.set_xlabel('States')
# ax.set_ylabel('Bing Search Bias')
# ax.legend()
# # Line Segments
# for i, p1, p2 in zip(x1, y1, y2):
#     newline([i, p1], [i, p2])


fig, axs = plt.subplots(2, 3)
# fig.suptitle("Google's Auto complete bias")
auto_complete_words = ['US Election *',
'US Political Party *',
'Party *',
'Candidate *',
'Politics *',
'Political News *']
counter = 0
unweighted_scores_dem = []
for phrase in ddg_ac_scores:
    if counter % 2 == 0:
        unweighted_scores_dem = [value[0] for key, value in phrase.items()]
    else:
        unweighted_scores_rep = [value[1] for key, value in phrase.items()]
        dem_x_range = np.arange(1, len(unweighted_scores_dem)+1)
        rep_x_range = np.arange(1, len(unweighted_scores_rep)+1)
        x_idx = math.floor(counter/6)
        y_idx = counter % 3
        # if counter == 0:
        #     axs = axs1
        # elif counter == 1:
        #     axs = axs2
        # elif counter == 2:
        #     axs = axs3
        # elif counter == 3:
        #     axs = axs4
        # elif counter == 4:
        #     axs = axs5
        # elif counter == 5:
        #     axs = axs6
        # axs[x_idx, y_idx].yaxis.set_major_locator(MaxNLocator(integer=True))
        axs[x_idx, y_idx].set_ylim([0, 11])
        axs[x_idx, y_idx].plot(dem_x_range, unweighted_scores_dem, color='dodgerblue',
                 label='Democratic Suggestions')
        axs[x_idx, y_idx].plot(rep_x_range, unweighted_scores_rep, color='indianred',
                 label='Republican Suggestions')
        axs[x_idx, y_idx].set_title(auto_complete_words[math.floor(counter/2)])
        # axs[x_idx, y_idx].set_ylabel('Suggestions')
        # axs[x_idx, y_idx].xaxis.set_ticks(np.arange(min(dem_x_range), max(dem_x_range)
        #                                             + 1, 5))
    counter = counter+1


# plt.ylim([-0.06, 0.01])
# plt.plot(ddg_x, ddg_y, color='red', marker='^', markerfacecolor='none', linestyle = '',
#          label='DuckDuckGo')
# plt.plot(b_select_x, b_select_y, color='blue', marker='^', markerfacecolor='none',
#          linestyle='',
#          label='Bing')
# plt.plot(g_select_x, g_select_y, color='orange', marker='^', markerfacecolor='none',
#          linestyle='',
#          label='Google')
# plt.legend(loc="upper left")
# zip joins x and y coordinates in pairs
plt.show()
