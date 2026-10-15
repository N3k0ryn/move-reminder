import SwiftUI
import Combine

final class AppViewModel: ObservableObject {

    // MARK: - Published state (views read these)

    @Published private(set) var currentTime   = Date()
    @Published               var prefs:        Prefs
    @Published private(set) var stats:         Stats
    @Published               var isOnLunch     = false
    @Published               var activePanel   = AppPanel.main
    @Published private(set) var panelHidden    = false

    // Pre-computed display values, refreshed every tick
    @Published private(set) var reminderText   = ""
    @Published private(set) var motivationText = ""
    @Published private(set) var gradientTop    = Color.black
    @Published private(set) var gradientBottom = Color.black
    @Published private(set) var currentMode    = AppMode.off

    // Settings-panel draft values
    @Published var draftStart:    Int
    @Published var draftEnd:      Int
    @Published var draftInterval: Int

    // MARK: - Private

    private var hasGreeted = false
    private var hideSlot   = -1
    private var timer:       Timer?

    // MARK: - Init

    init() {
        let p         = Prefs.load()
        prefs         = p
        draftStart    = p.startHour
        draftEnd      = p.endHour
        draftInterval = p.intervalMinutes
        stats         = Stats.load(dayKey: Self.dayKey(Date()))
        startTimer()
    }

    deinit {
        timer?.invalidate()
        // Clear stats on quit instead of saving to disk
        stats = Stats(date: AppViewModel.dayKey(Date()), completed: 0, ignored: 0)
    }

    // MARK: - Timer

    private func startTimer() {
        let t = Timer(timeInterval: 0.25, repeats: true) { [weak self] _ in
            self?.tick()
        }
        RunLoop.main.add(t, forMode: .common)
        timer = t
        tick()  // populate immediately on launch
    }

    private func tick() {
        let now  = Date()
        currentTime = now
        ensureStatsDay(now)

        let slot = slotIndex(date: now, interval: prefs.intervalMinutes)
        let mode = computeMode(for: now)
        currentMode = mode

        updateDisplayText(now: now, mode: mode, slot: slot)

        let (top, bot) = palette(mode: mode, slot: slot)
        gradientTop    = top
        gradientBottom = bot

        // Auto-reveal at the start of a new interval
        if !isOnLunch && panelHidden && mode == .active && slot != hideSlot {
            panelHidden = false
        }
    }

    // MARK: - Display text

    private func updateDisplayText(now: Date, mode: AppMode, slot: Int) {
        let morning    = isMorningHalf(date: now, start: prefs.startHour, end: prefs.endHour)
        let motivLines = morning ? MORNING_MOTIVATIONS : AFTERNOON_MOTIVATIONS

        switch mode {
        case .weekend:
            reminderText   = pickLine(WEEKEND, slot: slot)
            motivationText = pickLine(motivLines, slot: slot)

        case .lunch:
            reminderText   = "Away on lunch — prompts are paused and will not count against you."
            motivationText = "Tap Back when you return"

        case .active:
            let reminders  = morning ? MORNING_REMINDERS : AFTERNOON_REMINDERS
            let period     = morning ? "Morning wakeup" : "Afternoon reset"
            reminderText   = "\(period): \(pickLine(reminders, slot: slot))"
            if !hasGreeted {
                hasGreeted     = true
                motivationText = morning ? "Good morning!" : "Good afternoon!"
            } else {
                motivationText = pickLine(motivLines, slot: slot)
            }

        case .off:
            let hour = Calendar.current.component(.hour, from: now)
            if hour >= prefs.endHour {
                let tally      = "Shift tally · \(stats.completed) completed · \(stats.ignored) ignored"
                reminderText   = tally
                motivationText = ""
            } else {
                reminderText   = pickLine(OFF_HOURS, slot: slot)
                motivationText = pickLine(motivLines, slot: slot)
            }
        }
    }

    // MARK: - Actions

    func onCompleted() {
        guard activePanel == .main else { return }
        if isWorkHours(date: currentTime) && !isOnLunch {
            stats.completed += 1
        }
        hideUntilNextSlot()
    }

