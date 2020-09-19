class Blackjack:
    def getPoints(self, hand):
        points = [0]
        for card in hand:
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
            if res == 21 and len(hand) == 2: # check natural blackjack
                if (hand[0].value == 1 and hand[1].value >= 11) or \
                   (hand[1].value == 1 and hand[0].value >= 11): # natural blackjack
                    res = float('inf')
        return res

class Piggy:
    pass