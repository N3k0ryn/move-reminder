import SwiftUI

struct SettingsView: View {
    @EnvironmentObject var vm: AppViewModel

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {

            // ── Title ─────────────────────────────────────────────────
            Text("Shift setup  ·  v\(APP_VERSION)")
                .font(.system(size: 12, weight: .bold))
                .foregroundStyle(Color(hex: "fff8e7"))
                .padding(.horizontal, 14)
                .padding(.top, 12)

            Spacer()

            // ── Start hour ────────────────────────────────────────────
            HStack {
                Text("Start  \(hourLabel(vm.draftStart))")
                    .font(.system(size: 13, weight: .bold))
                    .foregroundStyle(.white)
                Spacer()
                NudgeButton("−") { vm.nudgeStart(-1) }
                NudgeButton("+") { vm.nudgeStart(+1) }
            }
            .padding(.horizontal, 14)

            Spacer()

            // ── End hour ──────────────────────────────────────────────
            HStack {
                Text("End    \(hourLabel(vm.draftEnd))")
                    .font(.system(size: 13, weight: .bold))
                    .foregroundStyle(.white)
                Spacer()
                NudgeButton("−") { vm.nudgeEnd(-1) }
                NudgeButton("+") { vm.nudgeEnd(+1) }
            }
            .padding(.horizontal, 14)

            Spacer()

            // ── Interval ──────────────────────────────────────────────
            HStack {
                Text("Interval (min)")
                    .font(.system(size: 13, weight: .bold))
                    .foregroundStyle(.white)
                Spacer()
                IntervalButton(
                    label:    vm.draftInterval == 20 ? "• 20" : "20",
                    action:   { vm.setInterval(20) }
                )
                IntervalButton(
                    label:    vm.draftInterval == 30 ? "• 30" : "30",
                    action:   { vm.setInterval(30) }
                )
            }
            .padding(.horizontal, 14)

            Spacer()

            // ── Footer ────────────────────────────────────────────────
            HStack(alignment: .bottom) {
                Text(MADE_WITH)
                    .font(.system(size: 9))
                    .foregroundStyle(Color(hex: "ffe8c8"))
                Spacer()
                Button("Done") { vm.closeSettings() }
                    .font(.system(size: 12, weight: .bold))
                    .buttonStyle(TextButtonStyle())
            }
            .padding(.horizontal, 14)
            .padding(.bottom, 10)
        }
    }
}

// MARK: - Private sub-views

private struct NudgeButton: View {
    let label:  String
    let action: () -> Void
    init(_ label: String, action: @escaping () -> Void) {
        self.label  = label
        self.action = action
    }
    var body: some View {
        Button(label, action: action)
            .font(.system(size: 16, weight: .bold))
            .buttonStyle(TextButtonStyle())
    }
}

private struct IntervalButton: View {
    let label:  String
    let action: () -> Void
    var body: some View {
        Button(label, action: action)
            .font(.system(size: 12, weight: .bold))
            .buttonStyle(TextButtonStyle())
    }
}
