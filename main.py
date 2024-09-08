from Game import Game
import argparse
import os
from tqdm import tqdm

# Parse arguments
parser = argparse.ArgumentParser(description='Process arguments about an NBA game.')
parser.add_argument('--path', type=str,
                    help='a path to json file to read the events from',
                    required=True)
parser.add_argument('--event', type=int, default=0,
                    help="""an index of the event to create the animation to
                            (the indexing start with zero, if you index goes beyond out
                            the total number of events (plays), it will show you the last
                            one of the game)""")
parser.add_argument('--gif', action='store_true',
                    help='Create a GIF of the event')
parser.add_argument('--out_dir', type=str, default="output_training_files",
                    help="name of output directory")

args = parser.parse_args()

# Ensure the output directory exists
os.makedirs(args.out_dir, exist_ok=True)

# Define the output filename
parent_dir = os.path.basename(os.path.dirname(args.path))
basename = os.path.basename(args.path)
output_filename = args.out_dir + "/" + parent_dir + ".txt"

# Initialize the Game object
game = Game(path_to_json=args.path, event_index=args.event, output=output_filename)

# Get the last index
last_index = game.get_last_index()

# Process events with tqdm progress bar
for i in tqdm(range(0, last_index), desc="Processing events", unit="event"):
    try:
        game = Game(path_to_json=args.path, event_index=i, output=output_filename)
        game.read_json()
        game.start(create_gif=args.gif)
    except Exception as e:
        continue

