# obstruction
very simple text-based obstruction game with online mode

This is simple Obstruction game. You can choose with which symbol you
want to play and if you like to begin. Your opponent will be stupid AI
(at least for now). When somebody wins (you or AI) the game will ask if you
want to play another one.

### How to control the game:
    - every move you will choose coordinates (row col <both integers>),
        where to put your symbol
    - please make sure you separate them with any whitespace (eg. tab)
        but not newline (enter)
    - confirm your input with <enter> key
    example:
        if playground will look like this <Player O is AI>:

                0   1   2   3
              +---+---+---+---+
            0 |   | * | O | * |
              +---+---+---+---+
            1 |   | * | * | * |
              +---+---+---+---+
            2 |   |   |   |   |
              +---+---+---+---+
            3 |   |   |   |   |
              +---+---+---+---+

        and you want to place 'X' to the bottom left corner, then the
        coordinates of it would be: 3 (this is row, the <3> integer)
                                    0 (this is column, <0> integer)
        the game will ask for input, after your input: 3    0
        the playground will look like this:

                0   1   2   3
              +---+---+---+---+
            0 |   | * | O | * |
              +---+---+---+---+
            1 |   | * | * | * |
              +---+---+---+---+
            2 | * | * |   |   |
              +---+---+---+---+
            3 | X | * |   |   |
              +---+---+---+---+

This game also supports online mode, so you can play this game with your
friends (if you have any). The rules are the same as above, but the game
starts differently. You can create game with `--create` argument, which also 
requires `--port` (ports above 5000 pretends to be safe).  
e.g. `./obstruction.py --create --port 5050`  
Game will ask for your preferences and returns to you your public IP address,
which you can share with your friend also with the integer `port`.  
If you want to connect to already created game, use `--connect` argument with 
public IP address of your friend and also don't forget to use the `--port`.  
How to connect to the game above: `./obstruction --connect friend's_public_ip
--port 5050`  
### Update
    first of all if you want to create the game, you need to do port 
    forwarding and also the way how the online mode is done is not secure
    for you at all so I am working on alternative (I guess I will need
    remote host).
