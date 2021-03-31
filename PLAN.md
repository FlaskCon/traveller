### DATA

- [ ] Users
- * existing

- [ ] Conf
- title
- year /y/2021
- cfp start date
- cfp end date
- :: talks
- :: schedule

- [ ] Schedule
- :: sessions

- [ ] session
- talk id
- date
- start time
- end time

- [ ] talks
- title
- slug
- summary
- description
- accepted
- conf id
- :: talk proposal
- :: presenters

- [ ] presenters - bridge table
- talk id
- users

- [ ] talk proposal
- status (active, archived)
- talk id
- score
- ::reviewers

- [ ] reviewers - bridge table
- talkproposal id
- users

### VIEWS

- [ ] dashboard
- if reviewer: active proposals
- profile info
- submitted talks

- [ ] new talk


user:admin -> view:dashboard -> view:new conf -> 
user:speaker -> view:dashboard -> view:new talk
