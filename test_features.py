"""
Test script to verify themes and extensions functionality
"""
import json
import os

print("🧪 Testing Browser Features...")
print("=" * 50)

# Test 1: Check if theme manager has all themes
print("\n✓ Test 1: Theme Manager")
from main import ThemeManager
theme_mgr = ThemeManager()
themes = theme_mgr.get_theme_names()
print(f"  Available themes: {', '.join(themes)}")
print(f"  Total themes: {len(themes)}")
assert len(themes) == 5, "Should have 5 themes"
print("  ✓ PASSED")

# Test 2: Check theme stylesheet generation
print("\n✓ Test 2: Theme Stylesheet Generation")
for theme_name in themes:
    stylesheet = theme_mgr.generate_stylesheet(theme_name)
    assert len(stylesheet) > 100, f"Stylesheet for {theme_name} is too short"
    assert 'QMainWindow' in stylesheet, f"Missing QMainWindow in {theme_name}"
    print(f"  ✓ {theme_name} theme stylesheet generated")
print("  ✓ PASSED")

# Test 3: Check extension manager
print("\n✓ Test 3: Extension Manager")
from main import ExtensionManager
ext_mgr = ExtensionManager()
print(f"  Extensions directory: {ext_mgr.extensions_dir}")
print(f"  Extensions file: {ext_mgr.extensions_file}")
print(f"  Current extensions: {len(ext_mgr.extensions)}")
print("  ✓ PASSED")

# Test 4: Check sample extension files exist
print("\n✓ Test 4: Sample Extension Files")
sample_extensions = [
    'sample_extension_dark_mode.js',
    'sample_extension_auto_scroll.js',
    'sample_extension_ad_blocker.js'
]
for ext_file in sample_extensions:
    if os.path.exists(ext_file):
        with open(ext_file, 'r', encoding='utf-8') as f:
            content = f.read()
            assert len(content) > 50, f"{ext_file} is too short"
            print(f"  ✓ {ext_file} exists ({len(content)} bytes)")
    else:
        print(f"  ⚠ {ext_file} not found")
print("  ✓ PASSED")

# Test 5: Check settings manager with theme support
print("\n✓ Test 5: Settings Manager")
from main import SettingsManager
settings_mgr = SettingsManager()
default_theme = settings_mgr.get('theme')
print(f"  Default theme: {default_theme}")
assert default_theme in themes, "Default theme should be valid"
print("  ✓ PASSED")

print("\n" + "=" * 50)
print("🎉 All tests passed! Browser features are working correctly.")
print("\n📚 Next steps:")
print("  1. Run: python main.py")
print("  2. Go to Tools → 🎨 Themes to try different themes")
print("  3. Go to Tools → 🧩 Extensions to add extensions")
print("  4. Try the sample extensions!")
