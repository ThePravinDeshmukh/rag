#!/usr/bin/env python3
"""
Project Cleanup - Remove unused and duplicate files
Keep only essential files for your multi-PDF nutrition system
"""

import os
import shutil

def analyze_project_files():
    """Analyze which files are essential vs redundant"""
    
    essential_files = {
        # Core system
        'rag.py': 'Main enhanced RAG system (KEEP)',
        'web_local.py': 'Web interface (KEEP)', 
        'web_app.py': 'Alternative web interface (EVALUATE)',
        
        # Configuration
        'requirements_minimal.txt': 'Dependencies (KEEP)',
        '.env': 'Environment variables (KEEP)',
        
        # Documentation  
        'README.md': 'Main documentation (KEEP)',
        'CLEANUP_SUMMARY.md': 'Cleanup history (KEEP)',
        'PROBLEM_SOLVED.md': 'Solution documentation (KEEP)',
        
        # Essential demo/test
        'demo_multilingual.py': 'Main demo (KEEP)',
        'test_final.py': 'Comprehensive tests (KEEP)',
    }
    
    redundant_files = {
        # Duplicate/old test files
        'test.py': 'Old test file',
        'test_cereals.py': 'Specific cereal test (covered by test_final.py)',
        'test_multilingual.py': 'Specific multilingual test (covered by test_final.py)', 
        'test_oats_final.py': 'Specific oats test',
        
        # Old demo files
        'demo.py': 'Old demo (replaced by demo_multilingual.py)',
        
        # Debug/analysis files (temporary)
        'debug_extraction.py': 'Temporary debug file',
        'debug_oats.py': 'Temporary debug file',
        'check_oats_raw.py': 'Temporary analysis',
        'analyze_pdf.py': 'Temporary analysis',
        
        # Comparison files (educational but not needed)
        'comparison_analysis.py': 'Educational comparison',
        'simple_cereal_lookup.py': 'Alternative approach demo',
        'multi_pdf_manager.py': 'One-time analysis tool',
        
        # Generated files
        'cereal_data.json': 'Generated output from simple lookup',
        
        # Old documentation
        'README_NEW.md': 'Duplicate documentation',
        'README_SIMPLE.md': 'Old simple version docs',
        
        # Old UI files
        'ui_demo.html': 'Static HTML demo',
        'app_render.py': 'Alternative web interface (if web_local.py works)',
        
        # Old cleanup
        'cleanup_old_rag.py': 'One-time cleanup script (already used)',
    }
    
    print("🗂️  Project File Analysis")
    print("=" * 50)
    
    print("✅ **Essential Files (KEEP):**")
    for file, desc in essential_files.items():
        status = "✅" if os.path.exists(file) else "❌ MISSING"
        print(f"  {status} {file} - {desc}")
    
    print(f"\n🗑️  **Redundant Files (CAN REMOVE):**")
    for file, desc in redundant_files.items():
        status = "📁" if os.path.exists(file) else "⚪ Not found"
        print(f"  {status} {file} - {desc}")
    
    return essential_files, redundant_files

def cleanup_project():
    """Remove redundant files to clean up the project"""
    
    essential_files, redundant_files = analyze_project_files()
    
    print(f"\n🧹 Starting Project Cleanup...")
    print("-" * 30)
    
    removed_count = 0
    kept_count = 0
    
    for file in redundant_files.keys():
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"✅ Removed: {file}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Failed to remove {file}: {e}")
        else:
            print(f"⚪ Not found: {file}")
    
    print(f"\n📊 Cleanup Summary:")
    print(f"✅ Essential files kept: {len(essential_files)}")
    print(f"🗑️  Redundant files removed: {removed_count}")
    
    print(f"\n📁 Your Clean Project Structure:")
    print("Core System:")
    print("  • rag.py - Enhanced RAG with multilingual support")
    print("  • web_local.py - Web interface")
    print("  • demo_multilingual.py - Main demo script")
    print("  • test_final.py - Comprehensive tests")
    print()
    print("Configuration:")
    print("  • requirements_minimal.txt - Dependencies")
    print("  • .env - Environment settings")
    print()
    print("Documentation:")
    print("  • README.md - Project documentation")
    print("  • CLEANUP_SUMMARY.md - Cleanup history")
    print("  • PROBLEM_SOLVED.md - Solution documentation")
    print()
    print("Data:")
    print("  • docs/ - Your 13 PDF documents")
    print("  • venv/ - Virtual environment")

if __name__ == "__main__":
    cleanup_project()
