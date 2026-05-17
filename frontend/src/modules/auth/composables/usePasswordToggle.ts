import { computed, ref } from "vue";

export function usePasswordToggle() {
    const isPasswordVisible = ref(false);

    const inputType = computed(() => {
        return isPasswordVisible.value ? "text" : "password";
    });

    const iconClass = computed(() => {
        return isPasswordVisible.value
            ? "fa-solid fa-eye-slash"
            : "fa-solid fa-eye";
    });

    const ariaLabel = computed(() => {
        return isPasswordVisible.value
            ? "Скрыть пароль"
            : "Показать пароль";
    });

    function showPassword(): void {
        isPasswordVisible.value = true;
    }

    function hidePassword(): void {
        isPasswordVisible.value = false;
    }

    function togglePasswordVisibility(): void {
        isPasswordVisible.value = !isPasswordVisible.value;
    }

    return {
        isPasswordVisible,
        inputType,
        iconClass,
        ariaLabel,
        showPassword,
        hidePassword,
        togglePasswordVisibility,
    };
}