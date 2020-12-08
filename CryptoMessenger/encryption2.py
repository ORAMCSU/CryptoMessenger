""" Module contenant les méthodes de cryptage et décryptage du DES et du RSA."""

from random import randint
import pickle as pk
import numpy as np

# --------------------Cryptage DES--------------------

def DES_crypt(ki,mesag):
    key=""
    msg_crypt=""
    msgl = []
    PC2 = []

# --------------------Cryptage des clefs--------------------

    # Convertit la clef de 8 carcatères maximum en binaire.
    for k in range(len(ki)):
        binar = bin(ord(ki[k]))[2:].zfill(8)
        key += (binar)
    key = key.zfill(64)


    # Mélange les bits de la clef selon ce schéma en 2 groupes de 28 bits.
    C = key[56]+key[48]+key[40]+key[32]+key[24]+key[16]+key[8]\
            +key[0]+key[57]+key[49]+key[41]+key[33]+key[25]+key[17]\
            +key[9]+key[1]+key[58]+key[50]+key[42]+key[34]+key[26]\
            +key[18]+key[10]+key[2]+key[59]+key[51]+key[43]+key[35]

    D = key[62]+key[54]+key[46]+key[38]+key[30]+key[22]+key[14]\
            +key[6]+key[61]+key[53]+key[45]+key[37]+key[29]+key[21]\
            +key[13]+key[5]+key[60]+key[52]+key[44]+key[36]+key[28]\
            +key[20]+key[12]+key[4]+key[27]+key[19]+key[11]+key[3]


    n = 0

    # Fait une première boucle pour obtenir les 16 clefs intermédiaires.
    for loop in range(16):
        n = n + 1
        if n == 1 or n == 2  or n == 9 or n == 16:

            # Déplace selon le numéro de l'itération, 1 ou 2 bits de la clef.
            C = C[1:28]+C[0]
            D = D[1:28]+D[0]
        else:
            C = C[2:28]+C[0:2]
            D = D[2:28]+D[0:2]

        # Rassemble les 2 groupes.
        K = C + D

        # Procède à un nouveau mélange de bits.
        PC = K[13]+K[16]+K[10]+K[23]+K[0]+K[4]\
            +K[2]+K[27]+K[14]+K[5]+K[20]+K[9]\
            +K[22]+K[18]+K[11]+K[3]+K[25]+K[7]\
            +K[15]+K[6]+K[26]+K[19]+K[12]+K[1]\
            +K[40]+K[51]+K[30]+K[36]+K[46]+K[54]\
            +K[29]+K[39]+K[50]+K[44]+K[32]+K[47]\
            +K[43]+K[48]+K[38]+K[55]+K[33]+K[52]\
            +K[45]+K[41]+K[49]+K[35]+K[28]+K[31]

        # Ajoute à la liste chaque clef intermédiaire de 48 bits.
        PC2.append(PC)

