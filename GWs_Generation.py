from params import * 

# We pick a system with mass log(Mc/Msun) = 1.4 and mass ratio q = 0.8, chosen for being comparable to the system that generated GW150914, the first detected gravitational wave signal. You can adjust the values below; for best results, choose log(Mc/Msun) between 0.0 and 2.0 and q between 0.1 and 1.0, the ranges over which these parameters have been tested.

L_logMC = np.arange(0.0,2.0,0.1)
L_q = np.arange(0.1,1.0,0.1)

# params map
combinations = list(itertools.product(L_logMC, L_q))
N_com = len(combinations)

for i in range(N_com):
    logMc  = combinations[i][0]
    q      = combinations[i][1]

    print("Working with the parameters logMC = %s , q = %s"%(logMc,q))
    subprocess.run(["python", "WaveForme_Generation.py"]) 
