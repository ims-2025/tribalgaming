/* =========================================================
   TribalGaming.com — Production configuration
   Edit this ONE file with your service endpoints and every
   form across the site will start submitting for real.
   ========================================================= */

window.TG_CONFIG = {

  // -------- NEWSLETTER (Morning Brief) --------
  //
  // Pick ONE provider and fill in the id/url. Leave the others as-is.
  //
  // Option A · Buttondown (recommended — simplest, great for newsletters)
  //   1. Sign up at buttondown.email
  //   2. Find your username at Settings → Account
  //   3. Paste it here:
  newsletter: {
    provider: "none",                    // change to "buttondown", "mailchimp", or "convertkit" once configured
    buttondown: { username: "YOUR_BUTTONDOWN_USERNAME" },
    mailchimp:  { formAction: "https://YOUR_USER.usXX.list-manage.com/subscribe/post?u=XXXXX&id=XXXXX" },
    convertkit: { formId:     "YOUR_CONVERTKIT_FORM_ID" },
  },

  // -------- CONTACT FORM --------
  //
  // Formspree is the easiest (free plan: 50 submissions/month).
  //   1. Sign up at formspree.io
  //   2. Create a new form; copy the 8-character form ID
  //   3. Paste it here:
  contact: {
    provider: "none",                    // change to "formspree" once configured
    formspree: { formId: "YOUR_FORMSPREE_FORM_ID" },   // e.g. "xabczxyz"
  },

  // -------- ANALYTICS --------
  //
  // Pick ONE. Both include a privacy-friendly default (Plausible).
  analytics: {
    provider: "none",                    // change to "plausible" or "ga4" once configured
    plausible: { domain: "tribalgaming.com" },
    ga4:       { measurementId: "G-XXXXXXXXXX" },
  },

  // -------- SITE --------
  site: {
    url: "https://tribalgaming.com",
    name: "TribalGaming.com",
  },
};
