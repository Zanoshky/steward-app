#!/usr/bin/env python3
"""Builds the guide pages in docs/ from the bodies below. Run after any edit and commit docs/. Fails on any dash.

The look is the Zanoshky Standard, the same as the Fileglow guide: docs/tokens.css is a copy of the house
tokens (never edit it here), docs/style.css the guide's own parts. Both are inlined into every page so no
stylesheet holds up the first paint. Every label in these pages is the app's own word, taken from its code."""
import re
from pathlib import Path

D = Path(__file__).parent / "docs"
REPO = "https://github.com/Zanoshky/steward-app"
PLAY = "https://play.google.com/store/apps/details?id=com.zanoshky.steward"
SITE = "https://steward.zanoski.com"
MAIL = "marko@zanoski.com"
SUBS = "https://play.google.com/store/account/subscriptions"
NAV = [("index.html", "Home"), ("guide.html", "Guide"), ("cookbook.html", "Cookbook"), ("runbook.html", "Runbook"), ("faq.html", "Questions"), ("report.html", "Report a bug")]

CSS = "\n".join((D / f).read_text() for f in ("tokens.css", "style.css"))
CSS = re.sub(r"/\*.*?\*/", "", CSS, flags=re.S)
CSS = re.sub(r"\s*\n\s*", "\n", CSS).strip()


def page(name, title, desc, body):
    for bad in ("\u2014", "\u2013", " - "):
        if bad in body or bad in desc:
            raise SystemExit(f"{name}: dash {bad!r} in copy")
    nav = "".join(f'<a class="hide-s" href="{h}"{" aria-current=\"page\"" if h == name else ""}>{t}</a>' for h, t in NAV)
    foot = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == name else ""}>{t}</a>' for h, t in
                   [(SITE, "Home"), ("index.html", "User guide"), ("faq.html", "Questions"), ("report.html", "Report a bug"),
                    (f"{SITE}/privacy", "Privacy"), (f"{SITE}/delete", "Delete data"), (f"{SITE}/terms", "Terms")])
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · Steward user guide</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#f6f7f9" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">
<meta property="og:title" content="{title} · Steward user guide">
<meta property="og:description" content="{desc}">
<link rel="icon" href="img/icon.svg" type="image/svg+xml">
<link rel="preload" href="fonts/jetbrains-mono-bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/inter-regular.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="bar">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="img/icon.svg" alt="" width="34" height="34"><span>Steward</span></a>
    <nav aria-label="Guide pages">{nav}<a class="key" href="{PLAY}">Get the app</a></nav>
  </div>
</header>
<main id="main" class="page">
  <div class="wrap">
{body}
  </div>
</main>
<footer>
  <div class="wrap">
    <span>Steward by <a href="https://zanoski.com">Marko Zanoski</a></span>
    <nav aria-label="Footer">{foot}</nav>
    <p class="lic">Guide text and images are shared under CC BY 4.0. The Steward app itself is proprietary.</p>
  </div>
