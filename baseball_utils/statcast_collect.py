"""
Collect statcast (pitch F/X before 2015) data on a pitch-by-pitch level

Using requests and bs4

Snippet from baseballsavant.mlb.com/statcast_search

<div id="player_auto_complete">
    <label for="player_lookup">Players:</label>
    <select id="player_lookup" name="player_lookup[]">\
        <option></option>
        <option value="{MLB ID}">{LAST NAME}, {FIRST NAME}</option>
        ...
    </select>
</div>

Parse through the above to get player names/ids

Sequentially request data from 2008 to the present year

Problem: How do we tell who is a pitcher and who is a catcher?
"""

statcast_url = 'https://baseballsavant.mlb.com/statcast_search'

savant_headers = {
    'hfPt': '',
    'hfAB': '',
    'hfBBT': '',
    'hfPR': '',
    'hfZ': '',
    'stadium': '',
    'hfBBL': '',
    'hfNewZones': '',
    'hfGT': 'R|',
    'hfC': '',
    'hfSea': '2017|',  # Season: {Year} |*
    'hfSit': '',
    'player_type': 'pitcher',
    'hfOuts': '',
    'opponent': '',
    'pitcher_throws': '',
    'batter_stands': '',
    'hfSA': '',
    'game_date_gt': '',
    'game_date_lt': '',
    'player_lookup[]': 477132,
    'team': '',
    'position': '',
    'hfRO': '',
    'home_road': '',
    'hfFlag': '',
    'metric_1': '',
    'hfInn': '',
    'min_pitches': 0,
    'min_results': 0,
    'group_by': 'name',
    'sort_col': 'pitches',
    'player_event_sort': 'h_launch_speed',
    'sort_order': 'desc',
    'min_abs': 0,
    'type': 'details',
    'player_id': 477132,
}

csv_headers = {
    'all': True,
    'hfPt': '',
    'hfAB': '',
    'hfBBT': '',
    'hfPR': '',
    'hfZ': '',
    'stadium': '',
    'hfBBL': '',
    'hfNewZones': '',
    'hfGT': 'R|',  # R -> Regular season?
    'hfC': '',
    'hfSea': '2017|',  # Season: {year}|+
    'hfSit': '',
    'player_type': 'pitcher',
    'hfOuts': '',
    'opponent': '',
    'pitcher_throws': '',
    'batter_stands': '',
    'hfSA': '',
    'game_date_gt': '',
    'game_date_lt': '',
    'player_lookup[]': 477132,
    'team': '',
    'position': '',
    'hfRO': '',
    'home_road': '',
    'hfFlag': '',
    'metric_1': '',
    'hfInn': '',
    'min_pitches': 0,
    'min_results': 0,
    'group_by': 'name',
    'sort_col': 'pitches',
    'player_event_sort': 'h_launch_speed',
    'sort_order': 'desc',
    'min_abs': 0,
    'type': 'details'
}
