import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from vr_sim import render_simulation_html

# =========================================================
# LUNA BASE - BEYOND SURVIVAL
# Created by Team W.A.I.D.
# =========================================================

st.set_page_config(
    page_title="LUNA BASE | Beyond Survival",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# NASA SVS "Moon Phases" video used as the welcome-page background.
NASA_MOON_VIDEO_URL = (
    "https://svs.gsfc.nasa.gov/vis/a010000/a014900/a014992/"
    "Moon_Phases_Near_Far_Waning_720.mp4"
)

# =========================================================
# DESIGN
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #12345b 0%, transparent 35%),
        radial-gradient(circle at 90% 80%, #17234c 0%, transparent 35%),
        linear-gradient(135deg, #050b18, #101c35, #080d1b);
    color: white;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4 {
    color: white !important;
    font-weight: 800 !important;
}

p, li, label {
    color: #DCE8F5;
}

.hero {
    text-align: center;
    padding: 45px 20px;
    background: linear-gradient(145deg, #172B49, #101C35);
    border: 1px solid #2677A5;
    border-radius: 22px;
    margin-bottom: 25px;
}

.hero-title {
    font-size: 58px;
    font-weight: 900;
    letter-spacing: 5px;
    color: #FFFFFF;
}

.hero-subtitle {
    font-size: 22px;
    color: #00D4E8;
    font-weight: bold;
}

/* Video hero is used ONLY on the welcome screen. */
.lunar-video-hero {
    position: relative;
    width: 100%;
    height: 430px;
    overflow: hidden;
    border: 1px solid #2677A5;
    border-radius: 22px;
    margin-bottom: 25px;
    background: #050b18;
}

.lunar-video-hero video {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.lunar-video-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(
        90deg,
        rgba(3, 8, 20, 0.88) 0%,
        rgba(3, 8, 20, 0.55) 55%,
        rgba(3, 8, 20, 0.20) 100%
    );
}

.lunar-video-content {
    position: absolute;
    z-index: 2;
    left: 35px;
    right: 25px;
    bottom: 42px;
    color: white;
    text-align: left;
}

.lunar-video-title {
    color: #FFFFFF;
    font-size: clamp(38px, 6vw, 64px);
    font-weight: 900;
    letter-spacing: 5px;
    line-height: 1.1;
    margin: 0;
}

.lunar-video-subtitle {
    color: #00D4E8;
    font-size: clamp(16px, 2.5vw, 23px);
    font-weight: 800;
    letter-spacing: 2px;
    margin-top: 10px;
}

.lunar-video-description {
    color: #F0F5FA;
    font-size: 17px;
    margin-top: 18px;
}

.panel {
    background: linear-gradient(145deg, #172B49, #101C35);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #2677A5;
    margin-bottom: 18px;
}

.small-label {
    color: #00D4E8;
    letter-spacing: 3px;
    font-size: 12px;
    font-weight: bold;
}

.stButton > button {
    background: linear-gradient(90deg, #087CA7, #365DE8);
    color: white;
    border: 1px solid #36C9E5;
    border-radius: 12px;
    padding: 13px;
    font-weight: bold;
    width: 100%;
    min-height: 45px;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #00A6C7, #526FFF);
    color: white;
    border: 1px solid white;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #172B49, #101C35);
    padding: 15px;
    border-radius: 14px;
    border: 1px solid #2677A5;
}

[data-testid="stMetricValue"] {
    color: #00D4E8;
    font-weight: bold;
}

[data-testid="stMetricLabel"] {
    color: #DCE8F5;
}

.footer {
    text-align: center;
    color: #8EA9C4;
    margin-top: 45px;
    font-size: 13px;
}

@media (max-width: 600px) {
    .lunar-video-hero {
        height: 360px;
    }

    .lunar-video-content {
        left: 20px;
        right: 20px;
        bottom: 25px;
    }

    .lunar-video-title {
        letter-spacing: 2px;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# MISSION INFORMATION
#
# Each mission has ONE assigned activity per day.
# The number of activities matches the mission duration:
# Day 1 uses the first activity, Day 2 the second, and so on.
# Activity format: (name, resource effects, short description)
# =========================================================

missions = [
    {
        "name": "Establish the Lunar Base",
        "duration": 3,
        "level": "BEGINNER",
        "description": "Build the foundation of human life on the Moon.",
        "objective": "Establish a safe and functioning lunar base.",
        "fact": "The Moon has an extremely thin exosphere. Humans cannot breathe it, so astronauts need pressurised habitats and spacesuits.",
        "activities": [
            (
                "Inspect the habitat",
                {"health": 8, "power": -8},
                "Check the habitat structure and seals to make sure the crew is safe."
            ),
            (
                "Check life-support systems",
                {"oxygen": 10, "power": -10},
                "Test the systems that supply air and keep the habitat running."
            ),
            (
                "Organise food and water supplies",
                {"food": 10, "water": 10},
                "Sort and store supplies so the crew can use them efficiently."
            )
        ]
    },
    {
        "name": "Lunar Surface Exploration",
        "duration": 4,
        "level": "INTERMEDIATE",
        "description": "Explore the lunar landscape and collect scientific information.",
        "objective": "Explore the lunar surface and gather scientific data.",
        "fact": "The Moon's gravity is about one-sixth of Earth's gravity.",
        "activities": [
            (
                "Explore the lunar surface",
                {"science": 15, "oxygen": -10, "health": -3},
                "Leave the base in your spacesuits and survey the surrounding terrain."
            ),
            (
                "Collect lunar soil samples",
                {"science": 12, "power": -8},
                "Gather regolith samples for scientists to study back at base."
            ),
            (
                "Study rock formations",
                {"science": 10, "power": -5, "oxygen": -5},
                "Examine nearby rocks and craters to learn about the Moon's history."
            ),
            (
                "Return safely to base",
                {"health": 8, "oxygen": -5},
                "Bring the crew and the samples back to the habitat."
            )
        ]
    },
    {
        "name": "Search for Lunar Water",
        "duration": 5,
        "level": "INTERMEDIATE",
        "description": "Investigate possible water ice deposits near the lunar poles.",
        "objective": "Search for water ice and study its potential uses.",
        "fact": "NASA's SOFIA airborne observatory confirmed the presence of water molecules on the sunlit Moon in 2020.",
        "activities": [
            (
                "Travel to the polar region",
                {"power": -10, "oxygen": -5, "science": 5},
                "Drive the rover towards the lunar south pole, where water ice may be found."
            ),
            (
                "Scan a permanently shadowed crater",
                {"science": 15, "power": -12},
                "Use instruments to look for signs of ice in a crater that never sees sunlight."
            ),
            (
                "Collect ice samples",
                {"water": 12, "science": 10, "oxygen": -8},
                "Carefully collect samples of possible water ice."
            ),
            (
                "Analyse collected samples",
                {"science": 15, "power": -8},
                "Test the samples to learn how much water they contain."
            ),
            (
                "Return and store the water",
                {"water": 10, "health": 5},
                "Bring the samples home and add the water to the base supplies."
            )
        ]
    },
    {
        "name": "Restore Base Operations",
        "duration": 2,
        "level": "ADVANCED",
        "description": "Respond to technical problems and restore essential systems.",
        "objective": "Repair damaged equipment and protect the crew.",
        "fact": "Lunar surface temperatures can reach around 127°C in sunlight and drop to around -173°C in darkness.",
        "activities": [
            (
                "Repair electrical equipment",
                {"power": 15, "health": -3},
                "Find and fix the damaged equipment that is draining the base's power."
            ),
            (
                "Restore life-support systems and check crew health",
                {"oxygen": 15, "power": -10, "health": 10},
                "Bring life support back to full strength and make sure the crew is well."
            )
        ]
    },
    {
        "name": "Sustainable Lunar Settlement",
        "duration": 2,
        "level": "EXPERT",
        "description": "Prepare the base for long-term human settlement.",
        "objective": "Develop a sustainable lunar settlement.",
        "fact": "Water could potentially be processed to provide drinking water, oxygen and ingredients for rocket propellant.",
        "activities": [
            (
                "Develop water recycling",
                {"water": 15, "science": 10, "power": -8},
                "Build a system that cleans and reuses the base's water."
            ),
            (
                "Improve energy systems and plan the settlement",
                {"power": 15, "science": 15, "food": -5},
                "Upgrade the power supply and map out how people could live here long-term."
            )
        ]
    }
]


# Fun facts that pop up inside the simulation (one per day, cycling).
MISSION_FACTS = [
    [
        missions[0]["fact"],
        "A full day-night cycle on the Moon lasts about 29.5 Earth days, so sunlight can last around two weeks at a time.",
        "Moon dust is sharp and sticky because wind and water have never worn it smooth, so it can damage suits and equipment."
    ],
    [
        missions[1]["fact"],
        "The Moon is slowly drifting away from Earth at about 3.8 centimetres every year.",
        "From the near side of the Moon, Earth stays in almost the same spot in the sky because the Moon always shows us the same face.",
        "With almost no wind or rain on the Moon, footprints can last for a very long time."
    ],
    [
        missions[2]["fact"],
        "NASA's LCROSS mission found water in a permanently shadowed crater near the Moon's south pole in 2009.",
        "Some polar craters have been in permanent shadow for billions of years, which is why ice may survive there.",
        "Permanently shadowed craters are among the coldest places ever measured in the solar system.",
        "Water ice can be split into hydrogen and oxygen, which can be used for breathing and for rocket fuel."
    ],
    [
        missions[3]["fact"],
        "A lunar night lasts about two weeks, so bases need ways to store power or find sunlight."
    ],
    [
        missions[4]["fact"],
        "Some peaks near the lunar poles get sunlight almost all the time, which makes them promising places for solar power."
    ]
]

for _mission, _facts in zip(missions, MISSION_FACTS):
    _mission["facts"] = _facts

# What the player works on in the simulation for each activity.
ACTIVITY_TARGETS = {
    "Inspect the habitat": "habitat",
    "Check life-support systems": "console",
    "Organise food and water supplies": "supplies",
    "Explore the lunar surface": "flag",
    "Collect lunar soil samples": "soil",
    "Study rock formations": "rocks",
    "Return safely to base": "habitat",
    "Travel to the polar region": "rover",
    "Scan a permanently shadowed crater": "crater",
    "Collect ice samples": "ice",
    "Analyse collected samples": "lab",
    "Return and store the water": "recycler",
    "Repair electrical equipment": "powerbox",
    "Restore life-support systems and check crew health": "console",
    "Develop water recycling": "recycler",
    "Improve energy systems and plan the settlement": "solar",
}


# =========================================================
# EMERGENCIES - ONE DIFFERENT EMERGENCY PER MISSION
#
# Every emergency has three response options:
#   "reserve" - uses one emergency reserve
#   "power"   - needs enough electricity (power_cost)
#   "ignore"  - ignores the warning and suffers a penalty
# =========================================================

emergencies = [
    # MISSION 1 - Establish the Lunar Base
    {
        "title": "OXYGEN SYSTEM WARNING",
        "warning": (
            "A possible life-support problem has been detected. "
            "Oxygen production is dropping."
        ),
        "options": [
            {
                "label": "Use an emergency reserve",
                "kind": "reserve",
                "effects": {"oxygen": 15, "health": 5},
                "message": "Emergency oxygen reserve successfully used!"
            },
            {
                "label": "Repair the system using electricity",
                "kind": "power",
                "power_cost": 15,
                "effects": {"power": -15, "oxygen": 10, "health": 3},
                "message": "The oxygen system has been repaired!"
            },
            {
                "label": "Ignore the warning",
                "kind": "ignore",
                "effects": {"oxygen": -15, "health": -10},
                "message": "The warning was ignored. The crew has suffered a loss."
            }
        ]
    },
    # MISSION 2 - Lunar Surface Exploration
    {
        "title": "SOLAR RADIATION ALERT",
        "warning": (
            "A burst of solar particles has been detected while the crew "
            "is outside the base. Radiation levels are rising."
        ),
        "options": [
            {
                "label": "Use an emergency reserve (radiation shelter kit)",
                "kind": "reserve",
                "effects": {"health": 10},
                "message": "The crew sheltered safely using the emergency kit!"
            },
            {
                "label": "Retreat to base and power the radiation shield",
                "kind": "power",
                "power_cost": 15,
                "effects": {"power": -15, "health": 5},
                "message": "The crew is safe behind the radiation shield!"
            },
            {
                "label": "Keep working outside",
                "kind": "ignore",
                "effects": {"health": -20, "oxygen": -5},
                "message": "The crew was exposed to radiation and their health has dropped."
            }
        ]
    },
    # MISSION 3 - Search for Lunar Water
    {
        "title": "EXTREME COLD ALERT",
        "warning": (
            "Instruments and spacesuits are struggling in the permanently "
            "shadowed crater, where temperatures can drop extremely low."
        ),
        "options": [
            {
                "label": "Use an emergency reserve (spare heaters)",
                "kind": "reserve",
                "effects": {"power": 10, "health": 5},
                "message": "The spare heaters kept the crew and equipment warm!"
            },
            {
                "label": "Power the heating systems",
                "kind": "power",
                "power_cost": 15,
                "effects": {"power": -15, "health": 5, "science": 5},
                "message": "The heaters are working and the instruments are stable!"
            },
            {
                "label": "Continue without extra heating",
                "kind": "ignore",
                "effects": {"power": -10, "health": -12, "science": -10},
                "message": "The cold damaged equipment and some science data was lost."
            }
        ]
    },
    # MISSION 4 - Restore Base Operations
    {
        "title": "POWER GRID FAILURE",
        "warning": (
            "A fault in the electrical grid has shut down several "
            "base systems. Power is dropping fast."
        ),
        "options": [
            {
                "label": "Use an emergency reserve (backup battery)",
                "kind": "reserve",
                "effects": {"power": 20, "health": 3},
                "message": "The backup battery restored power to the base!"
            },
            {
                "label": "Restart the grid using remaining electricity",
                "kind": "power",
                "power_cost": 10,
                "effects": {"power": -10, "oxygen": 10, "water": 5},
                "message": "The grid has been restarted and key systems are back online!"
            },
            {
                "label": "Wait and hope it fixes itself",
                "kind": "ignore",
                "effects": {"power": -20, "oxygen": -10, "health": -5},
                "message": "The fault got worse and several systems lost power."
            }
        ]
    },
    # MISSION 5 - Sustainable Lunar Settlement
    {
        "title": "WATER RECYCLING FAILURE",
        "warning": (
            "The new water recycling system has developed a leak "
            "and precious water is being lost."
        ),
        "options": [
            {
                "label": "Use an emergency reserve (spare water supply)",
                "kind": "reserve",
                "effects": {"water": 15, "health": 5},
                "message": "The spare water supply covered the loss!"
            },
            {
                "label": "Repair the recycler using electricity",
                "kind": "power",
                "power_cost": 15,
                "effects": {"power": -15, "water": 12},
                "message": "The recycler has been repaired and the leak is sealed!"
            },
            {
                "label": "Ignore the warning",
                "kind": "ignore",
                "effects": {"water": -20, "health": -8},
                "message": "The leak continued and the base lost a lot of water."
            }
        ]
    }
]


# How each emergency looks in the simulation.
for _emergency, _hazard in zip(
    emergencies, ["oxygen", "radiation", "cold", "power", "water"]
):
    _emergency["hazard"] = _hazard


# =========================================================
# QUIZ QUESTIONS - FOUR PER MISSION
# =========================================================

quizzes = [
    [
        {
            "question": "Why do astronauts need spacesuits on the Moon?",
            "options": [
                "Because the Moon is too bright",
                "Because the Moon has no breathable atmosphere",
                "Because the Moon is too small",
                "Because gravity is too strong"
            ],
            "answer": 1,
            "explanation": "The Moon has an extremely thin exosphere. Astronauts need protection and oxygen."
        },
        {
            "question": "What is the main purpose of a lunar habitat?",
            "options": [
                "To provide astronauts with a safe living environment",
                "To make the Moon bigger",
                "To create sunlight",
                "To increase gravity"
            ],
            "answer": 0,
            "explanation": "A habitat provides shelter and supports essential life systems."
        },
        {
            "question": "Which resource is essential for human breathing?",
            "options": [
                "Electricity",
                "Food",
                "Oxygen",
                "Lunar soil"
            ],
            "answer": 2,
            "explanation": "Astronauts need oxygen to breathe and survive."
        },
        {
            "question": "Why must a lunar base monitor its resources?",
            "options": [
                "To decorate the base",
                "To make missions shorter",
                "To avoid using technology",
                "To ensure the crew has what it needs to survive"
            ],
            "answer": 3,
            "explanation": "Resources are limited, so they must be carefully monitored."
        }
    ],
    [
        {
            "question": "What is the Moon's gravity compared with Earth's?",
            "options": [
                "About the same",
                "About one-sixth",
                "Twice as strong",
                "Six times stronger"
            ],
            "answer": 1,
            "explanation": "The Moon's gravity is approximately one-sixth of Earth's."
        },
        {
            "question": "What is lunar regolith?",
            "options": [
                "A type of spacecraft",
                "A lunar storm",
                "Loose material covering the Moon's surface",
                "A type of astronaut food"
            ],
            "answer": 2,
            "explanation": "Regolith is the loose dust, soil and broken rock covering the lunar surface."
        },
        {
            "question": "Why do astronauts collect lunar soil samples?",
            "options": [
                "To study the Moon's composition and history",
                "To grow ordinary grass immediately",
                "To increase oxygen in space",
                "To create gravity"
            ],
            "answer": 0,
            "explanation": "Samples help scientists understand the Moon's composition and history."
        },
        {
            "question": "What should astronauts do after exploring the surface?",
            "options": [
                "Leave their equipment behind",
                "Ignore their oxygen levels",
                "Continue exploring without checking supplies",
                "Return safely and check their resources"
            ],
            "answer": 3,
            "explanation": "Astronauts must monitor their resources and return safely."
        }
    ],
    [
        {
            "question": "Where might water ice be preserved on the Moon?",
            "options": [
                "Inside the Sun",
                "In permanently shadowed polar craters",
                "On the Earth's surface",
                "Inside every lunar rock"
            ],
            "answer": 1,
            "explanation": "Some permanently shadowed lunar craters may preserve water ice."
        },
        {
            "question": "Which NASA observatory confirmed water molecules on the sunlit Moon in 2020?",
            "options": [
                "Hubble",
                "Voyager",
                "SOFIA",
                "Apollo 11"
            ],
            "answer": 2,
            "explanation": "NASA's SOFIA airborne observatory confirmed water molecules on the sunlit Moon."
        },
        {
            "question": "What could lunar water potentially be used to produce?",
            "options": [
                "Drinking water and oxygen",
                "Plastic trees",
                "Earth's oceans",
                "Sunlight"
            ],
            "answer": 0,
            "explanation": "Water could be processed for drinking, oxygen and potentially rocket propellant."
        },
        {
            "question": "Why is searching for lunar water important?",
            "options": [
                "It makes the Moon warmer",
                "It changes the Moon's orbit",
                "It removes all lunar dust",
                "It could support future human exploration"
            ],
            "answer": 3,
            "explanation": "Local water resources could help support longer missions and future settlements."
        }
    ],
    [
        {
            "question": "What should astronauts do when a critical life-support system fails?",
            "options": [
                "Ignore the warning",
                "Respond quickly and follow emergency procedures",
                "Switch off every system",
                "Leave the base immediately without a plan"
            ],
            "answer": 1,
            "explanation": "Life-support problems require quick and careful action."
        },
        {
            "question": "Why is electricity important in a lunar base?",
            "options": [
                "It increases the Moon's gravity",
                "It creates water from nothing",
                "It powers important equipment and systems",
                "It changes the weather"
            ],
            "answer": 2,
            "explanation": "Electricity supports equipment, communication and life-support systems."
        },
        {
            "question": "What can extreme lunar temperatures affect?",
            "options": [
                "Equipment and astronaut safety",
                "The number of stars",
                "The size of Earth",
                "The speed of sunlight"
            ],
            "answer": 0,
            "explanation": "Extreme temperatures can create serious challenges for equipment and crew."
        },
        {
            "question": "Why are emergency reserves useful?",
            "options": [
                "They make missions unnecessary",
                "They increase the number of astronauts",
                "They remove all risks",
                "They provide backup resources during emergencies"
            ],
            "answer": 3,
            "explanation": "Backup supplies help crews respond to unexpected problems."
        }
    ],
    [
        {
            "question": "What does a sustainable lunar settlement aim to achieve?",
            "options": [
                "Use all resources immediately",
                "Depend entirely on Earth forever",
                "Support people over a longer period",
                "Avoid scientific research"
            ],
            "answer": 2,
            "explanation": "Sustainability means supporting human activity over the long term."
        },
        {
            "question": "Why is recycling water important in space?",
            "options": [
                "It helps conserve limited supplies",
                "It makes the Moon bigger",
                "It increases sunlight",
                "It removes the need for oxygen"
            ],
            "answer": 0,
            "explanation": "Recycling helps reduce the amount of water that must be transported."
        },
        {
            "question": "What is one possible use of lunar soil?",
            "options": [
                "Creating Earth's atmosphere",
                "Changing the Moon's gravity",
                "Making oceans",
                "Researching future construction materials"
            ],
            "answer": 3,
            "explanation": "Scientists are investigating ways lunar material could support future construction."
        },
        {
            "question": "What is one major challenge of long-term lunar settlement?",
            "options": [
                "Too much breathable air",
                "Managing limited resources and protecting the crew",
                "Having too many oceans",
                "Avoiding all technology"
            ],
            "answer": 1,
            "explanation": "Long-term settlement requires reliable systems and careful resource management."
        }
    ]
]


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "page": "welcome",
    "completed_missions": [],
    "current_mission": 0,
    "day": 1,
    "oxygen": 80,
    "water": 80,
    "food": 80,
    "power": 80,
    "health": 100,
    "science": 0,
    "emergency_reserves": 2,
    "emergency_used": False,
    "emergency_result": None,
    "action_done": False,
    "mission_log": [],
    "quiz_answers": {},
    "quiz_score": 0,
    "last_quiz_score": 0,
    "quiz_passed": False,
    "failure_reason": "",
    "total_score": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def change_resource(resource, amount):
    current = st.session_state[resource]
    st.session_state[resource] = max(0, min(100, current + amount))


def apply_effects(effects):
    """Apply a dictionary of resource changes (science can't go below 0)."""
    for resource, amount in effects.items():
        if resource == "science":
            st.session_state.science = max(0, st.session_state.science + amount)
        else:
            change_resource(resource, amount)


def reset_mission():
    st.session_state.day = 1
    st.session_state.oxygen = 80
    st.session_state.water = 80
    st.session_state.food = 80
    st.session_state.power = 80
    st.session_state.health = 100
    st.session_state.science = 0
    st.session_state.emergency_reserves = 2
    st.session_state.emergency_used = False
    st.session_state.emergency_result = None
    st.session_state.action_done = False
    st.session_state.mission_log = []
    st.session_state.quiz_answers = {}
    st.session_state.quiz_score = 0
    st.session_state.quiz_passed = False
    st.session_state.failure_reason = ""


def mission_failed():
    if st.session_state.oxygen <= 0:
        return "Oxygen supplies have been depleted."

    if st.session_state.water <= 0:
        return "The crew has run out of water."

    if st.session_state.food <= 0:
        return "Food supplies have been depleted."

    if st.session_state.health <= 0:
        return "Crew health has reached a critical level."

    return None


def emergency_day(mission):
    """The day of the mission on which the emergency strikes."""
    return min(mission["duration"], max(2, (mission["duration"] + 2) // 2))


def todays_activity():
    """Return the activity automatically assigned to the current day."""
    mission = missions[st.session_state.current_mission]
    activities = mission["activities"]
    index = min(st.session_state.day - 1, len(activities) - 1)
    return activities[index]


def apply_activity():
    name, effects, _description = todays_activity()

    apply_effects(effects)

    # Daily resource consumption
    change_resource("oxygen", -5)
    change_resource("water", -4)
    change_resource("food", -4)
    change_resource("power", -3)

    st.session_state.mission_log.append(
        f"Day {st.session_state.day}: {name}"
    )

    st.session_state.action_done = True


def start_mission(number):
    reset_mission()
    st.session_state.current_mission = number
    st.session_state.page = "mission"


def complete_quiz():
    questions = quizzes[st.session_state.current_mission]
    score = 0

    for i, question in enumerate(questions):
        selected = st.session_state.quiz_answers.get(i)

        if selected == question["answer"]:
            score += 1

    st.session_state.quiz_score = score
    st.session_state.last_quiz_score = score

    if score >= 2:
        st.session_state.quiz_passed = True

        mission_number = st.session_state.current_mission + 1

        if mission_number not in st.session_state.completed_missions:
            st.session_state.completed_missions.append(mission_number)

        st.session_state.total_score += score

        st.session_state.page = "results"
    else:
        st.session_state.page = "quiz_results"


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div style="text-align:center; margin-bottom:15px;">
    <span class="small-label">W.A.I.D. PRESENTS</span>
</div>
""", unsafe_allow_html=True)


# =========================================================
# WELCOME PAGE
# Video background appears ONLY on this page.
# Uses the NASA video URL (or assets/lunar_background.mp4 if present).
# =========================================================

if st.session_state.page == "welcome":

    # NASA Scientific Visualization Studio video used as the background.
    video_source = NASA_MOON_VIDEO_URL

    # Optional: if you download the video to assets/lunar_background.mp4,
    # the app uses the local copy instead (more reliable without internet).
    video_path = Path("assets/lunar_background.mp4")

    if video_path.is_file():
        try:
            video_base64 = base64.b64encode(video_path.read_bytes()).decode("utf-8")
            video_source = f"data:video/mp4;base64,{video_base64}"
        except OSError:
            pass  # keep using the NASA URL

    # NOTE: the HTML is built as one string with no blank lines or indentation.
    # Markdown turns indented lines / lines after a blank line into a code block.
    hero_html = (
        '<div class="lunar-video-hero">'
        f'<video autoplay muted loop playsinline>'
        f'<source src="{video_source}" type="video/mp4"></video>'
        '<div class="lunar-video-overlay"></div>'
        '<div class="lunar-video-content">'
        '<div class="lunar-video-title">LUNA BASE</div>'
        '<div class="lunar-video-subtitle">BEYOND SURVIVAL. INTO THE UNKNOWN.</div>'
        '<div class="lunar-video-description">'
        'Your decisions. Your crew. Your mission.<br>'
        'Can you survive and build a future on the Moon?'
        '</div>'
        '</div>'
        '</div>'
    )

    st.markdown(hero_html, unsafe_allow_html=True)

    st.caption("Background video: NASA's Scientific Visualization Studio (svs.gsfc.nasa.gov).")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="panel">
            <h3>🧑‍🚀 SURVIVE</h3>
            <p>Protect your crew and manage essential resources.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="panel">
            <h3>🔬 EXPLORE</h3>
            <p>Discover the Moon and investigate scientific mysteries.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="panel">
            <h3>🧠 LEARN</h3>
            <p>Test your knowledge through interactive mission quizzes.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Your mission starts here.")

    if st.button("🚀 START YOUR ADVENTURE"):
        st.session_state.page = "selection"
        st.rerun()

    if st.button("📖 HOW TO PLAY"):
        st.session_state.page = "instructions"
        st.rerun()


# =========================================================
# INSTRUCTIONS PAGE
# =========================================================

elif st.session_state.page == "instructions":

    st.title("📖 HOW TO PLAY")

    st.markdown("""
    <div class="panel">
        <h3>Welcome, Commander!</h3>

        Your job is to complete five lunar missions.

        <br><br>

        <b>1. Choose your mission</b><br>
        Start with Mission 01. Complete missions to unlock the next ones.

        <br><br>

        <b>2. Manage your resources</b><br>
        Monitor oxygen, water, food, electricity and crew health.

        <br><br>

        <b>3. Put on your visor</b><br>
        You are on the Moon in first person. Drag (or use the arrow keys)
        to look around. Aim the circle at the glowing TASK marker and hold
        it there to perform today's activity, then press the button below
        the simulation. Tap 🥽 VR MODE to use a phone VR headset.

        <br><br>

        <b>4. Fix the emergency</b><br>
        Every mission has a different emergency. Find the flashing fault,
        then choose how your crew will respond.

        <br><br>

        <b>5. Complete the quiz</b><br>
        Each mission has four questions. You need at least two correct answers to pass.

        <br><br>

        <b>6. Complete all five missions</b><br>
        Your final goal is to establish a sustainable lunar settlement.
    </div>
    """, unsafe_allow_html=True)

    st.info(
        "Remember: Your resources are limited. "
        "Every decision can affect your mission."
    )

    if st.button("🚀 LET'S GO"):
        st.session_state.page = "selection"
        st.rerun()

    if st.button("⬅ BACK"):
        st.session_state.page = "welcome"
        st.rerun()


# =========================================================
# MISSION SELECTION
# =========================================================

elif st.session_state.page == "selection":

    st.title("🚀 MISSION CONTROL")

    st.write("Choose your next mission, Commander.")

    completed = len(st.session_state.completed_missions)

    st.progress(completed / 5)

    st.write(f"MISSIONS COMPLETED: {completed}/5")

    for index, mission in enumerate(missions):

        mission_number = index + 1

        unlocked = (
            mission_number == 1
            or mission_number - 1 in st.session_state.completed_missions
        )

        done = mission_number in st.session_state.completed_missions

        st.markdown('<div class="panel">', unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(f"### MISSION 0{mission_number}")

            st.markdown(f"**{mission['name']}**")

            st.write(mission["description"])

            st.caption(
                f"LEVEL: {mission['level']} | "
                f"DURATION: {mission['duration']} DAYS"
            )

            if done:
                st.success("MISSION COMPLETED ✓")

            elif not unlocked:
                st.warning("🔒 COMPLETE THE PREVIOUS MISSION TO UNLOCK")

        with col2:

            if done:
                st.success("COMPLETED")

            elif unlocked:
                if st.button(
                    "START MISSION",
                    key=f"start_{mission_number}"
                ):
                    start_mission(index)
                    st.rerun()

            else:
                st.write("🔒 LOCKED")

        st.markdown('</div>', unsafe_allow_html=True)

    if completed == 5:
        st.success("🏆 ALL FIVE MISSIONS COMPLETED!")

        if st.button("VIEW FINAL ACHIEVEMENT"):
            st.session_state.page = "final"
            st.rerun()

    if st.button("⬅ MAIN MENU"):
        st.session_state.page = "welcome"
        st.rerun()


# =========================================================
# MISSION DASHBOARD
# =========================================================

elif st.session_state.page == "mission":

    mission = missions[st.session_state.current_mission]
    emergency = emergencies[st.session_state.current_mission]
    day = st.session_state.day
    em_day = emergency_day(mission)

    st.title(f"🌙 MISSION 0{st.session_state.current_mission + 1}")

    st.subheader(mission["name"])

    st.info(mission["objective"])

    st.markdown(f"### DAY {day} / {mission['duration']}")

    st.progress(day / mission["duration"])

    activity_name, _effects, activity_description = todays_activity()

    # Is today the emergency day, and where are we in it?
    emergency_active = (
        day == em_day
        and st.session_state.action_done
        and not st.session_state.emergency_used
    )
    emergency_resolved_today = (
        day == em_day and st.session_state.emergency_used
    )

    result = st.session_state.emergency_result

    if emergency_active:
        sim_phase = "emergency"
    elif emergency_resolved_today and result:
        sim_phase = "resolved_ok" if result["ok"] else "resolved_bad"
    else:
        sim_phase = "activity"

    sim_config = {
        "mission_number": st.session_state.current_mission + 1,
        "mission_name": mission["name"],
        "day": day,
        "duration": mission["duration"],
        "activity_name": activity_name,
        "target": ACTIVITY_TARGETS.get(activity_name, "console"),
        "done": bool(st.session_state.action_done),
        "resources": {
            "oxygen": st.session_state.oxygen,
            "water": st.session_state.water,
            "food": st.session_state.food,
            "power": st.session_state.power,
            "health": st.session_state.health,
        },
        "science": st.session_state.science,
        "reserves": st.session_state.emergency_reserves,
        "fact": mission["facts"][(day - 1) % len(mission["facts"])],
        "phase": sim_phase,
        "hazard": emergency["hazard"],
        "emergency_title": emergency["title"],
        "result_text": result["text"] if (result and emergency_resolved_today) else "",
    }

    # FIRST-PERSON SIMULATION (helmet visor view)

    components.html(render_simulation_html(sim_config), height=545)

    st.caption(
        "🥽 Drag (or use the arrow keys) to look around. Aim the circle at the "
        "glowing TASK marker and hold it there to perform the activity. "
        "Science facts are educational; resource values are simplified simulations."
    )

    # DAILY ACTIVITY - ASSIGNED AUTOMATICALLY

    st.markdown(
        f"""
        <div class="panel">
            <span class="small-label">TODAY'S ASSIGNED ACTIVITY</span>
            <h3>{activity_name}</h3>
            <p>{activity_description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.action_done:

        if st.button("COMPLETE TODAY'S ACTIVITY 🚀"):

            apply_activity()

            reason = mission_failed()

            if reason:
                st.session_state.failure_reason = reason
                st.session_state.page = "failed"

            st.rerun()

    else:
        st.success("Today's activity has been completed!")

    # EMERGENCY - STRIKES ON ONE DAY OF EACH MISSION, DIFFERENT EVERY TIME

    if emergency_active:

        st.markdown("---")
        st.markdown("## ⚠️ MISSION EMERGENCY CENTRE")

        st.warning(
            f"{emergency['title']}: {emergency['warning']} "
            "Find the flashing fault in the simulation, then choose how your crew will respond."
        )

        option_labels = [option["label"] for option in emergency["options"]]

        emergency_choice = st.radio(
            "What should the crew do?",
            option_labels,
            key=f"emergency_{st.session_state.current_mission}"
        )

        if st.button("CONFIRM EMERGENCY DECISION"):

            option = next(
                o for o in emergency["options"]
                if o["label"] == emergency_choice
            )

            if option["kind"] == "reserve":

                if st.session_state.emergency_reserves > 0:

                    st.session_state.emergency_reserves -= 1
                    apply_effects(option["effects"])

                    st.session_state.emergency_result = {
                        "ok": True,
                        "text": option["message"]
                    }

                else:
                    st.error("No emergency reserves are available.")
                    st.stop()

            elif option["kind"] == "power":

                if st.session_state.power >= option["power_cost"]:

                    apply_effects(option["effects"])

                    st.session_state.emergency_result = {
                        "ok": True,
                        "text": option["message"]
                    }

                else:
                    st.error(
                        "Not enough electricity! "
                        "The repair could not be completed."
                    )
                    st.stop()

            else:

                apply_effects(option["effects"])

                st.session_state.emergency_result = {
                    "ok": False,
                    "text": option["message"]
                }

            st.session_state.emergency_used = True

            reason = mission_failed()

            if reason:
                st.session_state.failure_reason = reason
                st.session_state.page = "failed"

            st.rerun()

    elif emergency_resolved_today and result:

        st.markdown("---")
        st.markdown("## ⚠️ MISSION EMERGENCY CENTRE")

        if result["ok"]:
            st.success(f"{emergency['title']}: {result['text']}")
        else:
            st.error(f"{emergency['title']}: {result['text']}")

    # DETAILED STATUS (the same numbers are shown on the visor)

    with st.expander("📊 DETAILED MISSION STATUS"):

        resource_columns = st.columns(5)

        resources = [
            ("🫁 OXYGEN", "oxygen"),
            ("💧 WATER", "water"),
            ("🍱 FOOD", "food"),
            ("⚡ POWER", "power"),
            ("❤️ CREW", "health")
        ]

        for column, (label, key) in zip(resource_columns, resources):

            with column:
                st.metric(label, f"{st.session_state[key]}%")
                st.progress(st.session_state[key] / 100)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("🔬 SCIENCE POINTS", st.session_state.science)

        with col2:
            st.metric(
                "🧰 EMERGENCY RESERVES",
                st.session_state.emergency_reserves
            )

    # END DAY (the emergency must be dealt with first)

    st.markdown("---")

    if st.session_state.action_done and not emergency_active:

        if st.session_state.day < mission["duration"]:

            if st.button("🌅 END DAY AND CONTINUE"):

                st.session_state.day += 1
                st.session_state.action_done = False

                st.rerun()

        else:

            if st.button("🧠 PROCEED TO MISSION QUIZ"):

                st.session_state.quiz_answers = {}
                st.session_state.page = "quiz"

                st.rerun()

    elif emergency_active:
        st.info("Deal with the emergency before ending the day.")

    if st.button("⬅ RETURN TO MISSION CONTROL"):

        st.session_state.page = "selection"
        st.rerun()


# =========================================================
# QUIZ PAGE
# =========================================================

elif st.session_state.page == "quiz":

    mission_number = st.session_state.current_mission

    mission = missions[mission_number]

    questions = quizzes[mission_number]

    st.title("🧠 MISSION KNOWLEDGE TEST")

    st.subheader(mission["name"])

    st.info(
        "Commander, it's time to test what you have learned. "
        "Answer all four questions."
    )

    st.progress(0)

    for i, question in enumerate(questions):

        st.markdown(
            f'<div class="panel"><b>QUESTION {i + 1} OF 4</b>',
            unsafe_allow_html=True
        )

        st.markdown(f"### {question['question']}")

        answer = st.radio(
            "Choose your answer:",
            question["options"],
            key=f"quiz_{mission_number}_{i}",
            index=None
        )

        if answer is not None:
            st.session_state.quiz_answers[i] = question["options"].index(answer)

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("PASS MARK: 2 OUT OF 4")

    if st.button("SUBMIT MY ANSWERS 🚀"):

        if len(st.session_state.quiz_answers) != 4:

            st.warning("Please answer all four questions first.")

        else:

            complete_quiz()
            st.rerun()

    if st.button("⬅ RETURN TO MISSION"):

        st.session_state.page = "mission"
        st.rerun()


# =========================================================
# QUIZ RESULTS - FAILED
# =========================================================

elif st.session_state.page == "quiz_results":

    st.title("📊 QUIZ RESULTS")

    st.error(
        f"You scored {st.session_state.last_quiz_score}/4."
    )

    st.write(
        "You need at least 2 correct answers to pass this mission."
    )

    st.markdown("### REVIEW YOUR ANSWERS")

    questions = quizzes[st.session_state.current_mission]

    for i, question in enumerate(questions):

        selected = st.session_state.quiz_answers.get(i)

        correct = question["answer"]

        if selected == correct:
            st.success(f"Question {i + 1}: Correct!")

        else:
            st.error(
                f"Question {i + 1}: "
                f"Correct answer: {question['options'][correct]}"
            )

        st.caption(question["explanation"])

    if st.button("🔄 TRY THE QUIZ AGAIN"):

        st.session_state.quiz_answers = {}
        st.session_state.page = "quiz"
        st.rerun()

    if st.button("RETURN TO MISSION CONTROL"):

        st.session_state.page = "selection"
        st.rerun()


# =========================================================
# MISSION RESULTS - PASSED
# =========================================================

elif st.session_state.page == "results":

    mission = missions[st.session_state.current_mission]

    st.balloons()

    st.title("🏆 MISSION COMPLETED!")

    st.success(
        f"Congratulations! You completed {mission['name']}."
    )

    st.markdown("""
    <div class="hero">
        <div style="font-size:55px;">🌙 🏆</div>
        <h1>MISSION SUCCESSFUL</h1>
        <p class="hero-subtitle">
            ANOTHER STEP TOWARDS A FUTURE ON THE MOON
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "QUIZ SCORE",
            f"{st.session_state.last_quiz_score}/4"
        )

    with col2:
        st.metric(
            "SCIENCE POINTS",
            st.session_state.science
        )

    with col3:
        st.metric(
            "MISSIONS COMPLETED",
            len(st.session_state.completed_missions)
        )

    st.markdown("### 📋 MISSION ACTIVITY LOG")

    for activity in st.session_state.mission_log:
        st.write("✅ " + activity)

    if len(st.session_state.completed_missions) == 5:

        st.success(
            "You have completed all five lunar missions!"
        )

        if st.button("🏆 VIEW FINAL ACHIEVEMENT"):

            st.session_state.page = "final"
            st.rerun()

    else:

        if st.button("🚀 CONTINUE TO NEXT MISSION"):

            st.session_state.page = "selection"
            st.rerun()

    if st.button("🏠 RETURN TO MAIN MENU"):

        st.session_state.page = "welcome"
        st.rerun()


# =========================================================
# MISSION FAILURE
# =========================================================

elif st.session_state.page == "failed":

    st.title("🚨 MISSION FAILURE")

    st.error(
        st.session_state.failure_reason
    )

    st.markdown("""
    <div class="hero">
        <div style="font-size:55px;">⚠️</div>
        <h1>MISSION COMPROMISED</h1>
        <p>
        Space exploration is challenging.
        Learn from your decisions and try again.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write(
        "Your crew's survival depends on careful resource management."
    )

    if st.button("🔄 RETRY MISSION"):

        start_mission(st.session_state.current_mission)
        st.rerun()

    if st.button("RETURN TO MISSION CONTROL"):

        st.session_state.page = "selection"
        st.rerun()


# =========================================================
# FINAL ACHIEVEMENT
# =========================================================

elif st.session_state.page == "final":

    st.balloons()

    st.title("🌍 BEYOND SURVIVAL")

    st.markdown("""
    <div class="hero">
        <div style="font-size:75px;">🌙 🚀 🏆</div>
        <div class="hero-title">MISSION ACCOMPLISHED</div>
        <div class="hero-subtitle">
            YOU HAVE HELPED BUILD A FUTURE ON THE MOON.
        </div>
        <br>
        <p>
        From establishing a lunar base to planning a
        sustainable settlement, you have completed
        the journey.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.metric(
        "TOTAL QUIZ POINTS",
        f"{st.session_state.total_score}/20"
    )

    st.metric(
        "MISSIONS COMPLETED",
        "5/5"
    )

    st.success(
        "Congratulations, Commander! "
        "The future of lunar exploration is in your hands."
    )

    if st.button("🔄 PLAY AGAIN"):

        st.session_state.completed_missions = []
        st.session_state.total_score = 0

        reset_mission()

        st.session_state.page = "welcome"

        st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    <hr>
    <b>LUNA BASE | BEYOND SURVIVAL</b><br>
    Developed by W.A.I.D. — Women in Artificial Intelligence Development<br>
    Exploring possibilities for the future of human space exploration 🚀
</div>
""", unsafe_allow_html=True)
