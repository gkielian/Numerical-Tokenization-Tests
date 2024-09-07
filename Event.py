import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from Constant import Constant
from Moment import Moment
from Team import Team
from PIL import Image
import imageio


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

    def generate_frame(self, moment_index):
        fig, ax = plt.subplots()
        ax.set_xlim(Constant.X_MIN, Constant.X_MAX)
        ax.set_ylim(Constant.Y_MIN, Constant.Y_MAX)
        ax.axis('off')

        start_moment = self.moments[moment_index]

        # Draw players and ball
        player_circles = [Circle((player.x, player.y), Constant.PLAYER_CIRCLE_SIZE, color=player.color)
                          for player in start_moment.players]
        ball_circle = Circle((start_moment.ball.x, start_moment.ball.y), Constant.PLAYER_CIRCLE_SIZE, color='orange')

        for circle in player_circles:
            ax.add_patch(circle)
        ax.add_patch(ball_circle)

        fig.canvas.draw()

        # Convert plot to numpy array
        width, height = fig.get_size_inches() * fig.get_dpi()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8').reshape(int(height), int(width), 3)
        plt.close(fig)
        return image

    def save_event_frame(self, file_path, create_ascii=False):
        with open(file_path, 'a') as file:
            for i in range(len(self.moments)):
                ascii_image = None
                if create_ascii:
                    image = self.generate_frame(i)
                    ascii_image = self.asciify_image(image)
                moment = self.moments[i]
                clock_text = 'Quarter {:d}, {:02d}:{:02d}, Shot Clock: {:03.1f}\n'.format(
                    moment.quarter,
                    int(moment.game_clock) % 3600 // 60,
                    int(moment.game_clock) % 60,
                    moment.shot_clock)

                player_locations = "Player locations: " + ", ".join(
                    f"{'H' if idx < 5 else 'A'}{idx%5}: ({player.x:.1f}, {player.y:.1f})"
                    for idx, player in enumerate(moment.players)
                ) + "\n"

                ball_location = f"Ball location: ({moment.ball.x:.1f}, {moment.ball.y:.1f}, {moment.ball.radius:.1f})\n"

                file.write(f"Moment {i + 1}:\n")
                file.write(clock_text)
                file.write(player_locations)
                file.write(ball_location)
                if create_ascii:
                    file.write(ascii_image + "\n\n")

    def asciify_image(self, image, width=80):
        gray_image = np.dot(image[..., :3], [0.2989, 0.587, 0.114])
        height, original_width = gray_image.shape
        aspect_ratio = height / float(original_width)
        new_height = int(aspect_ratio * width * 0.55)
        resized_gray_image = np.array(Image.fromarray(gray_image).resize((width, new_height)))

        chars = np.array(list(' .:-=+*#%@'))
        bins = np.linspace(0, 255, len(chars) + 1)
        ascii_image = np.clip(np.digitize(resized_gray_image, bins) - 1, 0, len(chars) - 1)
        ascii_art = "\n".join("".join(chars[pixel] for pixel in row) for row in ascii_image)

        return ascii_art

    def save_gif(self, gif_path):
        frames = []
        for i in range(len(self.moments)):
            image = self.generate_frame(i)
            frames.append(image)
        imageio.mimsave(gif_path, frames, duration=0.1)  # You can adjust the duration as needed

# Usage example:
# event = load_your_event_data_somehow()
# event_instance = Event(event)
# event_instance.save_ascii_image('game_ascii_art.txt')
# event_instance.save_gif('game_animation.gif')

