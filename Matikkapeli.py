"""
Gui-projekti: Matikkapeli
    Tavoitteena on luoda peli, jossa pelaajalta kysytään yksinkertaisia
    matikka-aiheisia monivalintakysymyksiä. Halutaan myös, että pelaaja
    pystyy asettamaan itselleen sopivan vaikeustason sekä vaihtamaan
    kysyttävien kysymysten lukumäärää valikosta.
        Kysymykset ovat sellaisia, että yleissivistynyt henkilö
    kykenee ymmärtämään kysymykset, mutta niihin vastaaminen oikein
    vaatii pelaajalta nokkeluutta.
        Peli alkaa, kun pelaaja painaa nappia Start. Kun pelaaja on
    vastannut kysymykseen painamalla vaihtoehtoa, seuraavaan kysymykseen
    pääsee painamalla  nappia Next. Kun pelaaja on vastannut kaikkiin
    kysymyksiin, painamalla nappia Next pelaajalle kerrotaan, kuinka hyvin
    hän pärjäsi.
"""

from tkinter import *
import random
import math

class Mathgame:
    def __init__(self):
        """
        Määritellään luokan Mathgame attribuutit.
        """
        self.__mainwindow = Tk()
        # Määritellään pelin vaikeustaso.
        self.__difficulty = "Easy"
        # Määritellään pelissä kysyttävien kysymysten lukumäärä.
        self.__number_of_questions = 5
        # Alla olevilla attribuuteilla kontrolloidaan pelin kulkua.
        self.__number_of_correct_answers = 0
        self.__number_of_asked_questions = 0
        
        self.__asked_question = ""
        self.__correct_answer = ""
        
        self.__choice_a = ""
        self.__choice_b = ""
        self.__choice_c = ""
        self.__choice_d = ""
        
        self.__game_on = False
        self.__button_start_on = True
        self.__button_next_on = False
        self.__button_alternative_on = False
        
        # Valikot:
        self.__menu_bar = Menu(self.__mainwindow)
        # Määritellään valikko setting_menu, josta voidaan vaihtaa pelin asetuksia.
        self.__setting_menu = Menu(self.__menu_bar)
        self.__menu_bar.add_cascade(label = "Settings", menu = self.__setting_menu)
        # Määritellään vaikeustasovalikko difficulty_menu.
        self.__difficulty_menu = Menu(self.__setting_menu)
        self.__setting_menu.add_cascade(label = "Change difficulty", menu = self.__difficulty_menu)
        # Vaikeustasoja on kolme, Easy, Normal ja Hard.
        self.__difficulty_menu.add_command(label = "Easy", command = self.difficulty_to_easy)
        self.__difficulty_menu.add_command(label = "Normal", command = self.difficulty_to_normal)
        self.__difficulty_menu.add_command(label = "Hard", command = self.difficulty_to_hard)
        # Määritellään valikko number_of_questions, josta voidaan vaihtaa
        # kysymysten lukumäärän.
        self.__number_of_questions_menu = Menu(self.__setting_menu)
        self.__setting_menu.add_cascade(label = "Change the number of questions", menu = self.__number_of_questions_menu)
        # Kysymysten lukumääräksi voidaan asettaa 10, 30, 50 tai 100.
        self.__number_of_questions_menu.add_command(label = "5", command = self.questions_to_5)
        self.__number_of_questions_menu.add_command(label = "10", command = self.questions_to_10)
        self.__number_of_questions_menu.add_command(label = "15", command = self.questions_to_15)
        self.__number_of_questions_menu.add_command(label = "30", command = self.questions_to_30)
        self.__mainwindow.config(menu = self.__menu_bar)
        
        # Label-komponentti, johon ilmestyy kysyttävä kysymys.
        self.__question_label = Label(self.__mainwindow, text = "Question:")
        
        # Valintanapit. Monivalinnat ilmestyvät nappien päälle ja kysymykseen
        # vastataan painamalla nappia.
        self.__a_button = Button(self.__mainwindow, text = "", width = 8, command = self.answer_a)
        self.__b_button = Button(self.__mainwindow, text = "", width = 8, command = self.answer_b)
        self.__c_button = Button(self.__mainwindow, text = "", width = 8, command = self.answer_c)
        self.__d_button = Button(self.__mainwindow, text = "", width = 8, command = self.answer_d)
        
        # Label-komponentti, johon ilmestyy tulokset. 
        self.__result = Label(self.__mainwindow, text = "")
        
        # Aloitusnappi. Tätä painamalla aloitetaan peli.
        self.__start_button = Button(self.__mainwindow, text = "Start", command = self.start_game)
        
        # Lopetusnappi. Tätä painamalla päätetään ohjelman suoritus.
        self.__quit_button = Button(self.__mainwindow, text = "Quit", command = self.quit_game)
        
        # Label-komponentti, johon ilmestyy pelin jälkeen pelin lopputulos.
        self.__game_result = Label(self.__mainwindow, text = "")
        
        # Seuraava-nappi. Tätä painamalla päästään seuraavaan kysymykseen.
        self.__next_button = Button(self.__mainwindow, text = "Next", command = self.next_question)
        
        # Komponenttien asettelu:
        self.__question_label.place(x = 0, y = 0)
        
        self.__a_button.place(x = 30, y = 30)
        self.__b_button.place(x = 130, y = 30)
        self.__c_button.place(x = 30, y = 80)
        self.__d_button.place(x = 130, y = 80)

        self.__result.place(x = 0, y = 190)
        self.__game_result.place(x = 0, y = 210)
        
        self.__start_button.place(x = 0, y = 160)
        self.__quit_button.place(x = 180, y = 160)
        self.__next_button.place(x = 0, y = 130)
    
    # Metodeilla difficulty_to_vaikeustaso ja questions_to_n vaihdetaan
    # pelin asetuksia. Jos pelaaja yrittää vaihtaa asetuksia kesken
    # kesken pelin, kerrotaan pelaajalle, että niin ei voi tehdä. Tätä
    # hallitaan attribuutilla game_on.
    def difficulty_to_easy(self):
        """
        Tällä metodilla vaihdetaan pelin vaikeustaso tasolle Easy.
        """
        if self.__game_on:
            self.__result.config(text = "You can't modify the settings in the middle of a game!")
        else:
            if self.get_difficulty() == "Easy":
                self.__result.config(text = "Difficulty was already set to " + self.get_difficulty())
            else:
                self.__difficulty = "Easy"
                self.__result.config(text = "Difficulty was changed to " + self.get_difficulty() + ".")
            
        
    def difficulty_to_normal(self):
        """
        Tällä metodilla vaihdetaan pelin vaikeustaso tasolle Normal.
        """
        if self.__game_on:
            self.__result.config(text = "You can't modify the settings in the middle of a game!")
        else:
            if self.get_difficulty() == "Normal":
                self.__result.config(text = "Difficulty was already set to " + self.get_difficulty())
            else:
                self.__difficulty = "Normal"
                self.__result.config(text = "Difficulty was changed to " + self.get_difficulty() + ".")
    
    def difficulty_to_hard(self):
        """
        Tällä metodilla vaihdetaan pelin vaikeustaso tasolle Easy.
        """
        if self.__game_on:
            self.__result.config(text = "You can't modify the settings in the middle of a game!")
        else:
            if self.get_difficulty() == "Hard":
                self.__result.config(text = "Difficulty was already set to " + self.get_difficulty() + ".")
            else:
                self.__difficulty = "Hard"
                self.__result.config(text = "Difficulty was changed to " + self.get_difficulty() + ".")
                
    def questions_to_5(self):
        """
        Tällä metodilla vaihdetaan pelin kysymysten lukumäärä lukumääräksi 10.
        """
        if self.__game_on:
            self.__result.config(text = "You can't modify the settings in the middle of a game!")
        else:
            if self.get_number_of_questions() == 5:
                self.__result.config(text = "Number of questions was already set to " + str(self.get_number_of_questions()) + ".")
            else:
                self.__number_of_questions = 5
                self.__result.config(text = "Number of questions was changed to " + str(self.get_number_of_questions()) + ".")
        
    def questions_to_10(self):
        """
        Tällä metodilla vaihdetaan pelin kysymysten lukumäärä lukumääräksi 30.
        """
        if self.__game_on:
            self.__result.config(text = "You can't modify the settings in the middle of a game!")
        else:
            if self.get_number_of_questions() == 10:
                self.__result.config(text = "Number of questions was already set to " + str(self.get_number_of_questions()) + ".")
            else:
                self.__number_of_questions = 10
                self.__result.config(text = "Number of questions was changed to " + str(self.get_number_of_questions()) + ".")
    
    def questions_to_15(self):
        """
        Tällä metodilla vaihdetaan pelin kysymysten lukumäärä lukumääräksi 50.
        """
        if self.__game_on:
            self.__result.config(text = "You can't modify the settings in the middle of a game!")
        else:
            if self.get_number_of_questions() == 15:
                self.__result.config(text = "Number of questions was already set to " + str(self.get_number_of_questions()) + ".")
            else:
                self.__number_of_questions = 15
                self.__result.config(text = "Number of questions was changed to " + str(self.get_number_of_questions()) + ".")
        
    def questions_to_30(self):
        """
        Tällä metodilla vaihdetaan pelin kysymysten lukumäärä lukumääräksi 100.
        """
        if self.__game_on:
            self.__result.config(text = "You can't modify the settings in the middle of a game!")
        else:
            if self.get_number_of_questions() == 30:
                self.__result.config(text = "Number of questions was already set to " + str(self.get_number_of_questions()) + ".")
            else:
                self.__number_of_questions = 30
                self.__result.config(text = "Number of questions was changed to " + str(self.get_number_of_questions()) + ".")

    def generate_question(self):
        """"
        Tällä metodilla generoidaan vaikeustasoa vastaava kysymys. Metodi
        palauttaa listan, joka on muodossa
            [Kysymys, Oikea vastaus] + [väärät vastaukset].
        """
        
        if self.get_difficulty() == "Easy":
            # Vaikeustaso Easy:
            Question = easy_sum()
        elif self.get_difficulty() == "Normal":
            # Vaikeustaso Normal:
            n = random.sample(range(2),1)[0]
            if n == 0:
                Question = normal_sum()
            else:
                Question = normal_and_hard_product()
        else:
            # Vaikeustaso Hard:
            n = random.sample(range(10),1)[0]
            if n in range(3):
                Question = normal_and_hard_product()
            elif n in range(3,6):
                Question = hard_sum()
            elif n == 6:
                Question = hard_is_prime()
            elif n == 7:
                Question = hard_approximate_sqrt()
            elif n == 8:
                Question = hard_is_fibonacci()
            else:
                Question = hard_power()
        return Question

    # Seuraavaksi määritellään metodit, joita kutsutaan nappeja painettaessa.
    def start_game(self):
        """
        Tätä metodia kutsutaan painamalla nappia start_button. Tällä metodilla
        aloitetaan peli. Mikäli peli on jo käynnissä, mitään ei tapahdu.
        """
        if self.__button_start_on == False:
            pass
        else:
            # Asetetaan peli alkutilanteeseen.
            self.__number_of_correct_answers = 0
            self.__number_of_asked_questions = 0
            self.__game_on = True
            # Asetetaan button_next_on = True, jotta kutsuttaessa metodia
            # next_question saadaan generoitua ensimmäinen kysymys.
            self.__button_next_on = True
            # Emme halua, että mitään tapahtuu napista start kesken pelin.
            self.__button_start_on = False
            self.__game_result.config(text = "")
            self.next_question()
            
    def next_question(self):
        """
        Tätä metodia kutsutaan painamalla nappia next_button tai kun peli
        aloitetaan metodilla start_game. Tällä metodilla generoidaan
        kysymys sekä vastausvaihtoehdot.
        """
        if self.__button_next_on == False:
            pass
        elif self.game_ended() == False:
            self.__result.config(text = "")
            self.alternative_buttons("on")
            self.__button_next_on = False
            self.__number_of_asked_questions = self.__number_of_asked_questions + 1
            Question = self.generate_question()
            self.__asked_question = Question[0]
            self.__correct_answer = Question[1]
            Alternatives = Question[1:]
            random.shuffle(Alternatives)
            self.__choice_a = Alternatives[0]
            self.__choice_b = Alternatives[1]
            self.__choice_c = Alternatives[2]
            self.__choice_d = Alternatives[3]
            
            self.__question_label.config(text = "Question: " + self.get_asked_question())
            self.__a_button.config(text = self.get_choice_a())
            self.__b_button.config(text = self.get_choice_b())
            self.__c_button.config(text = self.get_choice_c())
            self.__d_button.config(text = self.get_choice_d())
        else:
            # Jos peli on päättynyt, niin päätetään peli ja kerrotaan
            # pelaajalle, miten hän pärjäsi.
            self.__button_next_on = False
            self.__button_start_on = True
            self.__game_on = False
            result = str(self.get_number_of_correct_answers()) + "/" + str(self.get_number_of_questions())
            self.__game_result.config(text = "You answered " + result + " correct on the difficulty " + self.get_difficulty() + ".")
            self.__a_button.config(text = "")
            self.__b_button.config(text = "")
            self.__c_button.config(text = "")
            self.__d_button.config(text = "")
            self.__question_label.config(text = "Question:")
            self.__result.config(text = "")
                    
    def answer_a(self):
        """
        Tätä metodia kutsutaan, kun pelaaja vastaa vaihtoehdon a.
        """
        if self.__button_alternative_on == False:
            pass
        else:
            self.alternative_buttons("off")
            self.__button_next_on = True
            if self.get_choice_a() == self.get_correct_answer():
                self.__number_of_correct_answers = self.__number_of_correct_answers + 1
                self.__result.config(text = "Your answer is correct!")
            else:
                self.__result.config(text = "Incorrect! The correct answer is " + str(self.get_correct_answer()) + ".")
        
    def answer_b(self):
        """
        Tätä metodia kutsutaan, kun pelaaja vastaa vaihtoehdon b.
        """
        if self.__button_alternative_on == False:
            pass
        else:
            self.alternative_buttons("off")
            self.__button_next_on = True
            if self.get_choice_b() == self.get_correct_answer():
                self.__number_of_correct_answers = self.__number_of_correct_answers + 1
                self.__result.config(text = "Your answer is correct!")
            else:
                self.__result.config(text = "Incorrect! The correct answer is " + str(self.get_correct_answer()) + ".")
                
    def answer_c(self):
        """
        Tätä metodia kutsutaan, kun pelaaja vastaa vaihtoehdon c.
        """
        if self.__button_alternative_on == False:
            pass
        else:
            self.alternative_buttons("off")
            self.__button_next_on = True
            if self.get_choice_c() == self.get_correct_answer():
                self.__number_of_correct_answers = self.__number_of_correct_answers + 1
                self.__result.config(text = "Your answer is correct!")
            else:
                self.__result.config(text = "Incorrect! The correct answer is " + str(self.get_correct_answer()) + ".")
        
    def answer_d(self):
        """
        Tätä metodia kutsutaan, kun pelaaja vastaa vaihtoehdon d.
        """
        if self.__button_alternative_on == False:
            pass
        else:
            self.alternative_buttons("off")
            self.__button_next_on = True
            if self.get_choice_d() == self.get_correct_answer():
                self.__number_of_correct_answers = self.__number_of_correct_answers + 1
                self.__result.config(text = "Your answer is correct!")
            else:
                self.__result.config(text = "Incorrect! The correct answer is " + str(self.get_correct_answer()) + ".")
    
    def start(self):
        """
        Käynnistetään käyttöliittymä.
        """
        self.__mainwindow.mainloop()
        
    def get_difficulty(self):
        """
        Palautetaan vaikeustaso.
        """
        return self.__difficulty
    
    def get_number_of_questions(self):
        """
        Palautetaan kysymysten lukumäärä.
        """
        return self.__number_of_questions
    
    def get_number_of_correct_answers(self):
        """
        Palautetaan pelaaja oikein vastattujen kysymysten lukumäärä.
        """
        return self.__number_of_correct_answers
    
    def get_number_of_asked_questions(self):
        """
        Palautetaan pelissä kysyttyjen kysymysten lukumäärä.
        """
        return self.__number_of_asked_questions
    
    def get_asked_question(self):
        """
        Palautetaan kysytty kysymys.
        """
        return self.__asked_question
    
    def get_correct_answer(self):
        """
        Palautetaan oikea vastaus.
        """
        return self.__correct_answer
    
    def get_choice_a(self):
        """
        Palautetaan vastausvaihtoehto a.
        """
        return self.__choice_a
    
    def get_choice_b(self):
        """
        Palautetaan vastausvaihtoehto b.
        """
        return self.__choice_b
    
    def get_choice_c(self):
        """
        Palautetaan vastausvaihtoehto c.
        """
        return self.__choice_c
    
    def get_choice_d(self):
        """
        Palautetaan vastausvaihtoehto d.
        """
        return self.__choice_d
    
    def alternative_buttons(self, mode):
        """
        Tällä metodilla voidaan laittaa vaihtoehtonapit päälle ja pois päältä.
        """
        if mode == "on":
            self.__button_alternative_on = True
        else:
            self.__button_alternative_on = False
            
    def game_ended(self):
        """
        Metodi tarkastaa onko peli päättynyt, eli onko 
        kysyttyjen kysymysten lukumäärä = kysymysten lukumäärä?
        """
        if self.get_number_of_questions() == self.get_number_of_asked_questions():
            return True
        else:
            return False
        
    def quit_game(self):
        self.__mainwindow.destroy()


