
from rich.console import Console
from hardware.leds import setup_leds, cleanup_leds
from hardware.motor import setup_motor, cleanup_motor
from hardware.sensors import sensor_controller
from hardware.buttons import setup_buttons
from game.blackjack import blackjack
from utils.mqtt_client import mqtt_client

def main():
    console = Console()

    try:
        console.print("[bold]Initializing hardware...[/bold]")
        setup_leds()
        setup_buttons()
        setup_motor()

        if not sensor_controller.setup_sensors(bus_number=0):
            console.print("[bold red]Failed to initialize sensors![/bold red]")
            return  # Stop further execution if sensors don't initialize

        if mqtt_client is None:
            console.print("[bold red]MQTT client not initialized![/bold red]")
            return  # Stop further execution if MQTT client is not initialized

        console.print("[bold green]Starting Blackjack game...[/bold green]")
        blackjack()  # Start the game logic
        
    except KeyboardInterrupt:
        console.print("\n[bold red]Game interrupted by user.[/bold red]")  # Handle user interruption (Ctrl+C)
    except Exception as e:
        console.print(f"\n[bold red]Error: {e}[/bold red]")  # Catch other exceptions
    finally:
        console.print("[bold]Cleaning up...[/bold]")
        cleanup_leds()  # Clean up LED setup
        cleanup_motor()  # Clean up motor setup
        sensor_controller.cleanup()  # Clean up sensor setup
        console.print("[bold green]Done.[/bold green]")  # Indicate completion

if __name__ == "__main__":
    main()