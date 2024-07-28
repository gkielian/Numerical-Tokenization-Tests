# NBA Player Movements

This is a script for visualization of NBA games from raw SportVU logs.

If you admire both Spurs' and Warriors' ball movement, Brad Stevens' playbook, or just miss KD in OKC you'll find this entertaining.

## Examples

![Spurs](https://github.com/linouk23/NBA-Player-Movements/blob/master/examples/spurs.gif)
![Warriors](https://github.com/linouk23/NBA-Player-Movements/blob/master/examples/warriors.gif)
![Celtics](https://github.com/linouk23/NBA-Player-Movements/blob/master/examples/celtics.gif)
![Durant](https://github.com/linouk23/NBA-Player-Movements/blob/master/examples/durant.gif)

## Usage

1. Clone this repo:

  ```bash
  $ git clone https://github.com/linouk23/NBA-Player-Movements
  ```

2. Choose any NBA game from `data/2016.NBA.Raw.SportVU.Game.Logs` directory.

3. Generate an animation for the play by running the following script:

  ```bash
  $ python3 main.py --path=Celtics@Lakers.json --event=140
  ```

  ```
  required arguments:
    --path PATH    a path to json file to read the events from

  optional arguments:
    --event EVENT  an index of the event to create the animation to
                   (the indexing start with zero, if you index goes beyond out
                   the total number of events (plays), it will show you the last
                   one of the game)
    -h, --help     show the help message and exit
  ```

## Tokenization

# CSV Tokenization

will have equal value frames

Category tokens:
team: 1 of 30 tokens -- unique

Utilize, rotary position embeddings (trying fire too), as we already mark time with "Numeric tokens"
(Mess with the order so we can try krmsnorm too)

Numeric Tokens:
scores: zero-padded decimal
score difference: zero-padded decimal
shotclock: zero-padded decimal
gameclock: zero-padded decimal
quarter: decimal

Using zero padded decimal, for possibility that decimal things like reaching
triple digits might have psychological effects.

Of course we'll also do split digits

Quantized Locations:

possibly multiple representations

1. map of board in grid only
2. map of the board in hex only
3. numerical representation only
4. "pocket" world models (build visual model, context length expense, but train
   to active printing this only if a specific token prefix after newline. This
   will ensure the model still has this world model, and can use for prediction,
   but doesn't waste context space, can just "keep in mind" and make predictions on deltas.)
5. vector tokens only -- might be one of the easiest ways to start
6. csv of values paired with ascii-fied image of the plays (play with different quantization, and coordinates)

ball:
players
player number

Hoop:
after first pass, try to label with the team for that quarter.

Different ways to the location.
probably good is to build in understanding of the different zones.
Tokens
r, theta + R, Phi

time quantization
=

# Vector tokenization

x, y tokenization (best probably to have this from the center)
r, theta, from left hoop
R, Phi, from right hoop

# Training settings

as long a context as possible

### Presentation

Presentation could include the Famous Mistral Doom hackathon of San Francisco.

Follow-up experiments fine-tuning the method for MNIST, Rubiks Cubes, then games like chess...

Realization this has potential for quickly adapting LLMs for 2d world models.
*We can directly teach LLMs quickly to build world models, asking them to draw
pictures.*



Story of Dr. Feynmann, inspiration from fun with Cafeteria Plates to Quantum ElectroDynamics/Physics Nobel Prize
And of course this is hella fun : )

# Labels

left court, right court
inside 3 point line
inside key

# MVP

## ASCII

Setting up for pocket world models:
T: quarter, clock time, shotclock time
I: court image
C: player locations
B: ball location

randomize the order of the last three.

court image, shotclock and
ball with height (quantized)
players with unique symbols


## Vector

numerics in wallclock - also serves as position embedding (try with and without rope)
10x team symbol, player_token, (x,y from center) x, y, r from left hoop, r from right hoop
basket ball location, x,y,z, x,y,r left hoop, x,y,r right hoop

