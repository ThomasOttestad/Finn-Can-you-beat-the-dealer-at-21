import random
import sys
  

class Card:
    def __init__(self,suit,value):
        self.suit = suit
        self. value = value
        self.numValue = self.getNumValue(self.value)
         
    def getNumValue(self,value):
        try:
            intValue = int(value)
            return intValue
        except:
            if (value == 'A'):
                return 11
            else:
                return 10
            
        
class Deck:
    def __init__(self):
        self.deck = self.createDeck()
        if len(sys.argv) == 1:   
            self.shuffle()      
            
    def CreateDeckHelper(self,card):
        splitString = [char for char in card]
        if len(splitString) == 3:
            suit, val1, val2 = splitString
            value = val1+val2
            return suit, value
        else:           
            suit, value = splitString
            return suit, value
            
    def createDeck(self):
        cards = []
        if len(sys.argv) > 1:
            cards = self.readInput(sys.argv[1])
        else:
            cards = self.getCards()
        cardList = []
        for card in cards: 
            suit, value = self.CreateDeckHelper(card)
            newCard = Card(suit, value)
            cardList.append(newCard)
        return cardList
     
    def draw(self):
        if len(self.deck) == 0:
            return False
        else:
            return self.deck.pop(0)

    def shuffle(self):
        random.shuffle(self.deck)        
            
    def displayDeck(self):
        for i in self.deck:
            print(i.suit, i.value, i.numValue)
        print(len(self.deck))    
        
    def readInput(self, input):
        with open(input) as file:
            line = [line.rstrip() for line in file]
        
        list = line[0].split()
        list2 = []
        for i in list:
            list2.append(i.strip(','))
            
        return list2
   
    def getCards(self):
        with open("cards.in") as file:
            lines = [line.rstrip() for line in file]
        return lines

class Player:
    def __init__(self,name):
        self.name = name
        self.hand = []
        self.score = 0
        
    def newCard(self, card):
        self.hand.append(card)
        tempValue = 0 
        self.score += card.numValue
            
        
class Game:
    def __init__(self):
        self.players = self.createPlayers()
        self.deck = Deck()
        self.gameOver = False
        
    def createPlayers(self):
        players = []
        sam = Player('Sam')
        dealer = Player('Dealer')
        players.append(sam)
        players.append(dealer)
        return players
    
    def deal(self):
        for player in self.players:
            self.playerDraw(player)
        for player in self.players:
            self.playerDraw(player) 
    
    def play(self):          
        
        self.deal()              
        self.checkDouleAce()
        self.checkBlackjack()    
        
        while self.players[0].score < 17:
            if(self.gameOver):
                return
            tmp = self.playerDraw(self.players[0])
            self.over21()
            if(not tmp):
                return
        
        while self.players[1].score <= self.players[0].score:
            if(self.gameOver):
                return
            self.playerDraw(self.players[1])
            self.over21()

        self.endGame(self.players[1].name)
              
    def over21(self):
        if self.players[0].score > 21:
            self.endGame(self.players[1].name)
            return True
        elif self.players[1].score > 21:
            self.endGame(self.players[0].name)
            return True
        return False
                 
    def playerDraw(self,player):
        card = self.deck.draw()
        if card == False:
            self.deckEmpty()
            return False
        else:
            player.newCard(card)  
            return True
            
    def checkDouleAce(self):  
        if self.players[1].score == 22:
            if self.players[0].score == 22:
                self.endGame(self.players[1].name) 
                return True
            else: 
                self.endGame(self.players[0].name) 
                return True
                
        elif self.players[0].score == 22:
            self.endGame(self.players[1].name) 
            return True
        return False          
        
    def checkBlackjack(self):   
        if self.players[0].score == 21:
            self.endGame(self.players[0].name) 
        elif self.players[1].score == 21:
            self.endGame(self.players[1].name) 
    
    def deckEmpty(self):
        if self.players[0].score > self.players[1].score:
            self.endGame(self.players[0].name)
            return self.players[0].name
        elif self.players[1].score > self.players[0].score:
            self.endGame(self.players[1].name)
            return self.players[1].name
            
        else:
            self.endGame('Draw')
            return 'Draw'
        
    def endGame(self, winner):
        if(not self.gameOver):
            self.gameOver = True
            sys.stdout.write(str(winner)+ '\n')
            for player in self.players:
                sys.stdout.write(str(player.name) + ': ')
                for i in player.hand:          
                    if i == player.hand[-1]:
                        sys.stdout.write(str(i.suit + i.value) + '\n')
                    else:
                        sys.stdout.write(str(i.suit + i.value) + ', ')
            return winner
        else: return False

if __name__ == '__main__':     
    game = Game()  
    game.play()  
                       