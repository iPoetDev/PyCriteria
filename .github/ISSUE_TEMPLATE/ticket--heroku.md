---
name: 'Ticket: Heroku'
about: 'Ticket: Heroku Level Impediments & Technical Issues'
title: "[Ticket] Heroku: "
labels: ''
assignees: iPoetDev

---

# Heroku Ticket: #

##### Pre-flight

- [ ] Have read the documentation: ⭐⭐⭐⭐⭐ of 5
- [ ] Have searched StackOverflow: ⭐⭐⭐⭐⭐ of 5
- [ ] Found most relevant topic: ⭐⭐⭐⭐⭐ of 5

## Current Config Checklist

### Account
- [ ]  MFA: Enabled: OTP ☑ | Device Factors ☑
- [ ]  API Key: Set ☑ | Not Regenerated 
- [ ]  SSH: No Key used ☑

### Managed Account 
- [ ]  Third Party Services: GitHub OAuth: Connected ☑ | Tested ☑ | No Issues ☑
- [ ]  API Authorisations: Heroku CLI: Connected ☑ | Login IP  ☑ | Logs ☑ | 
- [ ]  Apps Authorisations: 
                   Heroku Dashbord Intellij: Connected ☑ | Global ☑ | Plugin
                   Heroku WWW (Production):  Connected ☑ | Identity, Read ☑ | Logs ☑ | 

### Dashboard https://dashboard.heroku.com/apps

- Pipeline: deploy-auto ☑ | Staging ☑ | App: PyCriteria ☑ | Last Deploy: Deployed May 8 at 4:19 PM
- App: Pycriteria

#### Pipeline 
- No Add Ons
- Dyno formation: Eco Dynos | On | `web node index.js` ☑
- Collaborator: Deploy Count: 5
- Build: Succeed | Failed | Timestamp:  May 8 at 4:18 PM 
- Config Vars: Changed:  Yes | No | Intent: To Increase verbosity of logs
- Deploy: Method: GitHub
   GitHub-Heroku Flow: 
   1. Push to main branch on each commit
   2. Creates a Pull Request from/into deployment branch from main for reach release/deploy code
   3. Final Checks for Pull Request
   4. New code on deployment branch gets auto deployed to Heroku
- Automatic Deploys: Enabled ☑ | Does not wait for CI to pass ☑ | Branch: Heroku 
- Manual Deploy:  Branch: Heroku 
- Metrics: Not enabled
- Access: As per dashboard
- Settings: EU |  Stack: ****-22 | Framework: Node, Python, | Slug: 74.3/500 | 
- Config Vars: As per dashboard
- Buildpacks (in sequence): 1, Heroku/nodejs (standard) ☑ | 2, Heroku/python ☑
- SSL Certs: None
- Domains: None
- Maintenance Mode: On  | Off ☑
- Delete App: No ☑


## Ticket

- [ ] Category of Issue: 
  >> General Platform Features | Account Management |  Domains & Routing | Security | Billing | Heroku Postgres | Heroku Connect | Heroku Redis | Heroku Kafka, CI, Pipelines & Review apps | Platform Error Codes | Command Line Tools.
- [ ] Grants Read-only Access:  Date:  Time: 
  - [ ] Has Removed Read-only access: Date:  Time: 

### Summarize the issue clearly 

>

### Outline in detail.

>

- [ ] Category
- [ ] Application Type:
- [ ] Steps
- [ ] Screenshots
- [ ] Logs

#### Affected Application

> Application, Team, Pipeline, Add-on, Dyno, Logs

### Steps to reproduce
>> This could be a series of commands or a step-by-step walkthrough of the Dashboard

#### Screenshots
>> Any screen-shots of the issue, if available

## Application

- [ ] application is owned by a Team or Personal Heroku account
- [ ] IF issue is Pipeline-related, specify the name of the affected Pipeline
- [ ] IF issue is Add-on related, specify the components and/or applications that are affected
- [ ] ERROR CODES: 
      > https://devcenter.heroku.com/articles/error-codes

## Logs

```ruby

```

---

#### References

  i: Before Opening a Ticket: Read https://help.heroku.com/JYBXPRFN/before-opening-a-ticket
 ii: DevCenter: https://devcenter.heroku.com/
iii: Search by Keywords: https://help.heroku.com/
iv: Error Codes: https://devcenter.heroku.com/articles/error-codes

Category Issue Links
- [ ] General Platform Features: https://help.heroku.com/r?uri=https%3A%2F%2Fhelp.heroku.com%2Fn%2F236%2Fgeneral-platform-features
- [ ] Account Management: https://help.heroku.com/r?uri=https%3A%2F%2Fhelp.heroku.com%2Fn%2F5%2Faccount-management
- [ ] Domains & Routing: https://help.heroku.com/r?uri=https%3A%2F%2Fhelp.heroku.com%2Fn%2F8%2Fdomains-routing
- [ ] Security: https://help.heroku.com/r?uri=https%3A%2F%2Fhelp.heroku.com%2Fn%2F12%2Fsecurity
- [ ] Billing, Verification & Payments: https://help.heroku.com/r?uri=https%3A%2F%2Fhelp.heroku.com%2Fn%2F2%2Fbilling-verification-payments
- [ ] Heroku Postgres: https://help.heroku.com/r?uri=https%3A%2F%2Fhelp.heroku.com%2Fn%2F3%2Fheroku-postgres
- [ ] Heroku Connect: https://help.heroku.com/r?uri=https%3A%2F%2Fhelp.heroku.com%2Fn%2F10%2Fheroku-connect
- [ ] Heroku Redis: https://help.heroku.com/r?uri=https%3A%2F%2Fhelp.heroku.com%2Fn%2F22%2Fheroku-redis
- [ ]  Heroku Kafka: https://help.heroku.com/r?uri=https%3A%2F%2Fhelp.heroku.com%2Fn%2F21%2Fheroku-kafka
- [ ] CI, Pipelines & Review apps: https://help.heroku.com/r?uri=https%3A%2F%2Fhelp.heroku.com%2Fn%2F15%2Fci-pipelines-review-apps
- [ ] Platform Error Codes: https://help.heroku.com/r?uri=https%3A%2F%2Fhelp.heroku.com%2Fn%2F248%2Fplatform-error-codes
- [ ] Command Line Tools: https://help.heroku.com/r?uri=https%3A%2F%2Fhelp.heroku.com%2Fn%2F268%2Fcommand-line-tools
