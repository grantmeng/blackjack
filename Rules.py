class Blackjack:
    def getPoints(self, player):
        points = [0]
        for card in player.hand:
            newPoints = []
            cardVal = 10 if card.value >= 11 else card.value
            if cardVal == 1:
                for i in range(len(points)):
                    if points[i] + 1 <= 21:
                        newPoints.append(points[i] + 1)
                for i in range(len(points)):
                    if points[i] + 11 <= 21:
                        newPoints.append(points[i] + 11)
            else:
                for i in range(len(points)):
                    if points[i] + cardVal <= 21:
                        newPoints.append(points[i] + cardVal)
            points = newPoints
        res = float('-inf') # default set as bursted
        if points:
            res = max(points)
            if res == 21 and len(player.hand) == 2: # check natural blackjack
                if (player.hand[0].value == 1 and player.hand[1].value >= 11) or \
                   (player.hand[1].value == 1 and player.hand[0].value >= 11): # natural blackjack
                    res = float('inf')
        return res

class Piggy:
    pass