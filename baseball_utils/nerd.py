"""nerd.py: script to download data and calculate NERD scores

Pitcher Formula:
    Components:
        - xFIP-
        - Swinging-Strike Rate (SwStrk)
        - Strike Rate (Strk)
        - Velocity (Velo)
        - Age
        - Pace
        - ERA- - xFIP- (Luck)
        - Knuckleball Rate (KN)

    N = (zxFIP-*2) + (zSwStrk/2) + (zStrk/2) + zVelo + zAge + (zPace/2) +
        (Luck/20) + (KN*5) + Constant
    Constant ~= 3.8

    population: pitchers w/ 20+ IP
    velo, age, luck: always positive
    velo, age: capped at 2.0
    luck: capped at 1.0

Team Formula:
    Components:
        - Park-Adjusted Batting Runs Above Average (Bat)
        - Park-Adjusted Home Run Rate (HR%)
        - Baserunning Runs (BsR)
        - Bullpen xFIP (Bull)
        - Defensive Runs (Def)
        - Payroll, where below average is better (Pay)
        - Batter Age, where younger is better (Age)
        - Expected Wins, Per WAR, Minus Actual Wins (Luck)

    N = zBat + zHR% + (zBull/2) + (zDef/2) + (zDef/2) + zPay + zAge +
        (Luck/2) + Constant
    Constant ~= 4.0

    pay, age, luck: always positive
    luck: capped at 2.0
"""
from datetime import datetime
from urllib.parse import urlencode

from requests_html import HTMLSession, HTMLResponse
from splinter import Browser

FG_BASE = 'https://www.fangraphs.com'
YEAR = datetime.now().year
MIN_IP = 20

session = HTMLSession()


def csv_payload(res: HTMLResponse):
    asp = res.html.find('.aspNetHidden')
    payload = {}
    for elem in asp:
        for inp in elem.find('input'):
            payload[inp.attrs['name']] = inp.attrs['value']
    return payload


def pitchers(season: int = YEAR, ip: int = MIN_IP, stat_type: int = 8):
    url = FG_BASE + '/leaders.aspx'
    params = {
        'pos': 'all',
        'stats': 'pit',
        'lg': 'all',
        'qual': ip,
        'type': stat_type,
        'season': season,
    }
    res = session.get(url, params=params)
    payload = csv_payload(res)
    res = session.post(url, params=params, data=payload)


def splinter_test():
    base_url = FG_BASE + '/leaders.aspx'
    params = {
        'pos': 'all',
        'stats': 'pit',
        'lg': 'all',
        'qual': 20,
        'type': 8,
        'season': 2018,
    }
    url = base_url + '?' + urlencode(params)
    print(url)
    with Browser('chrome') as browser:
        browser.visit(url)
        browser.click_link_by_partial_text('Export Data')


def main():
    # pitchers()
    splinter_test()


if __name__ == '__main__':
    main()
