import { ref } from "vue";

interface DashboardSidebarOptions {
    desktopBreakpoint?: number;
    sidebarSelector?: string;
    overlaySelector?: string;
    toggleSelector?: string;
    topbarActionsSelector?: string;
}

const DEFAULT_DESKTOP_BREAKPOINT = 1180;

function queryOne<T extends HTMLElement>(selector: string): T | null {
    return document.querySelector<T>(selector);
}

export function useDashboardSidebar(options: DashboardSidebarOptions = {}) {
    const isSidebarOpen = ref(false);

    const desktopBreakpoint = options.desktopBreakpoint ?? DEFAULT_DESKTOP_BREAKPOINT;
    const sidebarSelector = options.sidebarSelector ?? "#dashboardSidebar, .dashboard-sidebar";
    const overlaySelector = options.overlaySelector ?? "#dashboardSidebarOverlay, .dashboard-sidebar-overlay";
    const toggleSelector = options.toggleSelector ?? "#dashboardMobileToggle, .dashboard-mobile-menu-btn, .dashboard-mobile-toggle";
    const topbarActionsSelector = options.topbarActionsSelector ?? ".teacher-dashboard-topbar-actions";

    let dashboardSidebar: HTMLElement | null = null;
    let dashboardSidebarOverlay: HTMLElement | null = null;
    let dashboardMobileToggle: HTMLButtonElement | null = null;
    let sidebarToggleHandler: EventListener | null = null;
    let sidebarOverlayHandler: EventListener | null = null;
    let resizeHandler: EventListener | null = null;
    let keydownHandler: EventListener | null = null;

    function syncSidebarState(isOpen: boolean): void {
        isSidebarOpen.value = isOpen;
    }

    function ensureSidebarToggleButton(): HTMLButtonElement | null {
        const existingButton = queryOne<HTMLButtonElement>(toggleSelector);

        if (existingButton) {
            return existingButton;
        }

        const topbarActions = queryOne<HTMLElement>(topbarActionsSelector);

        if (!topbarActions) {
            return null;
        }

        const button = document.createElement("button");
        button.id = "dashboardMobileToggle";
        button.type = "button";
        button.className = "dashboard-icon-btn dashboard-mobile-toggle";
        button.setAttribute("aria-label", "Открыть меню");
        button.innerHTML = '<i class="fas fa-bars"></i>';

        topbarActions.prepend(button);
        return button;
    }

    function setOverlayOpen(isOpen: boolean): void {
        dashboardSidebarOverlay?.classList.toggle("is-open", isOpen);
        dashboardSidebarOverlay?.classList.toggle("is-active", isOpen);
    }

    function openDashboardSidebar(): void {
        syncSidebarState(true);

        if (!dashboardSidebar || !dashboardSidebarOverlay) {
            return;
        }

        dashboardSidebar.classList.add("is-open");
        setOverlayOpen(true);
        document.body.classList.add("menu-open");
    }

    function closeDashboardSidebar(): void {
        syncSidebarState(false);

        if (!dashboardSidebar || !dashboardSidebarOverlay) {
            return;
        }

        dashboardSidebar.classList.remove("is-open");
        setOverlayOpen(false);
        document.body.classList.remove("menu-open");
    }

    function openSidebar(): void {
        openDashboardSidebar();
    }

    function closeSidebar(): void {
        closeDashboardSidebar();
    }

    function toggleSidebar(): void {
        if (isSidebarOpen.value) {
            closeSidebar();
            return;
        }

        openSidebar();
    }

    function init(): void {
        if (typeof document === "undefined") {
            return;
        }

        dashboardSidebar = queryOne<HTMLElement>(sidebarSelector);
        dashboardSidebarOverlay = queryOne<HTMLElement>(overlaySelector);
        dashboardMobileToggle = ensureSidebarToggleButton();

        if (!dashboardSidebar || !dashboardSidebarOverlay) {
            return;
        }

        closeDashboardSidebar();

        if (!dashboardMobileToggle) {
            return;
        }

        sidebarToggleHandler = () => {
            toggleSidebar();
        };

        sidebarOverlayHandler = () => {
            closeDashboardSidebar();
        };

        resizeHandler = () => {
            if (window.innerWidth > desktopBreakpoint) {
                closeDashboardSidebar();
            }
        };

        keydownHandler = (event: Event) => {
            if (event instanceof KeyboardEvent && event.key === "Escape") {
                closeDashboardSidebar();
            }
        };

        dashboardMobileToggle.addEventListener("click", sidebarToggleHandler);
        dashboardSidebarOverlay.addEventListener("click", sidebarOverlayHandler);
        window.addEventListener("resize", resizeHandler);
        document.addEventListener("keydown", keydownHandler);
    }

    function destroy(): void {
        if (dashboardMobileToggle && sidebarToggleHandler) {
            dashboardMobileToggle.removeEventListener("click", sidebarToggleHandler);
        }

        if (dashboardSidebarOverlay && sidebarOverlayHandler) {
            dashboardSidebarOverlay.removeEventListener("click", sidebarOverlayHandler);
        }

        if (resizeHandler) {
            window.removeEventListener("resize", resizeHandler);
        }

        if (keydownHandler && typeof document !== "undefined") {
            document.removeEventListener("keydown", keydownHandler);
        }

        if (typeof document !== "undefined") {
            document.body.classList.remove("menu-open");
        }

        syncSidebarState(false);

        dashboardSidebar = null;
        dashboardSidebarOverlay = null;
        dashboardMobileToggle = null;
        sidebarToggleHandler = null;
        sidebarOverlayHandler = null;
        resizeHandler = null;
        keydownHandler = null;
    }

    return {
        isSidebarOpen,
        closeSidebar,
        openSidebar,
        toggleSidebar,

        closeDashboardSidebar,
        destroy,
        init,
        openDashboardSidebar,
    };
}
