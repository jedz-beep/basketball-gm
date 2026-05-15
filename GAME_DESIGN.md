# Basketball GM — European Edition
## Master Game Design Document
### ⚠️ THIS FILE NEVER CHANGES — It is the permanent source of truth
### Version 2.0 — Design Lock (after full design conversation)

---

## Vision

A deep, realistic General Manager simulation for **professional basketball worldwide** —
with a strong emphasis on the European model that no game has captured until now.

Unlike NBA 2K MyGM, this game puts the full GM role at the center:
budgets, relationships, scouting, staff, contracts, and the human dynamics
that define whether a club succeeds or fails.

**There is no game like this for European basketball. This is the gap.**

---

## Core Design Pillars

1. **Depth over speed** — Every decision matters. No arcade shortcuts.
2. **European authenticity** — Real mechanics of European basketball management.
3. **You are the GM, not the coach** — Strategic decisions, not tactical ones.
4. **Relationships drive everything** — Owner, coach, players, staff, agents.
5. **Realistic consequences** — Financial collapse, relegation, being fired.
6. **Career progression** — Your reputation grows. Better clubs notice you.

---

## The GM Role — Exactly What You Do

### Your Responsibilities
- Negotiate and sign your own contract with the owner
- Set and manage the team roster (contracts, signings, releases, loans)
- Hire and fire the Head Coach and all support staff (including Head of Scouting)
- Manage annual budget with club ownership — stay within limits
- Define recruitment targets and communicate needs to Head of Scouting
- Negotiate player transfers and free agent signings (through agents)
- Manage relationships: owner, head coach, players, staff, media
- Manage youth academy (budget, staff, promotion decisions)
- Handle financial crises and board pressure

### What Belongs to the Head Coach (Not You)
- Match tactics and formations
- In-game substitutions
- Player rotation and minutes distribution
- Day-to-day training sessions

The GM sets the stage. The coach performs on it. Conflict between them
is one of the most interesting dynamics in the game.

---

## Player Data

**Players are fictional** (no real-name license needed at launch).
However, they are generated to feel real:
- Realistic name pools per nationality/region
- Attribute distributions based on real basketball archetypes
- Career trajectories that mirror real player development patterns
- Designed so a future real-data update is a data swap, not a rebuild

---

## World Leagues

All real-world professional basketball leagues are represented, each with
their own rules, salary structures, import limits, and prestige level.

### European Leagues (primary focus)
- EuroLeague (top European club competition)
- EuroCup, Basketball Champions League
- ACB (Spain), Lega Basket (Italy), BSL (Turkey), Jeep Elite (France)
- Liga Endesa, VTB United League, Bundesliga, Winner League (Israel)
- All national leagues with promotion/relegation

### NBA (North America)
- Full realistic mechanics (see NBA section below)
- Different GM experience: franchise model, no relegation

### Other Leagues
- Australia (NBL), South America, Asia Pacific
- Lower leagues in all European countries (needed for relegation)

**GM Reputation** determines which leagues and clubs are accessible at career start.
New GM → small club in lower division. Top GM → offers from elite clubs.

---

## Leagues: Rules Per Competition

Each league has its own:
- Import/foreign player limits (see below)
- Salary cap or budget ceiling (soft cap, hard cap, or none)
- Transfer window dates (Summer + January standard, varies)
- Contract length regulations
- Playoff format
- Relegation/promotion rules

---

## Foreign Player (Import) Limits

Every European league restricts the number of non-domestic players.
These limits are encoded per league and enforced in roster management.

Examples:
- Most leagues: 3–4 non-EU players in the active roster
- Some leagues: separate limits for non-EU vs EU foreigners
- EuroLeague: additional eligibility rules per competition

**This is a core resource constraint** — every signing decision is affected by import slots.

---

## NBA — Full Realistic Mechanics

### Salary Cap System
- Hard salary cap (unlike most European leagues)
- Luxury tax above the cap threshold
- Max contract values based on years of experience
- Exceptions: Mid-level exception, veteran minimum, rookie scale

### Draft System
- Annual NBA Draft (June) — two rounds
- Pre-draft: scout college and international prospects over the season
- Hidden attributes (potential, athleticism) revealed through scouting
- Draft pick trades — picks are assets, can be traded years in advance
- Lottery system for bottom-ranked teams

### Trade System
- Trade deadline (February) — active trading period
- Must match salaries within rules
- Trade proposals come from other GMs (AI) and can be initiated by you
- Player requested trades — agent calls you

