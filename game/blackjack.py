from rich.console import Console
import random
import time
from hardware.leds import set_color, run_led_chaser, victory_light_show
from hardware.motor import rotate_motor, dealer_bust_celebration
from hardware.buttons import check_buttons
from hardware.sensors import sensor_controller
from game.cards import create_deck, deal_card, calculate_hand_value, suggest_move
from game.display import display_game_state

console = Console()

def motor_win_celebration():
    """Special motor pattern for winning"""
    for _ in range(2):
        rotate_motor(50, 0.002)
        rotate_motor(-50, 0.002)
    dealer_bust_celebration()

def motor_short_buzz():
    """Quick motor movement for notifications"""
    rotate_motor(20, 0.003)
    rotate_motor(-20, 0.003)

def motor_shuffle_effect():
    """Motor effect for shuffling cards"""
    for _ in range(3):
        rotate_motor(30, 0.004)
        rotate_motor(-30, 0.004)
        time.sleep(0.1)

def blackjack():
    level = 1
    deck = create_deck()
    random.shuffle(deck)
    
    while level <= 12:
        # Initial setup
        sensor_data = sensor_controller.read_sensors()
        
        # Temperature check
        if sensor_controller.check_temperature(sensor_data['temperature']):
            console.print("[bold orange1]Temperature is too high! Cool down...[/bold orange1]", justify="center")
            set_color(255, 165, 0)
            rotate_motor(100, 0.005)  # Slow movement for warning
            time.sleep(3)
            set_color(0, 0, 0)
            exit()

        # Reshuffle if needed
        if len(deck) < 15:
            deck = create_deck()
            random.shuffle(deck)
            set_color(0, 0, 255)
            motor_shuffle_effect()  # Special shuffle motor effect
            time.sleep(1.5)
            set_color(0, 0, 0)
            time.sleep(0.5)

        # Deal initial hands with blue LED
        set_color(0, 0, 255)
        motor_short_buzz()  # Quick buzz for each card
        player_hand = [deal_card(deck), deal_card(deck)]
        time.sleep(1.0)
        
        # Dark mode check - give dealer blackjack if light < 100 lux
        if sensor_data['light'] < 100:
            dealer_hand = [('A', 'Spades'), ('10', 'Spades')]
        else:
            dealer_hand = [deal_card(deck), deal_card(deck)]
        set_color(0, 0, 255)
        motor_short_buzz()  # Quick buzz for dealer cards
        time.sleep(1.0)
        
        set_color(0, 0, 0)
        time.sleep(0.8)

        # Player's turn
        while True:
            display_game_state(level, dealer_hand, player_hand, True)
            
            # Show suggested move
            suggestion = suggest_move(player_hand, dealer_hand[0])
            console.print(f"[bold cyan]Suggested move: {suggestion}[/bold cyan]", justify="center")
            
            player_value = calculate_hand_value(player_hand)
            if player_value > 21:
                set_color(255, 0, 0)
                rotate_motor(80, 0.001)  # Fast, jerky movement for bust
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
                rotate_motor(40, 0.003)  # Medium movement for hit
                player_hand.append(deal_card(deck))
                display_game_state(level, dealer_hand, player_hand, True)
                time.sleep(0.8)
                set_color(0, 0, 0)
            elif action == 's':
                set_color(0, 255, 0)
                rotate_motor(25, 0.005)  # Slow, deliberate movement for stand
                display_game_state(level, dealer_hand, player_hand, True)
                time.sleep(0.8)
                set_color(0, 0, 0)
                break

        # Dealer's turn if player didn't bust
        if calculate_hand_value(player_hand) <= 21:
            display_game_state(level, dealer_hand, player_hand, False)
            
            # Dealer draws cards with orange LED
            while calculate_hand_value(dealer_hand) < 17:
                set_color(255, 165, 0)
                rotate_motor(15, 0.005)  # Small, slow movements for dealer draw
                dealer_hand.append(deal_card(deck))
                display_game_state(level, dealer_hand, player_hand, False)
                time.sleep(1)
                set_color(0, 0, 0)

            # Determine winner with motor effects
            dealer_value = calculate_hand_value(dealer_hand)
            player_value = calculate_hand_value(player_hand)
            
            if dealer_value > 21:
                console.print("[green]Dealer busts! You win![/green]", justify="center")
                dealer_bust_celebration()
                motor_win_celebration()
                run_led_chaser()
                level += 1
                set_color(0, 255, 0)
                time.sleep(2)
                set_color(0, 0, 0)
                if level > 12:
                    victory_light_show()
            elif dealer_value > player_value:
                console.print("[red]Dealer wins![/red]", justify="center")
                set_color(255, 0, 0)
                rotate_motor(120, 0.001)  # Fast, strong movement for loss
                rotate_motor(-120, 0.001)
                time.sleep(2)
                set_color(0, 0, 0)
            elif dealer_value < player_value:
                console.print("[green]You win![/green]", justify="center")
                run_led_chaser()
                motor_win_celebration()
                level += 1
                set_color(0, 255, 0)
                time.sleep(2)
                set_color(0, 0, 0)
                if level > 12:
                    victory_light_show()
            else:
                console.print("[yellow]It's a tie![/yellow]", justify="center")
                set_color(255, 255, 0)
                for _ in range(3):  # Pulsing pattern for tie
                    rotate_motor(30, 0.003)
                    rotate_motor(-30, 0.003)
                    time.sleep(0.2)
                time.sleep(1.5)
                set_color(0, 0, 0)

    console.print("[bold blue]CONGRATULATIONS! You've completed all levels![/bold blue]", justify="center")
    set_color(0, 0, 255)
    # Extended celebration for game completion
    for _ in range(3):
        motor_win_celebration()
        time.sleep(0.5)
    time.sleep(3)
    set_color(0, 0, 0)