import SwiftUI
import Foundation

// MARK: - Enums

enum AppMode { case active, off, weekend, lunch }
enum AppPanel { case main, settings }

// MARK: - Constants

let startHourChoices = Array(6...11)   // 6 AM – 11 AM
let endHourChoices   = Array(13...20)  // 1 PM – 8 PM
let intervalChoices  = [20, 30]
let workWeekdays     = 2...6           // Calendar.weekday: 2 = Mon, 6 = Fri

// MARK: - Prefs

struct Prefs: Codable {
    var startHour:       Int
    var endHour:         Int
    var intervalMinutes: Int

    static let `default` = Prefs(startHour: 9, endHour: 17, intervalMinutes: 20)

    static func load() -> Prefs {
        guard let data = try? Data(contentsOf: prefsURL),
              var p    = try? JSONDecoder().decode(Prefs.self, from: data)
        else { return .default }
        if !startHourChoices.contains(p.startHour)      { p.startHour = 9 }
        if !endHourChoices.contains(p.endHour)           { p.endHour   = 17 }
        if p.startHour >= p.endHour                      { p.startHour = 9; p.endHour = 17 }
        if !intervalChoices.contains(p.intervalMinutes)  { p.intervalMinutes = 20 }
        return p
    }

    func save() {
        guard let data = try? JSONEncoder().encode(self) else { return }
        try? data.write(to: Prefs.prefsURL, options: .atomic)
    }

    private static var prefsURL: URL { appDataDir().appendingPathComponent("prefs.json") }
}

// MARK: - Stats

struct Stats: Codable {
    var date:      String
    var completed: Int
    var ignored:   Int

    static func load(dayKey: String) -> Stats {
        guard let data = try? Data(contentsOf: statsURL),
              let s    = try? JSONDecoder().decode(Stats.self, from: data),
              s.date == dayKey
        else { return Stats(date: dayKey, completed: 0, ignored: 0) }
        return s
    }

    func save() {
        guard let data = try? JSONEncoder().encode(self) else { return }
        try? data.write(to: Stats.statsURL, options: .atomic)
    }

    private static var statsURL: URL { appDataDir().appendingPathComponent("stats.json") }
}

// MARK: - Data directory

func appDataDir() -> URL {
    let base = FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0]
    let dir  = base.appendingPathComponent("MoveReminder", isDirectory: true)
    try? FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)
    return dir
}

// MARK: - Time helpers

func slotIndex(date: Date, interval: Int) -> Int {
    let cal    = Calendar.current
    let hour   = cal.component(.hour,   from: date)
    let minute = cal.component(.minute, from: date)
    return (hour * 60 + minute) / max(1, interval)
}

func isMorningHalf(date: Date, start: Int, end: Int) -> Bool {
    let cal    = Calendar.current
    let hour   = cal.component(.hour,   from: date)
    let minute = cal.component(.minute, from: date)
    let mid    = Double(start) + Double(end - start) / 2.0
    return Double(hour) + Double(minute) / 60.0 < mid
}

// MARK: - Display helpers

func hourLabel(_ hour: Int) -> String {
    let suffix = hour < 12 ? "AM" : "PM"
    let h12    = hour % 12 == 0 ? 12 : hour % 12
    return "\(h12):00 \(suffix)"
}

func hoursLabel(start: Int, end: Int) -> String {
    "\(hourLabel(start)) – \(hourLabel(end))"
}

func tallyPep(completed: Int, ignored: Int) -> String {
    let total = completed + ignored
    guard total > 0 else {
        return "No prompts logged this shift — tomorrow is a fresh start."
    }
    let pct = 100.0 * Double(completed) / Double(total)
    switch pct {
    case ..<50:  return "Your tally was low, try to beat it tomorrow!"
    case ..<70:  return "Good job getting there!"
    case ..<80:  return "That was a strong day!"
    case ..<90:  return "Great day — keep stacking those wins!"
    case ..<100: return "Excellent work!"
    default:
        return "Congratulations! You worked hard to keep your health strong today! " +
               "Repeat tomorrow for a stronger body!"
    }
}

// MARK: - Rotation (seeded per-day shuffle)

func pickLine(_ lines: [String], slot: Int) -> String {
    guard !lines.isEmpty else { return "" }
    let today   = Calendar.current.startOfDay(for: Date())
    let ordinal = Calendar.current.ordinality(of: .day, in: .era, for: today) ?? 1
    var rng     = SeededGenerator(seed: UInt64(bitPattern: Int64(ordinal &+ lines.count)))
    var order   = lines
    order.shuffle(using: &rng)
    return order[slot % order.count]
}

struct SeededGenerator: RandomNumberGenerator {
    private var state: UInt64
    init(seed: UInt64) {
        // LCG — fast, uniform enough for shuffling exercise lists
        state = seed == 0 ? 6364136223846793005 : seed
    }
    mutating func next() -> UInt64 {
        state = state &* 6364136223846793005 &+ 1442695040888963407
        return state
    }
}

// MARK: - Color helper

/// Convenience for building SwiftUI Colors from 0–255 component values.
func rgb(_ r: Double, _ g: Double, _ b: Double) -> Color {
    Color(red: r / 255, green: g / 255, blue: b / 255)
}