### Other NBA-Specific Mechanics
- Rookie contracts and scale
- Player options and team options in contracts
- No-trade clauses
- Franchise relocation if club goes bankrupt (not dissolution)

---

## Time Progression — Hybrid System

Two buttons always available:

**"Next Day"** — Advance one calendar day. Used during:
- Transfer windows (every day can bring new offers)
- Pre-season (busy period)
- Any time you want full control

**"Next Event"** — Jump to the next important calendar item:
- Next match
- Transfer deadline
- Board meeting
- Contract expiry warning
- Agent call or staff request

Used in quiet mid-season periods to avoid clicking through empty days.

### Calendar Events (year-round)
- Pre-season (July–September): staff hiring, player signings, tour matches
- Season start (October): league begins
- November/January: EuroLeague/EuroCup windows
- January window: mid-season transfers
- International breaks: players called up by national teams
- Playoffs (April–May)
- Off-season (June): draft (NBA), contract renewals, free agency opens

---

## International Breaks and National Team Call-Ups

When national teams call up players for FIBA windows:
- Affected players leave for 2–3 weeks
- Impact on team: shorter rotation, tactical adjustments by coach
- Risk: injury risk increases during international duty
- Positive side: player returns with higher morale if national team performs well
- Development impact: young players called up develop faster

**This is not in your control** — but managing around it is part of the GM job.

---

## Starting the Game — Career Mode

Like Football Manager:
- Choose your GM profile (experience level, preferred regions, reputation)
- Choose a club from any available league
  - Top club: high budget, instant pressure, must win trophies
  - Mid-table club: stable, moderate expectations, room to grow
  - Small/struggling club: low budget, may have debt, chance to build something special
- Some clubs start with financial problems, internal conflicts, or a weak squad
- GM reputation unlocks better job offers over time

---

## GM Career Progression

### Reputation System
- Reputation score grows with achievements (trophies, financial stability, player development)
- High reputation → elite clubs offer you contracts mid-season or at season end
- Reputation takes damage from: being fired for poor results, financial scandals, public conflicts

### Career Events
- Other clubs can approach you (through your agent) with job offers
- You can resign and apply for open positions
- You can be fired (see Firing below)
- Retiring from management (end of career mode — optional)

### GM Contract
- At every new job, the owner offers a contract
- Negotiate terms: salary (personal), budget authority, transfer autonomy, length
- Stronger negotiating position = better contract terms
- Can trigger renegotiation mid-contract after major success

---

## Owner Relationships

### The 8 Owner Archetypes

Each owner is a blend of archetypes (e.g. 60% Trophy Hunter + 40% Prestige Seeker):

| Archetype | Primary Goal | Happy When | Angry When |
|-----------|-------------|------------|------------|
| **The Investor** | Club profitability | Revenue up, costs down | Financial losses |
| **The Trophy Hunter** | Trophies above all | Championships, deep runs | Any season without a trophy |
| **The Local Hero** | Community and local identity | Local players starting, fan love | Foreign-heavy roster, fan backlash |
| **The Talent Developer** | Sell players at a profit | High-fee player sales | Overpaying for aging stars |
| **The Prestige Seeker** | Fame and European glory | EuroLeague, famous signings | Stuck in lower leagues |
| **The Fan's Man** | Supporter relationship | Crowd atmosphere, fan satisfaction | Bad PR, fan protests |
| **The Hands-On** | Feels in control | Asked for input, consulted | Decisions made without him |
| **The Hands-Off** | Full GM autonomy | Leaves you alone | Any direct request |

### Owner Dynamic Factors (beyond archetypes)
- Personal relationship quality (trust, communication frequency)
- Whether owner sides with you or head coach in conflicts
- Whether owner respects financial discipline or wants to splash money
- Mood affected by: recent results, media attention, fan sentiment, financial performance

### Owner–GM–Coach Triangle
If GM and head coach conflict, the owner decides who stays.
Factors in that decision:
- Whose side is closer to owner's archetype
- Who has the better relationship with the owner
- Who has been at the club longer
- Recent results attribution (who gets credit or blame)

---

## Firing and Dismissal

You can be fired when:
- Results fall far short of seasonal objectives
- Financial mismanagement causes crisis
- Owner–GM relationship breaks down completely
- After a conflict with the coach that the owner resolves against you

