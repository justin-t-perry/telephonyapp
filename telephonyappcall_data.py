"""
Sample call transcript data for the Contact Center Call Summary Dashboard.
In production, this would come from a telephony system or call recording platform.
"""

SAMPLE_CALLS = [
    {
        "call_id": "CC-20260329-001",
        "agent": "Maria Santos",
        "customer": "James Whitfield",
        "customer_tier": "Gold",
        "date": "2026-03-29",
        "time": "09:14 AM",
        "duration_seconds": 412,
        "queue": "Billing",
        "phone": "+1 (555) 234-8891",
        "previous_calls": 3,
        "transcript": """Agent: Thank you for calling Execute Support, my name is Maria. How can I help you today?
Customer: Hi Maria, I'm really frustrated. I've been charged twice for my subscription this month and I need this fixed immediately.
Agent: I completely understand your frustration, Mr. Whitfield. Nobody wants to see a double charge. Let me pull up your account right away. Can I have your account number?
Customer: It's 4492-7781. And this isn't the first time this has happened. Last quarter I had a similar issue.
Agent: I see your account now, and I can confirm there is a duplicate charge of $149.99 on March 15th. I sincerely apologize for this recurring issue. Let me process a refund for the duplicate charge right now.
Customer: Okay, but what are you going to do to make sure this doesn't happen again?
Agent: That's a fair question. I'm going to flag your account for our billing team to review the automated payment process. I'll also add a note to escalate if any duplicate charges appear. You should see the refund within 3-5 business days.
Customer: Fine. I appreciate you handling it quickly at least.
Agent: Of course. Is there anything else I can help you with today?
Customer: No, that's it. Thanks Maria.
Agent: Thank you, Mr. Whitfield. Have a great day."""
    },
    {
        "call_id": "CC-20260329-002",
        "agent": "Derek Thompson",
        "customer": "Susan Park",
        "customer_tier": "Platinum",
        "date": "2026-03-29",
        "time": "10:32 AM",
        "duration_seconds": 687,
        "queue": "Technical Support",
        "phone": "+1 (555) 891-3320",
        "previous_calls": 1,
        "transcript": """Agent: Execute Technical Support, this is Derek. How can I assist you?
Customer: Hi Derek, I can't log into the dashboard. I keep getting an error that says "session expired" but I just changed my password yesterday.
Agent: I'm sorry to hear that, Ms. Park. That can definitely be annoying. Let me check your account status. What email do you have on file?
Customer: susan.park@meridiangroup.com
Agent: Thank you. I can see your account here. It looks like the password reset may not have fully synced across our authentication servers. This can sometimes happen when there's a cache issue. Can you try clearing your browser cache and cookies, then attempting to log in again?
Customer: I already tried that. I also tried a different browser and it still doesn't work.
Agent: Okay, let me try something else. I'm going to force a session reset on our end. This will invalidate all existing sessions and you'll need to log in fresh. Give me just a moment... Alright, that's done. Can you try logging in now?
Customer: Hold on... Yes! That worked! I'm in now. Thank you.
Agent: Excellent! The issue was likely a stale session token that wasn't cleared during the password reset. If this happens again, you can also try using an incognito window as a quick workaround while you contact us.
Customer: Good to know. One more thing — is there a way to set up two-factor authentication? My IT team has been asking about it.
Agent: Absolutely. If you go to Settings, then Security, you'll see an option for Two-Factor Authentication. You can use an authenticator app or SMS. I'd recommend the authenticator app for better security.
Customer: Perfect, I'll set that up. Thanks Derek!
Agent: Happy to help. Have a great day!"""
    },
    {
        "call_id": "CC-20260329-003",
        "agent": "Maria Santos",
        "customer": "Robert Chen",
        "customer_tier": "Silver",
        "date": "2026-03-29",
        "time": "11:05 AM",
        "duration_seconds": 298,
        "queue": "Sales",
        "phone": "+1 (555) 442-7710",
        "previous_calls": 0,
        "transcript": """Agent: Thank you for calling Execute, this is Maria. How can I help you?
Customer: Hi, I'm interested in upgrading our plan. We currently have the Starter plan but we're growing and need more seats.
Agent: That's great to hear your business is growing! I'd be happy to help with that. How many seats are you currently using and how many would you need?
Customer: We have 10 now and we'd need about 25.
Agent: Perfect. For 25 seats, our Professional plan would be the best fit. It includes everything in Starter plus advanced analytics, priority support, and custom integrations. The per-seat cost actually goes down at that tier.
Customer: What's the pricing look like?
Agent: The Professional plan at 25 seats would be $89 per seat per month, compared to the $99 you're paying now on Starter. So you'd get more features at a lower per-seat cost. The total would be $2,225 per month.
Customer: That sounds reasonable. Can we do an annual contract for a better rate?
Agent: Absolutely. With an annual commitment, we can bring that down to $79 per seat, so $1,975 per month billed annually. That's a 20% savings overall.
Customer: I'll need to run this by my CFO. Can you send me a proposal?
Agent: Of course! I'll email you a detailed proposal within the hour. What's the best email?
Customer: robert.chen@bluelineventures.com
Agent: Got it. I'll include a comparison sheet and ROI calculator as well. Is there anything else I can help with?
Customer: No, that covers it. Thanks Maria.
Agent: Thank you, Robert. I look forward to helping you upgrade!"""
    },
    {
        "call_id": "CC-20260329-004",
        "agent": "Priya Nair",
        "customer": "Angela Morrison",
        "customer_tier": "Gold",
        "date": "2026-03-29",
        "time": "01:47 PM",
        "duration_seconds": 543,
        "queue": "Billing",
        "phone": "+1 (555) 667-2243",
        "previous_calls": 7,
        "transcript": """Agent: Execute Billing Department, this is Priya. How may I help you?
Customer: I want to cancel my account. I've had nothing but problems with your service.
Agent: I'm sorry to hear you've had a negative experience, Ms. Morrison. Before I process the cancellation, would you mind sharing what issues you've encountered? I want to make sure we address any outstanding problems.
Customer: Where do I start? The reporting module has been broken for weeks, I can never get through to support, and now my invoice has charges for features I never activated.
Agent: I understand, and I appreciate you sharing that. Let me look into each of these. Regarding the reporting module, we did have an issue that was resolved in our March 15th update. Have you tried it since then?
Customer: No, I gave up on it honestly.
Agent: I understand. The fix has been deployed and it's working well now. Regarding the support wait times, we've recently expanded our support team and average wait times have dropped significantly. And let me check on those charges... I see two add-on charges for API Access and Custom Branding. Were these not something you activated?
Customer: I definitely didn't activate Custom Branding. The API access I might have clicked by accident.
Agent: I'll remove the Custom Branding charge immediately and refund the last two months for that — that's $59.98 back to you. For the API access, would you like to keep it or remove it as well?
Customer: Remove it. I don't need it.
Agent: Done. Both add-ons are removed and the refund is processing. Ms. Morrison, given these issues, would you consider staying if I could offer you a 30% discount for the next three months so you can re-evaluate the service with the fixes in place?
Customer: ...I suppose I could try it for another few months at that rate.
Agent: Wonderful. I've applied the discount. You'll also have my direct extension — 4417 — if you run into any issues. I want to make sure your experience improves.
Customer: Okay, thank you Priya. I appreciate you actually listening.
Agent: Of course. That's what I'm here for. Have a good afternoon."""
    },
    {
        "call_id": "CC-20260329-005",
        "agent": "Derek Thompson",
        "customer": "Marcus Williams",
        "customer_tier": "Platinum",
        "date": "2026-03-29",
        "time": "03:22 PM",
        "duration_seconds": 195,
        "queue": "Technical Support",
        "phone": "+1 (555) 998-1102",
        "previous_calls": 2,
        "transcript": """Agent: Execute Technical Support, Derek speaking.
Customer: Hey Derek, quick question. How do I export my dashboard data to a CSV file?
Agent: Hi Marcus! That's a simple one. On your dashboard, click the three-dot menu in the upper right corner of any widget, then select "Export Data." You'll get options for CSV, Excel, or PDF.
Customer: Oh I see it now. I was looking under the Settings menu. And can I schedule automatic exports?
Agent: Yes! Go to Settings, then Scheduled Reports. You can set up daily, weekly, or monthly exports that get emailed directly to you or your team.
Customer: Perfect, exactly what I needed. Thanks!
Agent: Anytime, Marcus. Have a good one!"""
    },
    {
        "call_id": "CC-20260329-006",
        "agent": "Priya Nair",
        "customer": "David Kim",
        "customer_tier": "Silver",
        "date": "2026-03-29",
        "time": "04:10 PM",
        "duration_seconds": 830,
        "queue": "Technical Support",
        "phone": "+1 (555) 331-5578",
        "previous_calls": 5,
        "transcript": """Agent: Execute Technical Support, this is Priya. How can I help?
Customer: Hi Priya. I'm having a serious issue. Our entire team's data from last week seems to have disappeared from the analytics dashboard. We had a board presentation tomorrow and now all our reports are blank.
Agent: Oh no, I understand the urgency. Let me look into this right away. Can you tell me your company account ID?
Customer: It's ENT-90432. This is really critical. My VP is going to lose it if we can't get this data back.
Agent: I've pulled up your account. I can see that your data storage shows normal usage levels, so the data likely hasn't been deleted — it may be a display issue. Let me check a few things. What date range are you looking at?
Customer: March 20th through March 28th. Everything before the 20th shows fine.
Agent: Okay, I think I see the problem. There was a data pipeline update on March 19th and it looks like your custom date filters may have been reset. Let me walk you through re-configuring them. Go to Analytics, then click on the gear icon next to your date range selector.
Customer: Okay, I'm there.
Agent: Now click "Data Sources" and make sure all your connected sources show a green checkmark. Do any show yellow or red?
Customer: Two of them show yellow — "CRM Sync" and "Marketing Events."
Agent: That's the issue. Click on each one and hit "Reconnect." It should prompt you to re-authorize.
Customer: Doing it now... Okay, both are green now. And... yes! The data is coming back! I can see last week's numbers populating.
Agent: Excellent! It may take a few minutes for everything to fully reload, but your data is all there. For your board presentation, I'd recommend exporting the reports to PDF once they're fully loaded, just as a backup.
Customer: That's a great idea. Priya, you just saved my career. Thank you so much.
Agent: I'm glad we could get it sorted quickly! If you notice anything else off, don't hesitate to call back. Good luck with the presentation!
Customer: Thanks again. You're the best."""
    },
    {
        "call_id": "CC-20260329-007",
        "agent": "Maria Santos",
        "customer": "Lisa Hoffman",
        "customer_tier": "Gold",
        "date": "2026-03-29",
        "time": "04:55 PM",
        "duration_seconds": 365,
        "queue": "Sales",
        "phone": "+1 (555) 776-4490",
        "previous_calls": 1,
        "transcript": """Agent: Thank you for calling Execute Sales, this is Maria. How can I help you today?
Customer: Hi Maria, I'm looking into your enterprise plan for our company. We have about 200 employees and we need something with SSO integration and dedicated support.
Agent: Absolutely, I'd be happy to walk you through our Enterprise offering. For 200 seats, you'd be looking at our Enterprise tier which includes SSO via SAML and OIDC, a dedicated customer success manager, 99.9% uptime SLA, custom onboarding, and priority support with a 1-hour response time.
Customer: What about data residency? We have compliance requirements that data needs to stay in the US.
Agent: Great question. Our Enterprise plan includes US data residency by default. We host on AWS us-east-1 and us-west-2, and we can provide a data processing agreement and SOC 2 Type II certification for your compliance team.
Customer: That's exactly what we need. What's the pricing?
Agent: For 200 seats on Enterprise with annual billing, we're looking at $69 per seat per month. That comes to $13,800 per month or $165,600 annually. For a multi-year commitment, we can discuss additional savings.
Customer: I'll need to bring this to our procurement team. Can you set up a demo call with our CTO next week?
Agent: Absolutely! I'll send you a calendar link. What day works best?
Customer: Tuesday or Wednesday afternoon.
Agent: I'll send options for both. You'll also receive our Enterprise security whitepaper and a custom ROI analysis. Who should I include on the invite?
Customer: Me, our CTO Karen Wells, and our IT Director Tom Nguyen.
Agent: Perfect. I'll have everything to you by end of day. Thank you, Lisa!
Customer: Thanks Maria, talk soon."""
    }
]
