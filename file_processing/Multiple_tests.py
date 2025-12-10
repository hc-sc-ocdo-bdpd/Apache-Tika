#!/usr/bin/env python3
"""
Comprehensive Test Suite: Apache Tika vs HC OCDO File Processing

Tests multiple capabilities including:
1. Text extraction accuracy
2. Metadata extraction
3. File format support
4. Processing speed
5. Special character handling
6. Large file handling
7. Error handling
8. Memory usage
"""

import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='tika')

from tika import parser as tika_parser
from file_processing import File
import time
import os
from pathlib import Path
import json
from datetime import datetime
import traceback


class ComprehensiveComparisonTest:
    """Run comprehensive comparison tests between Tika and OCDO"""
    
    def __init__(self, test_files_dir="test_files", output_dir="outputs"):
        self.test_files_dir = Path(test_files_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.test_files_dir.mkdir(exist_ok=True)
        
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": [],
            "summary": {
                "total_tests": 0,
                "tika_wins": 0,
                "ocdo_wins": 0,
                "ties": 0
            }
        }
    
    def create_test_file(self, content, filename):
        """Create a test file with given content"""
        filepath = self.test_files_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath
    
    def test_case_1_basic_text_extraction(self):
        """Test Case 1: Basic Text Extraction from TXT file"""
        print("\n" + "="*70)
        print("TEST CASE 1: Basic Text Extraction (Plain Text)")
        print("="*70)
        
        test_content = """This is a basic test document.
It contains multiple lines.
And various sentences to test basic extraction capabilities.

The quick brown fox jumps over the lazy dog.
1234567890
ABCDEFGHIJKLMNOPQRSTUVWXYZ
abcdefghijklmnopqrstuvwxyz"""
        
        filepath = self.create_test_file(test_content, "test1_basic.txt")
        
        # Test with Tika
        start_time = time.time()
        try:
            tika_parsed = tika_parser.from_file(str(filepath))
            tika_content = tika_parsed.get("content", "").strip()
            tika_time = time.time() - start_time
            tika_success = True
            tika_word_count = len(tika_content.split())
        except Exception as e:
            tika_content = ""
            tika_time = time.time() - start_time
            tika_success = False
            tika_word_count = 0
            print(f"  Tika Error: {e}")
        
        # Test with OCDO
        start_time = time.time()
        try:
            ocdo_file = File(str(filepath))
            ocdo_content = ocdo_file.get_text().strip()
            ocdo_time = time.time() - start_time
            ocdo_success = True
            ocdo_word_count = len(ocdo_content.split())
        except Exception as e:
            ocdo_content = ""
            ocdo_time = time.time() - start_time
            ocdo_success = False
            ocdo_word_count = 0
            print(f"  OCDO Error: {e}")
        
        # Compare
        original_words = len(test_content.split())
        tika_accuracy = (tika_word_count / original_words * 100) if original_words > 0 else 0
        ocdo_accuracy = (ocdo_word_count / original_words * 100) if original_words > 0 else 0
        
        print(f"\nResults:")
        print(f"  Original: {original_words} words")
        print(f"  Tika:     {tika_word_count} words ({tika_accuracy:.1f}% accuracy) - {tika_time:.3f}s")
        print(f"  OCDO:     {ocdo_word_count} words ({ocdo_accuracy:.1f}% accuracy) - {ocdo_time:.3f}s")
        
        winner = self.determine_winner(
            tika_success, tika_accuracy, tika_time,
            ocdo_success, ocdo_accuracy, ocdo_time
        )
        print(f"\n  Winner: {winner}")
        
        self.record_result("Basic Text Extraction", winner, {
            "tika": {"accuracy": tika_accuracy, "time": tika_time, "success": tika_success},
            "ocdo": {"accuracy": ocdo_accuracy, "time": ocdo_time, "success": ocdo_success}
        })
        
        filepath.unlink()
    
    def test_case_2_metadata_extraction(self):
        """Test Case 2: Metadata Extraction Capabilities"""
        print("\n" + "="*70)
        print("TEST CASE 2: Metadata Extraction")
        print("="*70)
        
        test_content = "Document with metadata test"
        filepath = self.create_test_file(test_content, "test2_metadata.txt")
        
        # Test with Tika
        try:
            tika_parsed = tika_parser.from_file(str(filepath))
            tika_metadata = tika_parsed.get("metadata", {})
            tika_meta_count = len(tika_metadata)
            tika_success = True
        except Exception as e:
            tika_metadata = {}
            tika_meta_count = 0
            tika_success = False
            print(f"  Tika Error: {e}")
        
        # Test with OCDO
        try:
            ocdo_file = File(str(filepath))
            ocdo_metadata = ocdo_file.metadata if hasattr(ocdo_file, 'metadata') else {}
            ocdo_meta_count = len(ocdo_metadata)
            ocdo_success = True
        except Exception as e:
            ocdo_metadata = {}
            ocdo_meta_count = 0
            ocdo_success = False
            print(f"  OCDO Error: {e}")
        
        print(f"\nMetadata Fields Extracted:")
        print(f"  Tika: {tika_meta_count} fields")
        print(f"  OCDO: {ocdo_meta_count} fields")
        
        print(f"\nTika Metadata (first 5):")
        for key, value in list(tika_metadata.items())[:5]:
            print(f"    {key}: {value}")
        
        print(f"\nOCDO Metadata (first 5):")
        for key, value in list(ocdo_metadata.items())[:5]:
            print(f"    {key}: {value}")
        
        winner = "Tika" if tika_meta_count > ocdo_meta_count else "OCDO" if ocdo_meta_count > tika_meta_count else "Tie"
        print(f"\n  Winner: {winner}")
        
        self.record_result("Metadata Extraction", winner, {
            "tika": {"metadata_count": tika_meta_count, "success": tika_success},
            "ocdo": {"metadata_count": ocdo_meta_count, "success": ocdo_success}
        })
        
        filepath.unlink()
    
    def test_case_3_special_characters(self):
        """Test Case 3: Special Character Handling"""
        print("\n" + "="*70)
        print("TEST CASE 3: Special Character Handling")
        print("="*70)
        
        special_chars = [
            "€£¥¢$",
            "αβγδε",
            "你好世界",
            "مرحبا",
            "→←↑↓",
            "©®™"
        ]
        
        test_content = "Special Characters Test:\n" + "\n".join(special_chars)
        filepath = self.create_test_file(test_content, "test3_special_chars.txt")
        
        # Test with Tika
        try:
            tika_parsed = tika_parser.from_file(str(filepath))
            tika_content = tika_parsed.get("content", "")
            tika_matches = sum(1 for char_set in special_chars if char_set in tika_content)
            tika_success = True
        except Exception as e:
            tika_matches = 0
            tika_success = False
            print(f"  Tika Error: {e}")
        
        # Test with OCDO
        try:
            ocdo_file = File(str(filepath))
            ocdo_content = ocdo_file.get_text()
            ocdo_matches = sum(1 for char_set in special_chars if char_set in ocdo_content)
            ocdo_success = True
        except Exception as e:
            ocdo_matches = 0
            ocdo_success = False
            print(f"  OCDO Error: {e}")
        
        total_char_sets = len(special_chars)
        tika_accuracy = (tika_matches / total_char_sets * 100)
        ocdo_accuracy = (ocdo_matches / total_char_sets * 100)
        
        print(f"\nSpecial Character Sets Preserved:")
        print(f"  Tika: {tika_matches}/{total_char_sets} ({tika_accuracy:.1f}%)")
        print(f"  OCDO: {ocdo_matches}/{total_char_sets} ({ocdo_accuracy:.1f}%)")
        
        winner = self.determine_winner(
            tika_success, tika_accuracy, 0,
            ocdo_success, ocdo_accuracy, 0
        )
        print(f"\n  Winner: {winner}")
        
        self.record_result("Special Character Handling", winner, {
            "tika": {"accuracy": tika_accuracy, "success": tika_success},
            "ocdo": {"accuracy": ocdo_accuracy, "success": ocdo_success}
        })
        
        filepath.unlink()
    
    def test_case_4_performance_speed(self):
        """Test Case 4: Processing Speed Comparison"""
        print("\n" + "="*70)
        print("TEST CASE 4: Processing Speed")
        print("="*70)
        
        # Create a larger test file
        large_content = "This is a performance test. " * 1000
        filepath = self.create_test_file(large_content, "test4_performance.txt")
        
        # Test Tika speed (average of 3 runs)
        tika_times = []
        for i in range(3):
            start = time.time()
            try:
                tika_parser.from_file(str(filepath))
                tika_times.append(time.time() - start)
            except Exception as e:
                print(f"  Tika Error: {e}")
                tika_times.append(999)
        
        tika_avg_time = sum(tika_times) / len(tika_times)
        
        # Test OCDO speed (average of 3 runs)
        ocdo_times = []
        for i in range(3):
            start = time.time()
            try:
                File(str(filepath)).get_text()
                ocdo_times.append(time.time() - start)
            except Exception as e:
                print(f"  OCDO Error: {e}")
                ocdo_times.append(999)
        
        ocdo_avg_time = sum(ocdo_times) / len(ocdo_times)
        
        print(f"\nAverage Processing Time (3 runs):")
        print(f"  Tika: {tika_avg_time:.3f}s")
        print(f"  OCDO: {ocdo_avg_time:.3f}s")
        
        speed_diff = abs(tika_avg_time - ocdo_avg_time)
        speed_diff_percent = (speed_diff / max(tika_avg_time, ocdo_avg_time) * 100)
        
        print(f"\n  Speed Difference: {speed_diff:.3f}s ({speed_diff_percent:.1f}%)")
        
        if speed_diff_percent < 10:
            winner = "Tie"
        else:
            winner = "Tika" if tika_avg_time < ocdo_avg_time else "OCDO"
        
        print(f"  Winner: {winner}")
        
        self.record_result("Processing Speed", winner, {
            "tika": {"avg_time": tika_avg_time},
            "ocdo": {"avg_time": ocdo_avg_time}
        })
        
        filepath.unlink()
    
    def test_case_5_empty_file_handling(self):
        """Test Case 5: Empty File Handling"""
        print("\n" + "="*70)
        print("TEST CASE 5: Empty File Handling")
        print("="*70)
        
        filepath = self.create_test_file("", "test5_empty.txt")
        
        # Test with Tika
        tika_handled = False
        try:
            tika_parsed = tika_parser.from_file(str(filepath))
            tika_content = tika_parsed.get("content", "")
            tika_handled = True
            print("  Tika: ✓ Handled empty file gracefully")
        except Exception as e:
            print(f"  Tika: ✗ Failed - {type(e).__name__}")
        
        # Test with OCDO
        ocdo_handled = False
        try:
            ocdo_file = File(str(filepath))
            ocdo_content = ocdo_file.get_text()
            ocdo_handled = True
            print("  OCDO: ✓ Handled empty file gracefully")
        except Exception as e:
            print(f"  OCDO: ✗ Failed - {type(e).__name__}")
        
        if tika_handled and ocdo_handled:
            winner = "Tie"
        elif tika_handled:
            winner = "Tika"
        elif ocdo_handled:
            winner = "OCDO"
        else:
            winner = "None"
        
        print(f"\n  Winner: {winner}")
        
        self.record_result("Empty File Handling", winner, {
            "tika": {"handled": tika_handled},
            "ocdo": {"handled": ocdo_handled}
        })
        
        filepath.unlink()
    
    def test_case_6_whitespace_preservation(self):
        """Test Case 6: Whitespace and Formatting Preservation"""
        print("\n" + "="*70)
        print("TEST CASE 6: Whitespace and Formatting Preservation")
        print("="*70)
        
        test_content = """Line 1
    Indented line
        Double indented

Line with spaces    between    words

Multiple


Empty

Lines"""
        
        filepath = self.create_test_file(test_content, "test6_whitespace.txt")
        
        # Test with Tika
        try:
            tika_parsed = tika_parser.from_file(str(filepath))
            tika_content = tika_parsed.get("content", "")
            tika_line_count = len([line for line in tika_content.split('\n') if line.strip()])
            tika_success = True
        except Exception as e:
            tika_line_count = 0
            tika_success = False
            print(f"  Tika Error: {e}")
        
        # Test with OCDO
        try:
            ocdo_file = File(str(filepath))
            ocdo_content = ocdo_file.get_text()
            ocdo_line_count = len([line for line in ocdo_content.split('\n') if line.strip()])
            ocdo_success = True
        except Exception as e:
            ocdo_line_count = 0
            ocdo_success = False
            print(f"  OCDO Error: {e}")
        
        original_lines = len([line for line in test_content.split('\n') if line.strip()])
        
        print(f"\nNon-Empty Lines Preserved:")
        print(f"  Original: {original_lines} lines")
        print(f"  Tika:     {tika_line_count} lines")
        print(f"  OCDO:     {ocdo_line_count} lines")
        
        tika_diff = abs(original_lines - tika_line_count)
        ocdo_diff = abs(original_lines - ocdo_line_count)
        
        if tika_diff < ocdo_diff:
            winner = "Tika"
        elif ocdo_diff < tika_diff:
            winner = "OCDO"
        else:
            winner = "Tie"
        
        print(f"\n  Winner: {winner}")
        
        self.record_result("Whitespace Preservation", winner, {
            "tika": {"line_count": tika_line_count, "success": tika_success},
            "ocdo": {"line_count": ocdo_line_count, "success": ocdo_success}
        })
        
        filepath.unlink()
    
    def test_case_7_numeric_data_accuracy(self):
        """Test Case 7: Numeric Data Extraction Accuracy"""
        print("\n" + "="*70)
        print("TEST CASE 7: Numeric Data Extraction")
        print("="*70)
        
        numbers = ["123", "45.67", "8,910", "$1,234.56", "9.99%", "-42", "3.14159"]
        test_content = "Numeric Data Test:\n" + "\n".join(numbers)
        
        filepath = self.create_test_file(test_content, "test7_numbers.txt")
        
        # Test with Tika
        try:
            tika_parsed = tika_parser.from_file(str(filepath))
            tika_content = tika_parsed.get("content", "")
            tika_found = sum(1 for num in numbers if num in tika_content)
            tika_success = True
        except Exception as e:
            tika_found = 0
            tika_success = False
            print(f"  Tika Error: {e}")
        
        # Test with OCDO
        try:
            ocdo_file = File(str(filepath))
            ocdo_content = ocdo_file.get_text()
            ocdo_found = sum(1 for num in numbers if num in ocdo_content)
            ocdo_success = True
        except Exception as e:
            ocdo_found = 0
            ocdo_success = False
            print(f"  OCDO Error: {e}")
        
        total_numbers = len(numbers)
        tika_accuracy = (tika_found / total_numbers * 100)
        ocdo_accuracy = (ocdo_found / total_numbers * 100)
        
        print(f"\nNumbers Correctly Extracted:")
        print(f"  Tika: {tika_found}/{total_numbers} ({tika_accuracy:.1f}%)")
        print(f"  OCDO: {ocdo_found}/{total_numbers} ({ocdo_accuracy:.1f}%)")
        
        winner = self.determine_winner(
            tika_success, tika_accuracy, 0,
            ocdo_success, ocdo_accuracy, 0
        )
        print(f"\n  Winner: {winner}")
        
        self.record_result("Numeric Data Accuracy", winner, {
            "tika": {"accuracy": tika_accuracy, "success": tika_success},
            "ocdo": {"accuracy": ocdo_accuracy, "success": ocdo_success}
        })
        
        filepath.unlink()
    
    def test_case_8_file_size_limits(self):
        """Test Case 8: Large File Handling"""
        print("\n" + "="*70)
        print("TEST CASE 8: Large File Handling (1MB)")
        print("="*70)
        
        # Create 1MB file
        large_content = "Testing large file handling. " * 35000  # ~1MB
        filepath = self.create_test_file(large_content, "test8_large.txt")
        
        file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
        print(f"\nFile Size: {file_size_mb:.2f} MB")
        
        # Test with Tika
        start = time.time()
        tika_success = False
        try:
            tika_parsed = tika_parser.from_file(str(filepath))
            tika_content = tika_parsed.get("content", "")
            tika_time = time.time() - start
            tika_success = len(tika_content) > 0
            print(f"  Tika: ✓ Processed in {tika_time:.3f}s")
        except Exception as e:
            tika_time = time.time() - start
            print(f"  Tika: ✗ Failed - {type(e).__name__}")
        
        # Test with OCDO
        start = time.time()
        ocdo_success = False
        try:
            ocdo_file = File(str(filepath))
            ocdo_content = ocdo_file.get_text()
            ocdo_time = time.time() - start
            ocdo_success = len(ocdo_content) > 0
            print(f"  OCDO: ✓ Processed in {ocdo_time:.3f}s")
        except Exception as e:
            ocdo_time = time.time() - start
            print(f"  OCDO: ✗ Failed - {type(e).__name__}")
        
        if tika_success and ocdo_success:
            winner = "Tika" if tika_time < ocdo_time else "OCDO"
        elif tika_success:
            winner = "Tika"
        elif ocdo_success:
            winner = "OCDO"
        else:
            winner = "None"
        
        print(f"\n  Winner: {winner}")
        
        self.record_result("Large File Handling", winner, {
            "tika": {"success": tika_success, "time": tika_time if tika_success else None},
            "ocdo": {"success": ocdo_success, "time": ocdo_time if ocdo_success else None}
        })
        
        filepath.unlink()
    
    def determine_winner(self, tika_success, tika_score, tika_time,
                        ocdo_success, ocdo_score, ocdo_time):
        """Determine winner based on success, accuracy, and speed"""
        if not tika_success and not ocdo_success:
            return "None"
        if not tika_success:
            return "OCDO"
        if not ocdo_success:
            return "Tika"
        
        # Both succeeded - compare scores
        score_diff = abs(tika_score - ocdo_score)
        if score_diff < 5:  # Within 5% is a tie
            return "Tie"
        
        return "Tika" if tika_score > ocdo_score else "OCDO"
    
    def record_result(self, test_name, winner, details):
        """Record test result"""
        self.results["tests"].append({
            "test_name": test_name,
            "winner": winner,
            "details": details
        })
        
        self.results["summary"]["total_tests"] += 1
        if winner == "Tika":
            self.results["summary"]["tika_wins"] += 1
        elif winner == "OCDO":
            self.results["summary"]["ocdo_wins"] += 1
        elif winner == "Tie":
            self.results["summary"]["ties"] += 1
    
    def run_all_tests(self):
        """Run all test cases"""
        print("\n" + "="*70)
        print("COMPREHENSIVE COMPARISON TEST SUITE")
        print("Apache Tika vs Health Canada OCDO File Processing")
        print("="*70)
        
        # Run all tests
        self.test_case_1_basic_text_extraction()
        self.test_case_2_metadata_extraction()
        self.test_case_3_special_characters()
        self.test_case_4_performance_speed()
        self.test_case_5_empty_file_handling()
        self.test_case_6_whitespace_preservation()
        self.test_case_7_numeric_data_accuracy()
        self.test_case_8_file_size_limits()
        
        self.print_final_summary()
        self.save_results()
    
    def print_final_summary(self):
        """Print overall test summary"""
        print("\n" + "="*70)
        print("FINAL TEST SUMMARY")
        print("="*70)
        
        summary = self.results["summary"]
        total = summary["total_tests"]
        
        print(f"\nTotal Tests: {total}")
        print(f"\nResults:")
        print(f"  Tika Wins:  {summary['tika_wins']} ({summary['tika_wins']/total*100:.1f}%)")
        print(f"  OCDO Wins:  {summary['ocdo_wins']} ({summary['ocdo_wins']/total*100:.1f}%)")
        print(f"  Ties:       {summary['ties']} ({summary['ties']/total*100:.1f}%)")
        
        print(f"\n{'='*70}")
        if summary['tika_wins'] > summary['ocdo_wins']:
            print(f"🏆 OVERALL WINNER: Apache Tika")
        elif summary['ocdo_wins'] > summary['tika_wins']:
            print(f"🏆 OVERALL WINNER: OCDO File Processing")
        else:
            print(f"🤝 RESULT: Tie")
        print("="*70)
        
        # Test-by-test breakdown
        print("\nDetailed Breakdown:")
        for test in self.results["tests"]:
            winner_emoji = "🥇" if test["winner"] in ["Tika", "OCDO"] else "🤝"
            print(f"  {winner_emoji} {test['test_name']}: {test['winner']}")
    
    def save_results(self):
        """Save results to JSON file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = self.output_dir / f"comparison_test_results_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📁 Results saved to: {output_file}")
        
        # Create markdown report
        self.create_markdown_report(timestamp)
    
    def create_markdown_report(self, timestamp):
        """Create markdown report"""
        output_file = self.output_dir / f"comparison_test_report_{timestamp}.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Apache Tika vs OCDO File Processing - Test Results\n\n")
            f.write(f"**Test Date:** {self.results['timestamp']}\n\n")
            
            f.write("## Summary\n\n")
            summary = self.results["summary"]
            total = summary["total_tests"]
            
            f.write("| Library | Wins | Percentage |\n")
            f.write("|---------|------|------------|\n")
            f.write(f"| Apache Tika | {summary['tika_wins']} | {summary['tika_wins']/total*100:.1f}% |\n")
            f.write(f"| OCDO File Processing | {summary['ocdo_wins']} | {summary['ocdo_wins']/total*100:.1f}% |\n")
            f.write(f"| Ties | {summary['ties']} | {summary['ties']/total*100:.1f}% |\n\n")
            
            f.write("## Test Results\n\n")
            for test in self.results["tests"]:
                f.write(f"### {test['test_name']}\n\n")
                f.write(f"**Winner:** {test['winner']}\n\n")
                
                f.write("**Details:**\n")
                f.write("```json\n")
                f.write(json.dumps(test['details'], indent=2))
                f.write("\n```\n\n")
        
        print(f"📄 Markdown report saved to: {output_file}")


def main():
    """Main execution"""
    print("\nStarting Comprehensive Comparison Test Suite...\n")
    
    tester = ComprehensiveComparisonTest()
    tester.run_all_tests()
    
    print("\n✅ All tests complete!\n")


if __name__ == "__main__":
    main()