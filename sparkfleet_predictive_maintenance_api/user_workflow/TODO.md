# User Workflow - TODO

## Spec Reference
Functional Requirement #4: User Workflow

## Tasks

### Approval Workflow
- [ ] Implement summary approval interface
- [ ] Allow users to revise AI-generated summaries
- [ ] Track approval status and history
- [ ] Enable summary editing before distribution

### Distribution ("Send to Stakeholders")
- [ ] Create single-click distribution function
- [ ] Route to GitHub, Email, Slack, Calendar
- [ ] Track distribution status
- [ ] Handle distribution failures/retries

### Dashboard
- [ ] Build dashboard UI for meeting overview
- [ ] Display meetings needing follow-up
- [ ] Show recurring requests and patterns
- [ ] Implement decision-tracking view
- [ ] Add filtering and sorting capabilities

## Acceptance Criteria
- [ ] Users can approve or edit AI summary and action items before distribution
- [ ] 'Send to Stakeholders' function distributes to all configured channels
- [ ] Dashboard displays meetings needing follow-up with status and deadlines

## Dependencies
- SparkFleet UI framework
- Integration modules (GitHub, calendar, Slack, email)