# --------------------Cryptage du message--------------------

    # Divise le message en groupe de 8 caractères.
    while len(mesag)>=8:
        binarc =""
        traitmt = mesag[0:8]
        mesag = mesag[8:]

        # Convertit chaque groupe de 8 en binaire.
        for k in range(8):
            binar = bin(ord(traitmt[k]))[2:].zfill(8)
            binarc += binar
        msgl.append(binarc)

    # Convertit les caractères restants en binaire.
    if len(mesag)!=0:
        binarc = ""
        for k in range(len(mesag)):
            binar = bin(ord(mesag[k]))[2:].zfill(8)
            binarc += (binar)
        binarc = binarc.zfill(64)
        msgl.append(binarc)

    # Prend chaque groupe de 8 caractères tour à tout (64 bits).
    for k in range(len(msgl)):
        msg = msgl[k]

        # Mélange les bits de chaque groupe de 8 caractères du message selon ce schéma en 2 groupes (pairs/impairs).
        L = msg[57]+msg[49]+msg[41]+msg[33]+msg[25]+msg[17]+msg[9]+msg[1]\
            +msg[59]+msg[51]+msg[43]+msg[35]+msg[27]+msg[19]+msg[11]+msg[3]\
            +msg[61]+msg[53]+msg[45]+msg[37]+msg[29]+msg[21]+msg[13]+msg[5]\
            +msg[63]+msg[55]+msg[47]+msg[39]+msg[31]+msg[23]+msg[15]+msg[7]

        R = msg[56]+msg[48]+msg[40]+msg[32]+msg[24]+msg[16]+msg[8]+msg[0]\
            +msg[58]+msg[50]+msg[42]+msg[34]+msg[26]+msg[18]+msg[10]+msg[2]\
            +msg[60]+msg[52]+msg[44]+msg[36]+msg[28]+msg[20]+msg[12]+msg[4]\
            +msg[62]+msg[54]+msg[46]+msg[38]+msg[30]+msg[22]+msg[14]+msg[6]\

        # Procède aux 16 itérations du message.
        for i in range (16):
                # Enregistre L sous un autre nom.
                L1 = L
                # L devient R.
                L = R

                # Expend R de 32 à 48 bits.
                expansion = R[31]+R[0]+R[1]+R[2]+R[3]+R[4]\
                            +R[3]+R[4]+R[5]+R[6]+R[7]+R[8]\
                            +R[7]+R[8]+R[9]+R[10]+R[11]+R[12]\
                            +R[11]+R[12]+R[13]+R[14]+R[15]+R[16]\
                            +R[15]+R[16]+R[17]+R[18]+R[19]+R[20]\
                            +R[19]+R[20]+R[21]+R[22]+R[23]+R[24]\
                            +R[23]+R[24]+R[25]+R[26]+R[27]+R[28]\
                            +R[27]+R[28]+R[29]+R[30]+R[31]+R[0]

                # Procède à un XOR entre la clef et l'expansion.
                somme = bin(int(PC2[i], 2)^int(expansion, 2))[2:].zfill(48)
                resultat_Xor = str(somme)

                # Divise le résultat en groupe de 6 bits.
                B1 = resultat_Xor[0:6]
                B2 = resultat_Xor[6:12]
                B3 = resultat_Xor[12:18]
                B4 = resultat_Xor[18:24]
                B5 = resultat_Xor[24:30]
                B6 = resultat_Xor[30:36]
                B7 = resultat_Xor[36:42]
                B8 = resultat_Xor[42:48]

                # Définit ces tableaux par défaut.

                S1 = np.array ([[14, 4,	13,	1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                                [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                                [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                                [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]])

                S2 = np.array ([[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                                [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                                [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                                [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]])

                S3 = np.array ([[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                                [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                                [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                                [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]])

                S4 = np.array ([[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                                [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                                [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                                [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]])

                S5 = np.array ([[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                                [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                                [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                                [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]])

                S6 = np.array ([[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                                [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                                [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                                [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]])

                S7 = np.array ([[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                                [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                                [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                                [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]])

                S8 = np.array ([[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                                [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                                [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                                [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]])

                """Selon les tableaux précédents, pour chaque groupe, la conversion en décimale
                du premier et dernier bit donnent le numéro de la ligne du tableau et la conversion
                en décimale des 4 bits du milieu donnent le numéro de la colonne du tableau."""

                SB1 = bin(S1[int(B1[0]+B1[5], 2)][int(B1[1:5], 2)])[2:].zfill(4)

                SB2 = bin(S2[int(B2[0]+B2[5], 2)][int(B2[1:5], 2)])[2:].zfill(4)

                SB3 = bin(S3[int(B3[0]+B3[5], 2)][int(B3[1:5], 2)])[2:].zfill(4)

                SB4 = bin(S4[int(B4[0]+B4[5], 2)][int(B4[1:5], 2)])[2:].zfill(4)

                SB5 = bin(S5[int(B5[0]+B5[5], 2)][int(B5[1:5], 2)])[2:].zfill(4)

                SB6 = bin(S6[int(B6[0]+B6[5], 2)][int(B6[1:5], 2)])[2:].zfill(4)

                SB7 = bin(S7[int(B7[0]+B7[5], 2)][int(B7[1:5], 2)])[2:].zfill(4)

                SB8 = bin(S8[int(B8[0]+B8[5], 2)][int(B8[1:5], 2)])[2:].zfill(4)

                # Obtient le numéro obtenu du tableau que l'on convertit en biniare (4 bits).
                Stotal = SB1 + SB2 + SB3 + SB4 + SB5 + SB6 + SB7 + SB8

                # Mélange la chaîne de bits (32 bits).
                permutation = Stotal[15]+Stotal[6]+Stotal[19]+Stotal[20]\
                            +Stotal[28]+Stotal[11]+Stotal[27]+Stotal[16]\
                            +Stotal[0]+Stotal[14]+Stotal[22]+Stotal[25]\
                            +Stotal[4]+Stotal[17]+Stotal[30]+Stotal[9]\
                            +Stotal[1]+Stotal[7]+Stotal[23]+Stotal[13]\
                            +Stotal[31]+Stotal[26]+Stotal[2]+Stotal[8]\
                            +Stotal[18]+Stotal[12]+Stotal[29]+Stotal[5]\
                            +Stotal[21]+Stotal[10]+Stotal[3]+Stotal[24]

                # Termine par un XOR entre la permutation et le L de départ.
                somme_Xor_Finale = bin(int(L1, 2)^int(permutation, 2))[2:].zfill(32)

                R = str(somme_Xor_Finale)

        # Fin de la boucle

        # Joint R16 et L16.
        boucle_16 = R+L

        # Finit le cryptage par un dernier mélange de bits (64 bits).
        msg_inter = boucle_16[39]+boucle_16[7]+boucle_16[47]+boucle_16[15]\
                    +boucle_16[55]+boucle_16[23]+boucle_16[63]+boucle_16[31]\
                    +boucle_16[38]+boucle_16[6]+boucle_16[46]+boucle_16[14]\
                    +boucle_16[54]+boucle_16[22]+boucle_16[62]+boucle_16[30]\
                    +boucle_16[37]+boucle_16[5]+boucle_16[45]+boucle_16[13]\
                    +boucle_16[53]+boucle_16[21]+boucle_16[61]+boucle_16[29]\
                    +boucle_16[36]+boucle_16[4]+boucle_16[44]+boucle_16[12]\
                    +boucle_16[52]+boucle_16[20]+boucle_16[60]+boucle_16[28]\
                    +boucle_16[35]+boucle_16[3]+boucle_16[43]+boucle_16[11]\
                    +boucle_16[51]+boucle_16[19]+boucle_16[59]+boucle_16[27]\
                    +boucle_16[34]+boucle_16[2]+boucle_16[42]+boucle_16[10]\
                    +boucle_16[50]+boucle_16[18]+boucle_16[58]+boucle_16[26]\
                    +boucle_16[33]+boucle_16[1]+boucle_16[41]+boucle_16[9]\
                    +boucle_16[49]+boucle_16[17]+boucle_16[57]+boucle_16[25]\
                    +boucle_16[32]+boucle_16[0]+boucle_16[40]+boucle_16[8]\
                    +boucle_16[48]+boucle_16[16]+boucle_16[56]+boucle_16[24]

        # Convertit le binaire en hexadécimal pour racourcir le message.
        msg_crypt = msg_crypt + hex(int(msg_inter,2))[2:].zfill(16)

    # Retourne le messsage crypté.
    return(msg_crypt)

#-------------------------------------------------------------------------------

# --------------------Décryptage DES--------------------

def DES_decrypt(ki,msg_crypt_final):
    PC2=[]
    msgl=[]
    key = ""
    msg_decrypt=""

# --------------------Cryptage des clefs--------------------

    # Convertit le clef en binaire (64 bits).
    for k in range(len(ki)):
        binar = bin(ord(ki[k]))[2:].zfill(8)
        key += (binar)
    key = key.zfill(64)

    # Procède comme le cryptage pour la clef.
    C = key[56]+key[48]+key[40]+key[32]+key[24]+key[16]+key[8]\
        +key[0]+key[57]+key[49]+key[41]+key[33]+key[25]+key[17]\
        +key[9]+key[1]+key[58]+key[50]+key[42]+key[34]+key[26]\
        +key[18]+key[10]+key[2]+key[59]+key[51]+key[43]+key[35]

    D = key[62]+key[54]+key[46]+key[38]+key[30]+key[22]+key[14]\
        +key[6]+key[61]+key[53]+key[45]+key[37]+key[29]+key[21]\
        +key[13]+key[5]+key[60]+key[52]+key[44]+key[36]+key[28]\
        +key[20]+key[12]+key[4]+key[27]+key[19]+key[11]+key[3]

    n = 0
    for loop in range(16):
        n = n + 1

        if n == 1 or n == 2  or n == 9 or n == 16:
            C = C[1:28]+C[0]
            D = D[1:28]+D[0]
        else:
            C = C[2:28]+C[0:2]
            D = D[2:28]+D[0:2]

        K = C + D

        PC = K[13]+K[16]+K[10]+K[23]+K[0]+K[4]\
            +K[2]+K[27]+K[14]+K[5]+K[20]+K[9]\
            +K[22]+K[18]+K[11]+K[3]+K[25]+K[7]\
            +K[15]+K[6]+K[26]+K[19]+K[12]+K[1]\
            +K[40]+K[51]+K[30]+K[36]+K[46]+K[54]\
            +K[29]+K[39]+K[50]+K[44]+K[32]+K[47]\
            +K[43]+K[48]+K[38]+K[55]+K[33]+K[52]\
            +K[45]+K[41]+K[49]+K[35]+K[28]+K[31]
        PC2.append(PC)
    # Inverse seulement l'ordre des clefs intermédiaires.
    PC2.reverse()

# --------------------Décryptage du message--------------------

    # Divise le message reçu en groupe de 16 caractères (64 bits).
    for loop in range(int(len(msg_crypt_final)/16)):
        msg_binar = bin(int(msg_crypt_final[0:16],16))[2:].zfill(64)
        msgl.append(msg_binar)
        msg_crypt_final = msg_crypt_final[16:]

    # Procède comme le cryptage pour le message.
    for k in range(len(msgl)):
        msg = msgl[k]

        L = msg[57]+msg[49]+msg[41]+msg[33]+msg[25]+msg[17]+msg[9]+msg[1]\
            +msg[59]+msg[51]+msg[43]+msg[35]+msg[27]+msg[19]+msg[11]+msg[3]\
            +msg[61]+msg[53]+msg[45]+msg[37]+msg[29]+msg[21]+msg[13]+msg[5]\
            +msg[63]+msg[55]+msg[47]+msg[39]+msg[31]+msg[23]+msg[15]+msg[7]

        R = msg[56]+msg[48]+msg[40]+msg[32]+msg[24]+msg[16]+msg[8]+msg[0]\
            +msg[58]+msg[50]+msg[42]+msg[34]+msg[26]+msg[18]+msg[10]+msg[2]\
            +msg[60]+msg[52]+msg[44]+msg[36]+msg[28]+msg[20]+msg[12]+msg[4]\
            +msg[62]+msg[54]+msg[46]+msg[38]+msg[30]+msg[22]+msg[14]+msg[6]\

        for i in range (16):

            L1 = L
            L = R

            expansion = R[31]+R[0]+R[1]+R[2]+R[3]+R[4]\
                        +R[3]+R[4]+R[5]+R[6]+R[7]+R[8]\
                        +R[7]+R[8]+R[9]+R[10]+R[11]+R[12]\
                        +R[11]+R[12]+R[13]+R[14]+R[15]+R[16]\
                        +R[15]+R[16]+R[17]+R[18]+R[19]+R[20]\
                        +R[19]+R[20]+R[21]+R[22]+R[23]+R[24]\
                        +R[23]+R[24]+R[25]+R[26]+R[27]+R[28]\
                        +R[27]+R[28]+R[29]+R[30]+R[31]+R[0]


            somme = bin(int(PC2[i], 2)^int(expansion, 2))[2:].zfill(48)
            resultat_Xor = str(somme)

            B1 = resultat_Xor[0:6]
            B2 = resultat_Xor[6:12]
            B3 = resultat_Xor[12:18]
            B4 = resultat_Xor[18:24]
            B5 = resultat_Xor[24:30]
            B6 = resultat_Xor[30:36]
            B7 = resultat_Xor[36:42]
            B8 = resultat_Xor[42:48]


            S1 = np.array ([[14, 4,	13,	1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]])

            S2 = np.array ([[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]])

            S3 = np.array ([[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]])

            S4 = np.array ([[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]])

            S5 = np.array ([[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]])

            S6 = np.array ([[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]])

            S7 = np.array ([[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]])

            S8 = np.array ([[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]])


            SB1 = bin(S1[int(B1[0]+B1[5], 2)][int(B1[1:5], 2)])[2:].zfill(4)

            SB2 = bin(S2[int(B2[0]+B2[5], 2)][int(B2[1:5], 2)])[2:].zfill(4)

            SB3 = bin(S3[int(B3[0]+B3[5], 2)][int(B3[1:5], 2)])[2:].zfill(4)

            SB4 = bin(S4[int(B4[0]+B4[5], 2)][int(B4[1:5], 2)])[2:].zfill(4)

            SB5 = bin(S5[int(B5[0]+B5[5], 2)][int(B5[1:5], 2)])[2:].zfill(4)

            SB6 = bin(S6[int(B6[0]+B6[5], 2)][int(B6[1:5], 2)])[2:].zfill(4)

            SB7 = bin(S7[int(B7[0]+B7[5], 2)][int(B7[1:5], 2)])[2:].zfill(4)

            SB8 = bin(S8[int(B8[0]+B8[5], 2)][int(B8[1:5], 2)])[2:].zfill(4)

            Stotal = SB1 + SB2 + SB3 + SB4 + SB5 + SB6 + SB7 + SB8

            permutation = Stotal[15]+Stotal[6]+Stotal[19]+Stotal[20]\
                        +Stotal[28]+Stotal[11]+Stotal[27]+Stotal[16]\
                        +Stotal[0]+Stotal[14]+Stotal[22]+Stotal[25]\
                        +Stotal[4]+Stotal[17]+Stotal[30]+Stotal[9]\
                        +Stotal[1]+Stotal[7]+Stotal[23]+Stotal[13]\
                        +Stotal[31]+Stotal[26]+Stotal[2]+Stotal[8]\
                        +Stotal[18]+Stotal[12]+Stotal[29]+Stotal[5]\
                        +Stotal[21]+Stotal[10]+Stotal[3]+Stotal[24]

            somme_Xor_Finale = bin(int(L1, 2)^int(permutation, 2))[2:].zfill(32)

            R = str(somme_Xor_Finale)

        # Fin de la boucle

        boucle_16 = R+L

        msg_inter = boucle_16[39]+boucle_16[7]+boucle_16[47]+boucle_16[15]\
                    +boucle_16[55]+boucle_16[23]+boucle_16[63]+boucle_16[31]\
                    +boucle_16[38]+boucle_16[6]+boucle_16[46]+boucle_16[14]\
                    +boucle_16[54]+boucle_16[22]+boucle_16[62]+boucle_16[30]\
                    +boucle_16[37]+boucle_16[5]+boucle_16[45]+boucle_16[13]\
                    +boucle_16[53]+boucle_16[21]+boucle_16[61]+boucle_16[29]\
                    +boucle_16[36]+boucle_16[4]+boucle_16[44]+boucle_16[12]\
                    +boucle_16[52]+boucle_16[20]+boucle_16[60]+boucle_16[28]\
                    +boucle_16[35]+boucle_16[3]+boucle_16[43]+boucle_16[11]\
                    +boucle_16[51]+boucle_16[19]+boucle_16[59]+boucle_16[27]\
                    +boucle_16[34]+boucle_16[2]+boucle_16[42]+boucle_16[10]\
                    +boucle_16[50]+boucle_16[18]+boucle_16[58]+boucle_16[26]\
                    +boucle_16[33]+boucle_16[1]+boucle_16[41]+boucle_16[9]\
                    +boucle_16[49]+boucle_16[17]+boucle_16[57]+boucle_16[25]\
                    +boucle_16[32]+boucle_16[0]+boucle_16[40]+boucle_16[8]\
                    +boucle_16[48]+boucle_16[16]+boucle_16[56]+boucle_16[24]

        msg_trad = ""

        for loop in range(8):
            if msg_inter[0:8]=="00000000":
                msg_inter = msg_inter[8:]
            else:
                # Ajoute chaque groupe de 8 caractères au message décodé.
                msg_trad += chr(int(msg_inter[0:8],2))
                msg_inter = msg_inter[8:]
        msg_decrypt = msg_decrypt + msg_trad

    # Retourne le message décrypté.
    return(msg_decrypt)

#-------------------------------------------------------------------------------

# --------------------PGCD--------------------
def pgcd(a,b) :
   while a%b != 0 :
      a, b = b, a%b
   return b;


# --------------------Bezout--------------------
def Bezout (a,b):
    u0=0
    r0=a
    r1=b
    u1=1
    v0=1
    v1=-r0//r1
    s=u0
    while r0%r1:
        r=r0
        r0=r1
        r1=r%r1
        u=u0
        v=v0
        u0=u1
        v0=v1
        q=r0//r1
        u1= u-q*u1
        v1=v-q*v1
        s=u0
    return s

# --------------------Création des clefs--------------------
def creat_clef(nom,p,q):
    """Fonction qui permet de définir son nom, sa clef publique et sa clef privée"""
    # Calcule n.
    n = p*q
    # Calcule l'indicatrice d'Euler m.
    m = (p-1)*(q-1)
    # Calcule c tel que c soit le plus petit nombre premier avec m.
    c = 2
    PGCD1 = pgcd(c,m)
    while PGCD1 != 1 :
        c = c + 1
        PGCD1 = pgcd(c,m)
    #----------------------------------------------------
    # S'assure que u est positif et supérieur à 2.
    u=Bezout(c,m)
    k=0
    while u<=2:
        k+=1
        u=u+k*m # En théorie on devrait s'assurer que u<m mais vu que l'on se sert toujours du premier k possible et non pas d'un k au hasard, c'est toujours le cas.
    #----------------------------------------------------
    publ=(n,c) # clé publique
    priv=(u,n) # clé privée
    #----------------------------------------------------
    clefs = {"clé_privée":priv,"clé_publique":publ,"name":nom}
    return(clefs)
    # Enregistre nos clés publique et privée dans un fichier.

# --------------------Cryptage RSA--------------------
def RSA_crypt(mot,clef):
    clef = clef.replace("(","")
    clef = clef.replace(")","")
    clef_publique = clef.split(",")
    try:
    # Vérifie que les nombres entrés pour la clef sont des entiers, dans le cas contraire une erreur est levée et on passe au except.
        n = int(clef_publique[0])
        c = int(clef_publique[1])
        liste=[]
        # Détermine le nombre de lettres dans le message.
        long_mot = len(mot)
        i = 0
        while i < long_mot :
            Ascii = ord(mot[i]) # Associe la valeur ascii du caractère au caractère.
            lettre_crypt = pow(Ascii,c)%n # Crypte le caractère ==> (ascii^c)modulo(n).
            i = i + 1 # Passe au caractère suivant.
            liste.append(str(lettre_crypt))
        chaine_affichee = " ".join(liste)
    # Affiche une erreur en cas de problème
    except ValueError:
        chaine_affichee = "Clef invalide"
    return(chaine_affichee)

#-------------------------------------------------------------------------------

# --------------------Décryptage RSA--------------------

def RSA_decrypt(chaine):
    with open("cles_ordi","rb") as fichier: # Récupère notre clé privée stockée dans le fichier.
        clef_privee = pk.Unpickler(fichier).load()["clé_privée"]
    liste = chaine.split(" ")
    decod = ""
    for k in range(len(liste)):
        lignes  = int(liste[k])
        z = pow(lignes,clef_privee[0])%clef_privee[1] # Décrypte le caractère ==> (lettre_crypt^u)modulo(n).
        h = chr(z) # Transforme la valeur trouvée à son caractère associé en ascii.
        decod += h

    # Retourne le message décodé.
    return(decod)
