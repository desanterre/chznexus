
```
▄█▄     ▄  █  ▄▄▄▄▄▄      ▄   ▄███▄      ▄    ▄      ▄▄▄▄▄   
█▀ ▀▄  █   █ ▀   ▄▄▀       █  █▀   ▀ ▀▄   █    █    █     ▀▄ 
█   ▀  ██▀▀█  ▄▀▀   ▄▀ ██   █ ██▄▄     █ ▀  █   █ ▄  ▀▀▀▀▄   
█▄  ▄▀ █   █  ▀▀▀▀▀▀   █ █  █ █▄   ▄▀ ▄ █   █   █  ▀▄▄▄▄▀    
▀███▀     █            █  █ █ ▀███▀  █   ▀▄ █▄ ▄█            
         ▀             █   ██         ▀      ▀▀▀             
                                                               
                                                         
```
```                            
                                                 
                     █   ██████                
                  ███  ██      ██              
                  █      ██      █             
                  █        ██     ██           
                  █         ██     ██          
                █████        ██     ██         
             ███     █        ██     █         
           ██         ██       █     ██        
   ████████            ██      ██     ██       
 ██      █              █               ██     
 ██                          █████  ███████    
  ██                       ██     ██      █    
    ████                   █   ██  █  █   ██   
       █                   █       ███ ███ █   
       ██                   ██   ██       ██   
        ██                                █    
          ███                           ██     
             ███████████████████████████       
```
## Features

- Connects to Chapatiz chat via WebSocket
- Spoofs visitor login to bypass restrictions
- Logs user join/leave events and chat messages
- Saves user information in Excel (`.xlsx`) files
- Archives chat messages in timestamped text logs
- Supports live chat message sending from the terminal
- Periodically sends pings to maintain connection

## Requirements

- Python 3.8 or newer
- Poetry for dependency management

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/ChzChatLogger.git
    cd chznexus
    ```
2. **Install dependencies with Poetry:**
    ```bash
    poetry install
    ```
3. **Start the bot:**
    ```bash
    make run
    ```
4. **(Optional) Enter the Poetry shell:**
    ```bash
    poetry shell
    ```

> **Note:** Ensure [Poetry](https://python-poetry.org/docs/#installation) and Python 3.8+ are installed on your system.

## Project Structure

- `bot/` — Core bot modules (WebSocket handler, chat utilities, user management)
- `bin/config.py` — Configuration constants (WebSocket URI, headers, file paths)
- `main.py` — Main entry point for the bot
- `outputs/` — Default folder for `.xlsx` and `.txt` logs

## Logs and Output Data

All logs and output files are saved in the `outputs/` directory by default:

- `user_logins.xlsx` — Stores user IDs and usernames for every user who logs into the chat while the bot is running.
- `user_talk_log.txt` — Timestamped text log of chat messages, including sender username and user ID.

This structure keeps chat data organized and easy to analyze or archive. You can change the output folder path by modifying the configuration in `bin/config.py`.


## Possible Improvements

- **Full Login Support:** Implement a login client to authenticate users and maintain persistent sessions, moving beyond visitor spoofing.
- **Room/Channel Navigation:** Add commands to switch between rooms.
- **Auto-Trade Feature:** Develop automated trading capabilities.
- **Advanced Message Processing:** Integrate message filtering, keyword alerts, and customizable notifications.
- **Web Dashboard & API:** Provide a REST API and a web dashboard for real-time monitoring, control, and analytics.
- **Live Web Dashboard** Create a web interface that displays live chat messages, online users, room activity, and logs for easy monitoring.
- **WebSocket Broadcast Server** Expose a local WebSocket server that streams chat activity in real time to connected clients (e.g., browser dashboards, Discord bots).
- **REST API** Offer endpoints to retrieve data such as logged users, active rooms, and recent messages, enabling integration with external tools and services.

## Development and Testing

### Running Tests

Run all tests using:

```bash
make test
```

This executes the test suite with [pytest](https://docs.pytest.org/), covering core utilities, Excel logging, and mocked WebSocket interactions.

### Code Quality and Formatting

- `make black` — Format Python files with [Black](https://black.readthedocs.io/en/stable/).
- `make isort` — Organize imports using [isort](https://pycqa.github.io/isort/).
- `make lint` — Run both formatters for consistent code style.

### Useful Make Commands

- `make install` — Install dependencies via Poetry.
- `make shell` — Enter the Poetry virtual environment shell.
- `make run` — Start the main application.
- `make clean` — Remove temporary files and pytest cache.

Refer to the `Makefile` for additional commands and automation options.

## Contributing

Contributions are welcome! To contribute:

1. **Fork the repository** and create your branch from `main`.
2. **Install dependencies** using Poetry.
3. **Make your changes** with clear commit messages.
4. **Test your code** to ensure stability.
5. **Submit a pull request** describing your changes.

Please follow the existing code style and include relevant documentation or comments. For major changes, open an issue first to discuss your ideas.

