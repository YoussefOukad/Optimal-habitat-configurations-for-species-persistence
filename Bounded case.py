import random
import numpy as np
import math

def draw_grid(n,nr,nc,g): #n is n+ in the article
  # Create a grid of all white squares
  grid = [['.' for i in range(nr)] for j in range(nc)]

  # Randomly select n squares to be shaded black (habitat) symbolized as #
  L = [[]]
  for i in range(n):
    x = random.randint(0, nr-1)
    y = random.randint(0, nc-1)
    if [x,y] != L[i]:
        L.append([x,y])
        grid[x][y] = g
    else:
      while [x,y] == L[i]:
        x = random.randint(0, nr-1)
        y = random.randint(0, nc-1)
      L.append([x,y])
      grid[x][y] = g

  return grid

def print_grid(grid):
  for row in grid:
    for square in row:
      print(square, end=' ')
    print()


def habitat_abundance(n,nr,nc): #h
  return n/nr*nc

#So far, we have only randomly generated the habitat n+ on our space without taking in consideration the Fisher-Kolmogorov dynamics.

#The following two functions set the stage for incorporating the F-K equation dynamics ie; diffusion and reaction separately.

def diffusivity(grid, n, D, t):#We model the diffusion phenomenon as a random walk with step proportional to D
  habitat_coordinates = [[i,j] for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == '#']
  for m in range(t):
    for k in range(n):
      grid[habitat_coordinates[k][0]][habitat_coordinates[k][1]] = '.'
      habitat_coordinates[k][0] += random.choice([-D,D])
      habitat_coordinates[k][1] += random.choice([-D,D])
      grid[habitat_coordinates[k][0]][habitat_coordinates[k][1]] = '#'
    return grid


def growth_rate(grid,nc,nr,n,b,m,nu):#nu = growth rate = birth rate - mortality rate
  empty_coordinates = [[i,j] for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == '.']
  habitat_coordinates = [[i,j] for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == '#']
  if nu == 0:
      pass
  if nu > 0:
    for k in range(b): # r is necessarily smaller than or equal to nc*nr - n
      grid[empty_coordinates[random.randint(0,nc*nr-n)][0]][empty_coordinates[random.randint(0,nc*nr-n)][1]] = '#'
  if nu < 0:
    for s in range(m):# m is necessarily smaller than or equal to n
      grid[habitat_coordinates[random.randint(0,n)][0]][habitat_coordinates[random.randint(0,n)][1]] = '.'



def move_left(grid,nc,nr):
   #Shift all the squares in each row to the left
  for i in range(nr):
    for j in range(1,nc):
        if grid[i][j] == '#' and grid[i][j-1] != '#':
            grid[i][j-1] = grid[i][j]
            grid[i][j] = '.'

def move_right(grid,nc,nr):
   #Shift all the squares in each row to the right
  for i in range(nr-4):
    for j in range(nc-1):
        if grid[i][j] == '#' and grid[i][j+1] != '#':
            grid[i][j+1] = grid[i][j]
            grid[i][j] = '.'


def move_down(grid,nc,nr):
   #Shift all the squares in each column to the down
  for i in range(nr-1):
    for j in range(nc):
        if grid[i][j] == '#' and grid[i+1][j] != '#':
            grid[i+1][j] = grid[i][j]
            grid[i][j] = '.'

def reduce(grid,nc,nr):
    for j in range(nr):
      move_down(grid,nc,nr)
    for k in range(nc):
      move_left(grid,nc,nr)
    for j in range(nr):
      move_right(grid,nc,nr)
    for j in range(nc):
      move_down(grid,nc,nr)
    for k in range(nc):
      move_left(grid,nc,nr)






def clustering_distance(grid): #Based off cluster analysis method in Machine Learning
  habitat_coordinates = [[i,j] for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == '#']
  F = []
  for i in range(len(habitat_coordinates)):
    distances = []
    for j in range(len(habitat_coordinates)):
      if j != i:
        x1, y1 = habitat_coordinates[i]
        x2, y2 = habitat_coordinates[j]
        distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        distances.append(distance)
    F.append(np.sum(distances)/len(distances))
  return np.sum(F)/len(F)


         #Such distance is inversely proportional to connectedness, and therefore to persistence

gridd = draw_grid(90, 20, 20,'#')
print("Before Rearrangement")
print_grid(gridd)
print(clustering_distance(gridd))
reduce(gridd,20,20)
print('\n',end= '')
print("After Rearrangement")
print_grid(gridd)
print(clustering_distance(gridd))




#The gist of the code is based off cluster analysis. The type of clustering used to measure persistence is hierarchical clustering. We assume that connectivity brings about persistence although the literature is pretty complex on that matter (sometimes the opposite is true; habitat fragmentation brings about species persistences). Hierarchical clustering is different from other clustering models in the sense that it capitalizes upon connectivity as a criterion for grouping objecs (in our case; habitat) together.

#the literature suggests that habitat fragmentation is detrimental to species persistence (but not biodiversity) in the case of single-species models which is the case here.
