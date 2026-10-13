import SwiftUI

// MARK: - Root (gradient shell + panel switch)

struct RootView: View {
    @EnvironmentObject var vm: AppViewModel

    var body: some View {
        ZStack {
            LinearGradient(
                colors: [vm.gradientTop, vm.gradientBottom],
                startPoint: .top,
                endPoint: .bottom
            )
            .ignoresSafeArea()

            if vm.activePanel == .main {
                MainView()
            } else {
                SettingsView()
            }
        }
        .frame(width: 288, height: 216)
        .clipShape(RoundedRectangle(cornerRadius: 10, style: .continuous))
    }
}

// MARK: - Main panel

struct MainView: View {
    @EnvironmentObject var vm: AppViewModel

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {

            // ── Header row ───────────────────────────────────────────
            HStack(alignment: .top, spacing: 0) {
                Text(vm.titleLine)
                    .font(.system(size: 11, weight: .bold))
                    .foregroundStyle(Color(hex: "fff8e7"))
                Spacer(minLength: 6)
                Button("Setup") { vm.openSettings() }
                    .buttonStyle(TextButtonStyle())
                    .font(.system(size: 11))
            }
            .padding(.horizontal, 14)
            .padding(.top, 12)

            Spacer(minLength: 0)

            // ── Clock ────────────────────────────────────────────────
            Text(vm.timeString)
                .font(.system(size: 26, weight: .bold))
                .foregroundStyle(.white)
                .padding(.horizontal, 14)

            // ── Date ─────────────────────────────────────────────────
            Text(vm.dateString)
                .font(.system(size: 12))
                .foregroundStyle(Color(hex: "ffe8c8"))
                .padding(.horizontal, 14)
                .padding(.top, 2)

            // ── Work hours (tap → settings) ──────────────────────────
            Text(vm.hoursLabel)
                .font(.system(size: 12))
                .foregroundStyle(Color(hex: "ffe8c8"))
                .padding(.horizontal, 14)
                .padding(.top, 1)
                .onTapGesture { vm.openSettings() }

            Spacer(minLength: 4)

            // ── Motivation ───────────────────────────────────────────
            Text(vm.motivationText)
                .font(.system(size: 11, weight: .bold))
                .foregroundStyle(Color(hex: "fff4d6"))
                .padding(.horizontal, 14)
                .lineLimit(2)
                .fixedSize(horizontal: false, vertical: true)

            Spacer(minLength: 4)

            // ── Reminder prompt ──────────────────────────────────────
            Text(vm.reminderText)
                .font(.system(size: 11, weight: .bold))
                .foregroundStyle(.white)
                .padding(.horizontal, 14)
                .lineLimit(3)
                .fixedSize(horizontal: false, vertical: true)

            // ── Action buttons ───────────────────────────────────────
            HStack(spacing: 0) {
                if !vm.isOnLunch {
                    Button("Completed") { vm.onCompleted() }
                        .buttonStyle(TextButtonStyle())
                    Button("Ignore") { vm.onIgnore() }
                        .buttonStyle(TextButtonStyle())
                }
                Button(vm.isOnLunch ? "Back" : "Lunch") { vm.toggleLunch() }
                    .buttonStyle(TextButtonStyle())
                Spacer(minLength: 0)
            }
            .padding(.horizontal, 10)
            .padding(.top, 4)
            .padding(.bottom, 10)
        }
    }
}

// MARK: - Button style

struct TextButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .foregroundStyle(Color(hex: "fff8e7"))
            .padding(.horizontal, 4)
            .padding(.vertical, 4)
            .contentShape(Rectangle())
            .opacity(configuration.isPressed ? 0.45 : 1.0)
    }
}

// MARK: - Color(hex:) extension

extension Color {
    /// Initialise from a 6-character hex string with or without a leading `#`.
    init(hex: String) {
        var s = hex.trimmingCharacters(in: .alphanumerics.inverted)
        if s.count == 6 { s = "FF" + s }  // inject full-opacity alpha
        var n: UInt64 = 0
        Scanner(string: s).scanHexInt64(&n)
        self.init(
            red:   Double((n >> 16) & 0xFF) / 255,
            green: Double((n >>  8) & 0xFF) / 255,
            blue:  Double( n        & 0xFF) / 255
        )
    }
}