</footer>
</body>
</html>
"""
    (D / name).write_text(html)
    print(name)


page("index.html", "Home", "The user guide for Steward, the flight tracker for Android that keeps your gate and times live on the lock screen.", f"""
    <p class="lbl">User guide</p>
    <h1>Steward</h1>
    <p class="lede">Your flight, live on the lock screen. Steward finds your trips, keeps the gate and the times on your lock screen, and tells you the moment something changes, so you can stop checking the airline app.</p>
    <p>Flights only. No ads, no tracking and no sign in. Using it needs a subscription, and every plan starts with 3 days free from Google Play. The <a href="cookbook.html">cookbook</a> has short recipes and the <a href="runbook.html">runbook</a> has fixes.</p>
    <div class="keys">
      <a class="key filled" href="guide.html">Read the guide</a>
      <a class="key tonal" href="report.html">Report a bug or ask for a feature</a>
    </div>

    <div class="doc">
      <h2>What it does</h2>
      <dl class="rows plate">
        <div><dt>Live on the lock screen</dt><dd>From two hours before departure, one live update shows the gate, a countdown and one bar for the whole trip. On Android 16 and newer it sits in the status bar as a small chip.</dd></div>
        <div><dt>Alerts that matter</dt><dd>Gate changes, delays, diversions, boarding, take off, landing, the arrival gate and the bag belt. A cancelled flight shows the other nonstop flights on the route.</dd></div>
        <div><dt>No typing</dt><dd>Flight bookings in your calendar, a boarding pass PDF, a Wallet pass or a screenshot of the barcode: every leg is added with its seat.</dd></div>
        <div><dt>Share your ETA</dt><dd>A live link for whoever picks you up. It opens in any browser, shows the flight only, never your seat or name, and ends a few hours after you land.</dd></div>
        <div><dt>Passport</dt><dd>Every flight you follow fills it: a turning globe with the year's routes drawn in gold, the distance, the hours in the air and the airports.</dd></div>
      </dl>

      <h2>Plans</h2>
      <p>Every plan has every feature. Plans differ only in how many phones they cover. Each is monthly or yearly, with 3 days free from Google Play for new subscribers.</p>
      <dl class="rows plate">
        <div><dt>Steward</dt><dd>For 2 phones. 4.99 a month or 29.99 a year.</dd></div>
        <div><dt>Pro</dt><dd>Up to 10 phones. 9.99 a month or 59.99 a year.</dd></div>
        <div><dt>Unlimited</dt><dd>Every phone you have. 19.99 a month or 99.99 a year.</dd></div>
      </dl>
      <p style="margin-top:12px">These are the listed prices in US dollars. Google Play shows your own price, in your money and with tax, before you pay.</p>
    </div>
