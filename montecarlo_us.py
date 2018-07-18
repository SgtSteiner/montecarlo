import random
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime, timedelta


class Montecarlo:
    def __init__(self, d_param):
        self.d_param = d_param
        self.results = []
        self.hist = {}

    def run(self):
        for _ in range(self.d_param["simulation_max"]):
            acum = 0
            weeks = 0

            user_stories = random.randint(
                self.d_param["user_stories_low_estimated"],
                self.d_param["user_stories_high_estimated"]
            )

            while acum < user_stories:
                weeks += 1
                if self.d_param["samples_estimate_flag"] == "data":
                    acum += self.d_param["data_exp"][random.randint(0, len(self.d_param["data_exp"]) - 1)]
                else:
                    acum += random.randint(self.d_param["throughput_low_bound"], self.d_param["throughput_high_bound"])
            self.results.append(weeks)

        self.hist = Counter(self.results)

    def print_results(self):
        print("Duración %Prob.")
        print("======== ======")
        for weeks, percentage in sorted([(key, self.hist[key] / self.d_param["simulation_max"]) for key in self.hist]):
            print("{0:^8.0f} {1:>6.2%}".format(weeks, percentage))

        print("\nMedia = {0:.0f}\n".format(np.mean(self.results)))

    def print_quantile(self):
        print("%Prob. Duración   Fecha")
        print("====== ======== ==========")
        for quan in range(100, -5, -5):
            quand_date = self.d_param["start_date"] + timedelta(
                days=round(np.percentile(self.results, quan)) * self.d_param["throughput_unit"] * 7
            )
            print("{0:>5}% {1:^8.0f} {2}".format(
                quan, np.percentile(self.results, quan), quand_date.strftime("%d-%m-%Y")
            ))

    def draw_histogram(self):
        plt.hist(self.results, bins=len(self.hist), alpha=1, edgecolor='black', linewidth=1)
        plt.axvline(np.percentile(self.results, 85), color='r', linestyle='dashed', linewidth=2, label="Percentil 85")
        plt.suptitle("Método Montecarlo")
        plt.title("Frecuencia de finalizar entre {0} y {1} HU tras {2:,} iteraciones".format(
            self.d_param["user_stories_low_estimated"],
            self.d_param["user_stories_high_estimated"],
            self.d_param["simulation_max"]).replace(",", ".")
                  )
        plt.ylabel("Frecuencia")
        plt.xlabel("Duración en {0} semanas".format(self.d_param["throughput_unit"]))
        plt.legend()
        # plt.show()

    def draw_bar(self):
        plt.bar(self.hist.keys(), [value / self.d_param["simulation_max"] for value in self.hist.values()])
        plt.axvline(np.percentile(self.results, 85), color='r', linestyle='dashed', linewidth=2, label="Percentil 85")
        plt.suptitle("Método Montecarlo")
        plt.title("Probabilidad de finalizar entre {0} y {1} HU tras {2:,} iteraciones".format(
            self.d_param["user_stories_low_estimated"],
            self.d_param["user_stories_high_estimated"],
            self.d_param["simulation_max"]).replace(",", ".")
        )
        plt.ylabel("Probabilidad")
        plt.xlabel("Duración en {0} semanas".format(self.d_param["throughput_unit"]))
        plt.legend()
        # plt.show()


if __name__ == '__main__':
    # Initial configuration
    d_conf = dict()
    d_conf["user_stories_low_estimated"] = 30   # Number of user stories to be completed (low bound)
    d_conf["user_stories_high_estimated"] = 30  # Number of user stories to be completed (high bound)
    d_conf["simulation_max"] = 5000   # Number of simulations to be executed

    d_conf["throughput_low_bound"] = 1   # Lowest throughput estimate
    d_conf["throughput_high_bound"] = 5  # Higuest throughput estimate

    d_conf["throughput_unit"] = 1        # Throughput/Velocity per weeks or per sprint

    d_conf["start_date"] = datetime.now()  # First day of the forecast

    d_conf["data_exp"] = [3, 5, 2, 1, 5, 3, 5, 3, 3, 2, 3, 4, 4, 3, 3]

    d_conf["samples_estimate_flag"] = "data"

    # Run Montecarlo
    mc = Montecarlo(d_conf)
    mc.run()
    mc.print_results()
    mc.print_quantile()

    # Show the graphs
    plt.subplot(1, 2, 1)
    mc.draw_histogram()
    plt.subplot(1, 2, 2)
    mc.draw_bar()
    plt.show()
