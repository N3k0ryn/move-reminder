import SwiftUI
import AppKit
import Combine

@main
struct MoveReminderApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate

    var body: some Scene {
        Settings { EmptyView() }
    }
}

// MARK: - AppDelegate

final class AppDelegate: NSObject, NSApplicationDelegate {
    private var panel: FloatingPanel?
    let viewModel = AppViewModel()
    private var cancellables = Set<AnyCancellable>()

    func applicationDidFinishLaunching(_ notification: Notification) {
        NSApp.setActivationPolicy(.accessory)
        createPanel()
        installKeyHandler()
    }

    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
        false
    }

    // MARK: Panel setup

    private func createPanel() {
        let w: CGFloat = 288
        let h: CGFloat = 216
        let screen = NSScreen.main ?? NSScreen.screens[0]
        let x = screen.frame.midX - w / 2
        let y = screen.visibleFrame.maxY - h
        let rect = NSRect(x: x, y: y, width: w, height: h)

        let p = FloatingPanel(contentRect: rect)
        p.contentView = NSHostingView(rootView: RootView().environmentObject(viewModel))
        p.orderFrontRegardless()
        panel = p

        viewModel.$panelHidden
            .receive(on: RunLoop.main)
            .sink { [weak self] hidden in
                if hidden {
                    self?.panel?.orderOut(nil)
                } else {
                    self?.panel?.orderFrontRegardless()
                }
            }
            .store(in: &cancellables)
    }

    // MARK: Global key handler

    private func installKeyHandler() {
        NSEvent.addLocalMonitorForEvents(matching: .keyDown) { [weak self] event in
            guard let self else { return event }
            let mods = event.modifierFlags.intersection(.deviceIndependentFlagsMask)
            if event.keyCode == 53 {                                   // Escape
                self.viewModel.onIgnore()
                return nil
            }
            if mods == .command,
               let ch = event.charactersIgnoringModifiers?.lowercased(),
               ch == "w" || ch == "h" {
                self.viewModel.onIgnore()
                return nil
            }
            return event
        }
    }
}