""")

page("guide.html", "Guide", "How to use Steward: Flights, adding a flight, the flight screen, the live update, alerts, the boarding pass, Share ETA, Passport, Settings and the subscription.", f"""
    <div class="doc">
    <p class="lbl">Guide</p>
    <h1>How Steward works</h1>

    <h2>The first start</h2>
    <p>Steward runs on Android 10 or newer. It has no account and no sign in. Every trip you follow is watched live by a paid flight data service, so using Steward needs a subscription; there is no free version and no ads. New subscribers get 3 days free through Google Play.</p>
    <p>Steward asks for notifications, so alerts can reach you. Other asks come only when you turn on the thing that needs them: the calendar for Look in my calendar, and a rough location for From where I am.</p>

    <h2>Three tabs</h2>
    <p>The bar at the foot of the screen has three tabs, Flights, Passport and Settings, and a round add button for a new flight. Read at the top, tap at the bottom: the big buttons of each screen sit in thumb reach.</p>

    <h2>Flights</h2>
    <p>Flights is the home screen. Your next trips are listed under Next trips, each with a countdown, the gate when the airport gives it, and its status.</p>
    <dl class="rows plate">
      <div><dt>Found in your calendar</dt><dd>With Look in my calendar on, flights Gmail put in your calendar wait here. Tap Add, or Not mine to hide one.</dd></div>
      <div><dt>Travel day</dt><dd>On the day you fly, the next flight fills the top in big type: the gate (or Gate soon), when it leaves and the time to go, with Boarding pass and Share ETA buttons.</dd></div>
      <div><dt>Get gate and delay alerts</dt><dd>This card shows when notifications are off. Turn on fixes it.</dd></div>
      <div><dt>Your trips are not watched</dt><dd>Without a live subscription your trips stay here to read. See plans starts or restarts one.</dd></div>
    </dl>

    <h2>Add a flight</h2>
    <p>Tap the add button. Type the flight number, like OU 410, and pick the day from the chips above the box (Later picks any day). Times are local to the departure airport.</p>
    <dl class="rows plate">
      <div><dt>Find in my calendar</dt><dd>Reads your calendar on the phone and lists the flights Gmail put there.</dd></div>
      <div><dt>Share a booking</dt><dd>In Gmail or the airline app, tap Share and pick Steward. Steward finds the flight numbers and the date in the text and looks them up. Nothing else from the email is kept.</dd></div>
      <div><dt>Read a boarding pass</dt><dd>A screenshot of the pass from your photos, or a PDF or Wallet pass from the airline email. Every leg is added with its seat, and the pass is kept with its flight.</dd></div>
    </dl>

    <h2>The flight screen</h2>
    <p>Tap a trip to open it: the flight on a world map with the plane on its route, then the terminal, gate, seat and plane, a timeline with the planned times struck through, and words like 9m early. In the air it shows the altitude, the speed and the distance to go.</p>
    <dl class="rows plate">
      <div><dt>Before you fly</dt><dd>Boarding pass, Share ETA and Your plane at the foot. When to leave for the airport, Directions to open your maps app, and about when the doors close.</dd></div>
      <div><dt>Your plane</dt><dd>Most delays start with the plane before yours. From 25 hours out, Steward follows the aircraft that will fly your flight and shows the delay risk and its turnaround time.</dd></div>
      <div><dt>After landing</dt><dd>Welcome to the city, the local time and your body clock, the bag belt, and Share arrival, Passport and Return flight.</dd></div>
      <div><dt>Connections</dt><dd>With a next flight, Steward says how much time you have: Time to make it, Tight connection, or You may miss it.</dd></div>
      <div><dt>At the bottom</dt><dd>Show the live update again, Stop sharing the live link, and Stop following this flight (tap twice).</dd></div>
    </dl>
    <p style="margin-top:12px">Boarding and doors are estimates; the airline's own time wins.</p>

    <h2>The live update on the lock screen</h2>
    <p>From two hours before departure, one live update shows your flight: the gate, a countdown to boarding, take off or landing, and one bar for the whole trip. On Android 16 and newer it also sits in the status bar as a small chip, like B42, Board, +35 or Belt 7. The lock screen copy never shows your seat.</p>
    <p>Its buttons are Boarding pass (when a pass is kept), Share ETA, and Unpin. Unpin or a swipe hides it for that flight; Show the live update again, on the flight screen, brings it back.</p>

    <h2>Alerts</h2>
    <p>Gate and terminal changes, delays of 15 minutes or more, take off and landing with the arrival gate, the bag belt, and your plane running late. Reminders tell you when to check in, when to leave for the airport, and when boarding starts. Each has its own switch in Settings, Tell me about. Cancellations and diversions always come through; a cancelled flight shows the other nonstop flights on the route in the next day, ready to follow.</p>

    <h2>The boarding pass</h2>
    <p>Open Boarding pass on a flight and add the PDF or Wallet pass from the airline email, or a screenshot from the airline app. Steward reads the barcode and draws it again, sharp and at full brightness. The pass stays on this phone. With several legs, swipe for the others. Add to home screen makes a shortcut to your next pass.</p>
    <p>At boarding time a tap on the live update opens the pass over the lock screen, without unlocking. Only the pass shows, nothing else. Turn this off in Settings, Boarding pass.</p>

    <h2>Share ETA</h2>
    <p>Share ETA sends a live link to the people picking you up. It opens in any browser, with no app and no account. It shows the flight only, never your seat or your name, and it ends a few hours after you land. Tell them again when I land, in the share sheet, gives you a Send that I landed note on arrival. Stop sharing the live link, on the flight screen, ends it at once.</p>

    <h2>Passport</h2>
    <p>Every flight you follow lands in Passport when it reaches the gate. Passport opens on a turning globe with the year's routes drawn in gold; drag to turn it. Below it: the kilometres and how many times around Earth, the flights, the hours in the air and the airports, flights per month, how many arrived on time (within 15 minutes of the timetable), and the list of flights. With more than one year, tap a year to switch.</p>

    <h2>On the home screen and in Quick Settings</h2>
    <dl class="rows plate">
      <div><dt>Next flight widget</dt><dd>The countdown, gate and status of your next flight.</dd></div>
      <div><dt>Boarding pass tile</dt><dd>A Quick Settings tile with your next pass, one tap away.</dd></div>
      <div><dt>Shortcuts</dt><dd>Touch and hold the Steward icon for Boarding pass, Share ETA and Add flight.</dd></div>
    </dl>

    <h2>Settings</h2>
    <p>Settings is the third tab: cards of rows, in this order.</p>
    <dl class="rows plate">
      <div><dt>Ready for your trips</dt><dd>The things that let Steward reach you on time, each with a tick when on and a Fix button when off: Notifications, Live updates on the lock screen (Android 16 and newer), Exact timing (Android 12 and newer) and Pass on the lock screen.</dd></div>
      <div><dt>Tell me about</dt><dd>A switch for each alert: Check in, Time to leave for the airport, Boarding with your pass, Gate and terminal changes, Delays, My plane running late, Take off and landing, Bag belt on arrival, and Live update on the lock screen. Then Time to the airport, Be at the airport, and From where I am.</dd></div>
      <div><dt>Boarding pass</dt><dd>Show the pass on the lock screen.</dd></div>
      <div><dt>Finding flights</dt><dd>Look in my calendar, and Keep flights in my calendar, which writes each flight with its latest times, terminal and gate. Gmail's own event keeps the booked times.</dd></div>
      <div><dt>How it looks</dt><dd>Match the phone, Dark or Light, and Sky colours, a faint tint of the hour at the departure airport.</dd></div>
      <div><dt>Your plan</dt><dd>Your plan with when it renews or ends and the phones on it, Change, Manage subscription, and Restore purchase. Without a plan: Start your subscription.</dd></div>
      <div><dt>Your data</dt><dd>Download my data, a copy of what Steward's server keeps about this phone, and Delete my data.</dd></div>
      <div><dt>Help</dt><dd>Write to me: a question, a bug or an idea, by email.</dd></div>
      <div><dt>About</dt><dd>The privacy policy and the terms.</dd></div>
    </dl>

    <h2>The subscription</h2>
    <p>Steward is free to download, and using it needs a subscription. Every plan has every feature; plans differ only in how many phones they cover.</p>
    <dl class="rows plate">
      <div><dt>Steward</dt><dd>For 2 phones. 4.99 a month or 29.99 a year.</dd></div>
      <div><dt>Pro</dt><dd>Up to 10 phones. 9.99 a month or 59.99 a year.</dd></div>
      <div><dt>Unlimited</dt><dd>Every phone you have. 19.99 a month or 99.99 a year. Meant for personal and family use, about 200 trips followed at once.</dd></div>
    </dl>
    <p style="margin-top:12px">Prices are the listed ones in US dollars; Google Play shows your own price before you pay. New subscribers get 3 days free, one trial per Google account. After the trial the subscription starts unless you cancel in Google Play before it ends. A phone you have not opened Steward on for 30 days frees its place on your plan. If the subscription ends, your trips stay in the app as a read only list.</p>

    <h2>Privacy</h2>
    <p>No ads, no tracking, no analytics and no sign in. To watch a flight, Steward sends its server the flight number, the day and the seat you added, and a push token so alerts can reach your phone. Your calendar is read on the phone, and only the flight number and day of a flight you add leave it. Boarding passes stay on your phone. From where I am uses a rough location on the day of travel, kept on this phone. The full <a href="{SITE}/privacy">privacy policy</a> says what is kept and for how long.</p>

    <h2>Accessibility</h2>
    <p>Light and dark looks, big text and TalkBack labels. Buttons are at least 48 dp, and travel day mode reads as one sentence with TalkBack.</p>
    </div>
