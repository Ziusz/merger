#!/usr/bin/env python3
import os
import sys
import argparse
import fnmatch
from pathlib import Path

def merge_contracts(src_dir, output_file, extensions=None, exclude_patterns=None):
    """Merge all source files in directory into a single file with source comments."""
    
    if extensions is None:
        extensions = ['.sol']
    
    if exclude_patterns is None:
        exclude_patterns = ['node_modules', '.git', 'build', 'cache', 'out', 'artifacts']
    
    # Ensure extensions start with dot
    extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
    
    # Find all matching files
    matched_files = []
    for root, dirs, files in os.walk(src_dir):
        # Exclude directories based on patterns
        included_dirs = []
        for d in dirs:
            # A directory is excluded if it matches ANY of the patterns
            if not any(fnmatch.fnmatch(d, pattern) for pattern in exclude_patterns):
                included_dirs.append(d)
        
        dirs[:] = included_dirs
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                matched_files.append(os.path.join(root, file))
    
    # Sort files for consistent output
    matched_files.sort()
    
    if not matched_files:
        print(f"No files with extensions {extensions} found in {src_dir}")
        return
    
    # Write merged content
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(f"// Merged source files from {src_dir}\n")
        outfile.write(f"// Extensions: {', '.join(extensions)}\n")
        
        for file_path in matched_files:
            # Get relative path for cleaner comments
            rel_path = os.path.relpath(file_path, src_dir)
            
            try:
                # Read file content
                with open(file_path, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                
                # Write separator and source comment
                outfile.write(f"\n// {'='*80}\n")
                outfile.write(f"// Source: {rel_path}\n")
                outfile.write(f"// {'='*80}\n\n")
                
                # Write file content
                outfile.write(content)
                outfile.write("\n")
            except Exception as e:
                print(f"Warning: Could not read {rel_path}: {e}")
    
    # Print summary
    total_size = os.path.getsize(output_file)
    print(f"✓ Merged {len(matched_files)} files into {output_file}")
    print(f"  Total size: {total_size:,} bytes ({total_size/1024/1024:.2f} MB)")
    print(f"\nMerged files:")
    for f in matched_files[:10]:
        print(f"  - {os.path.relpath(f, src_dir)}")
    if len(matched_files) > 10:
        print(f"  ... and {len(matched_files) - 10} more files")

def main():
    parser = argparse.ArgumentParser(
        description="Merge source files into a single file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Merge Solidity contracts
  python merger.py src/ merged.sol
  
  # Merge TypeScript files
  python merger.py src/ merged.ts -e ts tsx
  
  # Merge multiple file types
  python merger.py . all_code.txt -e py js ts sol
  
  # Exclude specific directories by name
  python merger.py src/ output.sol --exclude test mocks
  
  # Exclude directories using wildcard patterns
  python merger.py src/ output.sol --exclude '*Test' '*_mocks'
"""
    )
    
    parser.add_argument('src_dir', help='Source directory to scan')
    parser.add_argument('output_file', help='Output file path')
    parser.add_argument('-e', '--extensions', nargs='+', 
                        help='File extensions to include (default: sol)')
    parser.add_argument('--exclude', nargs='+', 
                        help='Directory name patterns to exclude from scan (e.g., "mocks", "*Test")')
    
    args = parser.parse_args()
    
    # Validate source directory
    if not os.path.isdir(args.src_dir):
        print(f"Error: Source directory not found: {args.src_dir}")
        sys.exit(1)
    
    # Set default extensions if none provided
    extensions = args.extensions if args.extensions else ['sol']
    
    # Merge exclude directories with defaults
    exclude_patterns = ['node_modules', '.git', 'build', 'cache', 'out', 'artifacts']
    if args.exclude:
        exclude_patterns.extend(args.exclude)
    
    merge_contracts(args.src_dir, args.output_file, extensions, exclude_patterns)

if __name__ == "__main__":
    main()