<script setup lang="ts">
import type { CodeFormModel } from "../../types";

interface Props {
    isOpen: boolean;
    modelValue: CodeFormModel;
    title: string;
    text?: string;
    submitLabel: string;
    cancelLabel: string;
    isSubmitting?: boolean;
    generatedCode?: string;
}

interface Emits {
    (event: "update:modelValue", value: CodeFormModel): void;
    (event: "submit"): void;
    (event: "cancel"): void;
    (event: "close"): void;
    (event: "copy", value: string): void;
}

const props = withDefaults(defineProps<Props>(), {
    text: "",
    isSubmitting: false,
    generatedCode: "",
});

const emit = defineEmits<Emits>();

function updateField<K extends keyof CodeFormModel>(
    field: K,
    value: CodeFormModel[K],
): void {
    emit("update:modelValue", {
        ...props.modelValue,
        [field]: value,
    });
}

function getInputValue(event: Event): string {
    return (event.target as HTMLInputElement).value;
}
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
                <section class="org-code-card">
                    <header class="org-code-card__header">
                        <div>
                            <h2 class="org-code-card__title">
                                {{ title }}
                            </h2>

                            <p
                                v-if="text"
                                class="org-code-card__text"
                            >
                                {{ text }}
                            </p>
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
                    </header>

                    <form
                        class="org-code-modal"
                        @submit.prevent="$emit('submit')"
                    >
                        <label class="org-form__field">
                            <span class="org-form__label">
                                Код
                            </span>

                            <input
                                class="org-form__control"
                                type="text"
                                :value="modelValue.rawCode"
                                :disabled="isSubmitting"
                                placeholder="Оставьте пустым, чтобы сгенерировать автоматически"
                                @input="updateField('rawCode', getInputValue($event))"
                            />
                        </label>

                        <label class="org-form__field">
                            <span class="org-form__label">
                                Действует до
                            </span>

                            <input
                                class="org-form__control"
                                type="datetime-local"
                                :value="modelValue.expiresAt || ''"
                                :disabled="isSubmitting"
                                @input="
                                    updateField(
                                        'expiresAt',
                                        getInputValue($event) || null,
                                    )
                                "
                            />
                        </label>

                        <div
                            v-if="generatedCode"
                            class="org-code-modal__preview"
                        >
                            <span class="org-code-modal__preview-label">
                                Сгенерированный код
                            </span>

                            <span class="org-code-modal__preview-value">
                                {{ generatedCode }}
                            </span>

                            <button
                                class="org-code-card__copy"
                                type="button"
                                @click="$emit('copy', generatedCode)"
                            >
                                <i class="fas fa-copy"></i>
                                Скопировать
                            </button>
                        </div>

                        <footer class="org-code-card__actions">
                            <button
                                class="org-code-card__button"
                                type="button"
                                :disabled="isSubmitting"
                                @click="$emit('cancel')"
                            >
                                {{ cancelLabel }}
                            </button>

                            <button
                                class="org-code-card__button org-code-card__button--primary"
                                type="submit"
                                :disabled="isSubmitting"
                            >
                                {{ submitLabel }}
                            </button>
                        </footer>
                    </form>
                </section>
            </div>
        </div>
    </Teleport>
</template>
