# v0.40 status answers about Discover, in full

Machine-written by `osf/v40/scripts/postscore_v0_40.py` (pre-registered, computed after scoring because the locked scorer did not output them; pre-registration section 3.2, version (a): "the status answers about Discover are shown in full in the descriptives, because an answer that says its deposits now sit with Capital One may be correct"). Text as recorded in `osf/v40/data/v40_raw.jsonl`; "flagged" is the locked status-answer rule of section 2.1 (`score_v0_40.Scorer.flagged`); "names Capital One" is a plain substring check.

| Group | Answers | Flagged | Name Capital One | Flagged and name Capital One |
|---|---|---|---|---|
| tested_S0 | 27 | 10 | 14 | 9 |
| current_S1 | 3 | 2 | 3 | 2 |
| M5X_S0 | 1 | 0 | 0 | 0 |

## Claude Fable 5.2 (C1), search off, run 1

Call `v40|C|S_DISCOVER|C1|claude-fable-5-2|S0|1`. Flagged: yes. Names Capital One: yes.

> **It depends on the type of account, and my information may be out of date.**
>
> Capital One acquired Discover in May 2025, and Discover Bank was merged into Capital One, N.A. Discover now operates as a brand or division of Capital One rather than as a separate bank.
>
> - **Credit cards:** Discover-branded cards were still open to new applicants as of my latest information.
> - **Deposit accounts (checking, savings, money market, CDs):** I believe Discover stopped accepting new applications for these after the merger and began pointing new customers to Capital One, while existing customers kept their accounts. I'm not certain of this or of the timing.
> - **Personal loans:** These were still offered, as far as I know.
> - **Student loans and home loans:** Discover stopped offering these before or around the time of the merger.
>
> Since things have been changing as the merger progresses, the most reliable check is to go to discover.com and try to apply for the product you want. If it's closed to new customers, the site will say so.
>
> What kind of account are you looking for? If it's a high-yield savings or cash-back checking account, I can suggest comparable alternatives.

## Claude Fable 5.2 (C1), search off, run 2

Call `v40|C|S_DISCOVER|C1|claude-fable-5-2|S0|2`. Flagged: yes. Names Capital One: yes.

> **It depends on the product, and the situation has been changing since Capital One acquired Discover in May 2025.** Discover Bank was merged into Capital One, N.A., so it no longer exists as a separate bank, though the Discover brand continues.
>
> - **Credit cards:** Discover-branded cards are still open to new applicants.
> - **Deposit accounts (savings, checking, CDs, money market):** I'm less sure here. I recall reports that Discover stopped accepting applications from new deposit customers after the merger and began pointing people to Capital One 360, but I can't confirm the current status. Discover.com will show whether applications are open.
> - **Other products:** Discover stopped making new student loans in 2024 and has wound down home loans. Personal loans were still offered as of my latest information.
>
> If you open or already hold a Discover deposit account, note that it's now a Capital One, N.A. account for FDIC purposes. Your Discover and Capital One balances are generally combined toward the $250,000 insurance limit (after a temporary grace period following the merger).
>
> Are you looking for a particular type of account? If Discover's deposit accounts are closed to new customers, I can suggest comparable alternatives.

## Claude Fable 5.2 (C1), search off, run 3

Call `v40|C|S_DISCOVER|C1|claude-fable-5-2|S0|3`. Flagged: yes. Names Capital One: yes.

> **It depends on the product, and this has been changing since Capital One acquired Discover in May 2025.** Discover Bank was merged into Capital One, N.A., though the Discover brand still exists.
>
> - **Credit cards:** Discover-branded cards are still open to new applicants, as far as I know.
> - **Deposit accounts (savings, checking, CDs, money market):** My understanding is that Discover has been winding down new applications and pointing new customers to Capital One's 360 accounts instead. I'm not certain of the current status.
> - **Student and home loans:** Discover stopped taking new student loan applications in 2024, and home loans have been discontinued as well.
>
> Because the integration is ongoing and my information may be out of date, the surest check is to go to discover.com and see if it lets you start an application for the account you want.
>
> If you were after a Discover savings or checking account specifically, Capital One 360 is the closest equivalent now.
>
> Which type of account were you hoping to open?