# Lopuksi määritellään funktiot, joiden avulla generoidaan kysymykset.
def isprime(n):
    """
    Funktio ottaa parametrikseen positiivisen kokonaisluvun n ja
    kertoo, onko se alkuluku.

    """
    if n == 0 or n == 1:
        return False
    elif n == 2:
        return True
    else:
        return bool(all(n%i != 0 for i in range(2,math.ceil(math.sqrt(n))+1)))

def first_primes(n):
    """
    Funktio ottaa parametrikseen positiivisen kokonaisluvun n ja palauttaa
    joukon, joka sisältää alkuluvut, jotka ovat pienempää tai yhtösuurta
    kuin n.
    """
    Primes = set()
    for i in range(1,n+1):
        if isprime(i):
            Primes.add(i)
        else:
            pass
    return Primes 
    
def first_fibonacci(n):
    """
    Funktio ottaa parametrikseen luonnollisen luvun n ja palauttaa joukon,
    joka sisältää ensimmäiset n Fibonaccin lukua.
    """
    Fib = {0,1}
    first = 0
    second = 1
    if n == 0:
        return {0}
    elif n == 1:
        return {0,1}
    else:
        for i in range(2,n+1):
            first, second = second, first + second
            Fib.add(second)
        return Fib
# Seuraavaksi määritellään funktiot, jotka generoivat kysymykset. Jokainen
# niistä toimii kutakuinkin seuraavalla kaavalla:
        # 1. Generoidaan oikea vastaus,
        # 2. Määritellään populaatio, josta väärät vaihtoehdot valitaan,
        # 3. Generoidaaan kolme väärää vastausta,
        # 4. Määritellään pelaajalta kysyttävä kysymys,
        # 5. Palautetaan lista [Kysymys, Oikea vastaus] + [Väärät vastaukset].
