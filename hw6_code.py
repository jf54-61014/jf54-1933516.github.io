from collections import Counter
import random
# from functools import reduce
# import numpy as np


class Player:

    def __init__(self, total_score, wins, win_prob):
        self.total_score = total_score
        self.wins = wins
        self.win_prob = win_prob

    def CI(self):
        return min(self.win_prob), max(self.win_prob)

    def reset_score(self):
        self.total_score = 0

    def reset_wins(self):
        self.wins = 0

    @staticmethod
    def hot_dice(score, num_dice):
        """
        check if the roll is in the self.hot_dice situation that get score with all six dice
        """
        if score != 0 and num_dice == 0:
            return True
        else:
            return False

    @staticmethod
    def one_five_score_count(curr_num, counter):
        """
        takes in current number, counter, and dice list.
        Returns the sum score of single ones and fives and their total count
        """
        score = 0
        count = 0
        if curr_num != 1:
            score += counter[1]*100
            count += counter[1]
        if curr_num != 5:
            score += counter[5]*50
            count += counter[5]
        return score, count

    def get_score(self, dice):
        """
        takes in a list of dice number and sum up all the possible scores(include single ones and fives)
        Returns the scores, the number of dice left un-scored, and the dictionary stores the dice number and the count
        """
        dice.sort()
        counter = Counter(dice)  # gives a dictionary stores the dice number and the count
        if len(dice) == 6:  # cases score all six dice
            if dice == [1, 2, 3, 4, 5, 6]:  # a 1-6 straight
                return 1500, 0, counter
            elif any(counter[i] == 6 for i in counter):  # 6 of a kind
                return 3000, 0, counter
            elif any(dice.count(i) == 4 and dice.count(j) == 2 for i in range(1, 7) for j in range(1, 7)):  # 4 of a kind and a pair
                return 1500, 0, counter
            elif dice[0] == dice[1] == dice[2] and dice[3] == dice[4] == dice[5]:  # two triplets
                return 2500, 0, counter
            elif dice[0] == dice[1] and dice[2] == dice[3] and dice[4] == dice[5]:  # three pairs
                return 1500, 0, counter

        # cases score some dice in combination plus individual ones and fives
        score = 0
        for i in counter:
            if counter[i] == 5:  # 5 of a kind plus some single ones and fives
                score += 2000
                one_five_sum, count = self.one_five_score_count(i, counter)
                score += one_five_sum
                count += 5
                return score, len(dice)-count, counter
            elif counter[i] == 4:  # 4 of a kind plus some single ones and fives
                score += 1000
                one_five_sum, count = self.one_five_score_count(i, counter)
                score += one_five_sum
                count += 4
                return score, len(dice)-count, counter
            elif counter[i] == 3:  # 3 of a kind plus some single ones and fives
                if i == 1:
                    score += 1000
                else:
                    score += i*100
                one_five_sum, count = self.one_five_score_count(i, counter)
                score += one_five_sum
                count += 3
                return score, len(dice)-count, counter

        # no combinations, only sum up scores of ones and fives
        one_five_sum, count = self.one_five_score_count(-1, counter)
        return one_five_sum, len(dice)-count, counter
    
    @staticmethod
    def roll_dice(num_dice):
        """
        roll dice
        """
        return [random.randint(1, 6) for x in range(num_dice)]
    
    def strategy1(self, min_score, num_dice_thresh):
        """
        strategy 1:
        takes in a minimum score requirement, and a number of dice threshold.
        Keep rolling dices if you haven't met the minimum score requirement,
        or the number of dice is higher than the threshold.
        Return the total score get in this turn.
        """
        score, num_dice = 0, 6
        while score < min_score or num_dice > num_dice_thresh:
            dice = self.roll_dice(num_dice)
            roll_score, num_dice, counter = self.get_score(dice)
            # farkle situation, get 0 score
            if roll_score==0:
                return 0
            score += roll_score
            # self.hot_dice situation, roll again
            if self.hot_dice(roll_score, num_dice):
                hd_roll_score = self.strategy1(min_score-score, num_dice_thresh)
                # if farkle in self.hot_dice turn, lose all the points as well
                if hd_roll_score == 0:
                    return 0
                else:
                    score += hd_roll_score
        # minimum score requirement
        if score < min_score:
            return 0
        else:
            return score

    def strategy2(self, min_score, score_thresh):
        """
        strategy 2:
        takes in a minimum score requirement, a score threshold.
        Keep rolling dices if you haven't met the minimum score requirement,
        or score is lower than the threshold.
        Return the total score get in this turn.
        """
        score, num_dice = 0, 6
        while score < min_score or score < score_thresh:
            dice = self.roll_dice(num_dice)
            roll_score, num_dice, counter = self.get_score(dice)
            # farkle situation, get 0 score
            if roll_score == 0:
                return 0
            score += roll_score
            # self.hot_dice situation, roll again
            if self.hot_dice(roll_score, num_dice):
                hd_roll_score = self.strategy2(min_score - score, score_thresh - score)
                # if farkle in self.hot_dice turn, lose all the points as well
                if hd_roll_score == 0:
                    return 0
                else:
                    score += hd_roll_score
        # minimum score requirement
        if score < min_score:
            return 0
        else:
            return score

    def strategy3(self, min_score, score_thresh, num_dice_thresh):
        """
        strategy 3:
        takes in a minimum score requirement, a score threshold, and a number of dice threshold.
        Keep rolling dices if you haven't met the minimum score requirement,
        or score is lower than the threshold and the number of dice is higher than the threshold.
        Return the total score get in this turn.
        """
        score, num_dice = 0, 6
        while score < min_score or (num_dice > num_dice_thresh and score < score_thresh):
            dice = self.roll_dice(num_dice)
            roll_score, num_dice, counter = self.get_score(dice)
            # farkle situation, get 0 score
            if roll_score == 0:
                return 0
            score += roll_score
            # self.hot_dice situation, roll again
            if self.hot_dice(roll_score, num_dice):
                hd_roll_score = self.strategy3(min_score - score, score_thresh - score, num_dice_thresh)
                # if farkle in self.hot_dice turn, lose all the points as well
                if hd_roll_score == 0:
                    return 0
                else:
                    score += hd_roll_score
        # minimum score requirement
        if score < min_score:
            return 0
        else:
            return score

    def strategy4(self, min_score, num_dice_thresh):
        """
        strategy 4:
        takes in a minimum score requirement and number of dice threshold.
        Keep rolling dices if you haven't met the minimum score requirement,
        or the number of dice is higher than the threshold.
        If you have more than four dice and have some 1s or 5s, do not take triplet 2s or 3s.
        If you have more than three dice and no combination appear, only take one 1 if you have 1
        or take one 5 if you don't have 1.
        Return the total score get in this turn.
        """
        score, num_dice = 0, 6
        while score < min_score or num_dice > num_dice_thresh:
            ori_num_dice = num_dice
            dice = self.roll_dice(num_dice)
            roll_score, num_dice, counter = self.get_score(dice)
            # farkle situation, get 0 score
            if roll_score == 0:
                return 0

            # self.hot_dice situation, roll again
            if self.hot_dice(roll_score, num_dice):
                hd_roll_score = self.strategy4(min_score - score, num_dice_thresh)
                # if farkle in self.hot_dice turn, lose all the points as well
                if hd_roll_score == 0:
                    return 0
                else:
                    score += hd_roll_score
            else:
                # do not take triplet 2 or 3 in specific situation
                if ori_num_dice > 4:
                    if counter[2] == 3 and len(counter) > 2 and (counter[1] != 0 or counter[5] != 0):
                        roll_score -= 200
                        num_dice += 3
                    if counter[3] == 3 and len(counter) > 2 and (counter[1] != 0 or counter[5] != 0):
                        roll_score -= 300
                        num_dice += 3
                # take only one 1 or 5 in some situation
                if ori_num_dice > 3 and all(counter[i] < 3 for i in counter):
                    if counter[1] > 0:
                        roll_score -= 100 * (counter[1] - 1) + 50 * counter[5]
                        num_dice += counter[1] + counter[5] - 1
                    elif counter[5] > 0:
                        roll_score -= 50 * (counter[5] - 1)
                        num_dice += counter[5] - 1
            score += roll_score
        # minimum score requirement
        if score < min_score:
            return 0
        else:
            return score

    def strategy5(self, min_score, score_thresh):
        """strategy 5:
        takes in a minimum score requirement, a score threshold.
        Keep rolling dices if you haven't met the minimum score requirement,
        or score is lower than the threshold.
        If you have more than four dice and have some 1s or 5s, do not take triplet 2s or 3s.
        If you have more than three dice and no combination appear, only take one 1 if you have 1
        or take one 5 if you don't have 1.
        Return the total score get in this turn."""
        score, num_dice = 0, 6
        while score < min_score or score < score_thresh:
            ori_num_dice = num_dice
            dice = self.roll_dice(num_dice)
            # print("dice: ", dice)
            roll_score, num_dice, counter = self.get_score(dice)
            # farkle situation, get 0 score
            if roll_score == 0:
                return 0

            # self.hot_dice situation, roll again
            if self.hot_dice(roll_score, num_dice):
                hd_roll_score = self.strategy5(min_score - score, score_thresh)
                # if farkle in self.hot_dice turn, lose all the points as well
                if hd_roll_score == 0:
                    return 0
                else:
                    score += hd_roll_score
            else:
                # do not take triplet 2 or 3 in specific situation
                if ori_num_dice > 4:
                    if counter[2] == 3 and len(counter) > 2 and (counter[1] != 0 or counter[5] != 0):
                        roll_score -= 200
                        num_dice += 3
                    if counter[3] == 3 and len(counter) > 2 and (counter[1] != 0 or counter[5] != 0):
                        roll_score -= 300
                        num_dice += 3
                # take only one 1 or 5 in some situation
                if ori_num_dice > 3 and all(counter[i] < 3 for i in counter):
                    if counter[1] > 0:
                        roll_score -= 100 * (counter[1] - 1) + 50 * counter[5]
                        num_dice += counter[1] + counter[5] - 1
                    elif counter[5] > 0:
                        roll_score -= 50 * (counter[5] - 1)
                        num_dice += counter[5] - 1
            score += roll_score
        # minimum score requirement
        if score < min_score:
            return 0
        else:
            return score

    def strategy6(self, min_score, score_thresh, num_dice_thresh):
        """strategy 6:
        takes in a minimum score requirement, a score threshold, and a number of dice threshold.
        Keep rolling dices if you haven't met the minimum score requirement,
        or score is lower than the threshold and the number of dice is higher than the threshold.
        If you have more than four dice and have some 1s or 5s, do not take triplet 2s or 3s.
        If you have more than three dice and no combination appear, only take one 1 if you have 1
        or take one 5 if you don't have 1.
        Return the total score get in this turn."""
        score, num_dice = 0, 6
        while score < min_score or (num_dice > num_dice_thresh and score < score_thresh):
            ori_num_dice = num_dice
            dice = self.roll_dice(num_dice)
            roll_score, num_dice, counter = self.get_score(dice)
            # farkle situation, get 0 score
            if roll_score == 0:
                return 0

            # self.hot_dice situation, roll again
            if self.hot_dice(roll_score, num_dice):
                hd_roll_score = self.strategy6(min_score - score, score_thresh - score, num_dice_thresh)
                # if farkle in self.hot_dice turn, lose all the points as well
                if hd_roll_score == 0:
                    return 0
                else:
                    score += hd_roll_score
            else:
                # do not take triplet 2 or 3 in specific situation
                if ori_num_dice > 4:
                    if counter[2] == 3 and len(counter) > 2 and (counter[1] != 0 or counter[5] != 0):
                        roll_score -= 200
                        num_dice += 3
                    if counter[3] == 3 and len(counter) > 2 and (counter[1] != 0 or counter[5] != 0):
                        roll_score -= 300
                        num_dice += 3
                # take only one 1 or 5 in some situation
                if ori_num_dice > 3 and all(counter[i] < 3 for i in counter):
                    if counter[1] > 0:
                        roll_score -= 100 * (counter[1] - 1) + 50 * counter[5]
                        num_dice += counter[1] + counter[5] - 1
                    elif counter[5] > 0:
                        roll_score -= 50 * (counter[5] - 1)
                        num_dice += counter[5] - 1
            score += roll_score
        # minimum score requirement
        if score < min_score:
            return 0
        else:
            return score
