import datetime


class GameLogger:
    def __init__(self):
        self.log_entries = []
        self.start_time = datetime.datetime.now()

    def log(self, event_type, player=None, details=None, amount=None):
        entry = {
            'timestamp': datetime.datetime.now(),
            'event': event_type,
            'player': player.name if player else "System",
            'details': details,
            'amount': amount
        }
        self.log_entries.append(entry)

    def save_log(self, filename="monopoly_game_log.txt"):
        with open(filename, 'w') as f:
            f.write(f"Monopoly Game Log - Started {self.start_time}\n\n")
            for entry in self.log_entries:
                time_str = entry['timestamp'].strftime("%H:%M:%S")
                f.write(
                    f"[{time_str}] {entry['player']} - {entry['event']}: "
                    f"{entry['details'] or ''} "
                    f"{f'(${entry['amount']})' if entry['amount'] else ''}\n"
                )