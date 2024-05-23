import atexit
import json
import argparse
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import requests

class BlazeDoubleBot:
    def __init__(self, config):
        self.username = config['username']
        self.password = config['password']
        self.bet_amount = config['bet_amount']
        self.stop_loss_ratio = config['stop_loss_ratio']
        self.stop_win_ratio = config['stop_win_ratio']
        self.strategies = config['strategies']

        self.color_dict = {'black': 'B', 'red': 'R', 'white': 'W'}
        print('Initializing the robot ...')
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        self.driver = uc.Chrome(options=chrome_options)
        print('Accessing website ...')
        self.driver.get('https://blaze1.space/nt/games/double')
        sleep(10)
        print('Logging in ...')
        self.login()
        sleep(10)
        print('Logged ...')

        self.initial_balance = self.get_balance()
        self.current_balance = self.initial_balance
        self.stop_loss = self.initial_balance * self.stop_loss_ratio
        self.stop_win = self.initial_balance * self.stop_win_ratio

        # Registra a função para fechar o driver ao sair
        atexit.register(self.close_driver)

    def login(self):
        sleep(5)
        self.driver.find_element(By.XPATH, "//a[@class='link']").click()
        print('Clicking to login')
        sleep(5)
        self.driver.find_element(By.XPATH, "//input[contains(@name,'username')]").send_keys(self.username)
        print('Entering username')
        sleep(5)
        self.driver.find_element(By.XPATH, "//input[@name='password']").send_keys(self.password)
        print('Entering password')
        sleep(5)
        self.driver.find_element(By.CLASS_NAME, "red.submit.shared-button-custom.css-12vlaew").click()
        print('Logging in')
        sleep(5)

    def close_driver(self):
        self.driver.close()  # Fecha apenas a janela do navegador
        self.driver.quit()   # Encerra completamente o driver

    def is_time_to_bet(self):
        timer_text = self.driver.find_element(By.ID, "roulette-timer").text.lower()
        if 'rolling in' in timer_text:
            print(timer_text)
            return True
        return False

    def is_time_to_bet_api(self):
        info = requests.get('https://blaze1.space/api/roulette_games/current').json()
        if info['status'] == 'waiting':
            return True
        return False

    def get_history(self, size):
        try:
            history = self.driver.find_element(By.CLASS_NAME, 'entries.main')
            colors = [self.color_dict[div.get_attribute('class').split(' ')[-1]]
                      for div in history.find_elements(By.TAG_NAME, 'div')
                      if 'sm' in div.get_attribute('class')]
            return colors[:size]
        except Exception as e:
            print('Error getting history:', e)
            return ['n'] * size

    def get_history_api(self, size):
        colors = {0: 'W', 1: 'R', 2: 'B'}
        history = requests.get('https://blaze1.space/api/roulette_games/recent').json()
        history_list = [h['color'] for h in history][:size]
        return [colors[n] for n in history_list]

    def choose_color(self, color):
        bet_buttons = self.driver.find_elements(By.CLASS_NAME, color)
        for btn in bet_buttons:
            if 'x2' in btn.text:
                btn.click()
                break

    def place_bet(self, amount):
        self.driver.find_element(By.CLASS_NAME, 'input-field').clear()
        sleep(1)
        self.driver.find_element(By.CLASS_NAME, 'input-field').send_keys(amount)
        sleep(1)
        buttons = self.driver.find_elements(By.TAG_NAME, 'button')
        sleep(1)
        for b in buttons:
            if 'shared-button-custom css-1apb7jj' in b.get_attribute('class'):
                actions = ActionChains(self.driver)
                sleep(1)
                actions.click(b).perform()
                break

    def print_bet(self, color):
        print(f'''

Bet on {"Red" if color == "red" else "Black"}
Completed
Waiting for result ...

''')

    def print_bet_result(self, history, color):
        print("Green" if history[0] == self.color_dict[color] else "Red")

    def get_balance(self):
        return float(self.driver.find_element(By.CLASS_NAME, 'amount').text.replace(',', '.').split(' ')[-1])

    def strategy(self, history):
        for color, sequences in self.strategies.items():
            for sequence in sequences:
                if history == sequence:
                    return color
        return None

    def get_strategy_size(self):
        max_size = 0
        for sequences in self.strategies.values():
            for sequence in sequences:
                if len(sequence) > max_size:
                    max_size = len(sequence)
        return max_size

    def print_initialization_text(self):
        print(f'''
{50 * "*"}

***  Blaze Double Bet Bot Started   ***

Initial Balance: R$ {round(self.initial_balance, 2)}

Stop Loss: R$ {round(self.stop_loss, 2)}

Stop Win: R$ {round(self.stop_win, 2)}

Bet Amount: R$ {round(self.bet_amount, 2)}

{50 * "*"}

''')

    def print_final_text(self):
        print(f'''
{50 * "*"}

***  Blaze Double Bet Bot Finished   ***

Initial Balance: R$ {round(self.initial_balance, 2)}

Final Balance: R$ {round(self.current_balance, 2)}

{50 * "*"}

''')

    def wait_for_next_round(self):
        while True:
            try:
                self.driver.find_element(By.CLASS_NAME, 'time-left').find_element(By.TAG_NAME, 'span').text
            except:
                break

        while True:
            try:
                self.driver.find_element(By.CLASS_NAME, 'time-left').find_element(By.TAG_NAME, 'span').text
                return True
            except:
                pass

    def run(self):
        try:  
            self.print_initialization_text()
            strategy_size = self.get_strategy_size()
            while True:
                if self.stop_loss <= self.current_balance <= self.stop_win and self.current_balance - self.bet_amount >= 0:
                    if self.wait_for_next_round():
                        history = self.get_history_api(strategy_size)
                        color = self.strategy(history)
                        if color:
                            self.choose_color(color)
                            self.place_bet(self.bet_amount)
                            self.print_bet(color)
                            self.wait_for_next_round()
                            sleep(1)
                            history = self.get_history_api(strategy_size)
                            if history[0] != self.color_dict[color] and self.stop_loss <= self.current_balance <= self.stop_win and self.current_balance - self.bet_amount >= 0:
                                print('Gale 1')
                                self.place_bet(2 * self.bet_amount)
                                self.wait_for_next_round()
                                sleep(1)
                                history = self.get_history_api(strategy_size)
                                if history[0] != self.color_dict[color] and self.stop_loss <= self.current_balance <= self.stop_win and self.current_balance - self.bet_amount >= 0:
                                    print('Gale 2')
                                    self.place_bet(4 * self.bet_amount)
                                    self.wait_for_next_round()
                                    sleep(1)
                                    history = self.get_history_api(strategy_size)
                            self.print_bet_result(history, color)
                            sleep(8)
                            self.current_balance = self.get_balance()
                            print(self.current_balance)
                            print('Waiting 5 rounds to restart analysis ...')
                            sleep(150)
                            print('Analyzes restarted!\n\n')
                else:
                    self.print_final_text()
                    self.close_driver()
                    break
                sleep(2)
        except Exception as e:
            print(e)
            self.print_final_text()
            self.close_driver()
            

def main():
    parser = argparse.ArgumentParser(description='Blaze Double Bot')
    parser.add_argument('--config', type=str, default='config.json', help='config.json')
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = json.load(f)

    bot = BlazeDoubleBot(config)
    bot.run()

if __name__ == "__main__":
    main()


    bot = BlazeDoubleBot(config)
    bot.run()

if __name__ == "__main__":
    main()