""")

page("cookbook.html", "Cookbook", "Short Steward recipes: add a flight, read a boarding pass, share your ETA, get the pass on the lock screen, keep flights in your calendar, change or cancel your plan, and delete your data.", f"""
    <div class="doc">
    <p class="lbl">Cookbook</p>
    <h1>Short recipes</h1>
    <p>A few taps each. Everything here needs a live subscription, except the plan and data recipes.</p>

    <h2>Add a flight by its number</h2>
    <ol><li>Tap the round add button in the bar.</li><li>Pick the day from the chips above the box, or Later for another day.</li><li>Type the flight number, like OU 410, and search.</li><li>Tap the flight to follow it.</li></ol>

    <h2>Add the flights in your calendar</h2>
    <ol><li>Settings, Finding flights, turn on Look in my calendar, and allow the calendar.</li><li>Open Flights. Under Found in your calendar, tap Add, or Not mine.</li></ol>

    <h2>Add a trip from the booking email</h2>
    <ol><li>Open the booking email in Gmail or the trip in the airline app.</li><li>Tap Share and pick Steward.</li><li>Steward lists the flights it found. Add the ones you take.</li></ol>

    <h2>Add a boarding pass</h2>
    <ol><li>Open the flight, then Boarding pass.</li><li>Pick A screenshot, or A PDF or Wallet pass.</li><li>The pass is kept with that flight, with its seat.</li></ol>

    <h2>Have the pass open over the lock screen</h2>
    <ol><li>Settings, Boarding pass, turn on Show the pass on the lock screen.</li><li>From boarding time, tap the live update on the lock screen. Only the pass shows.</li></ol>

    <h2>Put your boarding pass in Quick Settings</h2>
    <ol><li>Keep your first boarding pass. On Android 13 and newer, Steward offers the tile once: tap Add.</li><li>Missed it? Edit your Quick Settings tiles and drag in Boarding pass. It shows your next pass, one tap away.</li></ol>

    <h2>Share your ETA</h2>
    <ol><li>Open the flight and tap Share ETA.</li><li>Pick the app to send it with, or Copy live link.</li><li>To end it early: the flight, then Stop sharing the live link.</li></ol>

    <h2>Know when to leave for the airport</h2>
    <ol><li>Settings, Tell me about, set Time to the airport and Be at the airport.</li><li>For a guess from where you are on the day, turn on From where I am. The longer time wins.</li></ol>

    <h2>Keep flights in your calendar</h2>
    <ol><li>Settings, Finding flights, turn on Keep flights in my calendar, and allow the calendar.</li><li>Each flight is written with its latest times, terminal and gate. Turn it off and every event Steward wrote is removed.</li></ol>

    <h2>Bring back the live update</h2>
    <ol><li>Open the flight.</li><li>Tap Show the live update again.</li></ol>

    <h2>Start your subscription</h2>
    <ol><li>Settings, Your plan, Start your subscription.</li><li>Pick Steward, Pro or Unlimited, then Monthly or Yearly.</li><li>Tap Try 3 days free. Google Play shows the price before you pay.</li></ol>

    <h2>Change your plan</h2>
    <ol><li>Settings, Your plan, tap your plan (Change).</li><li>Pick the plan and the period, then tap Switch to.</li></ol>

    <h2>Cancel your subscription</h2>
    <ol><li>Settings, Your plan, Manage subscription.</li><li>In Google Play, tap Cancel subscription. Steward keeps working to the end of the time you paid for.</li></ol>

    <h2>Use your plan on another phone</h2>
    <ol><li>Install Steward on the other phone, signed in to Google Play with the account that bought the plan.</li><li>Settings, Your plan, Restore purchase.</li></ol>

    <h2>Get a copy of your data</h2>
    <ol><li>Settings, Your data, Download my data.</li><li>Pick where to save the file. It is a JSON file.</li></ol>

    <h2>Delete your data</h2>
    <ol><li>Settings, Your data, Delete my data.</li><li>Tap Delete. Steward erases this phone from its server, removes the calendar events it wrote, clears the phone and closes.</li><li>This does not cancel your subscription. Cancel it in Google Play.</li></ol>
    </div>
