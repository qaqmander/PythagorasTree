# PythagorasTree

Draw Pythagoras tree concurrently with turtle.

Use coroutine to simulate scheduler with rr algorithm because turtle doesn't support multithread.

## Try

    git clone git@github.com:qaqmander/PythagorasTree.git && cd PythagorasTree && python3 pyth_tree.py
    
## To be improved...

Maybe each edge should cost same time in one step... But who cares?

Bad code style especially in generator definition because I haven't find good solution for it. It can't work if using traditional function to wrap `yield` obviously. Miss macro so much :( 
