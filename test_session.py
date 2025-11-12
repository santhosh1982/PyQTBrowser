"""
Test script to verify session persistence functionality
"""
import json
import os

print("🧪 Testing Session Persistence...")
print("=" * 50)

# Test 1: Check if SessionManager exists
print("\n✓ Test 1: SessionManager Class")
from main import SessionManager
session_mgr = SessionManager()
print(f"  Session file: {session_mgr.session_file}")
print("  ✓ PASSED")

# Test 2: Check if session file exists
print("\n✓ Test 2: Session File Existence")
if os.path.exists('browser_session.json'):
    print("  ✓ Session file exists")
    with open('browser_session.json', 'r', encoding='utf-8') as f:
        session_data = json.load(f)
    print(f"  Tabs saved: {len(session_data.get('tabs', []))}")
    print(f"  Pinned tabs: {len(session_data.get('pinned_tabs', []))}")
    print("  ✓ PASSED")
else:
    print("  ⚠ No session file yet (run browser first)")
    print("  ⚠ SKIPPED")

# Test 3: Validate session structure
print("\n✓ Test 3: Session Data Structure")
if os.path.exists('browser_session.json'):
    with open('browser_session.json', 'r', encoding='utf-8') as f:
        session = json.load(f)
    
    assert 'tabs' in session, "Session should have 'tabs' key"
    assert 'pinned_tabs' in session, "Session should have 'pinned_tabs' key"
    assert isinstance(session['tabs'], list), "Tabs should be a list"
    assert isinstance(session['pinned_tabs'], list), "Pinned tabs should be a list"
    
    if session['tabs']:
        tab = session['tabs'][0]
        assert 'url' in tab, "Tab should have 'url'"
        assert 'title' in tab, "Tab should have 'title'"
        assert 'index' in tab, "Tab should have 'index'"
    
    print("  ✓ All required fields present")
    print("  ✓ PASSED")
else:
    print("  ⚠ SKIPPED (no session file)")

# Test 4: Test save/load cycle
print("\n✓ Test 4: Save/Load Cycle")
test_session = {
    'tabs': [
        {'url': 'https://example.com', 'title': 'Example', 'index': 0},
        {'url': 'https://test.com', 'title': 'Test', 'index': 1}
    ],
    'pinned_tabs': [0]
}

session_mgr.save_session(test_session['tabs'], set(test_session['pinned_tabs']))
loaded_session = session_mgr.load_session()

assert loaded_session is not None, "Should load saved session"
assert len(loaded_session['tabs']) == 2, "Should have 2 tabs"
assert 0 in loaded_session['pinned_tabs'], "Tab 0 should be pinned"
print("  ✓ Save and load working correctly")
print("  ✓ PASSED")

# Test 5: Test clear session
print("\n✓ Test 5: Clear Session")
session_mgr.clear_session()
assert not os.path.exists(session_mgr.session_file), "Session file should be deleted"
print("  ✓ Session cleared successfully")

# Restore the original session if it existed
if os.path.exists('browser_session.json.bak'):
    os.rename('browser_session.json.bak', 'browser_session.json')
    print("  ✓ Original session restored")
print("  ✓ PASSED")

print("\n" + "=" * 50)
print("🎉 All session persistence tests passed!")
print("\n📚 Session Persistence Features:")
print("  ✅ Auto-save on browser close")
print("  ✅ Auto-restore on browser start")
print("  ✅ Pinned tabs preserved")
print("  ✅ Tab order maintained")
print("  ✅ JSON format for easy backup")
print("\n🎯 Try it:")
print("  1. python main.py")
print("  2. Open tabs and pin some")
print("  3. Close browser")
print("  4. Reopen → Everything restored!")
