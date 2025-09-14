#!/usr/bin/env python3
"""
Script to analyze the exact statistics of maibert_dataset.csv
for creating the classification dataset overview table
"""

import pandas as pd
import numpy as np

def analyze_dataset():
    # Load the dataset
    df = pd.read_csv('data/maibert_dataset.csv')
    
    print("=== DATASET ANALYSIS ===")
    print(f"Total samples: {len(df)}")
    print(f"Total categories: {df['labels'].nunique()}")
    print(f"Categories: {sorted(df['labels'].unique().tolist())}")
    print()
    
    # Add text statistics columns if they don't exist
    if 'text_length' not in df.columns:
        df['text_length'] = df['text'].str.len()
    if 'word_count' not in df.columns:
        df['word_count'] = df['text'].str.split().str.len()
    if 'sentence_count' not in df.columns:
        df['sentence_count'] = df['text'].str.split('[।!?]').str.len()
    
    # Define text complexity levels based on character length
    def categorize_text_length(length):
        if length < 100:
            return 'Short'
        elif length <= 1000:
            return 'Medium'
        else:
            return 'Long'
    
    df['complexity'] = df['text_length'].apply(categorize_text_length)
    
    print("=== OVERALL STATISTICS ===")
    print(f"Text Length - Mean: {df['text_length'].mean():.1f}, Std: {df['text_length'].std():.1f}")
    print(f"Word Count - Mean: {df['word_count'].mean():.1f}, Std: {df['word_count'].std():.1f}")
    print(f"Sentence Count - Mean: {df['sentence_count'].mean():.1f}, Std: {df['sentence_count'].std():.1f}")
    print()
    
    print("=== CATEGORY DISTRIBUTION ===")
    category_counts = df['labels'].value_counts().sort_values(ascending=False)
    for category, count in category_counts.items():
        print(f"{category:12}: {count:4d}")
    print()
    
    print("=== TEXT COMPLEXITY DISTRIBUTION ===")
    complexity_dist = df['complexity'].value_counts()
    for complexity, count in complexity_dist.items():
        print(f"{complexity:6}: {count:4d}")
    print()
    
    print("=== DETAILED TABLE DATA ===")
    print("Category | Short Count | Short Avg Words | Short Avg Sent | Medium Count | Medium Avg Words | Medium Avg Sent | Long Count | Long Avg Words | Long Avg Sent")
    print("-" * 120)
    
    categories = sorted(df['labels'].unique())
    totals = {'Short': {'count': 0, 'words': 0, 'sentences': 0},
              'Medium': {'count': 0, 'words': 0, 'sentences': 0},
              'Long': {'count': 0, 'words': 0, 'sentences': 0}}
    
    for category in categories:
        cat_data = df[df['labels'] == category]
        
        # Short texts
        short_texts = cat_data[cat_data['complexity'] == 'Short']
        short_count = len(short_texts)
        short_avg_words = short_texts['word_count'].mean() if short_count > 0 else 0
        short_avg_sent = short_texts['sentence_count'].mean() if short_count > 0 else 0
        
        # Medium texts
        medium_texts = cat_data[cat_data['complexity'] == 'Medium']
        medium_count = len(medium_texts)
        medium_avg_words = medium_texts['word_count'].mean() if medium_count > 0 else 0
        medium_avg_sent = medium_texts['sentence_count'].mean() if medium_count > 0 else 0
        
        # Long texts
        long_texts = cat_data[cat_data['complexity'] == 'Long']
        long_count = len(long_texts)
        long_avg_words = long_texts['word_count'].mean() if long_count > 0 else 0
        long_avg_sent = long_texts['sentence_count'].mean() if long_count > 0 else 0
        
        print(f"{category:12} | {short_count:10d} | {short_avg_words:14.1f} | {short_avg_sent:13.1f} | {medium_count:11d} | {medium_avg_words:15.1f} | {medium_avg_sent:14.1f} | {long_count:9d} | {long_avg_words:13.1f} | {long_avg_sent:12.1f}")
        
        # Update totals
        totals['Short']['count'] += short_count
        totals['Short']['words'] += short_avg_words * short_count if short_count > 0 else 0
        totals['Short']['sentences'] += short_avg_sent * short_count if short_count > 0 else 0
        
        totals['Medium']['count'] += medium_count
        totals['Medium']['words'] += medium_avg_words * medium_count if medium_count > 0 else 0
        totals['Medium']['sentences'] += medium_avg_sent * medium_count if medium_count > 0 else 0
        
        totals['Long']['count'] += long_count
        totals['Long']['words'] += long_avg_words * long_count if long_count > 0 else 0
        totals['Long']['sentences'] += long_avg_sent * long_count if long_count > 0 else 0
    
    # Calculate total averages
    short_total_avg_words = totals['Short']['words'] / totals['Short']['count'] if totals['Short']['count'] > 0 else 0
    short_total_avg_sent = totals['Short']['sentences'] / totals['Short']['count'] if totals['Short']['count'] > 0 else 0
    
    medium_total_avg_words = totals['Medium']['words'] / totals['Medium']['count'] if totals['Medium']['count'] > 0 else 0
    medium_total_avg_sent = totals['Medium']['sentences'] / totals['Medium']['count'] if totals['Medium']['count'] > 0 else 0
    
    long_total_avg_words = totals['Long']['words'] / totals['Long']['count'] if totals['Long']['count'] > 0 else 0
    long_total_avg_sent = totals['Long']['sentences'] / totals['Long']['count'] if totals['Long']['count'] > 0 else 0
    
    print("-" * 120)
    print(f"{'TOTAL':12} | {totals['Short']['count']:10d} | {short_total_avg_words:14.1f} | {short_total_avg_sent:13.1f} | {totals['Medium']['count']:11d} | {medium_total_avg_words:15.1f} | {medium_total_avg_sent:14.1f} | {totals['Long']['count']:9d} | {long_total_avg_words:13.1f} | {long_total_avg_sent:12.1f}")
    
    print("\n=== LATEX TABLE FORMAT ===")
    for category in categories:
        cat_data = df[df['labels'] == category]
        
        short_texts = cat_data[cat_data['complexity'] == 'Short']
        short_count = len(short_texts)
        short_avg_words = short_texts['word_count'].mean() if short_count > 0 else 0
        short_avg_sent = short_texts['sentence_count'].mean() if short_count > 0 else 0
        
        medium_texts = cat_data[cat_data['complexity'] == 'Medium']
        medium_count = len(medium_texts)
        medium_avg_words = medium_texts['word_count'].mean() if medium_count > 0 else 0
        medium_avg_sent = medium_texts['sentence_count'].mean() if medium_count > 0 else 0
        
        long_texts = cat_data[cat_data['complexity'] == 'Long']
        long_count = len(long_texts)
        long_avg_words = long_texts['word_count'].mean() if long_count > 0 else 0
        long_avg_sent = long_texts['sentence_count'].mean() if long_count > 0 else 0
        
        print(f"{category} & {short_count} & {short_avg_words:.1f} & {short_avg_sent:.1f} & {medium_count} & {medium_avg_words:.1f} & {medium_avg_sent:.1f} & {long_count} & {long_avg_words:.1f} & {long_avg_sent:.1f} \\\\")
    
    print(f"\\midrule")
    print(f"\\textbf{{Total}} & \\textbf{{{totals['Short']['count']}}} & \\textbf{{{short_total_avg_words:.1f}}} & \\textbf{{{short_total_avg_sent:.1f}}} & \\textbf{{{totals['Medium']['count']}}} & \\textbf{{{medium_total_avg_words:.1f}}} & \\textbf{{{medium_total_avg_sent:.1f}}} & \\textbf{{{totals['Long']['count']}}} & \\textbf{{{long_total_avg_words:.1f}}} & \\textbf{{{long_total_avg_sent:.1f}}} \\\\")

if __name__ == "__main__":
    analyze_dataset()