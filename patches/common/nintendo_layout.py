"""Nintendo-style pad: A on east, B on south, C on west only, and the menu
confirms with east."""


def patch(path, old, new):
    src = open(path).read()
    if src.count(old) != 1:
        raise SystemExit(f"nintendo_layout.py: expected one match in {path} for {old!r}")
    open(path, "w").write(src.replace(old, new))


patch("src/joystick_config.cpp", """	b.host_input.joy_button = SDL_CONTROLLER_BUTTON_A;
	b.button = GameTankButtons::P1_A;
	bindings.emplace_back(b);

	b.type = BindingTypes::JOYSTICK_BUTTON;
	b.host_input.joy_button = SDL_CONTROLLER_BUTTON_B;
	b.button = GameTankButtons::P1_B;
	bindings.emplace_back(b);

	b.type = BindingTypes::JOYSTICK_BUTTON;
	b.host_input.joy_button = SDL_CONTROLLER_BUTTON_X;
	b.button = GameTankButtons::P1_C;
	bindings.emplace_back(b);

	b.type = BindingTypes::JOYSTICK_BUTTON;
	b.host_input.joy_button = SDL_CONTROLLER_BUTTON_Y;
	b.button = GameTankButtons::P1_C;
	bindings.emplace_back(b);
""", """	b.host_input.joy_button = SDL_CONTROLLER_BUTTON_B;
	b.button = GameTankButtons::P1_A;
	bindings.emplace_back(b);

	b.type = BindingTypes::JOYSTICK_BUTTON;
	b.host_input.joy_button = SDL_CONTROLLER_BUTTON_A;
	b.button = GameTankButtons::P1_B;
	bindings.emplace_back(b);

	b.type = BindingTypes::JOYSTICK_BUTTON;
	b.host_input.joy_button = SDL_CONTROLLER_BUTTON_X;
	b.button = GameTankButtons::P1_C;
	bindings.emplace_back(b);
""")

patch("src/gte.cpp", """	io.ConfigFlags |= ImGuiConfigFlags_NavEnableGamepad;
""", """	io.ConfigFlags |= ImGuiConfigFlags_NavEnableGamepad;
	io.ConfigNavSwapGamepadButtons = true;
""")
