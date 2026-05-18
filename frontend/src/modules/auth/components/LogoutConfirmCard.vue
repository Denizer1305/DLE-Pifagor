<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";

import logoSrc from "@/assets/image/logo/logo.svg";
import { useAuthStore } from "@/stores/auth.store";
import { redirectAfterLogout } from "@/modules/auth/utils/auth-redirect.utils";

const router = useRouter();
const authStore = useAuthStore();

const isSubmitting = ref(false);

function goBack(): void {
    if (window.history.length > 1) {
        router.back();
        return;
    }

    void router.push({ name: "student-dashboard" });
}

async function logout(): Promise<void> {
    isSubmitting.value = true;

    try {
        await authStore.logout();
        await redirectAfterLogout(router);
    } finally {
        isSubmitting.value = false;
    }
}
</script>

<template>
    <div class="auth-shell">
        <div class="auth-card">
            <div class="auth-logo">
                <img
                    :src="logoSrc"
                    alt="Пифагор"
                />
            </div>

            <h1 class="auth-title">
                Завершить сеанс?
            </h1>

            <p class="auth-text">
                Вы собираетесь выйти из личного кабинета. После выхода для продолжения работы
                потребуется повторный вход в систему.
            </p>

            <div class="auth-info">
                <div class="auth-info-item">
                    <div class="auth-info-icon">
                        <i class="fa-solid fa-shield-halved"></i>
                    </div>

                    <div class="auth-info-copy">
                        <strong>Безопасное завершение</strong>
                        <span>Сеанс будет завершён на текущем устройстве.</span>
                    </div>
                </div>

                <div class="auth-info-item">
                    <div class="auth-info-icon">
                        <i class="fa-solid fa-right-to-bracket"></i>
                    </div>

                    <div class="auth-info-copy">
                        <strong>Повторный вход</strong>
                        <span>Вы сможете войти снова в любое время через страницу авторизации.</span>
                    </div>
                </div>
            </div>

            <div class="auth-actions">
                <button
                    class="auth-btn light"
                    type="button"
                    @click="goBack"
                >
                    <i class="fa-solid fa-arrow-left"></i>
                    Вернуться назад
                </button>

                <button
                    class="auth-btn primary"
                    type="button"
                    :disabled="isSubmitting"
                    @click="logout"
                >
                    <i :class="isSubmitting ? 'fa-solid fa-spinner fa-spin' : 'fa-solid fa-check'"></i>
                    {{ isSubmitting ? "Выходим..." : "Выйти из аккаунта" }}
                </button>
            </div>
        </div>
    </div>
</template>
