import { computed, ref } from "vue";
import { defineStore } from "pinia";

import type { RegistrationRole } from "@/modules/auth/types/auth-form.types";

export type AuthPageMode =
    | "login"
    | "register"
    | "forgot-password"
    | "reset-password"
    | "verify-email"
    | "logout";

export type AuthUiStatus =
    | "idle"
    | "loading"
    | "success"
    | "error";

export const useAuthUiStore = defineStore("auth-ui", () => {
    const currentPage = ref<AuthPageMode>("login");
    const selectedRegistrationRole = ref<RegistrationRole>("learner");

    const status = ref<AuthUiStatus>("idle");
    const message = ref("");
    const errorMessage = ref("");

    const isMobileMenuOpen = ref(false);
    const isPasswordVisible = ref(false);

    const isLoading = computed(() => status.value === "loading");
    const isSuccess = computed(() => status.value === "success");
    const isError = computed(() => status.value === "error");

    const selectedRegistrationRoleLabel = computed(() => {
        if (selectedRegistrationRole.value === "teacher") {
            return "Преподаватель";
        }

        if (selectedRegistrationRole.value === "guardian") {
            return "Родитель";
        }

        return "Учащийся";
    });

    function setCurrentPage(page: AuthPageMode): void {
        currentPage.value = page;
    }

    function setRegistrationRole(role: RegistrationRole): void {
        selectedRegistrationRole.value = role;
    }

    function setIdle(): void {
        status.value = "idle";
        message.value = "";
        errorMessage.value = "";
    }

    function setLoading(nextMessage = ""): void {
        status.value = "loading";
        message.value = nextMessage;
        errorMessage.value = "";
    }

    function setSuccess(nextMessage = ""): void {
        status.value = "success";
        message.value = nextMessage;
        errorMessage.value = "";
    }

    function setError(nextErrorMessage: string): void {
        status.value = "error";
        errorMessage.value = nextErrorMessage;
    }

    function clearMessages(): void {
        message.value = "";
        errorMessage.value = "";
    }

    function openMobileMenu(): void {
        isMobileMenuOpen.value = true;
    }

    function closeMobileMenu(): void {
        isMobileMenuOpen.value = false;
    }

    function toggleMobileMenu(): void {
        isMobileMenuOpen.value = !isMobileMenuOpen.value;
    }

    function showPassword(): void {
        isPasswordVisible.value = true;
    }

    function hidePassword(): void {
        isPasswordVisible.value = false;
    }

    function togglePasswordVisibility(): void {
        isPasswordVisible.value = !isPasswordVisible.value;
    }

    function resetAuthUiState(): void {
        currentPage.value = "login";
        selectedRegistrationRole.value = "learner";
        status.value = "idle";
        message.value = "";
        errorMessage.value = "";
        isMobileMenuOpen.value = false;
        isPasswordVisible.value = false;
    }

    return {
        currentPage,
        selectedRegistrationRole,
        selectedRegistrationRoleLabel,
        status,
        message,
        errorMessage,
        isMobileMenuOpen,
        isPasswordVisible,

        isLoading,
        isSuccess,
        isError,

        setCurrentPage,
        setRegistrationRole,
        setIdle,
        setLoading,
        setSuccess,
        setError,
        clearMessages,

        openMobileMenu,
        closeMobileMenu,
        toggleMobileMenu,

        showPassword,
        hidePassword,
        togglePasswordVisibility,

        resetAuthUiState,
    };
});