""")

page("runbook.html", "Runbook", "When something in Steward goes wrong: alerts not arriving, the live update, exact timing, calendar finds, boarding passes, the subscription, restore purchase, refunds and deleting your data.", f"""
    <div class="doc">
    <p class="lbl">Runbook</p>
    <h1>When something goes wrong</h1>
    <p>What you see, why it happens, and the taps that fix it. Most fixes start in Settings, Ready for your trips: anything with a Fix button there is off. More answers are in the <a href="faq.html">questions</a>.</p>

    <h2>Alerts do not arrive</h2>
    <p>Notifications are off, an alert switch is off, the subscription has ended, or the news was already known when you added the flight.</p>
    <ol><li>Settings, Ready for your trips. If Notifications says Off, tap Fix and allow them.</li><li>In Android's notification settings for Steward, check that Gate, delay and cancellation, Take off, landing and bags, and Check in, leave and boarding are not off or silent.</li><li>Settings, Tell me about: check the switch for that alert.</li><li>Settings, Your plan. Without a live subscription Steward gets no alerts at all, cancellations included.</li><li>A gate already given when you added the flight is not sent again; only a change is. A second alert of the same kind replaces the first.</li></ol>

    <h2>The live update is not on the lock screen</h2>
    <p>It starts two hours before departure, for one flight at a time. It may be switched off, unpinned for that flight, or not allowed to sit on the lock screen.</p>
    <ol><li>Settings, Tell me about: turn on Live update on the lock screen.</li><li>On Android 16 and newer, Settings, Ready for your trips: if it says Live updates are off for Steward, tap Fix and allow it.</li><li>If you unpinned or swiped it away, open the flight and tap Show the live update again.</li><li>Check that the phone's lock screen shows notifications.</li></ol>

    <h2>Leave now or boarding came a few minutes late</h2>
    <p>Exact timing is off, so Android may hold the reminder back while the phone sleeps.</p>
    <ol><li>Settings, Ready for your trips, Exact timing, Fix.</li><li>Allow Alarms and reminders for Steward, then come back.</li></ol>

    <h2>The pass asks me to unlock first</h2>
    <p>Show the pass on the lock screen is off.</p>
    <ol><li>Settings, Ready for your trips, Pass on the lock screen, Fix. Or Settings, Boarding pass, turn on Show the pass on the lock screen.</li></ol>

    <h2>The calendar finds nothing</h2>
    <p>Steward reads only flights that Gmail put into Google Calendar, from today on, and only with your OK.</p>
    <ol><li>Settings, Finding flights, turn on Look in my calendar, and allow the calendar.</li><li>In Google Calendar's settings, turn on Events from Gmail.</li><li>If Android no longer asks, Steward opens its app settings: allow Calendar there.</li><li>Or add the flight by its number.</li></ol>

    <h2>The calendar found the wrong flight</h2>
    <p>The flight number or day in the event did not match your trip.</p>
    <ol><li>Tap Not mine to hide it. It stays hidden for good.</li><li>Add the right flight by its number with the local departure day.</li><li>To stop calendar finds, Settings, Finding flights, turn off Look in my calendar.</li></ol>

    <h2>A boarding pass will not read</h2>
    <p>Steward could not find the barcode, or the pass is for another flight.</p>
    <ol><li>For a picture, use a sharper screenshot of the barcode.</li><li>If it says the pass is for another flight, add that flight first, or open the right pass.</li><li>If the gate scanner cannot read Steward's barcode, use the airline's own pass.</li></ol>

    <h2>My trips say they are not watched</h2>
    <p>The subscription ended or has not started. Your trips stay to read, but nothing is watched.</p>
    <ol><li>Settings, Your plan, See plans, and subscribe again. Steward picks up where it left off.</li></ol>

    <h2>I paid but Steward is still locked</h2>
    <p>The purchase is on another Google account, the payment is pending, or the phone has not asked Google Play yet.</p>
    <ol><li>Open the Play Store and check you are signed in with the account that bought the plan.</li><li>Settings, Your plan, Restore purchase.</li><li>If it says your payment is pending, Steward turns on when Google Play clears it.</li></ol>

    <h2>Restore purchase says no subscription</h2>
    <p>The Google account on this phone has no Steward plan. A plan bought with another account restores from that account.</p>
    <ol><li>Switch the Play Store to the account that bought it, then Restore purchase again.</li></ol>

    <h2>It says all the phones on my plan are in use</h2>
    <p>Steward covers 2 phones, Pro up to 10, Unlimited any number.</p>
    <ol><li>Tap Move up to the next plan on the plans page.</li><li>Or wait: a phone that has not opened Steward for 30 days frees its place.</li></ol>

    <h2>The subscription will not start</h2>
    <p>Google Play is not set up on this phone, not reachable, or the phone is offline.</p>
    <ol><li>Open the Play Store once and check you are signed in.</li><li>Update the Play Store, get online, then try again.</li></ol>

    <h2>Cancel the subscription or the trial</h2>
    <ol><li>Settings, Your plan, Manage subscription. Or Play Store, your profile, Payments and subscriptions, Subscriptions, Steward.</li><li>Tap Cancel subscription. Cancel a trial before the 3 days end and you are not charged.</li></ol>

    <h2>Get a refund</h2>
    <p>Google Play takes the payment, so refunds follow Google Play's rules.</p>
    <ol><li>Ask Google Play: open your order history at play.google.com, find the Steward order, and request a refund.</li><li>If Google sends you to the developer, write to <span class="mail">{MAIL}</span> with the order number.</li><li>A refund ends the plan. Cancelling does not refund; it keeps Steward on to the end of the time you paid for.</li></ol>

    <h2>The widget is out of date</h2>
    <p>The widget redraws on alerts, syncs and the system's widget period, so it can lag while the phone sleeps.</p>
    <ol><li>Open Steward once.</li><li>Still wrong? Remove the widget and add it again.</li></ol>

    <h2>Delete my data</h2>
    <p>Steward has no account; what its server keeps belongs to the phone the app is on.</p>
    <ol><li>Settings, Your data, Download my data first if you want a copy.</li><li>Settings, Your data, Delete my data, Delete.</li><li>Already uninstalled? Read <a href="{SITE}/delete">{SITE.removeprefix("https://")}/delete</a>, or write to <span class="mail">{MAIL}</span> with the number and day of a flight you followed.</li><li>Deleting data does not cancel the subscription. Cancel it in Google Play.</li></ol>
    </div>
