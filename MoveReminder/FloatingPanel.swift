import AppKit

/// A borderless, always-on-top panel that floats above all windows and spaces.
/// `isMovableByWindowBackground = true` lets the user drag it from any
/// non-interactive area; SwiftUI Buttons absorb their own clicks and do not
/// trigger a drag.
final class FloatingPanel: NSPanel {
    init(contentRect: NSRect) {
        super.init(
            contentRect: contentRect,
            styleMask: [.borderless, .nonactivatingPanel],
            backing: .buffered,
            defer: false
        )
        level                    = .floating
        collectionBehavior       = [.canJoinAllSpaces, .fullScreenAuxiliary,
                                    .stationary, .ignoresCycle]
        isOpaque                 = false
        backgroundColor          = .clear
        hasShadow                = true
        isMovableByWindowBackground = true
        isReleasedWhenClosed     = false
        alphaValue               = 0.97
    }

    override var canBecomeKey:  Bool { true  }
    override var canBecomeMain: Bool { false }
}
