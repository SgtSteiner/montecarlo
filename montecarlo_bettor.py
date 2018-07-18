import random
import matplotlib.pyplot as plt


def roll_dice():
    roll = random.randint(1, 100)

    if roll == 100:
        return False
    elif roll <= 50:
        return False
    elif 100 > roll >= 50:
        return True


def simple_bettor(funds, initial_wager, wager_count):
    value = funds
    wager = initial_wager

    w_x = []
    v_y = []

    current_wager = 1

    while current_wager < wager_count:
        if roll_dice():
            value += wager
        else:
            value -= wager

        w_x.append(current_wager)
        v_y.append(value)
        current_wager += 1

    # if value < 0:
    #     value = "Broke!"
    # print("Funds: ", value)
    plt.plot(w_x, v_y)


if __name__ == '__main__':
    x = 0
    while x < 100:
        simple_bettor(10000, 100, 10000)
        x += 1

    plt.ylabel('Account Value')
    plt.xlabel('Wager Count')
    plt.show()