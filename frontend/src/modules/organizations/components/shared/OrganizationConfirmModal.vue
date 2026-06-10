<script setup lang="ts">
interface Props {
    isOpen: boolean;
    title: string;
    text?: string;
    confirmLabel: string;
    cancelLabel: string;
    tone?: "neutral" | "danger" | "success" | "warning";
    isSubmitting?: boolean;
}

interface Emits {
    (event: "confirm"): void;
    (event: "cancel"): void;
    (event: "close"): void;
}

withDefaults(defineProps<Props>(), {
    text: "",
    tone: "neutral",
    isSubmitting: false,
});

defineEmits<Emits>();
</script>

<template>
    <Teleport to="body">
        <div
            v-if="isOpen"
            class="base-modal"
            role="dialog"
            aria-modal="true"
        >
            <div
                class="base-modal__backdrop"
                @click="$emit('close')"
            />

            <div class="base-modal__dialog">
                <section class="org-details">
                    <header class="org-details__header">
                        <div class="org-details__top">
                            <div class="org-details__identity">
                                <span class="org-details__icon">
                                    <slot name="icon">
                                        <i class="fas fa-circle-question"></i>
                                    </slot>
                                </span>

                                <div class="org-details__title-wrap">
                                    <span
                                        class="org-details__eyebrow"
                                        :class="`org-details__eyebrow--${tone}`"
                                    >
                                        {{ tone }}
                                    </span>

                                    <h2 class="org-details__title">
                                        {{ title }}
                                    </h2>

                                    <p
                                        v-if="text"
                                        class="org-details__subtitle"
                                    >
                                        {{ text }}
                                    </p>
                                </div>
                            </div>

                            <button
                                class="org-details__action"
                                type="button"
                                :disabled="isSubmitting"
                                aria-label="Закрыть"
                                @click="$emit('close')"
                            >
                                <i class="fas fa-xmark"></i>
                            </button>
                        </div>
                    </header>

                    <div
                        v-if="$slots.default"
                        class="org-details__body"
                    >
                        <slot />
                    </div>

                    <footer class="org-details__footer">
                        <p class="org-details__footer-text">
                            <slot name="hint" />
                        </p>

                        <div class="org-details__footer-actions">
                            <button
                                class="org-form__button"
                                type="button"
                                :disabled="isSubmitting"
                                @click="$emit('cancel')"
                            >
                                {{ cancelLabel }}
                            </button>

                            <button
                                class="org-form__button"
                                :class="{
                                    'org-form__button--danger': tone === 'danger',
                                    'org-form__button--primary': tone !== 'danger',
                                }"
                                type="button"
                                :disabled="isSubmitting"
                                @click="$emit('confirm')"
                            >
                                {{ confirmLabel }}
                            </button>
                        </div>
                    </footer>
                </section>
            </div>
        </div>
    </Teleport>
</template>
