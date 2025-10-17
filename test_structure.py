"""
Simple test script to verify the bot structure and imports.
"""

import sys


def test_imports():
    """Test that all modules can be imported."""
    try:
        import config
        print("✓ config module imported successfully")
        
        import gemini_client
        print("✓ gemini_client module imported successfully")
        
        import bot
        print("✓ bot module imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_config_structure():
    """Test that config module has required attributes."""
    try:
        from config import config
        
        # Check that config has the required attributes
        assert hasattr(config, 'discord_token'), "Missing discord_token attribute"
        assert hasattr(config, 'gemini_api_key'), "Missing gemini_api_key attribute"
        assert hasattr(config, 'validate'), "Missing validate method"
        
        print("✓ config module has all required attributes")
        return True
    except (ImportError, AssertionError) as e:
        print(f"✗ Config structure error: {e}")
        return False


def test_gemini_client_structure():
    """Test that GeminiClient has required methods."""
    try:
        from gemini_client import GeminiClient
        
        # Check that GeminiClient has required methods
        assert hasattr(GeminiClient, 'generate_content'), "Missing generate_content method"
        assert hasattr(GeminiClient, '_extract_text'), "Missing _extract_text method"
        
        print("✓ GeminiClient has all required methods")
        return True
    except (ImportError, AssertionError) as e:
        print(f"✗ GeminiClient structure error: {e}")
        return False


def test_bot_structure():
    """Test that GeminiBot has required methods."""
    try:
        from bot import GeminiBot
        
        # Check that GeminiBot has required methods
        assert hasattr(GeminiBot, 'on_ready'), "Missing on_ready method"
        assert hasattr(GeminiBot, 'on_message'), "Missing on_message method"
        
        print("✓ GeminiBot has all required methods")
        return True
    except (ImportError, AssertionError) as e:
        print(f"✗ GeminiBot structure error: {e}")
        return False


def main():
    """Run all tests."""
    print("Running structure tests...\n")
    
    tests = [
        test_imports,
        test_config_structure,
        test_gemini_client_structure,
        test_bot_structure
    ]
    
    results = [test() for test in tests]
    
    print(f"\n{'='*50}")
    if all(results):
        print("All tests passed! ✓")
        return 0
    else:
        print("Some tests failed! ✗")
        return 1


if __name__ == "__main__":
    sys.exit(main())