# Joissain tapauksissa väärät vaihtoehdot on valittu eri populaatioista.
# Tämä tehtiin sen takia, että vastausvaihtoehdoista saataisiin uskottavammat.

# Vaikeustason Easy kysymykset:
def easy_sum():
    """
    Funktio generoi kysymyksen "The sum n + m is equal to:" missä
    n ja m on satunnaisesti generoidut kokonaisluvut väliltä [50, 99].
    """
    random_numbers = random.sample(range(50,100),2)
    question = "The sum " + str(random_numbers[0]) + " + " + str(random_numbers[1]) + " is equal to" 
    correct_answer = sum(random_numbers)
    Numbers = set(range(100,200))
    try:
        Numbers.remove(correct_answer)
    except KeyError:
        pass
    wrong_answers = random.sample(Numbers,3)
    return [question, correct_answer] + wrong_answers
# Vaikeustason Normal kysymykset
def normal_sum():
    """
    Funktio generoi kysymyksen "The sum n + m is equal to:" missä
    n ja m on satunnaisesti generoidut kokonaisluvut väliltä [100, 999].

    """
    random_numbers = random.sample(range(100,1000),2)
    question = "The sum " + str(random_numbers[0]) + " + " + str(random_numbers[1]) + " is equal to" 
    correct_answer = sum(random_numbers)
    Population = set(range(200,2000))
    try:
        Population.remove(correct_answer)
    except KeyError:
        pass
    wrong_answers = random.sample(Population,3)
    return [question, correct_answer] + wrong_answers

