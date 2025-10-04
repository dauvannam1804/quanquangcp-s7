# Creating a Gmail Add-on

**Experiment Lab**  
- **Duration**: 45 minutes  
- **Credit**: 1  
- **Level**: Introductory  
- **Lab ID**: GSP249  

This lab may incorporate AI tools to support your learning.  

---

## Overview

Gmail add-ons automate tasks within Gmail, saving time and effort for users. Add-ons can examine incoming messages and act on them in various ways, such as:

- Displaying additional information in the Gmail UI.  
- Connecting to non-Google services to retrieve information or perform actions.  
- Providing interactive controls to allow users to send information to another service.  

**In this lab, you will create a Gmail Add-on that allows you to quickly change the labels of an email thread.**

---

## Setup and Requirements

### Before you start
- Labs are timed. Once you click **Start Lab**, the timer begins, and you cannot pause.  
- You will receive **temporary credentials** to sign in and use Gmail during this lab.  
- This lab runs in a **real cloud environment**.  

### What you need
- A standard web browser (Google Chrome recommended).  
- Sufficient time to complete the lab.  
- Use an **Incognito/Private window** to avoid conflicts between personal and student accounts.  

---

## Start the Lab and Sign in to Gmail

1. Click **Start Lab**.  
2. Open Gmail using the temporary credentials provided.  
   - Example:  
     - Username: `student-01-a07ba5915c28@qwiklabs.net`  
     - Password: `CvenMY8kW33l`  
3. Accept the terms if prompted.  
4. Gmail opens in your browser.  

---

## Task 1. Create the Script Project

1. Launch [Apps Script](https://script.google.com/) in a new tab.  
2. In the editor, open **Settings** and enable:  
   - *Show "appsscript.json" manifest file in editor*.  
3. Rename the project: **Gmail Add-on Quickstart**.  
4. Replace the content of `Code.gs` with the provided script.  

---

## Task 2. Update the Script Manifest

1. Open **appsscript.json** in the left menu.  
2. Replace its content with:

```json
{
  "oauthScopes": [
    "https://www.googleapis.com/auth/gmail.addons.execute",
    "https://www.googleapis.com/auth/gmail.addons.current.message.metadata",
    "https://www.googleapis.com/auth/gmail.modify"
  ],
  "gmail": {
    "name": "Gmail Add-on Quickstart - QuickLabels",
    "logoUrl": "https://www.gstatic.com/images/icons/material/system/1x/label_googblue_24dp.png",
    "contextualTriggers": [{
      "unconditional": {},
      "onTriggerFunction": "buildAddOn"
    }],
    "openLinkUrlPrefixes": [
      "https://mail.google.com/"
    ],
    "primaryColor": "#4285F4",
    "secondaryColor": "#4285F4"
  }
}
```

3. Save the project.  

---

## Task 3. Deploy the Add-on

1. In Apps Script, go to **Deploy > Test deployments**.  
2. For Application(s), choose **Gmail**, then click **Install**.  
3. Confirm by clicking **Done**.  
4. Open the Gmail add-on **Settings** tab to verify installation.  
   - If not visible, refresh Gmail and reinstall if necessary.  

---

## Task 4. Run the Add-on

1. Go back to Gmail and refresh.  
2. Open an email thread.  
3. Ensure the **right-side panel** is visible.  
4. Create labels:  
   - Create a label named **Test 1**.  
   - Create another named **Test 2**.  
5. Authorize the add-on:  
   - Click the add-on in the right-side panel.  
   - Select **Grant permission** → Choose the student account → **Allow**.  
   - If warned “app not verified,” click **Advanced > Go to Gmail Add-on Quickstart (unsafe)** → type **Continue** → Next.  

---

## Task 5. Use the Add-on

1. In the add-on menu, you should see **Test 1** and **Test 2** labels.  
2. Try these actions:  
   - Uncheck **Test 2** → it will be removed from the current thread.  
   - Check both **Test 1** and **Test 2** → both labels are applied.  
3. Verify changes by refreshing Gmail Inbox.  

---

## Congratulations 🎉

You successfully created and used a Gmail Add-on!  

With add-ons, you could also:  
- Show recent threads from a sender.  
- Translate emails instantly.  
- Integrate with other services.  

---

## Next Steps / Learn More

- Complete: **Google Apps Script: Access Google Sheets, Maps & Gmail in 4 Lines of Code**.  
- Learn more about Gmail Add-ons [here](https://developers.google.com/gmail/add-ons).  
- Explore Google Workspace Learning Center.  

---

## Google Cloud Training & Certification

Google Cloud training helps you master tools and best practices.  
- Courses from **fundamental to advanced levels**.  
- Options: **on-demand, live, virtual**.  
- Certifications validate your expertise.  

---

*Manual Last Updated: September 02, 2025*  
*Lab Last Tested: September 02, 2025*  

© 2025 Google LLC. Google and the Google logo are trademarks of Google LLC.  
Other company and product names may be trademarks of their respective owners.  
