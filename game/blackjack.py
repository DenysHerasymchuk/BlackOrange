from rich.console import Console
import random
import time
from hardware.leds import set_color, set_rgb_state, run_led_chaser
from hardware.motor import (rotate_motor, dealer_bust_celebration, 
                          motor_win_celebration, motor_short_buzz, 
                          motor_shuffle_effect)
from hardware.buttons import check_buttons
from hardware.sensors import sensor_controller
from game.cards import create_deck, deal_card, calculate_hand_value, suggest_move
from game.display import display_game_state

console = Console()

def blackjack():
    level = 1
    deck = create_deck()
    random.shuffle(deck)
    
    while level <= 12:
        # Initial setup
        sensor_data = sensor_controller.get_sensor_readings()
        
        # Temperature check
        current_temp = sensor_data['temperature']
        if sensor_controller.check_temperature(current_temp):
            console.print(f"[bold orange1]Temperature is {current_temp}°C (Threshold: {sensor_controller.TEMPERATURE_THRESHOLD}°C)[/bold orange1]", justify="center")
            console.print("[bold orange1]Cooling down for 5 seconds...[/bold orange1]", justify="center")
            
            for _ in range(3):  # Blink orange 3 times
                set_color(255, 165, 0)
                time.sleep(0.5)
                set_color(0, 0, 0)
                time.sleep(0.5)
            
            sensor_data = sensor_controller.get_sensor_readings()
            if sensor_controller.check_temperature(sensor_data['temperature']):
                console.print("[bold red]Still too hot! Exiting...[/bold red]", justify="center")
                exit()
            continue

        # Reshuffle if needed
        if len(deck) < 15:
            deck = create_deck()
            random.shuffle(deck)
            set_color(0, 0, 255)
            motor_shuffle_effect()
            time.sleep(1.5)
            set_color(0, 0, 0)
            time.sleep(0.5)

        # Deal initial hands
        set_color(0, 0, 255)
        motor_short_buzz()
        run_led_chaser()
        player_hand = [deal_card(deck), deal_card(deck)]
        time.sleep(1.0)
        
        # Dark mode check
        if sensor_data['light'] < 100:
            dealer_hand = [('A', 'Spades'), ('10', 'Spades')]
        else:
            dealer_hand = [deal_card(deck), deal_card(deck)]
        set_color(0, 0, 255)
        motor_short_buzz()
        time.sleep(1.0)
        
        set_color(0, 0, 0)
        time.sleep(0.8)

        # Player's turn
        while True:
            display_game_state(level, dealer_hand, player_hand, True)
            
            suggestion = suggest_move(player_hand, dealer_hand[0])
            console.print(f"[bold cyan]Suggested move: {suggestion}[/bold cyan]", justify="center")
            
            player_value = calculate_hand_value(player_hand)
            if player_value > 21:
                set_rgb_state(0)  # Lose (red)
                rotate_motor(80, 0.001)
                rotate_motor(-80, 0.001)
                display_game_state(level, dealer_hand, player_hand, True)
                time.sleep(2)
                set_color(0, 0, 0)
                break

            # Get player action
            action = None
            while action is None:
                action = check_buttons()
                time.sleep(0.1)

            if action == 'h':
                set_color(0, 0, 255)
                rotate_motor(40, 0.003)
                player_hand.append(deal_card(deck))
                display_game_state(level, dealer_hand, player_hand, True)
                time.sleep(0.8)
                set_color(0, 0, 0)
            elif action == 's':
                set_color(0, 255, 0)
                rotate_motor(25, 0.005)
                display_game_state(level, dealer_hand, player_hand, True)
                time.sleep(0.8)
                set_color(0, 0, 0)
                break

        # Dealer's turn if player didn't bust
        if calculate_hand_value(player_hand) <= 21:
            display_game_state(level, dealer_hand, player_hand, False)
            
            while calculate_hand_value(dealer_hand) < 17:
                set_color(255, 165, 0)
                rotate_motor(15, 0.005)
                dealer_hand.append(deal_card(deck))
                display_game_state(level, dealer_hand, player_hand, False)
                time.sleep(1)
                set_color(0, 0, 0)

            # Determine winner
            dealer_value = calculate_hand_value(dealer_hand)
            player_value = calculate_hand_value(player_hand)
            
            if dealer_value > 21:
                console.print("[green]Dealer busts! You win![/green]", justify="center")
                set_rgb_state(2)  # Win (green)
                dealer_bust_celebration()
                motor_win_celebration()
                run_led_chaser()
                level += 1
                time.sleep(2)
                set_color(0, 0, 0)
            elif dealer_value > player_value:
                console.print("[red]Dealer wins![/red]", justify="center")
                set_rgb_state(0)  # Lose (red)
                rotate_motor(120, 0.001)
                rotate_motor(-120, 0.001)
                time.sleep(2)
                set_color(0, 0, 0)
            elif dealer_value < player_value:
                console.print("[green]You win![/green]", justify="center")
                set_rgb_state(2)  # Win (green)
                run_led_chaser()
                motor_win_celebration()
                level += 1
                time.sleep(2)
                set_color(0, 0, 0)
            else:
                console.print("[yellow]It's a tie![/yellow]", justify="center")
                set_rgb_state(1)  # Tie (yellow)
                for _ in range(3):
                    rotate_motor(30, 0.003)
                    rotate_motor(-30, 0.003)
                    time.sleep(0.2)
                time.sleep(1.5)
                set_color(0, 0, 0)

    console.print("[bold blue]CONGRATULATIONS! You've completed all levels![/bold blue]", justify="center")
    set_color(0, 0, 255)
    for _ in range(3):
        motor_win_celebration()
        time.sleep(0.5)
    time.sleep(3)
    set_color(0, 0, 0)