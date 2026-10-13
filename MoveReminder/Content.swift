import SwiftUI

let APP_VERSION = "1.3.0"
let APP_NAME    = "Move Reminder"
let MADE_WITH   = "Made with Cursor ♥"

// MARK: - Exercise prompts

let MORNING_REMINDERS: [String] = [
    "Stand up: 10 air squats",
    "Chair squats - 10-12 reps",
    "Get that heart pumping! 20-30 jumping jacks!",
    "March in place for one minute",
    "High Knee March in place with Reach and Pull for 20 reps",
    "Get moving - jog in place 45 seconds",
    "Stand up butt kicks for 30 seconds",
    "Shadow boxing for 30 seconds",
    "Calf raises while you wait",
    "Wall sit for 20-30 seconds",
    "Standing side leg raises - 10 per leg",
    "Arm circle, big and small, 20 seconds of each",
    "Shake it out! Full body shake for 15 seconds",
    "Balance - Single leg stand, eyes closed - 15 seconds per side",
    "Reverse lunges - 10 per leg",
    "Standing hip circles - 10 each direction",
    "Wall push-ups - 10-15 reps",
    "Seated knee lifts - 30 seconds",
    "Desk plank hold - 20 seconds",
    "Standing torso rotations - 20 reps",
    "March with high knees for 30 seconds",
    "Quick stair climbs or step-ups - 1 minute",
    "Stand and reach for the ceiling, then side stretch - 5 each side",
    "Bodyweight squats to a chair and back up - 12 reps",
    "Arm pumps overhead for 30 seconds",
    "Nerd neck reset: chin tucks, 10 reps",
]

let AFTERNOON_REMINDERS: [String] = [
    "Desk push-ups or wall push-ups — 8–12",
    "Stretch: neck, shoulders, back, hips",
    "Drop a Plank for 20–30s",
    "Tricep dips off chair or floor - 8-10 reps",
    "On the floor: 12 Glute bridges",
    "Stretch, 10 Cat-cows",
    "Stretch, standing forward fold for 20 seconds",
    "Stretch, doorway chest stretch for 30 seconds",
    "Stretch, wrist and forearm stretch",
    "Stretch, 10 Ankle circles in each direction",
    "Stretch, standing spinal twist - 5 each side",
    "Balance, standing knee-to-elbow crunches - 10 per side",
    "Balance, bird dog - 10 each side",
    "Balance, side plank - 20 seconds per side",
    "Look out the window at something outside, aim for 20+ feet away (eye strain break)",
    "Toe touches for 10 each side",
    "Hip flexor stretch - 30 seconds per side",
    "Seated spinal twist - hold 20 seconds each side",
    "Spelunker stretch: reach one arm across your chest - 20s per side",
    "Shoulder rolls - 10 forward, 10 back",
    "Wrist circles and finger stretches - 30 seconds",
    "Neck stretches: ear to shoulder, 15 seconds each side",
    "Doorway pec stretch - 30 seconds per side",
    "Standing quad stretch - 20 seconds per leg",
    "Cross-body arm stretch - 20 seconds per arm",
    "Cat-camel stretch on the floor - 10 slow reps",
    "Hamstring stretch seated on a chair edge - 30 seconds",
    "Ankle alphabet: trace letters with each foot",
    "Deep squat hold (assisted if needed) - 20 seconds",
]

// MARK: - Motivations

let MORNING_MOTIVATIONS: [String] = [
    "A healthy body and mind keeps you grounded",
    "Have you hydrated?",
    "You are doing great!",
    "Remember you are the author of your life",
    "Small moves add up to a stronger you",
    "Show up for you — that's enough",
    "How are you feeling? Need to fill your water, get a snack?",
    "Everything you need to get it done is already inside of you",
    "Your wildest dream deserve a chance",
    "There's no such thing as the right time. Trust yourself and do it!",
    "Choose you. Every time.",
    "Your ending is still unwritten. It's never too late to create a life you love.",
    "Every day is a fresh start, a new opportunity to shine.",
    "Be confident in your abilities and trust yourself to succeed.",
    "You deserve to prioritize your well-being.",
]

let AFTERNOON_MOTIVATIONS: [String] = [
    "With every breath, release stress and inhale peace.",
    "Be kind to yourself in this hour.",
    "Unclench your jaw. Drop your shoulders.",
    "Progress, not perfection.",
    "Straighten up, your back will thank you.",
    "Sometimes letting go is the best way to free yourself.",
    "Drown out the fucking noise and keep doing you.",
    "The things that you say to yourself matter. Be kind.",
    "Ask yourself if it will matter in 10 years. If it won't, don't sweat it.",
    "Don't forget to celebrate the silent battles that you fought and won.",
    "No one else is dwelling on your mistakes. Move the fuck on.",
    "Tell the negative assholes in your head to sit in a corner for a lifelong timeout.",
    "Your best is more than enough, I promise.",
    "You are worthy of everything good in this life. Everything.",
    "Be a fucking weirdo. There's power in that.",
    "That thing you're self-conscious about is what makes you light up the fucking room.",
    "If you don't believe in yourself, how can you expect anyone else to?",
    "You are in control. You are in control. You are in control.",
    "Don't take anyone's shit. You are to be respected. Always.",
    "Your opinions aren't tattoos. You can change them any time.",
    "Be proud of who you are and all you have accomplished.",
]

// MARK: - Off-hours / weekend

let WEEKEND: [String] = [
    "Weekend — enjoy the rest; a short walk still counts",
    "If it is a showerless, stay in bed all day type of day, that's okay",
]

let OFF_HOURS: [String] = [
    "Off the clock — rest, hydrate, and move when it feels good",
    "Take some time to enjoy the things you worked hard for!",
]

// MARK: - Gradient palettes

let ACTIVE_PALETTES: [(Color, Color)] = [
    (rgb(255, 70,  50),  rgb(190, 20,  80)),
    (rgb(30,  190, 140), rgb(15,  70,  95)),
    (rgb(255, 170, 20),  rgb(200, 50,  30)),
    (rgb(90,  70,  255), rgb(40,  20,  140)),
    (rgb(40,  210, 255), rgb(20,  90,  160)),
    (rgb(255, 80,  170), rgb(90,  20,  90)),
    (rgb(120, 230, 50),  rgb(30,  100, 40)),
]
