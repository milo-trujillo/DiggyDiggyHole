# DiggyDiggyHole!

Idea: Multiplayer Dwarf-Fortress esque game.

## Overall design

Central server handles progression of time, world-gen, and AI.

Clients can connect to the server and ask for information about world state to view it

Clients can submit general fortress orders, such as "mine here, but a building here"

Orders are stored in some sort of list, no direct control over dwarves.

Time moves constantly as long as users are connected. (Determine that via UDP signature?)

## AI design

Idling dwarves pick a task at random from the list, if the task is impossible it is removed from the list.

After a period of time dwarves will look for a new job, with a higher chance of repeating the same task (maybe 2/3rds to start). This means miners will tend to continue mining, but may switch to another task if they get bored.

## Networking

Server sends out state with timestamps via UDP, prevents overload when lots of information moving.

Receives orders over UDP too? Less important, but would help with load if lots of users are connected.

## Time

Clock moves at fixed rate provided at least one client is connected. Connected is determined by a heartbeat. That is:

While clients are running they send a 'heartbeat' instruction every few seconds. Server maintains a dictionary of clients and how long it's been since they've sent a heartbeat. Every second that dictionary is examined, and all clocks increased by one. If user reaches 10 their entry is deleted. If there are zero entries, time is frozen.

This allows the game to progress in realtime regardless of player activity, but freeze if we all go to class.
