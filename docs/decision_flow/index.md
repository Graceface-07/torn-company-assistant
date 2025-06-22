# 🧭 Which Company Is Right For You?

Answer a few quick questions and we’ll recommend the companies that best fit your playstyle, budget, and goals.

---

## 🎯 What’s your main motivation?

- [ ] Passive income with low effort  
- [ ] Boosting my gym stats  
- [ ] Gaining a unique job special  
- [ ] Progressing fast via education or hacking  
- [ ] Roleplay / social fun

---

## 💰 What’s your starting budget?

- [ ] Under $100 million  
- [ ] $100M–$500M  
- [ ] Over $500M

---

## 💼 How active do you want to be?

- [ ] Passive / minimal micromanagement  
- [ ] Somewhat involved  
- [ ] Hands-on with staff roles and star progression

---

## ⚙️ What perk appeals most?

- [ ] Energy regeneration  
- [ ] Gym/stat boosts  
- [ ] Intelligence/hacking perks  
- [ ] Travel or vehicle efficiency  
- [ ] Crime or revive synergy

---

## 🎁 Want a job special?

- [ ] Yes — must match my perk  
- [ ] Yes — helpful even if unrelated  
- [ ] Not important

---

Once the assistant module is wired up, users will click **[Get My Recommendations]** and it’ll call the script.

---

### 🔁 2. `filters.yml`

This maps user choices to tag filters (to match `companies.yaml` tags):

```yaml
budget:
  Under $100 million: low_budget
  $100M–$500M: mid_budget
  Over $500M: high_budget

motivation:
  Passive income with low effort: passive_friendly
  Boosting my gym stats: stat_boost
  Gaining a unique job special: job_special
  Progressing fast via education or hacking: edu_synergy
  Roleplay / social fun: roleplay

activity:
  Passive / minimal micromanagement: staff_light
  Somewhat involved: moderate_staffing
  Hands-on: staff_heavy

perks:
  Energy regeneration: energy_gain
  Gym/stat boosts: gym_synergy
  Intelligence/hacking perks: hacking_ready
  Travel or vehicle efficiency: travel_synergy
  Crime or revive synergy: crime_helper

job_special:
  Yes — must match my perk: job_special_supports_perk
  Yes — helpful even if unrelated: has_job_special
  Not important: no_job_special
