"""Replace the desktop menu bar with a pad-driven pop-up, trimmed to what works
on a handheld. The game is paused and muted while it is open."""

PATH = "src/gte.cpp"
src = open(PATH).read()


def patch(old, new, count=1):
    global src
    if src.count(old) != count:
        raise SystemExit(f"handheld_menu.py: expected {count} match(es) for {old!r}")
    src = src.replace(old, new)


start = src.find("\t\tif(ImGui::BeginMainMenuBar()) {\n")
end_marker = "\t\t\tImGui::EndMainMenuBar();\n\t\t}\n#else\n"
end = src.find(end_marker)
if start < 0 or end < start:
    raise SystemExit("handheld_menu.py: menu bar block not found")

menu = """		ImGui::SetNextWindowPos(ImVec2(0, 0));
		ImGui::SetNextWindowSize(ImGui::GetIO().DisplaySize);
		ImGui::PushStyleVar(ImGuiStyleVar_WindowRounding, 0.0f);
		ImGui::PushStyleVar(ImGuiStyleVar_WindowPadding, ImVec2(0, 0));
		ImGui::PushStyleColor(ImGuiCol_WindowBg, ImVec4(0, 0, 0, 0.5f));
		ImGui::Begin("OverlayBackground", nullptr,
			ImGuiWindowFlags_NoDecoration |
			ImGuiWindowFlags_NoInputs |
			ImGuiWindowFlags_NoMove |
			ImGuiWindowFlags_NoBringToFrontOnFocus);
		ImGui::End();
		ImGui::PopStyleColor();
		ImGui::PopStyleVar(2);

		ImGui::SetNextWindowPos(ImVec2(20, 20), ImGuiCond_Always);
		ImGui::SetNextWindowBgAlpha(0.9f);
		if(!ImGui::IsAnyItemFocused()) {
			ImGui::SetNextWindowFocus();
		}
		menuOpening = false;
		ImGui::Begin("MainMenu", nullptr,
			ImGuiWindowFlags_AlwaysAutoResize |
			ImGuiWindowFlags_NoCollapse |
			ImGuiWindowFlags_NoMove |
			ImGuiWindowFlags_NoSavedSettings |
			ImGuiWindowFlags_NoTitleBar);
		ImGui::SetWindowFontScale(2.0f);
		if (ImGui::IsWindowAppearing())
			ImGui::SetKeyboardFocusHere(-1);

		if(ImGui::Selectable("Reset")) {
			resetQueued = 2;
			showMenu = false;
			setMenuMute(showMenu);
			joysticks->Reset();
		}
		ImGui::SliderInt("Volume", &AudioCoprocessor::singleton_acp_state->volume, 0, 256, "", ImGuiSliderFlags_NoInput);
		bool appMute = (muteMask & MUTE_SOURCE_MANUAL) != 0;
		ImGui::Checkbox("Mute Audio", &appMute);
		if(appMute) muteMask |= MUTE_SOURCE_MANUAL;
		else muteMask &= ~MUTE_SOURCE_MANUAL;
		AudioCoprocessor::singleton_acp_state->isMuted = (muteMask != 0);
		ImGui::Separator();
		if(ImGui::BeginMenu("Palette")) {
			ImGui::RadioButton("Unscaled Capture", &palette_select, PALETTE_SELECT_CAPTURE);
			ImGui::RadioButton("Full Contrast", &palette_select, PALETTE_SELECT_SCALED);
			ImGui::RadioButton("Cheap HDMI converter", &palette_select, PALETTE_SELECT_HDMI);
			ImGui::RadioButton("Flawed Theory (Legacy)", &palette_select, PALETTE_SELECT_OLD);
			ImGui::EndMenu();
		}
		if(ImGui::BeginMenu("Grid")) {
			ImGui::RadioButton("No grid", &grid_mode, GRID_NONE);
			ImGui::RadioButton("25% opacity", &grid_mode, GRID_25);
			ImGui::RadioButton("50% opacity", &grid_mode, GRID_50);
			ImGui::RadioButton("Full black grid", &grid_mode, GRID_FULL);
			ImGui::EndMenu();
		}
		ImGui::Checkbox("Instant Blits", &(blitter->instant_mode));
		if (ImGui::Checkbox("Joystick Paddle", &joystick_paddle_enabled)) {
			joysticks->SetHeldButtons(0);
		}
		if(ImGui::Selectable("Controllers")) {
			toggleControllerOptionsWindow();
		}
		ImGui::Separator();
		if(ImGui::Selectable("Exit")) {
			running = false;
		}
		ImGui::End();
"""
src = src[:start] + menu + src[end + len(end_marker) - len("#else\n"):]

patch("""#ifdef WRAPPER_MODE
	if(!paused && !showMenu) {
#else
	if(!paused) {
#endif
""", """	if(!paused && !showMenu) {
""")

patch("""	#ifdef WRAPPER_MODE
									setMenuMute(showMenu);
	#endif
""", """									setMenuMute(showMenu);
""", count=2)

open(PATH, "w").write(src)
