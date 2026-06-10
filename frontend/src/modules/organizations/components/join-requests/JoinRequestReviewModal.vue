<script setup lang="ts">
import type { JoinRequestReviewFormModel } from "../../types";

interface Props {
    isOpen: boolean;
    modelValue: JoinRequestReviewFormModel;
    title: string;
    text?: string;
    submitLabel: string;
    cancelLabel: string;
    tone?: "success" | "danger";
    isSubmitting?: boolean;
    errors?: Partial<Record<keyof JoinRequestReviewFormModel | "detail", string>>;
}

interface Emits {
    (event: "update:modelValue", value: JoinRequestReviewFormModel): void;
    (event: "submit"): void;
    (event: "cancel"): void;
    (event: "close"): void;
}

const props = withDefaults(defineProps<Props>(), {
    text: "",
    tone: "success",
    isSubmitting: false,
    errors: () => ({}),
});

const emit = defineEmits<Emits>();

function updateField<K extends keyof JoinRequestReviewFormModel>(
    field: K,
    value: JoinRequestReviewFormModel[K],
): void {
    emit("update:modelValue", {
        ...props.modelValue,
        [field]: value,
    });
}

function getTextareaValue(event: Event): string {
    return (event.target as HTMLTextAreaElement).value;
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
                <section class="org-request-review">
                    <div class="org-details">
                        <header class="org-details__header">
                            <div class="org-details__top">
                                <div class="org-details__identity">
                                    <span class="org-details__icon">
                                        {{ tone === "success" ? "✓" : "!" }}
                                    </span>

                                    <div class="org-details__title-wrap">
                                        <span class="org-details__eyebrow">
                                            {{ tone === "success" ? "Принятие" : "Отклонение" }}
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
                                    @click="$emit('close')"
                                >
                                    ×
                                </button>
                            </div>
                        </header>

                        <form
                            class="org-details__body"
                            @submit.prevent="$emit('submit')"
                        >
                            <p
                                v-if="errors.detail"
                                class="org-form__error"
                            >
                                {{ errors.detail }}
                            </p>

                            <div class="org-request-review__summary">
                                <h3 class="org-request-review__title">
                                    Комментарий к решению
                                </h3>

                                <p class="org-request-review__text">
                                    Комментарий сохранится в заявке и поможет пользователю понять решение.
                                </p>
                            </div>

                            <label class="org-form__field">
                                <span class="org-form__label">
                                    Комментарий
                                </span>

                                <textarea
                                    class="org-request-review__textarea"
                                    :value="modelValue.comment"
                                    :disabled="isSubmitting"
                                    placeholder="Например: заявка подтверждена, данные проверены"
                                    @input="updateField('comment', getTextareaValue($event))"
                                />

                                <span
                                    v-if="errors.comment"
                                    class="org-form__error"
                                >
                                    {{ errors.comment }}
                                </span>
                            </label>

                            <footer class="org-request-review__actions">
                                <button
                                    class="org-request-review__button"
                                    type="button"
                                    :disabled="isSubmitting"
                                    @click="$emit('cancel')"
                                >
                                    {{ cancelLabel }}
                                </button>

                                <button
                                    class="org-request-review__button"
                                    :class="{
                                        'org-request-review__button--approve': tone === 'success',
                                        'org-request-review__button--reject': tone === 'danger',
                                    }"
                                    type="submit"
                                    :disabled="isSubmitting"
                                >
                                    {{ submitLabel }}
                                </button>
                            </footer>
                        </form>
                    </div>
                </section>
            </div>
        </div>
    </Teleport>
</template>