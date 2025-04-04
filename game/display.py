from rich.console import Console
from rich.panel import Panel
from game.constants import SUITS
from hardware.sensors import sensor_controller  # Add this import

console = Console()

def draw_card(rank, suit):
    if rank == ' ' and suit == ' ':
        return [
            "┌─────────┐", "│░░░░░░░░░│", "│░░░░░░░░░│", "│░░░░░░░░░│",
            "│░░░░░░░░░│", "│░░░░░░░░░│", "└─────────┘"
        ]

    suit_symbol, color = SUITS[suit]
    return [
        f"┌─────────┐", f"│{rank.ljust(2)}       │", "│         │",
        f"│    {suit_symbol}    │", "│         │", f"│      {rank.rjust(2)} │", "└─────────┘"
    ]

def display_hand(hand, hide_first_card=False):
    cards = [draw_card(' ', ' ') if hide_first_card and i == 0 else draw_card(rank, suit) 
             for i, (rank, suit) in enumerate(hand)]
    return [" ".join(card[line] for card in cards) for line in range(len(cards[0]))]

def display_game_state(level, dealer_hand, player_hand, hide_dealer_card):
    console.clear()
    console.print(Panel(f"Level {level}/12", style="bold green", expand=False), justify="center")
    
    console.print(Panel("Dealer's Hand", style="bold red", expand=False), justify="center")
    for line in display_hand(dealer_hand, hide_dealer_card):
        console.print(line, justify="center")

    console.print()
    for line in display_hand(player_hand):
        console.print(line, justify="center")
    console.print(Panel("Your Hand", style="bold blue", expand=False), justify="center")

    # Display sensor data
    sensor_data = sensor_controller.read_sensors()
    console.print(
        f"Temperature: {sensor_data['temperature']:.1f}°C | "
        f"Light: {sensor_data['light']} lux | "
        f"Pressure: {sensor_data['pressure']:.1f} hPa",
        justify="center"
    )