After being fired:
- Garden leave period (paid, can't work elsewhere for X months per contract)
- Reputation takes a hit proportional to circumstances
- Other clubs' interest cools temporarily
- Can be re-hired: firing for impossible objectives ≠ career end

---

## Seasonal Objectives and Success Metrics

Owner sets at season start:
1. **Sporting objective** — League position target, cup progression, European qualification
2. **Financial objective** — Stay within budget, hit revenue targets, reduce debt
3. **Structural objective** — E.g. "Develop two youth players to first team", "Reduce average squad age"
4. **Hidden objective** — Depends on owner archetype (e.g. Prestige Seeker secretly wants EuroLeague even if not stated)

General success metrics (universal):
- Trophy wins (league, cups, European)
- Player development quality (scout finds who become stars)
- Financial health trajectory
- Youth academy output

---

## Head Coach Relationship

### Communication Options
- **Regular meetings** — Weekly check-in (morale, squad concerns, requests)
- **Tactical brief** — You inform coach of key targets, style preferences, priorities
- **Conflict resolution** — When coach is unhappy about squad or budget decisions
- **Crisis talks** — After poor run of results

### Coach Attributes
| Attribute | Description |
|-----------|-------------|
| Tactical Knowledge | System quality, adaptability |
| Player Development | How much players improve under him |
| Man-Management | Locker room harmony, morale effect |
| Rotation Philosophy | Does he use the full squad or only 8 players? |
| GM Relationship | Trust and alignment with your vision |
| Reputation | Affects ability to attract players |
| Ambition | Will he leave for a bigger club? |

### Coach Independence vs Compliance
High-reputation coaches: strong opinions, push back on your decisions
Low-reputation coaches: more compliant, risk of poor tactical output
Finding the right balance is part of the job.

---

## Playing Time Demands

When a player isn't getting enough minutes (coach's decision, not yours):
- Player becomes unhappy → morale drops
- Agent calls you to discuss the situation
- You can: talk to the player (calm him down short-term), talk to the coach (request more usage), arrange a loan, agree to sell

If unresolved: player asks to leave, public discontent, locker room tension.

---

## Locker Room Chemistry

Players have relationships with each other:
- Positive chemistry: boost in performance when playing together
- Negative relationships: cliques, arguments, public incidents
- Leadership hierarchy: veteran leaders stabilize the group

Chemistry factors:
- Nationality groups (players from same country bond)
- Personality clashes (star mentality vs team player)
- Minutes competition (two players at same position)
- Contract situation (player who wants to leave affects morale of others)

GM can intervene: team meetings, individual conversations, removing disruptive players.

---

## Agent System

Every player has an agent with their own personality:
- **The Pusher**: Always looking to maximize — calls often, demands more
- **The Loyal**: Prefers long-term deals, values stability
- **The Opportunist**: Open to all offers, plays clubs against each other
- **The Protector**: Fiercely guards client, hard to negotiate with

Agent interactions:
- Agent calls you to report client's interest in joining
- Agent presents contract demands in negotiations
- Agent accepts/rejects/counters your offers
- Agent threatens to pull client if you take too long

---

## Scouting System

### Department Structure
- GM hires a **Head of Scouting** (staff role, like head coach)
- Head of Scouting manages the scouting network and budget
- GM communicates needs: "I need a PG under 23 with high potential, European passport"
- Head of Scouting responds: "I need X budget and Y weeks to get you quality options"

### Head of Scouting Attributes
| Attribute | Description |
|-----------|-------------|
| Network Quality | How wide and deep their contacts are |
| Eye for Talent | Accuracy of potential assessment |
| Regional Specialization | Europe, Americas, Asia, etc. |
| Report Quality | How detailed and accurate their reports are |

### How Scouting Works
1. GM defines a player profile needed
2. Head of Scouting commits to a search (time + budget required)
3. Reports arrive over time — initially vague, more detail as scouting deepens
4. Hidden attributes (potential, consistency, professionalism) revealed gradually
5. Better Head of Scouting + more budget = faster and more accurate reports
6. Competing clubs may sign targets while you're still scouting

### Scouting Missions
- Can run multiple searches simultaneously (budget permitting)
- International scouting costs more but finds hidden gems
- Domestic scouting is cheaper and faster

---

## Youth Academy

### Full Deep System
Each club has a youth academy with multiple age groups (U16, U18, U21).

### GM Responsibilities for Academy
- Set academy budget (separate from first team)
- Hire academy director and youth coaches
- Define development philosophy ("develop and sell" vs "promote to first team")
- Decide which academy graduates to promote to senior squad

### How Academy Works
- Youth players develop over years based on: talent (hidden), coaching quality, training budget
- Academy results matter: wins/losses affect staff morale, board perception
- Best academy products can be sold for large fees (generates revenue)
- International breaks: national youth teams call up academy players
- Some owners place heavy value on academy output (local hero archetype)

