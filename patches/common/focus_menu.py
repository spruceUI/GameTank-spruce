"""Opening the menu puts pad navigation straight into the main menu bar,
which upstream only reaches with ImGui's hold-X/Y windowing gesture."""


def patch(path, old, new):
    src = open(path).read()
    if src.count(old) != 1:
        raise SystemExit(f"focus_menu.py: expected one match in {path} for {old!r}")
    open(path, "w").write(src.replace(old, new))


patch("src/imgui/imgui.cpp", """#endif // #ifndef IMGUI_DISABLE
""", """void GteFocusMainMenuBar()
{
    ImGuiContext& g = *GImGui;
    ImGuiWindow* window = ImGui::FindWindowByName("##MainMenuBar");
    if (!window)
        return;
    ImGui::FocusWindow(window);
    g.NavInputSource = ImGuiInputSource_Gamepad;
    window->NavLastIds[ImGuiNavLayer_Menu] = 0;
    ImGui::NavRestoreLayer(ImGuiNavLayer_Menu);
    ImGui::SetNavCursorVisibleAfterMove();
}

#endif // #ifndef IMGUI_DISABLE
""")

patch("src/gte.cpp", """void refreshScreen() {
""", """void GteFocusMainMenuBar();

void refreshScreen() {
""")

patch("src/gte.cpp", """			ImGui::EndMainMenuBar();
		}
#else
""", """			ImGui::EndMainMenuBar();
			if(menuOpening) {
				GteFocusMainMenuBar();
				menuOpening = false;
			}
		}
#else
""")
