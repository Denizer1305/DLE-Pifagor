<script setup lang="ts">
import type { SubjectFormModel } from "../../types";

interface Props {
    modelValue: SubjectFormModel;
    errors?: Partial<Record<keyof SubjectFormModel | "detail", string>>;
    title: string;
    text?: string;
    submitLabel: string;
    cancelLabel: string;
    isSubmitting?: boolean;
}

interface Emits {
    (event: "update:modelValue", value: SubjectFormModel): void;
    (event: "submit"): void;
    (event: "cancel"): void;
}

const props = withDefaults(defineProps<Props>(), {
    errors: () => ({}),
    text: "",
    isSubmitting: false,
});

const emit = defineEmits<Emits>();

function updateField<K extends keyof SubjectFormModel>(
    field: K,
    value: SubjectFormModel[K],
): void {
    emit("update:modelValue", {
        ...props.modelValue,
        [field]: value,
    });
}

function getInputValue(event: Event): string {
    return (event.target as HTMLInputElement).value;
}

function getTextareaValue(event: Event): string {
    return (event.target as HTMLTextAreaElement).value;
}
</script>

<template>
    <form
        class="org-form"
        @submit.prevent="$emit('submit')"
    >
        <section class="org-form__section">
            <header class="org-form__section-head">
                <div>
                    <h2 class="org-form__section-title">
                        {{ title }}
                    </h2>

                    <p
                        v-if="text"
                        class="org-form__section-text"
                    >
                        {{ text }}
                    </p>
                </div>
            </header>

            <p
                v-if="errors.detail"
                class="org-form__error"
            >
                {{ errors.detail }}
            </p>

            <div class="org-form__grid">
                <label class="org-form__field org-form__field--wide">
                    <span class="org-form__label">
                        Название <span class="org-form__required">*</span>
                    </span>

                    <input
                        class="org-form__control"
                        type="text"
                        :value="modelValue.name"
                        :disabled="isSubmitting"
                        placeholder="Например: Математика"
                        @input="updateField('name', getInputValue($event))"
                    />

                    <span
                        v-if="errors.name"
                        class="org-form__error"
                    >
                        {{ errors.name }}
                    </span>
                </label>

                <label class="org-form__field">
                    <span class="org-form__label">
                        Краткое название
                    </span>

                    <input
                        class="org-form__control"
                        type="text"
                        :value="modelValue.shortName"
                        :disabled="isSubmitting"
                        placeholder="Например: Мат."
                        @input="updateField('shortName', getInputValue($event))"
                    />

                    <span
                        v-if="errors.shortName"
                        class="org-form__error"
                    >
                        {{ errors.shortName }}
                    </span>
                </label>

                <label class="org-form__field">
                    <span class="org-form__label">
                        Код <span class="org-form__required">*</span>
                    </span>

                    <input
                        class="org-form__control"
                        type="text"
                        :value="modelValue.code"
                        :disabled="isSubmitting"
                        placeholder="math"
                        @input="updateField('code', getInputValue($event))"
                    />

                    <span
                        v-if="errors.code"
                        class="org-form__error"
                    >
                        {{ errors.code }}
                    </span>
                </label>

                <label class="org-form__field org-form__field--wide">
                    <span class="org-form__label">
                        Описание
                    </span>

                    <textarea
                        class="org-form__control org-form__textarea"
                        :value="modelValue.description"
                        :disabled="isSubmitting"
                        placeholder="Краткое описание предмета"
                        @input="updateField('description', getTextareaValue($event))"
                    />

                    <span
                        v-if="errors.description"
                        class="org-form__error"
                    >
                        {{ errors.description }}
                    </span>
                </label>
            </div>
        </section>

        <footer class="org-form__footer">
            <p class="org-form__footer-text">
                Предмет используется в назначениях преподавателей и учебных курсах.
            </p>

            <div class="org-form__actions">
                <button
                    class="org-form__button"
                    type="button"
                    :disabled="isSubmitting"
                    @click="$emit('cancel')"
                >
                    {{ cancelLabel }}
                </button>

                <button
                    class="org-form__button org-form__button--primary"
                    type="submit"
                    :disabled="isSubmitting"
                >
                    {{ submitLabel }}
                </button>
            </div>
        </footer>
    </form>
</template>