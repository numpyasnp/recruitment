import logging
import socket
import json
from datetime import datetime


class JsonTCPLogHandler(logging.Handler):
    def __init__(self, host="logstash", port=5959):
        super().__init__()
        self.host = host
        self.port = port
        self.sock = None
        self.connect_socket()

    def connect_socket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
        except Exception as e:
            print(f"[ELK Log] Failed to connect to Logstash at {self.host}:{self.port} -> {e}")
            self.sock = None

    def emit(self, record):
        try:
            if self.sock is None:
                self.connect_socket()
                if self.sock is None:
                    return  # Hala bağlantı yoksa log'u atla

            log_data = {
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "asctime": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            }

            # Extra alanları ayıkla
            standard_attrs = logging.LogRecord("", "", "", "", "", "", "", "").__dict__.keys()
            extras = {k: v for k, v in record.__dict__.items() if k not in standard_attrs}

            log_data.update(extras)

            self.sock.sendall((json.dumps(log_data) + "\n").encode("utf-8"))

        except (BrokenPipeError, ConnectionResetError):
            print("[ELK Log] Connection to Logstash was lost. Reconnecting...")
            self.sock.close()
            self.sock = None
            self.emit(record)  # tekrar dene
        except Exception as e:
            print(f"[ELK Log] Logging error: {e}")

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
        super().close()
