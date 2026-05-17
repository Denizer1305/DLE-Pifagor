<script setup lang="ts">
import { RouterLink } from "vue-router";

import AuthStatusCard from "@/modules/auth/components/AuthStatusCard.vue";
import { useVerifyEmailForm } from "@/modules/auth/composables/useVerifyEmailForm";

const {
    status,
    message,
} = useVerifyEmailForm();
</script>

<template>
    <div class="verify-email-status">
        <AuthStatusCard
            v-if="status === 'loading' || status === 'idle'"
            type="info"
            icon="fa-solid fa-spinner fa-spin"
            title="Проверяем email"
            :text="message"
        />

        <AuthStatusCard
            v-else-if="status === 'success'"
            type="success"
            title="Email подтверждён"
            :text="message"
        />

        <AuthStatusCard
            v-else
            type="error"
            title="Не удалось подтвердить email"
            :text="message"
        />

        <div class="auth-status-actions">
            <RouterLink
                class="auth-submit-btn"
                :to="{ name: 'login' }"
            >
                Перейти ко входу
                <i class="fa-solid fa-right-to-bracket"></i>
            </RouterLink>
        </div>
    </div>
</template>