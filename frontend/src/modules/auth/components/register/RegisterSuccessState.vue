<script setup lang="ts">
import { useI18n } from "@/composables/useI18n";

interface Emits {
    (event: "go-login"): void;
}

const emit = defineEmits<Emits>();
const { tr } = useI18n();
</script>

<template>
    <div class="auth-success-box">
        <div class="auth-success-box__icon">
            <i class="fa-solid fa-envelope-circle-check"></i>
        </div>

        <h3 class="auth-success-box__title">
            {{ tr("Проверьте электронную почту") }}
        </h3>

        <p class="auth-success-box__text">
            {{ tr("Мы отправили письмо для подтверждения email. После подтверждения вы сможете продолжить настройку аккаунта. Если письмо не пришло, проверьте папку «Спам» или попробуйте войти позже.") }}
        </p>

        <button
            class="auth-submit-btn"
            type="button"
            @click="emit('go-login')"
        >
            {{ tr("Перейти ко входу") }}
            <i class="fa-solid fa-right-to-bracket"></i>
        </button>
    </div>
</template>