### Youth Scouting
- Separate youth scouting budget
- Finding young talent (14–17 years old) and signing them to academy
- Long-term investment: results only visible years later

---

## Media and Communications

### Lightweight Media System
Not full press conferences — but periodic communication choices:

- After major events (big win, big loss, controversial signing, player conflict)
- Roughly once per month in normal periods
- Choose from 2–4 response options (professional, emotional, deflecting, honest)
- Affects: owner perception, fan sentiment, player morale, board confidence
- Very poor media handling can escalate situations unnecessarily

---

## Financial System

### Revenue Sources
| Source | Notes |
|--------|-------|
| Gate Receipts | Attendance × ticket price (affected by results + fan sentiment) |
| TV Rights | Share based on league position and market size |
| Sponsorships | Fixed + performance bonuses |
| European Cup Prize Money | Significant for EuroLeague/EuroCup participants |
| Player Transfers (sales) | Selling players at profit |
| Player Loans (fees received) | Loaning players out |
| Academy Sales | Selling developed youth players |

### Expenses
| Expense | Notes |
|---------|-------|
| Player Salaries | Largest cost, locked by contracts |
| Coaching and Staff Salaries | All staff combined |
| Scouting Department | Budget for search operations |
| Youth Academy | Separate budget allocation |
| Travel Costs | More away + European games = more cost |
| Medical and Fitness Staff | Affects injury recovery rates |
| Arena Operations | Fixed overhead |

---

## Financial Crisis — 4-Stage System

### Stage 1: 🟡 Warning
- Owner calls — budget has been exceeded
- Transfer budget frozen immediately
- Must present cost-reduction plan within the transfer window
- Relationships with owner takes damage

### Stage 2: 🟠 Crisis
- Mandatory player sales (the club needs cash)
- Cannot sign any new players
- Player wages may be deferred (affects morale)
- Coach and staff may ask about club stability

### Stage 3: 🔴 Seeking Investment
- Owner actively tries to sell the club
- A new buyer may appear — with a completely different owner archetype
- You may need to make the club attractive to potential buyers
- If new buyer comes: fresh start with their goals and personality

### Stage 4: ⚫ Bankruptcy
- No buyer found within a defined window
- Club enters administration
- Forced relegation one division below
- Some player contracts voided (players become free agents)
- Debts cleared — fresh start with minimal budget
- GM reputation takes major damage

### NBA Financial Specifics
- NBA owners are wealthier — bankruptcy almost never happens
- Instead: commissioner pressure, forced sale of franchise
- Extreme case: franchise **relocation** (team moves to a new city)
- Relocation is a unique event with major consequences for squad and fan relationships

---

## Contract System

| Field | Options |
|-------|---------|
| Length | 1–4 years (Europe), up to 5 years (NBA max) |
| Guarantee | Fully guaranteed / Partial / Non-guaranteed |
| Performance Bonuses | Minutes, scoring, awards, playoff appearances |
| Release Clause | Fixed fee that allows player to force exit |
| Buy-Out | Mutual agreement to terminate contract early |
| Player Option | Player decides at end of year X to extend or become FA |
| Team Option | Club decides at end of year X |
| No-Trade Clause | Player cannot be traded without consent (NBA) |
| Loan Agreement | Temporary transfer, fees and wages split per agreement |

---

## Relegation and Promotion

- Bottom 1–3 teams in each domestic league are relegated to the division below
- Top 1–2 teams in each lower division are promoted
- Playoff system in some leagues (play-offs for promotion/relegation)
- If relegated: budget typically drops, player contracts may have release clauses triggered
- If promoted: budget increases, must compete in harder league, attract new players

---

## Player Development

### Attribute Changes Over Time
- Young players (under 23) develop faster with:
  - High work ethic (hidden attribute)
  - Good coaching quality
  - Regular playing time
  - Not overloaded with internationals

- Peak players (25–29): stable, minor fluctuations
- Aging players (30+): gradual decline in athleticism (speed, vertical) while mental attributes may improve

### Development Boosts
- Loan to a club where they play regularly
- International call-ups (especially youth tournaments)
- Strong academy coaching
- High-quality Head Coach with good development attribute

---

## Injury System

- Injuries range from minor (1–3 days) to career-threatening (6–12 months)
- Factors affecting injury risk:
  - Overload (too many international breaks + heavy schedule)
  - Fitness staff quality
  - Player's age and physical attributes
  - Hidden professionalism attribute (how well they maintain their body)
