import datetime
from typing import List

from ..base_league import BaseLeague
from .team import Team
from .player import Player
from .matchup import Matchup
from .box_score import BoxScore
from .activity import Activity


class League(BaseLeague):
    '''Creates a League instance for Public/Private ESPN league'''

    def __init__(self, league_id: int, year: int, espn_s2=None, swid=None, username=None, password=None, debug=False):
        super().__init__(league_id=league_id, year=year, sport='nhl', espn_s2=espn_s2, swid=swid, username=username,
                         password=password, debug=debug)

        data = self._fetch_league()
        self._fetch_teams(data)

    def _fetch_league(self):
        data = super()._fetch_league()
        self.start_date = datetime.datetime.fromtimestamp(
            min([i[1][1] / 1000 for i in self._get_pro_schedule(1).items()])).date()
        self._fetch_players()
        self._map_matchup_ids(data['schedule'])
        return (data)

    def _map_matchup_ids(self, schedule):
        self.matchup_ids = {}
        for match in schedule:
            matchup_period = match.get('matchupPeriodId')
            scoring_periods = match['home'].get('pointsByScoringPeriod', {}).keys()
            if len(scoring_periods) > 0:
                if matchup_period not in self.matchup_ids:
                    self.matchup_ids[matchup_period] = sorted(scoring_periods)
                else:
                    self.matchup_ids[matchup_period] = sorted(
                        set(self.matchup_ids[matchup_period] + list(scoring_periods)))

    def _fetch_teams(self, data):
        '''Fetch teams in league'''
        pass

    def standings(self) -> List[Team]:
        pass

    def scoreboard(self, matchupPeriod: int = None) -> List[Matchup]:
        '''Returns list of matchups for a given matchup period'''
        pass

    def get_team_data(self, team_id: int) -> Team:
        pass

    def recent_activity(self, size: int = 25, msg_type: str = None) -> List[Activity]:
        '''Returns a list of recent league activities (Add, Drop, Trade)'''
        pass

    def free_agents(self, week: int = None, size: int = 50, position: str = None, position_id: int = None) -> List[
        Player]:
        '''Returns a List of Free Agents for a Given Week\n
        Should only be used with most recent season'''
        pass

    def box_scores(self, matchup_period: int = None, scoring_period: int = None, matchup_total: bool = True) -> List[
        BoxScore]:
        '''Returns list of box score for a given matchup or scoring period'''
        pass
