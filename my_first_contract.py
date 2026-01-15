# { "Depends": "py-genlayer:test" }

from genlayer import *

class Hello(gl.Contract):
    """
    My First Intelligent Contract!
    This contract stores a name and greets people.
    """
    name: str
    greeting_count: u256  # Count how many times we've greeted
    
    def __init__(self, name: str):
        """Initialize the contract with a name"""
        self.name = name
        self.greeting_count = 0
    
    @gl.public.view
    def run(self) -> str:
        """
        Read-only method that returns a greeting.
        This doesn't change any data or cost gas.
        """
        return f'Hello, {self.name}! You have been greeted {self.greeting_count} times.'
    
    @gl.public.view
    def get_name(self) -> str:
        """Get the current name"""
        return self.name
    
    @gl.public.write
    def set_name(self, name: str):
        """
        Change the name stored in the contract.
        This modifies state, so it requires a transaction.
        """
        print(f'Debug: Changing name from {self.name} to {name}')
        self.name = name
    
    @gl.public.write
    def greet(self) -> str:
        """
        Increment the greeting counter and return a message.
        This modifies state by increasing the counter.
        """
        self.greeting_count += 1
        print(f'Debug: Greeting count is now {self.greeting_count}')
        return f'Hello, {self.name}! This is greeting number {self.greeting_count}!'
