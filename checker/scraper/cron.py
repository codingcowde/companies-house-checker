from .scraper import CHeckerScraper
from .mail import send_email
from .models import load_flagged_from_database, load_zero_flagged_from_database, set_flag
import time, random

def run_scrape_job():
        flagged = load_flagged_from_database()
        unflagged = load_zero_flagged_from_database()

        for user in flagged:
            user.flag -= 1
            user.save()
        CHS = CHeckerScraper()
        for user in unflagged:            
            if result := CHS.run(user.name):                            
                send_email(
                    'Your Report from CHecker',
                    'emails/notification.htm',
                    user.email,
                    {
                    'result':result,
                    'user':user,
                    }
                )
                set_flag(user.name, user.email)
                # AVOID SPAMMING THE SERVER    
                seconds = random.randint(10, 60)                    
                time.sleep(seconds)
                
            
        