def normal_and_hard_product():
    """
    Funktio generoi kysymyksen "The product n * m is equal to:" missä
    n ja m on satunnaisesti generoidut kokonaisluvut väliltä [50, 99].

    """
    random_numbers = random.sample(range(50,100),2)
    question = "The product " + str(random_numbers[0]) + " * " + str(random_numbers[1]) + " is equal to" 
    correct_answer = random_numbers[0]*random_numbers[1]
    Population = set(range(2000,10000))
    try:
        Population.remove(correct_answer)
    except KeyError:
        pass
    Wrong_answers = random.sample(Population,3)
    return [question, correct_answer] + Wrong_answers
# Vaikeustason Hard kysymykset
def hard_sum():
    """
    Funktio generoi kysymyksen "The sum n + m is equal to:" missä
    n ja m on satunnaisesti generoidut kokonaisluvut väliltä [100000,499999].

    """
    random_numbers = random.sample(range(100000,500000),2)
    question = "The sum " + str(random_numbers[0]) + " + " + str(random_numbers[1]) + " is equal to" 
    correct_answer = sum(random_numbers)
    Population = set(range(300000,1500000))
    try:
        Population.remove(correct_answer)
    except KeyError:
        pass
    Wrong_answers = random.sample(Population,3)
    return [question, correct_answer] + Wrong_answers

