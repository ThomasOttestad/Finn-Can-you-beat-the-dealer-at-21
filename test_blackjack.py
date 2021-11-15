import sys
import unittest
import random
import io
import os
from blackjack import Player, Game, Card, Deck

class TestCard(unittest.TestCase):
    def test_getNumValue(self):
        temp1 = random.randint(2,10)
        temp2 = random.randint(2,10)  
        self.assertEqual(temp1, Card.getNumValue(self,temp1))
        self.assertEqual(temp2, Card.getNumValue(self,temp2))
        self.assertEqual(10, Card.getNumValue(self,"J"))
        self.assertEqual(10, Card.getNumValue(self,"K"))
        self.assertEqual(10, Card.getNumValue(self,"Q"))
        self.assertEqual(10, Card.getNumValue(self,"T"))
        self.assertEqual(11, Card.getNumValue(self,"A"))
        
        

class TestDeck(unittest.TestCase):
    def test_lenFullDeck(self):
        newdeck = Deck()
        self.assertEqual(len(newdeck.deck), 52)

    def test_Suits(self):
        newdeck = Deck()
        c, d, h, s = 0,0,0,0
        for card in newdeck.deck:
            if card.suit == 'C':
                c += 1
            elif card.suit == 'D':
                d += 1
            elif card.suit == 'H':
                h += 1
            elif card.suit == 'S':
                s += 1  
            else:
                self.assertEqual(True,False)
                
        self.assertEqual(c,13)
        self.assertEqual(d,13)
        self.assertEqual(h,13)        
        self.assertEqual(s,13)
    
    def test_createDeckHelper(self):
        self.assertEqual(Deck.CreateDeckHelper(self,'S10'), ('S','10'))
        self.assertEqual(Deck.CreateDeckHelper(self,'D2'), ('D','2'))
        self.assertEqual(Deck.CreateDeckHelper(self,'HK'), ('H','K'))
    
    def test_readInput(self):
        cardList = Deck.readInput(self, 'test.in')
        self.assertEqual(len(cardList), 10)
        
    def test_getCards(self):
        cardList = Deck.getCards(self)
        self.assertEqual(len(cardList), 52)
    
    def test_createDeck(self):
        deck1 = Deck()
        self.assertEqual(len(deck1.deck), 52)
        old_sys_argv = sys.argv
        sys.argv = old_sys_argv + ['test.in']
        deck2 = Deck()
        #dont do tests before sys.argv is reset
        sys.argv = old_sys_argv
        self.assertEqual(len(deck2.deck), 10)   

         
        
class TestPlayer(unittest.TestCase):
    def test_Newcard(self):
        card = Card('D','10')
        card2 = Card('S', '5')
        player = Player('test')
        player.newCard(card)
        player.newCard(card2)
        self.assertEqual(len(player.hand),2)
        self.assertEqual(player.hand[0],card)
        self.assertEqual(player.hand[1],card2)
        self.assertEqual(player.name, 'test')
        
class TestGame(unittest.TestCase):
    def test_createPlayers(self):
        players = Game.createPlayers(self)
        self.assertEqual('Sam',players[0].name)
        self.assertEqual('Dealer',players[1].name)
        
    def test_over21(self):
        #stops sys.stdout from writing during the test
        f = open(os.devnull, 'w')
        sys.stdout = f
        game = Game()
        for player in game.players:
            player.score = 22
        self.assertEqual(game.over21(), True)
        game.players[0].score -= 21
        self.assertEqual(game.over21(), True)
        game.players[1].score -= 21
        self.assertEqual(game.over21(), False)
        f.close()
        
    def test_doubleAce(self):
        game = Game()
        f = open(os.devnull, 'w')
        sys.stdout = f
        for player in game.players:
            player.score = 22
        self.assertEqual(game.checkDouleAce(), True)
        game.players[0].score -= 1
        self.assertEqual(game.checkDouleAce(), True)
        game.players[0].score += 1
        game.players[1].score -= 1
        self.assertEqual(game.checkDouleAce(), True)
        game.players[0].score -= 1
        self.assertEqual(game.checkDouleAce(), False)
        f.close()
        
    def test_playerDraw(self):
        game = Game()
        f = open(os.devnull, 'w')
        sys.stdout = f
        self.assertEqual(game.playerDraw(game.players[0]),True)
        game.deck.deck = []
        self.assertEqual(game.playerDraw(game.players[0]),False)
        f.close()
        
    def test_deckEmpty(self):
        game = Game()
        f = open(os.devnull, 'w')
        sys.stdout = f
        game.players[0].score = 20
        self.assertEqual(game.deckEmpty(),'Sam')
        game.players[1].score = 21
        self.assertEqual(game.deckEmpty(),'Dealer')
        game.players[1].score = 20
        self.assertEqual(game.deckEmpty(),'Draw')
        f.close()
        
    def test_endGame(self):
        game = Game()
        f = open(os.devnull, 'w')
        sys.stdout = f
        self.assertEqual(game.endGame('Sam'),'Sam')
        self.assertEqual(game.endGame('Sam'),False)
        game.gameOver = False
        self.assertEqual(game.endGame('Dealer'),'Dealer')
        self.assertEqual(game.endGame('Dealer'),False)   
        f.close()
        
    def test_deal(self):
        game = Game()
        f = open(os.devnull, 'w')
        sys.stdout = f
        game.deal()
        for player in game.players:
            self.assertEqual(len(player.hand), 2)
        f.close()