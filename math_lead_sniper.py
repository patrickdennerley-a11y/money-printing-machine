#!/usr/bin/env python3
"""
Math Lead Sniper - High-Precision Math Tutoring Lead Monitor

This script monitors Reddit and Google Alerts RSS feeds for math tutoring leads,
filters them using Google's Gemini AI, and sends notifications to Discord.

Author: Money Printing Machine
"""

import os
import sys
import time
import logging
from datetime import datetime, timedelta
from typing import Set, Dict, Optional
import hashlib

import praw
import feedparser
import requests
import google.generativeai as genai
from dotenv import load_dotenv


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('math_lead_sniper.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class MathLeadSniper:
    """Main class for monitoring and filtering math tutoring leads."""

    # Target subreddits to monitor
    SUBREDDITS = [
        'HomeworkHelp',
        'Calculus',
        'LearnMath',
        'MathHelp',
        'PreCalculus'
    ]

    # Keywords that trigger AI analysis
    TRIGGER_KEYWORDS = [
        'urgent', 'exam', 'tutor', 'fail', 'due', 'stuck',
        'help me', 'desperate', 'struggling', 'test tomorrow',
        'quiz', 'homework due', 'need help', 'can someone',
        'asap', 'deadline', 'final', 'midterm'
    ]

    # Gemini system instruction for lead qualification
    SYSTEM_INSTRUCTION = (
        "You are a lead qualifier for a math tutor. Analyze the following text. "
        "Does the user explicitly express a desperate need for help, tutoring, "
        "or is struggling with an upcoming exam? If it is a spam bot, a promotional ad, "
        "a general discussion about math, or a rant with no intent to learn, return NO. "
        "If it is a student explicitly asking for help, return YES. "
        "Respond with ONLY 'YES' or 'NO'."
    )

    # Cooldown period (in seconds) to prevent duplicate notifications
    COOLDOWN_PERIOD = 3600  # 1 hour

    def __init__(self):
        """Initialize the Math Lead Sniper with API credentials."""
        load_dotenv()

        # Load environment variables
        self.reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
        self.reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.reddit_user_agent = os.getenv('REDDIT_USER_AGENT', 'MathLeadSniper/1.0')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        self.google_alerts_rss_urls = os.getenv('GOOGLE_ALERTS_RSS_URLS', '').split(',')

        # Validate required environment variables
        self._validate_config()

        # Initialize Reddit client
        try:
            self.reddit = praw.Reddit(
                client_id=self.reddit_client_id,
                client_secret=self.reddit_client_secret,
                user_agent=self.reddit_user_agent
            )
            logger.info("Reddit client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Reddit client: {e}")
            raise

        # Initialize Gemini AI
        try:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                system_instruction=self.SYSTEM_INSTRUCTION
            )
            logger.info("Gemini AI initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini AI: {e}")
            raise

        # Cooldown tracking: stores hash of content -> timestamp
        self.processed_items: Dict[str, float] = {}

    def _validate_config(self):
        """Validate that all required environment variables are set."""
        missing = []

        if not self.reddit_client_id:
            missing.append('REDDIT_CLIENT_ID')
        if not self.reddit_client_secret:
            missing.append('REDDIT_CLIENT_SECRET')
        if not self.gemini_api_key:
            missing.append('GEMINI_API_KEY')
        if not self.discord_webhook_url:
            missing.append('DISCORD_WEBHOOK_URL')

        if missing:
            logger.error(f"Missing required environment variables: {', '.join(missing)}")
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    def _get_content_hash(self, content: str) -> str:
        """Generate a hash for content to track processed items."""
        return hashlib.md5(content.encode()).hexdigest()

    def _is_in_cooldown(self, content_hash: str) -> bool:
        """Check if content is in cooldown period."""
        if content_hash in self.processed_items:
            time_elapsed = time.time() - self.processed_items[content_hash]
            if time_elapsed < self.COOLDOWN_PERIOD:
                logger.debug(f"Content in cooldown ({time_elapsed:.0f}s elapsed)")
                return True
            else:
                # Remove from cooldown
                del self.processed_items[content_hash]
        return False

    def _mark_processed(self, content_hash: str):
        """Mark content as processed with current timestamp."""
        self.processed_items[content_hash] = time.time()

        # Clean up old entries (older than 2x cooldown period)
        cutoff_time = time.time() - (self.COOLDOWN_PERIOD * 2)
        self.processed_items = {
            k: v for k, v in self.processed_items.items()
            if v > cutoff_time
        }

    def _contains_trigger_keywords(self, text: str) -> bool:
        """Check if text contains any trigger keywords."""
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in self.TRIGGER_KEYWORDS)

    def _analyze_with_gemini(self, content: str) -> bool:
        """
        Analyze content with Gemini AI to determine if it's a qualified lead.

        Returns:
            True if Gemini returns 'YES', False otherwise
        """
        try:
            logger.info("Analyzing content with Gemini AI...")

            response = self.gemini_model.generate_content(
                content,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,  # Low temperature for consistent responses
                    max_output_tokens=10,  # We only need YES or NO
                )
            )

            result = response.text.strip().upper()
            logger.info(f"Gemini response: {result}")

            return 'YES' in result

        except Exception as e:
            logger.error(f"Error analyzing with Gemini: {e}")
            # On error, err on the side of caution and don't filter out
            return False

    def _send_discord_notification(self, title: str, snippet: str, link: str, source: str):
        """
        Send a formatted notification to Discord webhook.

        Args:
            title: Title of the lead
            snippet: Preview text of the content
            link: URL to the original post
            source: Source of the lead (Reddit or RSS)
        """
        try:
            # Create embed for rich Discord message
            embed = {
                "title": f"🎯 High-Quality Lead Found!",
                "description": f"**{title}**",
                "color": 0x00ff00,  # Green color
                "fields": [
                    {
                        "name": "📝 Snippet",
                        "value": snippet[:1000] + ("..." if len(snippet) > 1000 else ""),
                        "inline": False
                    },
                    {
                        "name": "🔗 Link",
                        "value": link,
                        "inline": False
                    },
                    {
                        "name": "📍 Source",
                        "value": source,
                        "inline": True
                    },
                    {
                        "name": "⏰ Detected",
                        "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "Math Lead Sniper - AI Powered Lead Detection"
                }
            }

            payload = {
                "embeds": [embed],
                "username": "Math Lead Sniper"
            }

            response = requests.post(
                self.discord_webhook_url,
                json=payload,
                timeout=10
            )

            if response.status_code == 204:
                logger.info(f"✅ Discord notification sent for: {title}")
            else:
                logger.error(f"Failed to send Discord notification: {response.status_code}")

        except requests.exceptions.Timeout:
            logger.error("Discord webhook request timed out")
        except Exception as e:
            logger.error(f"Error sending Discord notification: {e}")

    def _process_content(self, title: str, content: str, link: str, source: str):
        """
        Process a piece of content through the filtering pipeline.

        Args:
            title: Title of the content
            content: Main text content
            link: URL to the original content
            source: Source identifier (e.g., "r/Calculus" or "Google Alert")
        """
        # Check cooldown
        content_hash = self._get_content_hash(content)
        if self._is_in_cooldown(content_hash):
            logger.debug(f"Skipping (cooldown): {title}")
            return

        # Check for trigger keywords
        combined_text = f"{title} {content}"
        if not self._contains_trigger_keywords(combined_text):
            logger.debug(f"No trigger keywords found: {title}")
            return

        logger.info(f"🔍 Trigger keywords found in: {title}")

        # Analyze with Gemini AI
        if self._analyze_with_gemini(combined_text):
            logger.info(f"✅ QUALIFIED LEAD: {title}")

            # Send Discord notification
            self._send_discord_notification(
                title=title,
                snippet=content[:500],
                link=link,
                source=source
            )

            # Mark as processed
            self._mark_processed(content_hash)
        else:
            logger.info(f"❌ Not a qualified lead: {title}")

    def monitor_reddit_submissions(self):
        """Monitor Reddit submissions from target subreddits."""
        try:
            logger.info(f"Monitoring submissions from: {', '.join(self.SUBREDDITS)}")
            subreddit = self.reddit.subreddit('+'.join(self.SUBREDDITS))

            for submission in subreddit.stream.submissions(skip_existing=True):
                try:
                    title = submission.title
                    content = submission.selftext or ""
                    link = f"https://reddit.com{submission.permalink}"
                    source = f"r/{submission.subreddit.display_name}"

                    logger.debug(f"Processing submission: {title}")
                    self._process_content(title, content, link, source)

                except Exception as e:
                    logger.error(f"Error processing submission: {e}")
                    time.sleep(1)  # Brief pause before continuing

        except Exception as e:
            logger.error(f"Error in Reddit submission stream: {e}")
            raise

    def monitor_reddit_comments(self):
        """Monitor Reddit comments from target subreddits."""
        try:
            logger.info(f"Monitoring comments from: {', '.join(self.SUBREDDITS)}")
            subreddit = self.reddit.subreddit('+'.join(self.SUBREDDITS))

            for comment in subreddit.stream.comments(skip_existing=True):
                try:
                    # Use submission title as context
                    title = f"Comment on: {comment.submission.title}"
                    content = comment.body
                    link = f"https://reddit.com{comment.permalink}"
                    source = f"r/{comment.subreddit.display_name} (comment)"

                    logger.debug(f"Processing comment: {title}")
                    self._process_content(title, content, link, source)

                except Exception as e:
                    logger.error(f"Error processing comment: {e}")
                    time.sleep(1)  # Brief pause before continuing

        except Exception as e:
            logger.error(f"Error in Reddit comment stream: {e}")
            raise

    def monitor_rss_feeds(self):
        """Monitor Google Alerts RSS feeds."""
        if not self.google_alerts_rss_urls or self.google_alerts_rss_urls == ['']:
            logger.info("No RSS feeds configured, skipping RSS monitoring")
            return

        logger.info(f"Monitoring {len(self.google_alerts_rss_urls)} RSS feeds")

        # Track seen entries across all feeds
        seen_entries: Set[str] = set()

        while True:
            try:
                for rss_url in self.google_alerts_rss_urls:
                    if not rss_url.strip():
                        continue

                    try:
                        logger.debug(f"Fetching RSS feed: {rss_url}")
                        feed = feedparser.parse(rss_url)

                        for entry in feed.entries:
                            entry_id = entry.get('id', entry.get('link', ''))

                            # Skip if already seen
                            if entry_id in seen_entries:
                                continue

                            seen_entries.add(entry_id)

                            # Extract entry details
                            title = entry.get('title', 'No Title')
                            content = entry.get('summary', entry.get('description', ''))
                            link = entry.get('link', '')

                            logger.debug(f"Processing RSS entry: {title}")
                            self._process_content(title, content, link, "Google Alert")

                    except Exception as e:
                        logger.error(f"Error fetching RSS feed {rss_url}: {e}")

                # Check feeds every 5 minutes
                time.sleep(300)

            except Exception as e:
                logger.error(f"Error in RSS monitoring: {e}")
                time.sleep(60)  # Wait a minute before retrying

    def run(self):
        """Run the Math Lead Sniper (main entry point)."""
        logger.info("=" * 60)
        logger.info("🎯 Math Lead Sniper Started!")
        logger.info("=" * 60)
        logger.info(f"Monitoring subreddits: {', '.join(self.SUBREDDITS)}")
        logger.info(f"Trigger keywords: {', '.join(self.TRIGGER_KEYWORDS)}")
        logger.info(f"Cooldown period: {self.COOLDOWN_PERIOD}s")
        logger.info("=" * 60)

        import threading

        # Create threads for different monitoring tasks
        threads = []

        # Reddit submissions thread
        submission_thread = threading.Thread(
            target=self._run_with_retry,
            args=(self.monitor_reddit_submissions, "Reddit Submissions"),
            daemon=True
        )
        threads.append(submission_thread)

        # Reddit comments thread
        comment_thread = threading.Thread(
            target=self._run_with_retry,
            args=(self.monitor_reddit_comments, "Reddit Comments"),
            daemon=True
        )
        threads.append(comment_thread)

        # RSS feeds thread (if configured)
        if self.google_alerts_rss_urls and self.google_alerts_rss_urls != ['']:
            rss_thread = threading.Thread(
                target=self._run_with_retry,
                args=(self.monitor_rss_feeds, "RSS Feeds"),
                daemon=True
            )
            threads.append(rss_thread)

        # Start all threads
        for thread in threads:
            thread.start()

        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("\n🛑 Shutting down Math Lead Sniper...")
            sys.exit(0)

    def _run_with_retry(self, func, name: str):
        """
        Run a function with automatic retry on failure.

        Args:
            func: Function to run
            name: Name of the task (for logging)
        """
        retry_delay = 10
        max_retry_delay = 300  # 5 minutes

        while True:
            try:
                func()
            except KeyboardInterrupt:
                raise
            except Exception as e:
                logger.error(f"Error in {name}: {e}")
                logger.info(f"Retrying {name} in {retry_delay}s...")
                time.sleep(retry_delay)

                # Exponential backoff
                retry_delay = min(retry_delay * 2, max_retry_delay)


def main():
    """Main entry point."""
    try:
        sniper = MathLeadSniper()
        sniper.run()
    except KeyboardInterrupt:
        logger.info("\n🛑 Shutting down Math Lead Sniper...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
