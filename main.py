#!/usr/bin/env python3
from rich.console import Console
from hardware.leds import setup_leds, cleanup_leds
from hardware.motor import setup_motor, cleanup_motor
from hardware.sensors import sensor_controller
from hardware.buttons import setup_buttons
from game.blackjack import blackjack

def main():
    console = Console()
    
    try:
        # Initialize hardware
        console.print("[bold]Initializing hardware...[/bold]")
        setup_leds()
        setup_buttons()
        setup_motor()
        
        if not sensor_controller.setup_sensors(bus_number=0):
            console.print("[bold red]Failed to initialize sensors![/bold red]")
            return
        
        console.print("[bold green]Starting Blackjack game...[/bold green]")
        blackjack()
        
    except KeyboardInterrupt:
        console.print("\n[bold red]Game interrupted by user.[/bold red]")
    except Exception as e:
        console.print(f"\n[bold red]Error: {e}[/bold red]")
    finally:
        console.print("[bold]Cleaning up...[/bold]")
        cleanup_leds()
        cleanup_motor()
        sensor_controller.cleanup()
        console.print("[bold green]Done.[/bold green]")

if __name__ == "__main__":
    main()