""")

page("faq.html", "Questions", "Answers to common questions about Steward: the subscription and trial, phones per plan, privacy, the calendar, boarding passes and the live update.", f"""
    <div class="doc">
    <p class="lbl">Questions</p>
    <h1>Questions and fixes</h1>

    <h2>Why is there no free version?</h2>
    <p>Every trip you follow is watched live by a paid flight data service, around the clock. So Steward is free to download, using it needs a subscription, and there are no ads.</p>

    <h2>How does the free trial work?</h2>
    <p>New subscribers get 3 days free through Google Play, one trial per Google account. If you do not cancel in Google Play before the 3 days end, the subscription starts and Google Play charges you.</p>

    <h2>What is the difference between the plans?</h2>
    <p>Only the number of phones. Steward covers 2 phones, Pro up to 10, and Unlimited every phone you have. Every plan has every feature.</p>

    <h2>Does Steward track trains?</h2>
    <p>Not in this version. Steward follows flights.</p>

    <h2>Do I need an account?</h2>
    <p>No. There is no sign in and no email. The subscription belongs to the Google account that bought it.</p>

    <h2>What leaves my phone?</h2>
    <p>The flight number, the day and the seat you added, and a push token so alerts can reach you. Your calendar is read on the phone, and only the flight number and day of a flight you add leave it. Boarding passes stay on your phone. See the <a href="{SITE}/privacy">privacy policy</a>.</p>

    <h2>Does Steward read my email?</h2>
    <p>No. It reads flights Gmail put into your calendar, on the phone. When you share a booking email to Steward yourself, it finds the flight numbers and date in that text and keeps nothing else.</p>

    <h2>Why does it want my location?</h2>
    <p>Only if you turn on From where I am, so Steward can say when to leave from where you are. It is a rough location on the day of travel, kept on this phone.</p>

    <h2>What happens when my subscription ends?</h2>
    <p>Your trips stay in the app as a read only list. Steward stops watching them: no live updates, no alerts, no new trips. Subscribe again and it picks up where it left off.</p>

    <h2>Will I lose my boarding passes on a new phone?</h2>
    <p>Yes. Passes live only on the phone and are not backed up. Add them again on the new phone.</p>

    <h2>Why is the gate empty?</h2>
    <p>The airport has not given it yet. Steward says Gate soon and tells you the moment it is given.</p>

    <h2>Are boarding and door times exact?</h2>
    <p>They are estimates. The airline's own time wins.</p>

    <h2>Who sees my shared ETA?</h2>
    <p>Anyone with the link. It shows the flight only, never your seat or your name, and ends a few hours after you land. Stop sharing the live link, on the flight screen, ends it at once.</p>

    <h2>Why do I not see the status bar chip?</h2>
    <p>The chip in the status bar is on Android 16 and newer. On older Android the live update shows in the notification shade and on the lock screen.</p>

    <h2>How do I get a refund?</h2>
    <p>Google Play takes the payment, so refunds follow Google Play's rules. The <a href="runbook.html">runbook</a> has the steps.</p>

    <h2>How do I delete my data?</h2>
    <p>Settings, Your data, Delete my data. Without the app, read <a href="{SITE}/delete">the deletion page</a>.</p>
    </div>
