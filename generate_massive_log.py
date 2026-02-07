"""
Massive Log Generator for Long Context Showcase
Creates huge log files to demonstrate Gemini 3's extended context window.
"""
import random
from datetime import datetime, timedelta

def generate_massive_log(output_path='/tmp/massive_system.log', num_lines=50000):
    """
    Generate a massive system log with a needle-in-haystack critical error.
    
    This showcases Gemini 3's ability to analyze entire log files (10MB+)
    and find correlations that would be impossible with traditional tools.
    """
    
    print(f"[INFO] Generating {num_lines} log lines... (this may take a minute)")
    
    # Simulated services and log patterns
    services = ['nginx', 'postgresql', 'redis', 'rabbitmq', 'celery', 'gunicorn']
    log_levels = ['INFO', 'DEBUG', 'WARNING']
    normal_messages = [
        'Request processed successfully',
        'Connection established',
        'Cache hit',
        'Query executed in {}ms',
        'Background job completed',
        'Health check passed',
        'Metrics reported',
        'Session created'
    ]
    
    start_time = datetime.now() - timedelta(hours=2)
    
    with open(output_path, 'w') as f:
        for i in range(num_lines):
            timestamp = start_time + timedelta(seconds=i * 0.1)
            service = random.choice(services)
            level = random.choice(log_levels)
            message = random.choice(normal_messages)
            
            if '{}' in message:
                message = message.format(random.randint(10, 500))
            
            log_line = f"{timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} [{service}] {level}: {message}\n"
            f.write(log_line)
            
            # THE NEEDLE: Insert critical error at random position (around 60%)
            if i == int(num_lines * 0.6):
                critical_time = timestamp + timedelta(seconds=1)
                f.write(f"{critical_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} [postgresql] ERROR: Connection pool exhausted - max_connections=100 reached\n")
                f.write(f"{critical_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} [postgresql] CRITICAL: Database deadlock detected on table 'users'\n")
                f.write(f"{critical_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} [gunicorn] ERROR: Worker timeout (30s) - killing worker pid=15234\n")
    
    print(f"[OK] Generated {output_path}")
    print(f"[INFO] File size: ~{num_lines * 100 / 1024 / 1024:.2f} MB")
    print(f"[TEST] Challenge: Find the database deadlock error among {num_lines} lines")
    print(f"\n[DEMO] Agent objective: 'Analyze /tmp/massive_system.log and find any database errors'")

if __name__ == "__main__":
    generate_massive_log()
