def fat (n):
    resultado = n
    for i in range (1, n):resultado *= i
    return resultado
   # n = n * (n-1) * (n-2) * (n)