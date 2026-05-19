import { computed, ref } from "vue";

import { useI18n } from "@/composables/useI18n";

export function useMobileMenu() {
    const { t } = useI18n();
    const isMobileMenuOpen = ref(false);

    const mobileMenuLabel = computed(() => {
        return isMobileMenuOpen.value
            ? t("common.closeMenu")
            : t("common.openMenu");
    });

    const mobileMenuIcon = computed(() => {
        return isMobileMenuOpen.value
            ? "fa-solid fa-xmark"
            : "fa-solid fa-bars";
    });

    function openMobileMenu(): void {
        isMobileMenuOpen.value = true;
        document.body.classList.add("no-scroll");
    }

    function closeMobileMenu(): void {
        isMobileMenuOpen.value = false;
        document.body.classList.remove("no-scroll");
    }

    function toggleMobileMenu(): void {
        if (isMobileMenuOpen.value) {
            closeMobileMenu();
            return;
        }

        openMobileMenu();
    }

    return {
        isMobileMenuOpen,
        mobileMenuLabel,
        mobileMenuIcon,
        openMobileMenu,
        closeMobileMenu,
        toggleMobileMenu,
    };
}
