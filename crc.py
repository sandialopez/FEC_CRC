from bitarray import bitarray
import random

def cyclic_redundancy_check(filename: str, divisor: str, len_crc: int) -> int:
    """
    This function computes the CRC of a plain-text file
    arguments:
    filename: the file containing the plain-text
    divisor: the generator polynomium
    len_crc: The number of redundant bits (r)
    """

    redundancy = len_crc * bitarray('0')
    bin_file = bitarray()
    p = bitarray(divisor)
    len_p = len(p)
    with open(filename, 'rb') as file:
        bin_file.fromfile(file)
    cw = bin_file + redundancy
    rem = cw[0 : len_p]
    end = len(cw)
    for i in range(len_p, end + 1):
        if rem[0]:
            rem ^= p
        if i < end:
            rem = rem << 1
            rem[-1] = cw[i]
    msg = bin_file + rem[len_p-len_crc : len_p]
    return msg

def generador_errores(semilla: int, msg: int) -> int:
    #from numpy.random import Generator, MT19937, SeedSequence
    cw = bitarray(msg)
    random.seed(semilla)
    n = random.randint(4,20)
    inicio = random.randint(0, len(cw)-n)
    #invertimos el bit de la primera posicion para marcar el inicio
    if cw[inicio]==0:
        cw[inicio] = 1
    else:
        cw[inicio] = 0
    #los bits dentro del rango se invierten aleatoriamente
    for i in range(inicio+1, inicio+n-1):
        a=random.randint(0,1)
        if a==1:
            if cw[i]==0:
                cw[i] = 1
            else:
                cw[i] = 0
    #invertimos el bit de la ultima posicion para marcar el final
    if cw[inicio+n]==0:
        cw[inicio+n] = 1
    else:
        cw[inicio+n] = 0
    return cw

def Desco(msg: int, divisor: int, len_crc: int) -> int:
    p = bitarray(divisor)
    cw = bitarray(msg)
    len_p = len(p)
    rem = cw[0 : len_p]
    end = len(cw)
    for i in range(len_p, end + 1):
        if rem[0]:
            rem ^= p
        if i < end:
            rem = rem << 1
            rem[-1] = cw[i]
    r = rem[len_p-len_crc : len_p]
    #contamos los bits 0 en el crc
    cont=0
    for i in range(0, len(r)):
        if r[i]==0:
           cont=cont+1
    #verificamos si el msg es valido, si no se regresa un 1
    if cont==len(r):
        return 0
    else:
        return 1

def validador(muestra: int):
    cont=0
    for i in range(0, len(muestra)):
        cont=cont+muestra[i]
    cont = cont/100
    print(cont)

def main():
    semilla=input("semilla: ")
    semillas = [0] * 100
    random.seed(semilla)
    for i in range(100):
        semillas[i] = random.randint(0, 100)
    lts = [0] * 100
    for i in range(100):
        c = cyclic_redundancy_check('test.txt', '11011', 4)
        cw = generador_errores(int(semillas[i]), c)
        d = Desco(cw, '11011', 4)
        lts[i] = d
    validador(lts)

    for i in range(100):
        c = cyclic_redundancy_check('test.txt', '110011', 5)
        cw = generador_errores(int(semillas[i])+1, c)
        d = Desco(cw, '110011', 5)
        lts[i] = d
    validador(lts)

    for i in range(100):
        c = cyclic_redundancy_check('test.txt', '11001110100', 10)
        cw = generador_errores(int(semillas[i])+2, c)
        d = Desco(cw, '11001110100', 10)
        lts[i] = d
    validador(lts)

main()