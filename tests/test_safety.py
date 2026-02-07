import unittest
import shlex
from backend.tools.process import ProcessTools

class TestSafety(unittest.TestCase):
    def test_shlex_usage(self):
        """Verify absolute immunity to Shell Injection in kill commands."""
        # Mock strategy (not needed for this test)
        tools = ProcessTools(strategy=None)
        
        # Test Case 1: Malicious PID with semicolon
        malicious_input = "1234; rm -rf /"
        cmd = tools.kill_process_command(malicious_input, force=True)
        
        # Expectation: The malicious string should be quoted, rendering it harmless
        # kill -9 '1234; rm -rf /'
        expected_part = shlex.quote(malicious_input)
        self.assertIn(expected_part, cmd)
        self.assertNotIn("rm -rf /", cmd.replace(expected_part, "")) # Ensure raw injection is impossible

if __name__ == '__main__':
    unittest.main()