def hard_power():
    """
    Funktio generoi kysymyksen "n to the power of k is equal to", missä 
    n valitaan satunnaisesti joukosta {2,3,5} ja k valitaan satunnaisesti
    joukosta {4,5,6,7,8,9}. 
    """
    base = random.sample({2,3,5},1)[0]
    exponent = random.sample({4,5,6,7,8,9},1)[0]
    correct_answer = base**exponent
    question = str(base) + " to the power " + str(exponent) + " is equal to"
    Population1 = set(range(20, 100))
    Population2 = set(range(1000, 10000))
    Population3 = set(range(10000, 1000000))
    try:
        Population1.remove(correct_answer)
    except KeyError:
        pass
    try:
        Population2.remove(correct_answer)
    except KeyError:
        pass
    try:
        Population3.remove(correct_answer)
    except KeyError:
        pass
    Wrong_answers = random.sample(Population1, 1) + random.sample(Population2, 1) + random.sample(Population3, 1)
    return [question, correct_answer] + Wrong_answers

def hard_is_prime():
    """
    Funktio generoi kysymyksen "Which one of the numbers below is a prime
    number?" 
    """
    Primes = first_primes(1000)
    random_prime = random.sample(Primes,1)
    question = "Which one of the numbers below is a prime number?"
    Not_primes = set(range(1000)).difference(Primes)
    random_not_primes = random.sample(Not_primes, 3)
    return [question] + random_prime + random_not_primes
    
