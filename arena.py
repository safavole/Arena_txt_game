class Kostka:
    def __init__(self, pocet_sten = 6):
        self.__pocet_sten = pocet_sten

    def vrat_pocet_sten(self):
        return self.__pocet_sten

    def hod(self):
        import random as _random
        return _random.randint(1, self.__pocet_sten)

    def __str__(self):
        return str("Kostka s {0} stěnami".format(self.__pocet_sten))

    def __repr__(self):
        """
        Vrací řetězci kód pro funkci EVAL
        """
        return str("Kostka({0})".format(self.__pocet_sten))


class Bojovnik:
    """Bojovník v aréně"""

    def __init__(self, jmeno, zivot, utok, obrana, kostka):
        self._jmeno = jmeno
        self._zivot = zivot
        self._max_zivot = zivot
        self._utok = utok
        self._obrana = obrana
        self._kostka = kostka
        self.__zprava = " "

    def __str__(self):
        return str(self._jmeno)

    @property
    def nazivu(self):
        if self._zivot > 0:
            return True
        else:
            return False

    def graficky_ukazatel(self, aktualni, maximalni):
        celkem = 20
        pocet = int(aktualni / maximalni * celkem)
        if (pocet == 0 and self.nazivu):
            pocet = 1
        return "[{0}{1}]".format("#" * pocet, " " * (celkem - pocet))

    def graficky_zivot(self):
        return self.graficky_ukazatel(self._zivot, self._max_zivot)

    def bran_se(self, uder):
        zraneni = uder - (self._obrana + self._kostka.hod())
        if zraneni > 0:
            zprava = "{0} utrpěl poškození za {1} HP!".format(self._jmeno, zraneni)
            self._zivot = self._zivot - zraneni
            if self._zivot < 0:
                self._zivot = 0
                zprava = zprava[:-1] + " a zemřel."
        else:
            zprava = "{0} odrazil útok!".format(self._jmeno)
        self.__nastav_zpravu(zprava)

    def utoc(self, souper):
        uder = self._utok + self._kostka.hod()
        zprava = "{0} útočí s úderem za {1} HP!".format(self._jmeno, uder)
        self.__nastav_zpravu(zprava)
        souper.bran_se(uder)

    def __nastav_zpravu(self, zprava):
        self.__zprava = zprava

    def vrat_posledni_zpravu(self):
        return self.__zprava


class Arena:

    def __init__(self, bojovnik_1, bojovnik_2, kostka):
        self.__bojovnik_1 = bojovnik_1
        self.__bojovnik_2 = bojovnik_2
        self._kostka = kostka

    def __vykresli(self):
        self.__vycisti_obrazovku()
        print("-------------- Aréna -------------- \n")
        print("Bojovníci: \n")
        self.__vypis_bojovnika(self.__bojovnik_1)
        self.__vypis_bojovnika(self.__bojovnik_2)
        print("")

    def __vycisti_obrazovku(self):
        import sys as _sys
        import subprocess as _subprocess
        if _sys.platform.startswith("win"):
            _subprocess.call(["cmd.exe", "/C", "cls"])
        else:
            _subprocess.call(["clear"])

    def __vypis_zpravu(self, zprava):
        import time as _time
        print(zprava)
        _time.sleep(0.75)

    def zapas(self):
        import random as _random
        print("Vítejte v aréně!")
        print("Dnes se utkají {0} a {1}!".format(self.__bojovnik_1, self.__bojovnik_2))
        print("Zápas může začít stisknutím klávesy ENTER!", end=" ")
        input()
        if _random.randint(0, 1):
            (self.__bojovnik_1, self.__bojovnik_2) = (self.__bojovnik_2, self.__bojovnik_1)
        #test
        while (self.__bojovnik_1.nazivu and self.__bojovnik_2.nazivu):
            self.__bojovnik_1.utoc(self.__bojovnik_2)
            self.__vykresli()
            self.__vypis_zpravu(self.__bojovnik_1.vrat_posledni_zpravu())
            self.__vypis_zpravu(self.__bojovnik_2.vrat_posledni_zpravu())
            if self.__bojovnik_2.nazivu:
                self.__bojovnik_2.utoc(self.__bojovnik_1)
                self.__vykresli()
                self.__vypis_zpravu(self.__bojovnik_2.vrat_posledni_zpravu())
                self.__vypis_zpravu(self.__bojovnik_1.vrat_posledni_zpravu())
            print(" ")

    def __vypis_bojovnika(self, bojovnik):
        print(bojovnik)
        print("Život: {0}".format(bojovnik.graficky_zivot()))
        if isinstance(bojovnik, Mag):
            print("Mana: {0}".format(bojovnik.graficka_mana()))


class Mag(Bojovnik):
    def __init__(self, jmeno, zivot, utok, obrana, kostka, mana, magicky_utok):
        super().__init__(jmeno, zivot, utok, obrana, kostka)
        self.__mana = mana
        self.__max_mana = mana
        self.__magicky_utok = magicky_utok

    def _nastav_zpravu(self, zprava):
        self.__zprava = zprava

    def utoc(self, souper):
        #normalní útok
        if self.__mana < self.__max_mana:
            self.__mana = self.__mana + 10
            if self.__mana > self.__max_mana:
                self.__mana = self.__max_mana
            super().utoc(souper)
            # magický útok
        else:
            uder = self.__magicky_utok + self._kostka.hod()
            zprava = "{0} použil magii za {1} hp.".format(self._jmeno, uder)
            self._nastav_zpravu(zprava)
            self.__mana = 0
            souper.bran_se(uder)

    def graficka_mana(self):
        return self.graficky_ukazatel(self.__mana, self.__max_mana)


kostka = Kostka(10)
zalgoren = Bojovnik("Zalgoren", 100, 20, 10, kostka)
gandalf = Mag("Gandalf", 60, 15, 12, kostka, 30, 45)
arena = Arena(zalgoren, gandalf, kostka)

arena.zapas()
