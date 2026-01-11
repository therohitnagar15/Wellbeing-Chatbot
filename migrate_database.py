#!/usr/bin/env python3
"""
Database migration script to add missing columns to existing database.
This script handles schema updates for the Wellbeing Chatbot database.
"""

import sqlite3
import os

def migrate_database():
    """Add missing columns to existing database tables."""

    db_path = 'wellbeing.db'

    if not os.path.exists(db_path):
        print("Database file not found. No migration needed.")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if language column exists in users table
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]

        if 'language' not in column_names:
            print("Adding 'language' column to users table...")
            cursor.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'en'")
            print("✅ Added language column to users table")
        else:
            print("✅ Language column already exists in users table")

        # Check if other tables need updates
        # Check mood_logs table structure
        cursor.execute("PRAGMA table_info(mood_logs)")
        mood_columns = cursor.fetchall()
        mood_column_names = [col[1] for col in mood_columns]

        # Ensure mood_logs has proper structure
        if 'user_id' not in mood_column_names:
            print("⚠️  Warning: mood_logs table might need user_id column")
        else:
            print("✅ mood_logs table structure looks good")

        # Check chat_history table
        cursor.execute("PRAGMA table_info(chat_history)")
        chat_columns = cursor.fetchall()
        chat_column_names = [col[1] for col in chat_columns]

        if 'user_id' not in chat_column_names:
            print("⚠️  Warning: chat_history table might need user_id column")
        else:
            print("✅ chat_history table structure looks good")

        # Check feedback table
        cursor.execute("PRAGMA table_info(feedback)")
        feedback_columns = cursor.fetchall()
        feedback_column_names = [col[1] for col in feedback_columns]

        if 'user_id' not in feedback_column_names:
            print("⚠️  Warning: feedback table might need user_id column")
        else:
            print("✅ feedback table structure looks good")

        conn.commit()
        print("\n🎉 Database migration completed successfully!")

    except sqlite3.Error as e:
        print(f"❌ Database migration failed: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("Starting database migration...")
    migrate_database()
