<script setup lang="ts">
interface Props {
    isOpen: boolean;
    title: string;
    message: string;
    type?: "error" | "success" | "warning" | "info";
    buttonLabel?: string;
}

interface Emits {
    (event: "close"): void;
}

withDefaults(defineProps<Props>(), {
    type: "error",
    buttonLabel: "Понятно",
});

const emit = defineEmits<Emits>();
</script>

<template>
    <Teleport to="body">
        <div
            v-if="isOpen"
            class="auth-message-modal"
            role="dialog"
            aria-modal="true"
        >
            <button
                class="auth-message-modal__backdrop"
                type="button"
                aria-label="Закрыть окно"
                @click="emit('close')"
            ></button>

            <div :class="['auth-message-modal__card', `auth-message-modal__card--${type}`]">
                <div class="auth-message-modal__icon">
                    <i
                        v-if="type === 'error'"
                        class="fa-solid fa-circle-exclamation"
                    ></i>
                    <i
                        v-else-if="type === 'success'"
                        class="fa-solid fa-circle-check"
                    ></i>
                    <i
                        v-else-if="type === 'warning'"
                        class="fa-solid fa-triangle-exclamation"
                    ></i>
                    <i
                        v-else
                        class="fa-solid fa-circle-info"
                    ></i>
                </div>

                <div class="auth-message-modal__content">
                    <h3 class="auth-message-modal__title">
                        {{ title }}
                    </h3>

                    <p class="auth-message-modal__message">
                        {{ message }}
                    </p>
                </div>

                <button
                    class="auth-message-modal__button"
                    type="button"
                    @click="emit('close')"
                >
                    {{ buttonLabel }}
                </button>
            </div>
        </div>
    </Teleport>
</template>