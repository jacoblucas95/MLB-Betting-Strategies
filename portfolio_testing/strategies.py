# Team Bets

def home(game):
    return 'h'

def visitor(game):
    return 'v'

def home_underdogs_ml(game):
    if game.visitor_team_is_money_line_favorite:
        return 'h'
    else:
        return None

def visitor_underdogs_ml(game):
    if game.visitor_team_is_money_line_favorite:
        return None
    else:
        return 'v'

def home_favorites_ml(game):
    if game.visitor_team_is_money_line_favorite:
        return None
    else:
        return 'h'

def visitor_favorites_ml(game):
    if game.visitor_team_is_money_line_favorite:
        return 'v'
    else:
        return None

def home_underdogs_rl(game):
    if game.visitor_team_is_run_line_favorite:
        return 'h'
    else:
        return None

def visitor_underdogs_rl(game):
    if game.visitor_team_is_run_line_favorite:
        return None
    else:
        return 'v'

def home_favorites_rl(game):
    if game.visitor_team_is_run_line_favorite:
        return None
    else:
        return 'h'

def visitor_favorites_rl(game):
    if game.visitor_team_is_run_line_favorite:
        return 'v'
    else:
        return None

def longshot_teams_ml(game):
    if game.underdog_money_line_close >= 200:
        return 'dog'
    else:
        return None

def longshot_teams_rl(game):
    if game.underdog_run_line_odds_close >= 200:
        return 'dog'
    else:
        return None

# Game Bets

def overs(game):
    return 'o'

def unders(game):
    return 'u'

def favorites(game):
    return 'fav'

def underdogs(game):
    return 'dog'









