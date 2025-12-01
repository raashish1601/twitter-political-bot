"""
Scheduler Module - Handles posting schedule for optimal reach
"""
import schedule
import time
import random
from datetime import datetime
import pytz

class TweetScheduler:
    def __init__(self, post_callback):
        self.post_callback = post_callback
        self.ist = pytz.timezone('Asia/Kolkata')
        
        # Optimal posting times (IST) with some randomization
        self.posting_times = [
            (8, 30),  # 8:30 AM - Morning commute
            (13, 30), # 1:30 PM - Lunch break
            (20, 0)   # 8:00 PM - Evening peak
        ]
    
    def _get_randomized_time(self, hour, minute):
        """
        Add random minutes (0-30) to posting time for variation
        """
        random_minutes = random.randint(0, 30)
        total_minutes = minute + random_minutes
        if total_minutes >= 60:
            hour += 1
            total_minutes -= 60
        return f"{hour:02d}:{total_minutes:02d}"
    
    def setup_schedule(self):
        """
        Set up daily posting schedule
        """
        # Clear existing schedule
        schedule.clear()
        
        # Schedule posts at optimal times
        for hour, minute in self.posting_times:
            post_time = self._get_randomized_time(hour, minute)
            schedule.every().day.at(post_time).do(self._post_job)
            print(f"📅 Scheduled post at {post_time} IST")
    
    def _post_job(self):
        """
        Job to execute when it's time to post
        """
        current_time = datetime.now(self.ist).strftime('%Y-%m-%d %H:%M:%S IST')
        print(f"\n⏰ Posting time! ({current_time})")
        try:
            self.post_callback()
        except Exception as e:
            print(f"❌ Error in scheduled post: {e}")
    
    def run(self):
        """
        Run the scheduler (blocking)
        """
        print("🚀 Scheduler started. Waiting for posting times...")
        print(f"📊 Next posts scheduled at:")
        for job in schedule.jobs:
            print(f"   - {job.next_run.strftime('%Y-%m-%d %H:%M:%S IST')}")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def get_next_post_time(self):
        """
        Get the next scheduled post time
        """
        if schedule.jobs:
            return schedule.jobs[0].next_run
        return None