""")

page("report.html", "Report a bug", "How to report a Steward bug or ask for a feature on GitHub, or by email.", f"""
    <div class="doc" style="max-width:none">
    <p class="lbl">Report</p>
    <h1>Report a bug or ask for a feature</h1>
    <p style="margin-top:16px">Found something broken, or have an idea? Tell us on GitHub. A free GitHub account is all you need.</p>
    <div class="cards">
      <div class="card plate"><h2 class="h3">Bug report</h2><p>Something does not work, looks wrong, or crashes.</p><a class="key filled" href="{REPO}/issues/new?template=bug_report.yml">Report a bug</a></div>
      <div class="card plate"><h2 class="h3">Feature request</h2><p>Something you would like Steward to do.</p><a class="key tonal" href="{REPO}/issues/new?template=feature_request.yml">Ask for a feature</a></div>
    </div>
    </div>
    <div class="doc">
    <h2>Before you write</h2>
    <ul>
      <li>Search the <a href="{REPO}/issues">open issues</a> first. If yours is there, add a thumbs up or a comment.</li>
      <li>Check the <a href="runbook.html">runbook</a> and the <a href="faq.html">questions</a>.</li>
      <li>One problem per report makes it faster to fix.</li>
    </ul>

    <h2>What helps</h2>
    <dl class="rows plate">
      <div><dt>App version</dt><dd>Android settings, Apps, Steward.</dd></div>
      <div><dt>Phone model and Android version</dt><dd>Android settings, About phone.</dd></div>
      <div><dt>Which screen</dt><dd>Flights, Add flight, the flight screen, Your plane, the boarding pass, the live update, an alert, Passport, Settings, the plans page, or the widget.</dd></div>
      <div><dt>The flight</dt><dd>The flight number and day, if the bug is about one flight.</dd></div>
      <div><dt>Steps</dt><dd>What you did, one step per line, so we can do the same.</dd></div>
      <div><dt>Expected and actual</dt><dd>What you thought would happen, and what happened.</dd></div>
      <div><dt>A picture or a recording</dt><dd>A screenshot or a short screen recording. Drag it into the form.</dd></div>
    </dl>
    <p style="margin-top:16px">Issues on GitHub are public. Before you attach a screenshot, crop or cover anything private: your name, your seat, the barcode of a boarding pass and booking codes.</p>

    <h2>Other ways</h2>
    <p>No GitHub account, or something private? Write to <span class="mail">{MAIL}</span> (<a href="mailto:{MAIL}">write an email</a>). In the app: Settings, Help, Write to me.</p>
    </div>
""")
