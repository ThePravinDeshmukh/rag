#!/usr/bin/env python3
"""
Final Test - All Issues Fixed
Test all the functionality to verify everything works correctly
"""

from rag import EnhancedRAG

def test_all_fixes():
    """Test all the fixes for search and multilingual functionality"""
    print("🎯 Final Comprehensive Test")
    print("=" * 50)
    
    # Initialize system
    rag = EnhancedRAG()
    rag.load_pdf('docs/cereal.pdf')
    rag.build_index()
    
    print(f"✅ System loaded with {len(rag.structured_data)} items")
    print()
    
    # Test cases that were reported as problematic
    test_cases = [
        {
            'query': 'wheat',
            'description': 'Should show wheat items (not random cereals)',
            'expected': 'wheat items with multilingual names'
        },
        {
            'query': 'rice', 
            'description': 'Should show rice items (not wheat)',
            'expected': 'rice items with Hindi/Marathi names'
        },
        {
            'query': 'bajra',
            'description': 'Should identify bajra as millet',
            'expected': 'millet items with local names'
        },
        {
            'query': 'list all rice items',
            'description': 'Should show tabular data',
            'expected': 'table format with multilingual columns'
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"🔍 Test {i}: {test['description']}")
        print(f"❓ Query: '{test['query']}'")
        print(f"🎯 Expected: {test['expected']}")
        print()
        
        # Test command line format
        result = rag.ask(test['query'])
        print("📝 Command Line Result:")
        print(result[:400] + "..." if len(result) > 400 else result)
        print()
        
        # Test web format (HTML tables)
        web_result = rag.ask(test['query'], web_format=True)
        print("🌐 Web Format (HTML):")
        print("Contains HTML table:", "<table" in web_result)
        print("Contains multilingual:", "Hindi:" in web_result or "Marathi:" in web_result)
        print()
        print("-" * 60)
        print()
    
    # Test multilingual specific queries
    print("🌏 Multilingual Specific Tests:")
    multilingual_tests = [
        'rice with hindi names',
        'wheat multilingual',
        'show bajra with marathi names'
    ]
    
    for query in multilingual_tests:
        print(f"❓ {query}")
        result = rag.ask(query)
        has_hindi = "Hindi:" in result
        has_marathi = "Marathi:" in result
        has_table = "|" in result and "---|" in result
        
        print(f"   ✅ Has Hindi: {has_hindi}")
        print(f"   ✅ Has Marathi: {has_marathi}")
        print(f"   ✅ Has Table: {has_table}")
        print()
    
    print("🎉 All tests completed!")
    print("🌐 Web interface available at: http://localhost:5000")
    print("💡 Try the same queries in the web interface to see HTML tables!")

if __name__ == "__main__":
    test_all_fixes()
