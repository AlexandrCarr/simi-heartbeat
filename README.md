# 💌 Simi Heartbeat — Multi-Message Daily Notifier

A lightweight Flask backend that delivers personalized messages throughout the day via iPhone Shortcuts automations.

## 🎯 What This Does

Your iPhone will automatically receive custom messages at different times of day (morning, afternoon, evening) — all controlled by a simple Google Sheet that you can edit anytime.

## 📋 Project Structure

```
Simi/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── render.yaml         # Render.com deployment config
├── .env.example        # Environment variable template
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## 🚀 Quick Start Guide

### Step 1: Google Sheet Setup

**Your Google Sheet is already configured!**

Sheet URL: https://docs.google.com/spreadsheets/d/1lPz0z16biDwMUlrQ13VJUJpNiVug7QbGrQAomY5Z2BQ/edit?usp=sharing

Sheet ID: `1lPz0z16biDwMUlrQ13VJUJpNiVug7QbGrQAomY5Z2BQ`

Make sure your sheet has these **exact column headers** in row 1:
```
date | part | message
```

Example messages:
```
2025-11-09 | morning   | Good morning sunshine! ☀️
2025-11-09 | afternoon | Time for a coffee break ☕
2025-11-09 | evening   | You crushed it today! 💪
```

**Important:** Verify the sheet is shared as "Anyone with the link" with "Viewer" permissions.

### Step 2: Test Locally (Optional)

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. The `.env` file is already created with your Sheet ID!

3. Run the app:
   ```bash
   python app.py
   ```

4. Test in your browser:
   ```
   http://localhost:5000/daily?part=morning
   ```

   You should see:
   ```json
   {"message": "Good morning sunshine! ☀️"}
   ```

### Step 3: Deploy to Render

1. **Create a GitHub repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Simi Heartbeat"
   ```

   Create a new repo on GitHub and push:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/simi-heartbeat.git
   git branch -M main
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Render will auto-detect the `render.yaml` file
   - Click "Create Web Service"

3. **Add environment variable:**
   - In Render dashboard, go to your service
   - Click "Environment"
   - Add variable:
     - Key: `GOOGLE_SHEET_ID`
     - Value: `1lPz0z16biDwMUlrQ13VJUJpNiVug7QbGrQAomY5Z2BQ`
   - Click "Save Changes"

4. **Get your URL:**
   - After deployment completes, you'll get a URL like:
     ```
     https://simi-heartbeat.onrender.com
     ```

5. **Test it:**
   ```
   https://simi-heartbeat.onrender.com/daily?part=morning
   ```

### Step 4: Set Up iPhone Shortcuts

Create **three separate automations** (one for each time of day):

#### Morning Automation (9:00 AM)

1. Open **Shortcuts** app
2. Go to **Automation** tab
3. Tap **+** → **Create Personal Automation**
4. Select **Time of Day**
5. Set time to **9:00 AM**
6. Set **Repeat: Daily**
7. Tap **Next**
8. Add actions:
   - **Get Contents of URL**
     - URL: `https://your-render-url.onrender.com/daily?part=morning`
   - **Get Dictionary Value**
     - Key: `message`
   - **Show Notification**
     - Title: `Morning Message 💌`
     - Body: `Dictionary Value`
9. Tap **Next**
10. **Turn OFF** "Ask Before Running"
11. Tap **Done**

#### Afternoon Automation (1:00 PM)

Repeat the same steps, but:
- Time: **1:00 PM**
- URL: `https://your-render-url.onrender.com/daily?part=afternoon`
- Notification title: `Afternoon Check-in ☀️`

#### Evening Automation (8:00 PM)

Repeat the same steps, but:
- Time: **8:00 PM**
- URL: `https://your-render-url.onrender.com/daily?part=evening`
- Notification title: `Evening Thoughts 🌙`

## 📱 API Endpoints

### `GET /`
Health check endpoint
```json
{
  "status": "healthy",
  "service": "Simi Heartbeat"
}
```

### `GET /daily?part={morning|afternoon|evening}`
Get message for specific time of day
```json
{
  "message": "Your personalized message here"
}
```

### `GET /test`
View all messages in your sheet (for debugging)
```json
{
  "sheet_id": "1a2b3c...",
  "total_messages": 6,
  "messages": [...]
}
```

## 🎨 Customization Tips

### Add More Time Slots
Just add more rows with different `part` values:
```
2025-11-09 | midday    | Lunch break reminder 🍱
2025-11-09 | bedtime   | Time to wind down 😴
```

Then create matching automations in Shortcuts.

### Use Emojis
Make messages fun with emojis in your Google Sheet:
```
2025-11-09 | morning | Rise & shine! ☀️🌻💛
```

### Update Messages Anytime
Just edit the Google Sheet — changes take effect immediately (no redeployment needed).

### Add Weekend-Only Messages
Use different dates and create time-based automations in Shortcuts that only run on weekends.

## 🔧 Troubleshooting

### "No message found" error
- Check your Google Sheet date format is `YYYY-MM-DD`
- Verify the `part` value matches exactly (case-insensitive)
- Make sure the sheet is shared publicly

### Automation not running
- Check "Ask Before Running" is OFF
- Verify the automation is enabled (toggle should be green)
- Check notification permissions for Shortcuts app

### Server error
- Visit `/test` endpoint to see what's in your sheet
- Check Render logs for detailed error messages
- Verify `GOOGLE_SHEET_ID` environment variable is set

## 📝 Notes

- Messages are fetched fresh each time (no caching)
- If no message exists for today, you'll get a friendly fallback
- The Google Sheet must remain public (viewer access)
- Render free tier may sleep after inactivity — first request might be slow

## 💡 Future Ideas

- Add randomization (pick random message from a pool)
- Weather-based messages
- Mood tracking integration
- Photo attachments
- Voice message support

---

Made with 💛 for Simi
