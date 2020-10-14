## ESPN Fantasy Football Power Rankings

Currently using this module to do most of the heavy lifting: https://github.com/cwendt94/espn-api

Pull ESPN Fantasy Football league info, generate standings and power rankings, format it into crude HTML, and ship it out via email to a list of email addresses (using yagmail module)

Output email is pre-formatted with power rankings list including rank, team name, owner name, current record, and total season points scored. Below each team is a table that contains:
- Dominance score (more info below)
- Standings position (and previous position if we're past week 1)
- Season points, points against, and differential
- Previous game info including result, score, bench points, opponent, and opponent points
- Breakdown of best and worst performing players from last week's game
- List of any "goose eggs" - starting players who scored 0 or less points
- List of any "outstanding benchwarmers" - bench players that scored 25+ points AND outscored a starter in a position they could have played in
- Information about the next opponent (unless the season is over)

Output email also includes a small header section with highest and lowest scoring teams as well as info about best and worst performing players as well as the teams they are on

### Dominance scores

Dominance scores are calculated using the `league.power_rankings()` function provided by the `espn-api` module. The dominance score is calculated as follows:
1. a 2-step dominance matrix function is run across all matchups for the entire league
2. The output of that function for each team is multiplied by `0.8`
3. Total season points for each team is multiplied by `0.15`
4. Average margin of victory for each team is multiplied by `0.05`
5. Those three values are added together to create the dominance score for a given team

## Required modules

This script requires the following modules to be installed:

ESPN-API: https://github.com/cwendt94/espn-api - `pip install espn-api`  
YagMail: https://pypi.org/project/yagmail/ - `pip install yagmail`

## User-provided variables

The following information needs to be provided in order to run this script:
- **_ESPN_LEAGUE_ID**: found in the URL of your fantasy team
    - `https://fantasy.espn.com/football/team?leagueId=XXXXXXX&teamId=XX&seasonId=2020`
- **_ESPN_S2**: used for authentication for private leagues - more info below
- **_ESPN_SWID**: used for authentication for private leagues - more info below
- **_EMAIL_TO**: a comma-separated list of email addresses to send the power rankings to
- **_EMAIL_FROM**: the email address used to send the email. Yagmail is built to use GMail by default
- **_EMAIL_PASS**: password for the `_EMAIL_FROM` account. If using a GMail account with 2-factor auth enabled you will need to [generate an application password](https://support.google.com/accounts/answer/185833?hl=en)

These variables are currently passed in as environment variables to avoid defining them in source code

### ESPN S2 and SWID

Authenticating against the ESPN API using username and password is currently broken. Authentication must now be done using two cookies called `espn_s2` and `SWID`. The values for these two cookies can be found in Chrome DevTools (F12) under Applications -> Storage -> Cookies -> `https://www.espn.com` when logged into ESPN.com