def hard_approximate_sqrt():
    """
    Funktio generoi kysymyksen "Square root of p is approximately", missä p
    on satunnaisesti generoitu lukua 100 pienempi alkuluku. Oikea vastaus
    on p:n neliöjuuri neljän desimaalin tarkkuudella. Väärät vastaukset
    generoidaan aluksi valitsemalla kolme p:stä poikkeavaa lukua 100
    pienempää alkulukua. Väärät vastaukset ovat näiden alkulukujen
    neliöjuuret neljän desimaalin tarkkuudella. 
    """
    Primes = first_primes(100)
    random_prime = random.sample(Primes,1)[0]
    correct_answer = [round(math.sqrt(random_prime),2)]
    question = "Square root of " + str(random_prime) + " is approximately"
    Primes.remove(random_prime)
    random_three_primes = random.sample(Primes, 3)
    Wrong_answers = []
    for prime in random_three_primes:
        wrong_answer = round(math.sqrt(prime), 2)
        Wrong_answers.append(wrong_answer)
    return [question] + correct_answer + Wrong_answers

def hard_is_fibonacci():
    """
    Funktio generoi kysymyksen "Which one of the numbers below is a Fibonacci
    numbers?"
    """
    Fib = first_fibonacci(21)
    random_fib_number = random.sample(Fib,1)
    Population1 = set(range(1000))
    Population2 = set(range(5000))
    Population3 = set(range(10000))
    Not_fib1 = Population1.difference(Fib)
    Not_fib2 = Population2.difference(Fib)
    Not_fib3 = Population3.difference(Fib)
    Wrong_answers = random.sample(Not_fib1,1) + random.sample(Not_fib2,1) + random.sample(Not_fib3,1)
    question = "Which one of the numbers below is a Fibonacci number?"
    return [question] + random_fib_number + Wrong_answers
def main():
    ui = Mathgame()
    ui.start()
if __name__ == "__main__":
    main()