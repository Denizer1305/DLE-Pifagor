<script setup lang="ts">
interface Emits {
    (event: "go-login"): void;
}

const emit = defineEmits<Emits>();
</script>

<template>
    <div class="auth-success-box">
        <div class="auth-success-box__icon">
            <i class="fa-solid fa-envelope-circle-check"></i>
        </div>

        <h3 class="auth-success-box__title">
            Проверьте электронную почту
        </h3>

        <p class="auth-success-box__text">
            Мы отправили письмо для подтверждения email. После подтверждения вы сможете продолжить настройку аккаунта.
            Если письмо не пришло, проверьте папку «Спам» или попробуйте войти позже.
        </p>

        <button
            class="auth-submit-btn"
            type="button"
            @click="emit('go-login')"
        >
            Перейти ко входу
            <i class="fa-solid fa-right-to-bracket"></i>
        </button>
    </div>
</template>