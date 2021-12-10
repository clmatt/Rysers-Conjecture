#Written in python3

import numpy as np

#This is the program which uses additional information about G_5
#Assume that the vertices are 0,..9, with no edges between (0,1),(2,3),etc.
#All without loss of generality arguments are based on the result that any pair of vertices must be adjacent to vertices in every pair of colors

#Wlog the vertex adjacent to both 2,3 in blue is 0
#Wlog the vertex adjacent to both 0,1 in red is 2
#Now, we have two cases : the vertex adjacent to 0 in red and 1 in blue is 3 or 4

#Can relatively easily be parallelized by splitting up values of i, as these aren't dependent on each other

#Don't Change this
parts = [2,2,2,2,2] 
numParts = len(parts)

#Create Adjacency Matrix, based on list of edges 'edges', and some subset of vertices, and the total number of vertices, 'n'
#The adjacency matrix will contain 0's outside our subset of vertices
#Note we actually pass vertices that we don't want in our adjacency matrix, 'Xc'
def createAdjMat(edges,Xc,n):
	A = np.zeros((n,n), dtype=int)
			
	
	for e in edges:
		A[e[0]][e[1]] = 1
		A[e[1]][e[0]] = 1
								
	#Remove edges outside of X from adjacency matrices
	for i in Xc:
		for j in range(n):
			A[i][j] = 0
			A[j][i] = 0
	
	return A
	
#Determines if an adjacency matrix on a subset of vertices X is diameter < 3 (returns 1) or diameter >= 3 (returns 0)
def diameter2(A,X):
	#Check if A is diameter < 3 (A^2 + A has no non-zero entries outside of X)
	A = np.matmul(A,A) + A
	
	XSize = len(X)
				
	output = 1 #= 0 if X[R] not diameter < 3
	for i in range(XSize):
		for j in range(i+1,XSize):
			if((A[X[i]][X[j]] == 0) and (output)):
				output = 0 #X[R] not diameter < 3
	
	return output

#Determine number of vertices and Edges
n = 0 #Vertices
m = 0 #Edges

for i in range(numParts):
	n = n + parts[i]
	
	for j in range(i+1,numParts):
		m = m + parts[i]*parts[j]
		
#Vertices are 0,1,2,...,n-1		

#Create a list of all edges
#That is, pairs of vertices where each vertex is in a different part
temp1 = 0
temp2 = 0
edges = []

for i in range(numParts-1):
	temp2 = temp2 + parts[i]
	for j in range(parts[i]):
		for k in range(temp2, n):
			edges.append([temp1,k])
		
		temp1 = temp1 + 1
		
#Iterate over all possible colorings of the edges R and B
#i is a number between 0 2^numEdges which in binary is an indicator for R
i = 0
while i < (1 << (m)): #1 << (m) = 2^m 
	#Uncomment to provide updates on number of iterations completed and remaining
	#if i % 1000000 == 0:
		#print(i, " colorings checked out of ", 1 << (m))

	#See note at begining of program
	#Need to run both cases
	if (i % 16 == 3) and (i & (1 << 10) == 0) and (i & (1 << 11) != 0):
	#if (i % 8 == 3) and (i & (1 << 4) == 0) and (i & (1 << 10) == 0) and (i & (1 << 12) != 0):
		#From i (our indicator in binary) create R and B, lists of the red and blue edges 
		R = []
		B = []
		adjMatR = np.zeros((10,10),int)
		adjMatB = np.zeros((10,10),int)
		
		for j in range(m):
			if(i & (1 << j) == 0): #& is bitwise and
				B.append(edges[j])
				adjMatB[edges[j][0]][edges[j][1]] = 1
				adjMatB[edges[j][1]][edges[j][0]] = 1
			else:
				R.append(edges[j])				
				adjMatR[edges[j][0]][edges[j][1]] = 1
				adjMatR[edges[j][1]][edges[j][0]] = 1
		
		lemma = 1
		#Check if every pair has path of length 2 in both colors
		j = 0
		while j < 5:
			rr = 0
			rb = 0
			br = 0
			bb = 0
			
			for k in range(10):
				if (k != 2*j) and (k != 2*j+1):
					if (adjMatR[2*j][k] == 1 ) and (adjMatR[2*j+1][k] == 1):
						rr = 1
							
					elif (adjMatR[2*j][k] == 1 ) and (adjMatB[2*j+1][k] == 1):
						rb = 1
							
					elif (adjMatB[2*j][k] == 1 ) and (adjMatR[2*j+1][k] == 1):
						br = 1	
							
					elif (adjMatB[2*j][k] == 1 ) and (adjMatB[2*j+1][k] == 1):
						bb = 1
							
			if (rr == 0) or (rb == 0) or (br == 0) or (bb == 0):
				lemma = 0
				j = 5	
					
			j = j+1
			
		#Only need to check if lemma == 1
		if (lemma == 1):
			#Val = 0 iff there is a coloring with no decomposition into monochromatic subgraphs of diameter 2
			val = 1
				
			#Now go through and check if any covering of the vertices (X U Y > V) is such that both X and Y are diameter 2 in some colors
			#j in binary is an indicator for the vertices in X
			j = 1 << (n-1) #Note that wlog we may assume that j contains the last vertex
			while j < (1 << n):		
				#Create X and Xc (X complement) based on j
				X = []
				Xc = []
					
				for k in range(n):
					if(j & (1 << k) > 0):
						X.append(k)
					else:
						Xc.append(k)
						
				f = 0 #f == 1 iff one of the 2 subgraphs on X are diameter < 3 in some color		
					
				if diameter2(createAdjMat(R,Xc,n),X) == 1: #X[R] diameter < 3	
					f = 1 
					
				else:						
					if diameter2(createAdjMat(B,Xc,n),X) == 1: #X[B] diameter < 3
						f = 1 
					
				#f == 1 iff X[B] diameter < 3 or X[R] diameter < 3
				if f == 1:
					#k is a binary number which represents Y (the remaining vertices in our covering)
					k = (1 << (n)) - j-1 #Y must contain at least all vertices in V-X
					while k < (1 << (n)):
						#Check if V-X < Y < V
						if((j | k) == ((1<< n) -1)): #| is an elementwise or in binary
							#Note that this is repeated from above, where now we are looking at Y instead of X			
							#Calculate Y and Yc(ompliment) based on k
							Y = []
							Yc = []
								
							for l in range(n):
								if(k & (1 << l) > 0):
									Y.append(l)
								else:
									Yc.append(l)			
							
							f = 0 #f == 1 iff one of the 2 subgraphs on X are diameter < 3 in some color			
											
							if diameter2(createAdjMat(R,Yc,n),Y) == 1: #Y[R] diameter < 3	
								f = 1 
								
							else:						
								if diameter2(createAdjMat(B,Yc,n),Y) == 1: #Y[B] diameter < 3
									f = 1 
										
							#f == 1 iff Y[R] or Y[B] diameter < 3
							#Implies a covering of vertices, both monochromatic with diameter < 3, so we can move on to next coloring
							if f == 1:
								val = 0 #Val = 0 iff there is a coloring with no decomposition into monochromatic subgraphs of diameter 2
								j = 1 << n
								k = 1 << n
								
						k = k+1
				j = j+1
							
			if(val == 1): 
				print("Found a coloring with no two diameter two covers, the red edges are: ")
				print(R)
				exit()
	i = i+1					
				
print("Code finished, the value is 2")
exit()