    func onIgnore() {
        guard activePanel == .main else { return }
        if isWorkHours(date: currentTime) && !isOnLunch {
            stats.ignored += 1
        }
        hideUntilNextSlot()
    }

    func toggleLunch() {
        guard activePanel == .main else { return }
        isOnLunch.toggle()
        if isOnLunch && panelHidden { panelHidden = false }
    }

    func openSettings() {
        draftStart    = prefs.startHour
        draftEnd      = prefs.endHour
        draftInterval = prefs.intervalMinutes
        activePanel   = .settings
    }

    func closeSettings() {
        if draftStart < draftEnd {
            prefs = Prefs(startHour: draftStart, endHour: draftEnd, intervalMinutes: draftInterval)
            prefs.save()
        }
        activePanel = .main
    }

    func nudgeStart(_ delta: Int) {
        guard let idx = startHourChoices.firstIndex(of: draftStart) else { return }
        draftStart = startHourChoices[max(0, min(startHourChoices.count - 1, idx + delta))]
        if draftStart >= draftEnd {
            draftEnd = endHourChoices.first(where: { $0 > draftStart }) ?? endHourChoices.last!
        }
    }

    func nudgeEnd(_ delta: Int) {
        guard let idx = endHourChoices.firstIndex(of: draftEnd) else { return }
        draftEnd = endHourChoices[max(0, min(endHourChoices.count - 1, idx + delta))]
        if draftEnd <= draftStart {
            draftStart = startHourChoices.last(where: { $0 < draftEnd }) ?? startHourChoices.first!
        }
    }

    func setInterval(_ minutes: Int) { draftInterval = minutes }

    // MARK: - Computed display strings

    var timeString: String  { Self.timeFmt.string(from: currentTime) }
    var dateString: String  { Self.dateFmt.string(from: currentTime) }

    var tzLabel: String {
        TimeZone.current.abbreviation() ?? TimeZone.current.identifier
    }

    var shiftHoursLabel: String {
        hoursLabel(start: prefs.startHour, end: prefs.endHour)
    }

    var titleLine: String {
        var s = "\(APP_NAME)  ·  \(tzLabel)"
        if isOnLunch { s += "  ·  lunch" }
        return s
    }

    // MARK: - Private helpers

    private func ensureStatsDay(_ date: Date) {
        let key = Self.dayKey(date)
        if stats.date != key {
            stats      = Stats(date: key, completed: 0, ignored: 0)
            hasGreeted = false
        }
    }

    private func computeMode(for date: Date) -> AppMode {
        let weekday = Calendar.current.component(.weekday, from: date)
        guard workWeekdays.contains(weekday) else { return .weekend }
        if isOnLunch { return .lunch }
        return isWorkHours(date: date) ? .active : .off
    }

    private func isWorkHours(date: Date) -> Bool {
        let cal     = Calendar.current
        let weekday = cal.component(.weekday, from: date)
        let hour    = cal.component(.hour,    from: date)
        return workWeekdays.contains(weekday)
            && hour >= prefs.startHour
            && hour <  prefs.endHour
    }

    private func hideUntilNextSlot() {
        guard !panelHidden else { return }
        hideSlot    = slotIndex(date: currentTime, interval: prefs.intervalMinutes)
        panelHidden = true
    }

    private func palette(mode: AppMode, slot: Int) -> (Color, Color) {
        switch mode {
        case .active:  return ACTIVE_PALETTES[slot % ACTIVE_PALETTES.count]
        case .lunch:   return (rgb(40, 120, 90),  rgb(20, 50,  60))
        case .weekend: return (rgb(90, 40,  160), rgb(40, 140, 180))
        case .off:     return (rgb(50, 70,  110), rgb(30, 40,  70))
        }
    }

    static func dayKey(_ date: Date) -> String { dayFmt.string(from: date) }

    private static let timeFmt: DateFormatter = {
        let f = DateFormatter(); f.dateFormat = "h:mm:ss a"; return f
    }()
    private static let dateFmt: DateFormatter = {
        let f = DateFormatter(); f.dateFormat = "EEEE  ·  MMM d, yyyy"; return f
    }()
    private static let dayFmt: DateFormatter = {
        let f = DateFormatter(); f.dateFormat = "yyyy-MM-dd"; return f
    }()
}
