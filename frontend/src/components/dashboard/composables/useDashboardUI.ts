import { useDashboardMiniCalendar } from "@/components/dashboard/composables/useDashboardMiniCalendar";
import { useDashboardPanels } from "@/components/dashboard/composables/useDashboardPanels";
import { useDashboardSidebar } from "@/composables/dashboard/useDashboardSidebar";

export function useDashboardUI() {
    const sidebar = useDashboardSidebar();
    const miniCalendar = useDashboardMiniCalendar();
    const panels = useDashboardPanels();

    function init(): void {
        sidebar.init();
        miniCalendar.init();
        panels.init();
    }

    function destroy(): void {
        panels.destroy();
        miniCalendar.destroy();
        sidebar.destroy();
    }

    return {
        destroy,
        init,
        miniCalendar,
        panels,
        sidebar,
    };
}
