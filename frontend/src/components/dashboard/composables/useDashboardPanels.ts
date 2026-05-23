type DashboardPanelToggle = HTMLButtonElement;
type DashboardPanel = HTMLElement;

interface DashboardPanelOptions {
    desktopBreakpoint?: number;
    viewportPadding?: number;
}

const DEFAULT_DESKTOP_BREAKPOINT = 1180;
const DEFAULT_VIEWPORT_PADDING = 10;

export function useDashboardPanels(options: DashboardPanelOptions = {}) {
    const desktopBreakpoint = options.desktopBreakpoint ?? DEFAULT_DESKTOP_BREAKPOINT;
    const viewportPadding = options.viewportPadding ?? DEFAULT_VIEWPORT_PADDING;

    let toggles: DashboardPanelToggle[] = [];
    let panels: DashboardPanel[] = [];
    let activeName: string | null = null;
    let resizeHandler: EventListener | null = null;
    let scrollHandler: EventListener | null = null;

    function getToggleByName(name: string): DashboardPanelToggle | undefined {
        return toggles.find((button) => button.dataset.dashboardPanelToggle === name);
    }

    function getPanelByName(name: string): DashboardPanel | undefined {
        return panels.find((panel) => panel.dataset.dashboardPanel === name);
    }

    function closeAllPanels(): void {
        panels.forEach((panel) => {
            panel.classList.remove("is-open");
            panel.style.removeProperty("--panel-shift-x");
        });

        toggles.forEach((button) => {
            button.classList.remove("is-active");
            button.setAttribute("aria-expanded", "false");
        });

        document.querySelector(".teacher-dashboard-user")?.classList.remove("is-active");
        document.body.classList.remove("dashboard-panel-open");
        activeName = null;
    }

    function fitPanelIntoViewport(panel: DashboardPanel | undefined): void {
        if (!panel) {
            return;
        }

        panel.style.setProperty("--panel-shift-x", "0px");

        const rect = panel.getBoundingClientRect();
        let shiftX = 0;

        if (rect.right > window.innerWidth - viewportPadding) {
            shiftX -= rect.right - (window.innerWidth - viewportPadding);
        }

        if (rect.left < viewportPadding) {
            shiftX += viewportPadding - rect.left;
        }

        panel.style.setProperty("--panel-shift-x", `${Math.round(shiftX)}px`);
    }

    function fitActivePanel(): void {
        if (window.innerWidth <= desktopBreakpoint || !activeName) {
            return;
        }

        const panel = getPanelByName(activeName);

        if (!panel?.classList.contains("is-open")) {
            return;
        }

        fitPanelIntoViewport(panel);
    }

    function openPanel(name: string): void {
        const panel = getPanelByName(name);
        const toggle = getToggleByName(name);

        if (!panel || !toggle) {
            return;
        }

        closeAllPanels();
        panel.classList.add("is-open");
        toggle.classList.add("is-active");
        toggle.setAttribute("aria-expanded", "true");
        document.body.classList.add("dashboard-panel-open");
        activeName = name;

        if (window.innerWidth > desktopBreakpoint) {
            window.requestAnimationFrame(() => {
                fitPanelIntoViewport(panel);
            });
        }
    }

    function togglePanel(name: string): void {
        if (activeName === name) {
            closeAllPanels();
            return;
        }

        openPanel(name);
    }

    function onToggleClick(event: Event): void {
        const button = event.currentTarget as DashboardPanelToggle | null;
        const name = button?.dataset.dashboardPanelToggle;

        if (!name) {
            return;
        }

        event.preventDefault();
        event.stopPropagation();
        togglePanel(name);
    }

    function onDocumentClick(event: MouseEvent): void {
        const target = event.target;

        if (target instanceof Element && target.closest(".dashboard-header-control")) {
            return;
        }

        closeAllPanels();
    }

    function onEscape(event: KeyboardEvent): void {
        if (event.key === "Escape") {
            closeAllPanels();
        }
    }

    function init(): void {
        if (typeof document === "undefined") {
            return;
        }

        toggles = Array.from(document.querySelectorAll<DashboardPanelToggle>("[data-dashboard-panel-toggle]"));
        panels = Array.from(document.querySelectorAll<DashboardPanel>("[data-dashboard-panel]"));

        if (!toggles.length || !panels.length) {
            return;
        }

        toggles.forEach((button) => {
            button.addEventListener("click", onToggleClick);
        });

        resizeHandler = () => {
            fitActivePanel();
        };

        scrollHandler = () => {
            fitActivePanel();
        };

        document.addEventListener("click", onDocumentClick);
        document.addEventListener("keydown", onEscape);
        window.addEventListener("resize", resizeHandler);
        window.addEventListener("scroll", scrollHandler, true);
    }

    function destroy(): void {
        toggles.forEach((button) => {
            button.removeEventListener("click", onToggleClick);
        });

        if (typeof document !== "undefined") {
            document.removeEventListener("click", onDocumentClick);
            document.removeEventListener("keydown", onEscape);
            document.body.classList.remove("dashboard-panel-open");
        }

        if (resizeHandler) {
            window.removeEventListener("resize", resizeHandler);
        }

        if (scrollHandler) {
            window.removeEventListener("scroll", scrollHandler, true);
        }

        toggles = [];
        panels = [];
        resizeHandler = null;
        scrollHandler = null;
        activeName = null;
    }

    return {
        closeAllPanels,
        destroy,
        fitActivePanel,
        init,
        openPanel,
        togglePanel,
    };
}
