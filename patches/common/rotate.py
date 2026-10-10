"""GTE_ROTATE=<degrees>: draw each frame, menu included, into a texture the
size of the rotated screen and turn it onto the panel."""

PATH = "src/gte.cpp"
src = open(PATH).read()


def replace(old, new):
    global src
    if src.count(old) != 1:
        raise SystemExit(f"rotate.py: expected one match for {old!r}")
    src = src.replace(old, new)


replace("void refreshScreen() {\n", """static int gteRotate = -1;
static SDL_Texture *gteRotateTarget = NULL;

static void gteRotateBegin(int *w, int *h) {
	if(gteRotate < 0) {
		const char *env = getenv("GTE_ROTATE");
		gteRotate = env ? atoi(env) % 360 : 0;
	}
	if(!gteRotate) {
		SDL_GetWindowSize(mainWindow, w, h);
		return;
	}
	SDL_GetRendererOutputSize(mainRenderer, w, h);
	if(gteRotate == 90 || gteRotate == 270) {
		int t = *w;
		*w = *h;
		*h = t;
	}
	if(!gteRotateTarget) {
		gteRotateTarget = SDL_CreateTexture(mainRenderer, SDL_PIXELFORMAT_RGB888, SDL_TEXTUREACCESS_TARGET, *w, *h);
	}
	SDL_SetRenderTarget(mainRenderer, gteRotateTarget);
}

static void gteRotateEnd() {
	if(!gteRotateTarget) return;
	int w, h, tw, th;
	SDL_SetRenderTarget(mainRenderer, NULL);
	SDL_GetRendererOutputSize(mainRenderer, &w, &h);
	SDL_QueryTexture(gteRotateTarget, NULL, NULL, &tw, &th);
	SDL_Rect dst = { (w - tw) / 2, (h - th) / 2, tw, th };
	SDL_RenderClear(mainRenderer);
	SDL_RenderCopyEx(mainRenderer, gteRotateTarget, NULL, &dst, gteRotate, NULL, SDL_FLIP_NONE);
}

void refreshScreen() {
""")

replace("""	src.h = GT_HEIGHT;
	SDL_GetWindowSize(mainWindow, &scr_w, &scr_h);
""", """	src.h = GT_HEIGHT;
	gteRotateBegin(&scr_w, &scr_h);
""")

replace("""    ImGui_ImplSDL2_NewFrame();
	ImGui::NewFrame();
	if(showMenu) {
""", """    ImGui_ImplSDL2_NewFrame();
	if(gteRotateTarget) {
		int tw, th;
		SDL_QueryTexture(gteRotateTarget, NULL, NULL, &tw, &th);
		ImGui::GetIO().DisplaySize = ImVec2((float) tw, (float) th);
		ImGui::GetIO().DisplayFramebufferScale = ImVec2(1.0f, 1.0f);
	}
	ImGui::NewFrame();
	if(showMenu) {
""")

replace("""	ImGui_ImplSDLRenderer2_RenderDrawData(ImGui::GetDrawData(), mainRenderer);
#endif
	SDL_RenderPresent(mainRenderer);
""", """	ImGui_ImplSDLRenderer2_RenderDrawData(ImGui::GetDrawData(), mainRenderer);
#endif
	gteRotateEnd();
	SDL_RenderPresent(mainRenderer);
""")

open(PATH, "w").write(src)
