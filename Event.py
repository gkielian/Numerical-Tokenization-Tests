import numpy as np
from Constant import Constant
from Moment import Moment
from Team import Team

class Event:
    """A class for handling and showing events"""

    def __init__(self, event):
        moments = event['moments']
        self.moments = [Moment(moment) for moment in moments]
        home_players = event['home']['players']
        guest_players = event['visitor']['players']
        players = home_players + guest_players
        player_ids = [player['playerid'] for player in players]
        player_names = [" ".join([player['firstname'],
                        player['lastname']]) for player in players]
        player_jerseys = [player['jersey'] for player in players]
        values = list(zip(player_names, player_jerseys))
        # Example: 101108: ['Chris Paul', '3']
        self.player_ids_dict = dict(zip(player_ids, values))

    def bin_locations(self, x, y, x_min, x_max, y_min, y_max, x_bins, y_bins):
        x_bin = np.digitize(x, np.linspace(x_min, x_max, x_bins)) - 1
        y_bin = np.digitize(y, np.linspace(y_min, y_max, y_bins)) - 1
        return x_bin, y_bin

    def generate_ascii_frame(self, moment, x_bins, y_bins):
        court = np.full((y_bins, x_bins), '#')
        for i, player in enumerate(moment.players):
            x_bin, y_bin = self.bin_locations(player.x, player.y, Constant.X_MIN, Constant.X_MAX, Constant.Y_MIN, Constant.Y_MAX, x_bins, y_bins)
            symbol = str(i) if i < 5 else str(i - 5 + 5)  # Ensure the home team is 0-4, away team is 5-9
            court[y_bin, x_bin] = symbol

        ball_x_bin, ball_y_bin = self.bin_locations(moment.ball.x, moment.ball.y, Constant.X_MIN, Constant.X_MAX, Constant.Y_MIN, Constant.Y_MAX, x_bins, y_bins)
        court[ball_y_bin, ball_x_bin] = 'b'

        return "\n".join("".join(row) for row in court)

    def save_ascii_art(self, file_path, x_bins=200, y_bins=50):
        with open(file_path, 'w') as file:
            for i, moment in enumerate(self.moments):
                ascii_frame = self.generate_ascii_frame(moment, x_bins, y_bins)
                clock_text = 'Quarter {:d}, {:02d}:{:02d}, Shot Clock: {:03.1f}\n'.format(
                    moment.quarter,
                    int(moment.game_clock) % 3600 // 60,
                    int(moment.game_clock) % 60,
                    moment.shot_clock)
                file.write(f"Moment {i + 1}:\n")
                file.write(clock_text)
                file.write(ascii_frame + "\n\n")

# Usage example:
# event = load_your_event_data_somehow()
# event_instance = Event(event)
# event_instance.save_ascii_art('game_ascii_art.txt')