- Medical staff quality affects recovery speed
- GM decisions that increase injury risk: insufficient squad depth, poor fitness staff

---

## UI and Visual Design

### Design Philosophy
- **Modern and clean** — not the heavy spreadsheet look of older management games
- **Data-rich but accessible** — all key numbers visible at a glance, no hunting through menus
- **Intuitive navigation** — a new player should find their way without a tutorial
- **Designed for handoff to Claude Design** after prototype — base code must be clean and well-structured

### Technical Requirements
- Dark and light theme support
- Bilingual: Hebrew (RTL) and English — full language toggle
- All key stats visible on main screens (no excessive sub-menus)
- Responsive layout (different screen sizes)

### UI Screens (Complete List)
| Screen | Purpose |
|--------|---------|
| Main Menu | New career, load game, settings, language toggle |
| Career Hub | Dashboard: next match, latest news, urgent actions |
| Roster Management | Full squad — sortable, filterable by position/age/contract |
| Player Profile | Full attributes, contract, history, scouting report, morale |
| Transfer Market | Free agents + available targets + loan market |
| Contract Negotiation | Offer builder + agent response and counter-offers |
| Staff Management | All staff — hire/fire/check attributes |
| Head Coach Interface | Communication, requests, alignment check |
| League Table & Schedule | Standings, upcoming fixtures, results |
| Match Result Screen | Score, box score, key events, player ratings |
| Finance Dashboard | Budget tracker, revenue, expenses, projections |
| Board / Objectives | Owner goals, satisfaction meter, relationship status |
| Scouting Hub | Active missions, reports, player radar |
| Youth Academy | Age groups, players, staff, results, promotions |
| Owner Relationship | Trust level, archetype, history of interactions |
| GM Profile | Career stats, reputation, contract, history |
| Job Market | Available positions, clubs approaching you |
| Draft Room | (NBA only) Board, picks, trades, live draft simulation |
| Financial Crisis Screen | Stage, options, time remaining |

---

## MVP — Version 1.0 Scope

Everything below MUST be complete before Version 1.0:

### Core Loop
- [ ] One league (configurable) with 10–16 teams
- [ ] Full season simulation (all games played)
- [ ] Hybrid time system (next day + next event)

### Player & Transfer
- [ ] Player transfer window (buy/sell/loan)
- [ ] Contract system with all fields
- [ ] Agent system (3 agent personality types)
- [ ] Playing time demand conversations
- [ ] Foreign player limit enforcement

### Staff & Coaching
- [ ] Coaching staff hire/fire
- [ ] Head coach communication system
- [ ] Head of scouting with request system
- [ ] Basic scouting missions (1–2 simultaneous)

### Finance
- [ ] Full budget system (revenue + expenses)
- [ ] Financial crisis stages 1–4

### Youth
- [ ] Youth academy with one age group (U21)
- [ ] Academy budget and director
- [ ] Player promotion to first team

### GM Career
- [ ] GM contract negotiation with owner
- [ ] Reputation score
- [ ] Being fired and finding new job
- [ ] Owner personality system (4 of 8 archetypes)

### UI
- [ ] All 19 screens built and functional
- [ ] Hebrew + English language toggle
- [ ] Save and load game

### Progression
- [ ] Relegation and promotion
- [ ] Player development over seasons (basic)

---

## Version 2.0 — Future Features (Do NOT build yet)

- All 8 owner archetypes fully implemented
- NBA full mode (draft, hard cap, max contracts, relocation)
- All world leagues (100+ leagues)
- Multiple simultaneous European competitions
- Deep injury system (specific injury types, rehab)
- Full player morale and happiness tracking
- Full press conference system
- Financial Fair Play / FIBA regulations
- Youth academy all age groups
- Real-time league news feed
- Rival club narratives
- GM personal life events (family, health)
- Multiplayer (GMs competing in same league)

---

## Game Feel Goals

The player should feel like:
- A real European basketball club GM — not a coach, not a player
- Every budget euro matters
- The owner is a real presence (helpful or threatening, depending on personality)
- Players are people with ambitions and agents representing them
- The coach is a real partner — or a growing conflict
- Building over multiple seasons is deeply rewarding
- Relegation feels like a disaster; promotion feels like a triumph
- The game rewards intelligence, patience, and relationship management

---

*Document version 2.0 — Frozen after full design conversation.*
*Do not edit this file. Any scope changes require explicit discussion and a new version.*
