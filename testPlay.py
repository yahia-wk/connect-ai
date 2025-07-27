import board
import game
import player
import randomPlayer
from datetime import datetime
import csv
import time
import itertools
import multiprocessing as mp


def gatherData(isPruning, boardSize):
    boardSizeDict = boardSizeDict = { 1: (6,7,4,1),
                      2: (6,7,4,2),
                      3: (6,7,4,3),
                      4: (6,7,4,4),
                      5: (6,7,4,5),
                      6: (6,7,4,6),
                      7: (6,7,4,7)}
    
    seed = datetime.now().timestamp()
    p1 = player.Player("X", depth=boardSizeDict[boardSize][3])
    #p2 = player.Player("O", depth=3)
    p2 = randomPlayer.RandomPlayer("O", seed)

    g  = game.Game(p1, p2, boardSizeDict[boardSize][0], boardSizeDict[boardSize][1], boardSizeDict[boardSize][2])
    start = time.time()
    result = g.playGame(isPruning)
    end = time.time()

    return [result, p1.numExpanded, p1.numPruned, isPruning, boardSize, end-start]

def worker(args):
    return gatherData(*args)

def print_progress(iteration, total, bar_length=100):
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    print(f"\rProgress: |{bar}| {percent}% done", end='\n')
    if iteration == total: 
        print()

def main():
    isPruningOptions = [True]
    boardSizeOptions = [1,2,3,4,5,6,7]

    combinations = [(isPruning, boardSize) for isPruning in isPruningOptions for boardSize in boardSizeOptions]

    #repeat each combination a 1000 times
    tasks = combinations * 100
    totalTasks = len(tasks)

    #multiprocessing
    pool = mp.Pool()
    results = []
    for i, _ in enumerate(pool.imap_unordered(worker, tasks), 1):
        print_progress(i, totalTasks)
        results.append(_)

    pool.close()
    pool.join() 

    #write results to csv
    with open('test4depth.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["result", "numExpanded", "numPruned", "isPruning", "boardSize", "time"])
        writer.writerows(results)
        
    
if __name__ == "__main__":
    main()


#TODO make a test that first ONLY checks witn board size with constant winNum | DONE
    '''boardSizeDict = {'first': (4,5,4),
                     'second': (5,6,4),
                     'third': (6,7,4),
                     'fourth': (7,8,4),
                     'fifth': (8,9,4),
                     'sixth': (9,10,4)} THESE ARE THE BOARDS USED FOR TEST 1
                     SAMPLE SIZE IS 550
                     
                     other opponent: sample size: 50
                     
                     optimised AB intel: 100
                     
                     optimised random opp: 500'''
#TODO make a test that checks winNum with constant board size
    '''DID a test sample size of 550
    boardSizeDict = { 3: (7,8,3),
                      4: (7,8,4),
                      5: (7,8,5),
                      6: (7,8,6)}
                      Sample size with intekkeginet one : 50
                      
                      AB optimised: 100'
                      
                      AB random OPP: 500'''
#TODO make a test that checks both winNum and board size (small, medium, large game)
    ''' SAMPLE SIZE 550
    boardSizeDict = { 'small': (3,3,2),
                      'medium': (6,7,4),
                      'large': (9,10,7)}
    intelligent opponent sample size: 50
                      AB optimised intel: 100
                      
                      AB opt random: 500'''
#TODO variable depth effect 
    '''Sample Size of 550
    boardSizeDict = { 1: (6,7,4,1),
                      2: (6,7,4,2),
                      3: (6,7,4,3),
                      4: (6,7,4,4),
                      5: (6,7,4,5),
                      6: (6,7,4,6),
                      7: (6,7,4,7)}
                      
        AB optimised intel opponent: 100 REDOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'''
#TODO make test that compares the two evaluation functions, (time to win and nodesExpanded)
    ''' DONE SAMPLE SIZE 500'''
#TODO make two AI players play against each other and see who wins  and see if going first makes a difference