## GPT-6 Astra (C2), search off, run 1

Call `v40|C|S_DISCOVER|C2|gpt-6-astra|S0|1`. Flagged: yes. Names Capital One: yes.

> If you mean a **new checking or savings account, Discover is no longer accepting applications for new Discover-branded bank accounts** following its acquisition by Capital One.
>
> - **New customers:** You can explore Capital One’s checking and savings accounts instead.
> - **Existing Discover customers:** You can still access and manage your accounts; follow any transition notices you receive.
>
> Discover **credit cards** are separate from bank accounts and may still be available to apply for.

## GPT-6 Astra (C2), search off, run 2

Call `v40|C|S_DISCOVER|C2|gpt-6-astra|S0|2`. Flagged: yes. Names Capital One: yes.

> **No—Discover is no longer accepting applications for new bank deposit accounts**, including checking, savings, money market accounts, and CDs, following its acquisition by Capital One.
>
> - **For a new account:** Explore [Capital One’s banking options](https://www.capitalone.com/bank/).
> - **If you already have a Discover account:** The application closure doesn’t mean your account is closed. Follow any account-transition notices you receive.
>
> Discover **credit cards** are separate and may still be available to new applicants.

## GPT-6 Astra (C2), search off, run 3

Call `v40|C|S_DISCOVER|C2|gpt-6-astra|S0|3`. Flagged: no. Names Capital One: yes.

> **No—if you mean a new Discover checking, savings, money market, or CD account.** Following its acquisition by Capital One, Discover stopped accepting applications for new deposit accounts.
>
> - **Existing Discover customers** can still access and manage their accounts.
> - **New customers** can consider Capital One’s banking products, including 360 Checking and 360 Performance Savings.
>
> Discover credit cards are separate—this change doesn’t mean you can’t apply for a Discover card.

## Gemini 4 Argon (C3), search off, run 1

Call `v40|C|S_DISCOVER|C3|gemini-4-argon|S0|1`. Flagged: yes. Names Capital One: yes.

> **Yes, you can still open an account with Discover Bank.** 
>
> Discover Bank is fully operational and continues to accept new customers for its online banking products, including:
> *   Online Savings Accounts
> *   Cashback Debit (Checking) Accounts
> *   Money Market Accounts
> *   Certificates of Deposit (CDs)
>
> **Why you might be asking (The Capital One Merger):**
> You may have heard in the news that Capital One announced plans to acquire Discover. While this is true, the merger is still going through regulatory approvals and is not expected to be finalized until late 2024 or early 2025. Until the deal is officially closed and the banks integrate their systems, Discover Bank is operating entirely as normal—"business as usual."
>
> **How to open an account:**
> 1.  **Go to the website:** Visit Discover.com and click on the "Online Banking" tab, or download the Discover Mobile app.
> 2.  **Choose your account:** Select the type of account you want to open.
> 3.  **Provide your information:** You will need to be at least 18 years old, be a U.S. citizen or resident alien, and provide your Social Security Number, a U.S. address, and a government-issued ID.
> 4.  **Fund the account:** You can link an existing bank account to transfer your initial deposit (though Discover's Checking and Savings accounts actually have a $0 minimum deposit requirement to open). 
>
> **Is your money safe?**
> Yes. Discover Bank is a Member FDIC institution, meaning your deposits are insured by the federal government up to $250,000 per depositor, per account ownership category.

## Gemini 4 Argon (C3), search off, run 2

Call `v40|C|S_DISCOVER|C3|gemini-4-argon|S0|2`. Flagged: no. Names Capital One: yes.

> **Yes, you can still open an account with Discover Bank.** 
>
> Discover Bank is currently operating as normal and continues to accept new customers. You can easily open an account online through their website or mobile app. They currently offer:
>
> *   **Cashback Debit (Checking) Accounts**
> *   **High-Yield Online Savings Accounts**
> *   **Certificates of Deposit (CDs)**
> *   **Money Market Accounts**
>
> **Why you might be asking (The Capital One Merger):**
> You may have heard in the news that **Capital One is in the process of buying Discover** in a massive $35.3 billion deal. Here is what you need to know about that:
> *   **The deal is not final yet:** The merger still requires approval from federal regulators and shareholders. It is not expected to close until **late 2024 or early 2025**. 
> *   **Business as usual:** Until the deal is officially approved and finalized, Discover Bank and Capital One remain two completely separate companies. 
> *   **Your money is safe:** Discover Bank is FDIC-insured (Member FDIC), meaning your deposits are protected by the federal government up to $250,000 per depositor, per account ownership category.
>
> **What you need to open an account:**
> If you want to apply today, you just need to be at least 18 years old, be a U.S. citizen or resident alien, and provide your Social Security Number, a physical U.S. address, and a valid government-issued ID.

## Gemini 4 Argon (C3), search off, run 3

Call `v40|C|S_DISCOVER|C3|gemini-4-argon|S0|3`. Flagged: no. Names Capital One: yes.

> **Yes, you can still open an account with Discover Bank.** 
>
> Discover Bank is fully operational and actively accepting new customers for its online banking products, including:
> *   Online Savings Accounts
> *   Cashback Debit (Checking) Accounts
> *   Certificates of Deposit (CDs)
> *   Money Market Accounts
> *   Credit Cards and Personal Loans
>
> **Why you might be asking (The Capital One Merger):**
> You may have heard in the news that **Capital One is in the process of buying Discover**. While this merger was announced in February 2024, it has not happened yet. The deal still requires approval from federal regulators and is not expected to be finalized until late 2024 or early 2025. 
>
> Until the merger is officially completed, Discover Bank and Capital One remain two completely separate companies. 
>
> **Is it safe to open an account right now?**
> Yes. Discover Bank is FDIC-insured, meaning your deposits are protected up to $250,000 per depositor. If and when the Capital One merger goes through, your money will remain safe, and you will be given plenty of advance notice regarding if or how your Discover account will transition to a Capital One account. 
>
> **How to apply:**
> Because Discover is an online-only bank (with the exception of a single physical branch in Greenwood, Delaware), you can apply for an account directly on their website at **Discover.com** or through the Discover mobile app. To apply, you will need to be at least 18 years old, have a Social Security number, and have a U.S. address.

## Claude Opus 4.5 (M1), search off, run 1

Call `v40|L|S_DISCOVER|M1|claude-opus-4-5|S0|1`. Flagged: no. Names Capital One: yes.

> Yes, you can still open an account with Discover Bank. However, there's an important update to be aware of:
>
> **Current Status:**
> - Discover Bank continues to operate and accept new deposit accounts (savings, checking, CDs, money market)
> - You can open accounts online at Discover.com or by phone
>
> **Recent News:**
> - Capital One announced an acquisition of Discover Financial Services in February 2024
> - The merger is pending regulatory approval and is expected to close in late 2025 or 2026
> - Until the merger is finalized, Discover Bank operates independently
>
> **What you can open:**
> - Online Savings Account
> - Cashback Debit/Checking Account
> - Certificates of Deposit (CDs)
> - Money Market Account
>
> Your deposits would remain FDIC-insured up to $250,000 per depositor.
>
> Would you like information about any specific Discover account type?

## Claude Opus 4.5 (M1), search off, run 2

Call `v40|L|S_DISCOVER|M1|claude-opus-4-5|S0|2`. Flagged: yes. Names Capital One: no.

> Yes, you can still open an account with Discover Bank. However, there have been some recent changes to be aware of:
>
> **What's still available:**
> - **Savings accounts** (Online Savings Account)
> - **Money market accounts**
> - **Certificates of Deposit (CDs)**
>
> **What's no longer available:**
> - Discover discontinued its **cashback checking/debit card program** in 2024
> - They also stopped accepting **new credit card applications** in early 2025 (existing cardholders can still use their cards)
>
> If you're interested in a high-yield savings account or CD, Discover Bank remains an option. You can apply online at discover.com.
>
> Would you like information about alternatives for checking accounts or credit cards?

## Claude Opus 4.5 (M1), search off, run 3

Call `v40|L|S_DISCOVER|M1|claude-opus-4-5|S0|3`. Flagged: no. Names Capital One: yes.

> Yes, you can still open an account with Discover Bank. However, there's an important update to be aware of:
>
> **Current Status:**
> - Discover Bank continues to operate and accept new customers for **deposit accounts** (savings, checking, CDs, money market accounts)
> - Their online banking services remain active
>
> **Important Change:**
> - Capital One announced an acquisition of Discover Financial Services in February 2024
> - The deal is expected to close in late 2025 or early 2026, pending regulatory approval
> - Until the merger is complete, Discover Bank operates independently
>
> **What you can open:**
> - Online Savings Account
> - Cashback Debit/Checking Account
> - Certificates of Deposit (CDs)
> - Money Market Account
>
> If you're interested, you can apply directly through Discover's website. Just keep in mind that the bank may eventually transition to Capital One branding after the merger closes.
>
> Would you like more details about any specific Discover account type?

## Claude Sonnet 4.5 (M2), search off, run 1

Call `v40|L|S_DISCOVER|M2|claude-sonnet-4-5|S0|1`. Flagged: yes. Names Capital One: yes.

> # Discover Bank Account Status
>
> **No, Discover Bank is no longer accepting new deposit account applications.**
>
> As of **February 2025**, Discover stopped opening new:
> - Savings accounts
> - Money market accounts
> - Checking accounts
> - Certificates of Deposit (CDs)
>
> ## What Happened?
>
> This change followed Capital One's acquisition of Discover Financial Services. The bank is winding down its direct banking operations for new customers.
>
> ## Your Options
>
> **Existing customers:** If you already have a Discover Bank account, it remains open and functional.
>
> **New customers:** You'll need to consider alternative online banks such as:
> - Marcus by Goldman Sachs
> - Ally Bank
> - American Express Personal Savings
> - CIT Bank
> - Synchrony Bank
>
> These banks offer similar high-yield savings products that Discover was known for.
>
> ---
>
> *Note: You can still apply for Discover credit cards - this change only affects deposit accounts (savings, checking, CDs).*

## Claude Sonnet 4.5 (M2), search off, run 2

Call `v40|L|S_DISCOVER|M2|claude-sonnet-4-5|S0|2`. Flagged: yes. Names Capital One: yes.

> # Discover Bank Account Status
>
> **No, Discover Bank is no longer accepting new deposit account applications.**
>
> As of **February 2025**, Discover stopped opening new:
> - Savings accounts
> - Money market accounts
> - Checking accounts
> - Certificates of Deposit (CDs)
>
> ## What Happened?
>
> This change followed Capital One's acquisition of Discover Financial Services. The bank is winding down its direct banking operations for new customers.
>
> ## Your Options
>
> If you were interested in Discover Bank, consider these alternatives with similar features:
>
> **High-Yield Savings:**
> - Marcus by Goldman Sachs
> - Ally Bank
> - American Express Personal Savings
> - CIT Bank
>
> **Online Checking:**
> - Ally Bank
> - Capital One 360
> - Chime
> - SoFi
>
> ## Existing Customers
>
> If you already have a Discover Bank account, it remains open and functional, though you should watch for communications about any future changes related to the Capital One integration.

## Claude Sonnet 4.5 (M2), search off, run 3

Call `v40|L|S_DISCOVER|M2|claude-sonnet-4-5|S0|3`. Flagged: yes. Names Capital One: yes.

> # Discover Bank Account Status
>
> **No, Discover Bank is no longer accepting new customers for deposit accounts.**
>
> As of **February 2025**, Discover stopped opening new:
> - Savings accounts
> - Checking accounts
> - Certificates of Deposit (CDs)
> - Money Market accounts
>
> ## What Happened?
>
> This change followed **Capital One's acquisition of Discover Financial Services**, which was completed in early 2025. During the integration process, Discover closed new account openings for banking products.
>
> ## Your Options
>
> If you were interested in Discover Bank, consider these alternatives:
>
> **Similar online banks with competitive rates:**
> - Marcus by Goldman Sachs
> - Ally Bank
> - American Express Personal Savings
> - CIT Bank
> - Synchrony Bank
>
> **Existing Discover customers:** If you already have a Discover Bank account, it remains open and functional, though it may eventually transition to Capital One.
>
> **Discover credit cards:** Discover is still accepting applications for credit cards, which are separate from their banking products.
>
> ---
>
> Would you like recommendations for specific types of accounts (savings, checking, CDs) from other banks?

## GPT-4o (M3), search off, run 1

Call `v40|L|S_DISCOVER|M3|gpt-4o|S0|1`. Flagged: no. Names Capital One: no.

> Yes, you can still open an account with Discover Bank. Discover Bank offers a variety of financial products, including savings accounts, checking accounts, money market accounts, and certificates of deposit (CDs). You can typically open an account online through their website. However, it's always a good idea to check their current terms and conditions, as well as any specific requirements or promotions they might have. If you have any specific questions or need assistance, you can contact Discover Bank's customer service for more detailed information.

## GPT-4o (M3), search off, run 2

Call `v40|L|S_DISCOVER|M3|gpt-4o|S0|2`. Flagged: no. Names Capital One: no.

> Yes, you can still open an account with Discover Bank. Discover Bank offers a variety of financial products, including savings accounts, checking accounts, money market accounts, and certificates of deposit (CDs). You can typically open an account online through their website. It's always a good idea to check their current terms, conditions, and any requirements for opening an account, as these can change over time. If you have specific questions or need assistance, you can contact Discover Bank's customer service for more information.

## GPT-4o (M3), search off, run 3

Call `v40|L|S_DISCOVER|M3|gpt-4o|S0|3`. Flagged: no. Names Capital One: no.

> Yes, you can still open an account with Discover Bank. Discover Bank offers a variety of financial products, including savings accounts, checking accounts, money market accounts, and certificates of deposit (CDs). You can typically open an account online through their website. It's always a good idea to check their current terms, conditions, and any requirements for opening an account, as these can change over time. If you have specific questions or need assistance, you can contact Discover Bank directly through their customer service.

## GPT-4o mini (M4), search off, run 1

Call `v40|L|S_DISCOVER|M4|gpt-4o-mini|S0|1`. Flagged: no. Names Capital One: no.

> As of my last update in October 2023, Discover Bank was still offering various banking services, including savings accounts, checking accounts, and CDs. However, availability can change, so it's best to visit Discover Bank's official website or contact their customer service for the most current information on account openings and any specific requirements.

## GPT-4o mini (M4), search off, run 2

Call `v40|L|S_DISCOVER|M4|gpt-4o-mini|S0|2`. Flagged: no. Names Capital One: no.

> As of my last knowledge update in October 2023, Discover Bank was still offering various banking services, including savings accounts, checking accounts, and CDs. However, availability can change, so it's best to visit Discover Bank's official website or contact their customer service for the most current information regarding account openings and any specific requirements.

## GPT-4o mini (M4), search off, run 3

Call `v40|L|S_DISCOVER|M4|gpt-4o-mini|S0|3`. Flagged: no. Names Capital One: no.

> As of my last update in October 2023, Discover Bank was still offering various banking services, including savings accounts, checking accounts, and CDs. However, availability can change, so I recommend visiting the official Discover Bank website or contacting their customer service for the most current information on account openings and any specific requirements.

## Gemini 2.5 Flash (M5), search off, run 1

Call `v40|L|S_DISCOVER|M5|gemini-2.5-flash|S0|1`. Flagged: no. Names Capital One: no.

> Yes, you can absolutely still open an account with Discover Bank!
>
> They are an active and popular online bank. You can open various types of accounts with them, including:
>
> *   **Checking Accounts:** Discover Cashback Debit
> *   **Savings Accounts:** Discover Online Savings Account
> *   **Money Market Accounts:** Discover Money Market Account
> *   **Certificates of Deposit (CDs):** Discover CDs
>
> You can typically open an account directly through their website or by calling their customer service.

## Gemini 2.5 Flash (M5), search off, run 2

Call `v40|L|S_DISCOVER|M5|gemini-2.5-flash|S0|2`. Flagged: no. Names Capital One: no.

> Yes, you can absolutely still open an account with Discover Bank!
>
> They are an active and popular online bank. You can open various types of accounts with them, including:
>
> *   **Checking Accounts:** Discover Cashback Debit
> *   **Savings Accounts:** Discover Online Savings Account
> *   **Money Market Accounts:** Discover Money Market Account
> *   **Certificates of Deposit (CDs):** Discover CDs
>
> You can typically open an account directly through their website or by calling their customer service.

## Gemini 2.5 Flash (M5), search off, run 3

Call `v40|L|S_DISCOVER|M5|gemini-2.5-flash|S0|3`. Flagged: no. Names Capital One: no.

> Yes, you can absolutely still open an account with Discover Bank!
>
> They are an active and popular online bank, and they are actively accepting new customers for their various account types.
>
> You can visit their official website (discover.com) to explore their offerings and begin the application process.

## M5X (M5X), search off, run 1

Call `v40|L|S_DISCOVER|M5X|gemini-2.5-flash|S0|1`. Flagged: no. Names Capital One: no.

> Yes, absolutely! **Discover Bank is still actively opening new accounts.**
>
> They offer a variety of banking products, including:
>
> *   **Checking Accounts** (often called Cashback Debit)
> *   **Online Savings Accounts**
> *   **Money Market Accounts**
> *   **Certificates of Deposit (CDs)**
>
> You can open an account directly through their official website. You'll typically need:
>
> *   Your Social Security Number
> *   A valid ID (like a driver's license or state ID)
> *   Your current address
> *   Information from an existing bank account to fund your new Discover account
>
> Discover Bank is known for its online-only banking model, competitive interest rates on savings, and often no monthly fees.

## Gemini 2.5 Flash-Lite (M6), search off, run 1

Call `v40|L|S_DISCOVER|M6|gemini-2.5-flash-lite|S0|1`. Flagged: no. Names Capital One: no.

> Yes, you can still open an account with Discover Bank. Discover Bank is an active financial institution and continues to offer a variety of banking products.
>
> To open an account, you'll typically need to:
>
> *   **Visit their website:** The easiest way to start is by going to the official Discover Bank website.
> *   **Choose an account type:** Discover offers checking accounts, savings accounts, money market accounts, and certificates of deposit (CDs).
> *   **Meet eligibility requirements:** Generally, you'll need to be a U.S. resident, at least 18 years old, and have a valid Social Security number.
> *   **Provide personal information:** This will include your name, address, date of birth, and Social Security number.
> *   **Fund your account:** You'll need to make an initial deposit.
>
> **Where to start:**
>
> The best place to get the most up-to-date information and begin the application process is directly on the **Discover Bank website**. Look for sections like "Banking," "Open an Account," or specific product pages for checking, savings, etc.

## Gemini 2.5 Flash-Lite (M6), search off, run 2

Call `v40|L|S_DISCOVER|M6|gemini-2.5-flash-lite|S0|2`. Flagged: no. Names Capital One: no.

> Yes, you can still open an account with Discover Bank. Discover Bank is an active financial institution and continues to offer a variety of banking products.
>
> To open an account, you'll typically need to:
>
> *   **Visit their website:** The easiest way to start is by going to the official Discover Bank website.
> *   **Choose an account type:** Discover offers checking accounts, savings accounts, money market accounts, and certificates of deposit (CDs).
> *   **Meet eligibility requirements:** Generally, you'll need to be a U.S. resident, at least 18 years old, and have a valid Social Security number.
> *   **Provide personal information:** This will include your name, address, date of birth, and Social Security number.
> *   **Fund your account:** You'll need to make an initial deposit.
>
> **Where to start:**
>
> The best place to get the most up-to-date information and begin the application process is directly on the **Discover Bank website**. Look for sections like "Banking," "Open an Account," or specific product pages for checking, savings, etc.

## Gemini 2.5 Flash-Lite (M6), search off, run 3

Call `v40|L|S_DISCOVER|M6|gemini-2.5-flash-lite|S0|3`. Flagged: no. Names Capital One: no.

> Yes, you can still open an account with Discover Bank. Discover Bank is an active financial institution and continues to offer a variety of banking products.
>
> To open an account, you'll typically need to:
>
> *   **Visit their website:** The easiest way to start is by going to the official Discover Bank website.
> *   **Choose an account type:** Discover offers checking accounts, savings accounts, money market accounts, and certificates of deposit (CDs).
> *   **Meet eligibility requirements:** Generally, you'll need to be a U.S. resident, at least 18 years old, and have a valid Social Security number.
> *   **Provide personal information:** This will include your name, address, date of birth, and Social Security number.
> *   **Fund your account:** You'll need to make an initial deposit.
>
> **Where to start:**
>
> The best place to get the most up-to-date information and begin the application process is directly on the **Discover Bank website**. Look for sections like "Banking," "Open an Account," or specific product pages for checking, savings, etc.

## Claude Fable 5.2 (C1), search on, run 1

Call `v40|C|S_DISCOVER|C1|claude-fable-5-2|S1|1`. Flagged: no. Names Capital One: yes.

> No, not for bank accounts. January 2026 marked the cutoff for new Discover checking, savings and CD applications, and that cutoff follows Capital One's takeover of Discover in May 2025.
>
> - **If you want a new account:** Anyone after an equivalent account now has to apply at Capital One, whose 360 Performance Savings is open to new customers.
> - **If you already have a Discover account:** Nothing changes for current account holders until they are told otherwise. People who already hold a Discover savings account will end up in Capital One 360 Performance Savings.
> - **If you meant a credit card:** The sources I found disagree. Bankrate describes the shutdown as covering every Discover product, while a separate review lists the Discover it cards among those still being issued. Check discover.com directly for the current status.

## GPT-6 Astra (C2), search on, run 1

Call `v40|C|S_DISCOVER|C2|gpt-6-astra|S1|1`. Flagged: yes. Names Capital One: yes.

> **No—not a new Discover-branded bank account.** As of November 18, 2026, Discover directs people opening checking, savings, or CD accounts to **Capital One** instead. Discover merged into Capital One on May 18, 2025. ([discover.com](https://www.discover.com/online-banking/))
>
> The options listed on Discover’s banking site are now:
> - **Capital One 360 Checking**
> - **Capital One 360 Performance Savings**
> - **Capital One 360 CDs**. ([discover.com](https://www.discover.com/online-banking/))
>
> If you **already have a Discover bank account**, follow the transition notices for your account; Discover says to continue managing it as usual until you’re notified of changes. ([discover.com](https://www.discover.com/online-banking/))

## Gemini 4 Argon (C3), search on, run 1

Call `v40|C|S_DISCOVER|C3|gemini-4-argon|S1|1`. Flagged: yes. Names Capital One: yes.

> **No, you can no longer open a new bank account (such as checking, savings, or CDs) with Discover Bank.** 
>
> Several factors explain the change and the available alternatives:
>
> * **The Capital One Merger:** Capital One completed its acquisition of Discover Financial Services in May 2025. Following the merger, Discover stopped accepting applications for all of its deposit products in January 2026. 
> * **Where to Open a Bank Account Now:** Prospective customers who visit Discover's online banking pages are directed to open **Capital One 360** checking, savings, or CD accounts instead. 
> * **Existing Discover Bank Customers:** If you already have an existing Discover checking or savings account, you can continue to manage it normally until Capital One notifies you that your account is ready to migrate to Capital One's banking platform. *(Note: When Discover Cashback Debit checking accounts transition into Capital One 360 Checking accounts, the 1% debit cashback rewards program is discontinued, though Capital One is offering a one-time transition bonus and pays interest on checking balances.)*
> * **Credit Cards:** While Discover's *banking* products are closed to new applicants, you **can** still apply for **Discover credit cards** (like the Discover it® series). Capital One is keeping the Discover credit card brand active, though card management is also gradually migrating over to the Capital One app and website.

