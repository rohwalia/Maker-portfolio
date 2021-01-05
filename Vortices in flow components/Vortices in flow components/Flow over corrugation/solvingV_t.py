from sympy import solveset, log, Symbol, S, nsolve
A=5
k=0.41
Re=1000
x=Symbol('x')
eq=(((1/A)-2)/(0.05+log(k*Re)-log(abs(x/A))))-(x/A)
V_t=nsolve(eq, -1, domain=S.Reals)
print(V_t)