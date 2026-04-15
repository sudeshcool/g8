"""
Convert Excel files to SQLite database
"""
import pandas as pd
import sqlite3
import os

def convert_excel_to_sqlite():
    """Convert all Excel files to a single SQLite database"""
    
    # Database file path
    db_path = 'data.db'
    
    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")
    
    # Create connection
    conn = sqlite3.connect(db_path)
    print(f"Created new database: {db_path}")
    
    try:
        # Convert Crest Workspace SR (Service Requests) -> crest_workspace table
        print("\nConverting Crest Workspace SR.xlsx...")
        df_sr = pd.read_excel('Crest Workspace SR.xlsx')
        df_sr.to_sql('crest_workspace', conn, if_exists='replace', index=False)
        print(f"  ✓ Loaded {len(df_sr)} records into 'crest_workspace' table")
        
        # Convert Export with Category (Workplace tickets) -> export_category table
        print("\nConverting Export with Category for CREST.xlsx...")
        df_export = pd.read_excel('Export with Category for CREST.xlsx')
        df_export.to_sql('export_category', conn, if_exists='replace', index=False)
        print(f"  ✓ Loaded {len(df_export)} records into 'export_category' table")
        
        # Convert Decisions
        print("\nConverting decisions.xlsx...")
        df_decisions = pd.read_excel('decisions.xlsx')
        df_decisions.to_sql('decisions', conn, if_exists='replace', index=False)
        print(f"  ✓ Loaded {len(df_decisions)} records into 'decisions' table")
        
        # Create indexes for better performance
        print("\nCreating indexes...")
        cursor = conn.cursor()
        
        # Indexes for crest_workspace
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_crest_status ON crest_workspace(Status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_crest_priority ON crest_workspace(Priority)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_crest_category ON crest_workspace(Category)')
        
        # Indexes for export_category
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_export_status ON export_category(Status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_export_priority ON export_category(Priority)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_export_category ON export_category(Category)')
        
        print("  ✓ Indexes created")
        
        conn.commit()
        
        # Get database size
        db_size = os.path.getsize(db_path) / (1024 * 1024)  # Convert to MB
        print(f"\n✅ Conversion complete!")
        print(f"Database size: {db_size:.2f} MB")
        print(f"Database location: {os.path.abspath(db_path)}")
        
        # Show table info
        print("\nDatabase tables:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"  - {table[0]}: {count} records")
        
    except Exception as e:
        print(f"\n❌ Error during conversion: {e}")
        raise
    finally:
        conn.close()
        print("\nDatabase connection closed")

if __name__ == '__main__':
    print("=" * 60)
    print("Excel to SQLite Converter")
    print("=" * 60)
    convert_excel_to_sqlite()

# Made with Bob
