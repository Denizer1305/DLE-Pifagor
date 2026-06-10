<script setup lang="ts">
import { computed } from "vue";

import BaseSelect from "@/components/base/BaseSelect.vue";

import type { GroupCuratorFormModel } from "../../types";

interface SelectOption {
    label: string;
    value: number;
    hint?: string;
}

interface Props {
    modelValue: GroupCuratorFormModel;
    groupOptions: SelectOption[];
    teacherOptions: SelectOption[];
    errors?: Partial<Record<keyof GroupCuratorFormModel | "detail", string>>;
    title: string;
    text?: string;
    submitLabel: string;
    cancelLabel: string;
    isSubmitting?: boolean;
}

interface Emits {
    (event: "update:modelValue", value: GroupCuratorFormModel): void;
    (event: "submit"): void;
    (event: "cancel"): void;
}

const props = withDefaults(defineProps<Props>(), {
    errors: () => ({}),
    text: "",
    isSubmitting: false,
});

const emit = defineEmits<Emits>();

const groupSelectOptions = computed(() => createOptions(
    props.groupOptions,
    "Выберите группу",
));
const teacherSelectOptions = computed(() => createOptions(
    props.teacherOptions,
    "Выберите преподавателя",
));

function createOptions(options: SelectOption[], placeholder: string) {
    return [
        {
            label: placeholder,
            value: "",
        },
        ...options.map((option) => ({
            label: option.label,
            value: String(option.value),
        })),
    ];
}

function updateField<K extends keyof GroupCuratorFormModel>(
    field: K,
    value: GroupCuratorFormModel[K],
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

function getCheckboxValue(event: Event): boolean {
    return (event.target as HTMLInputElement).checked;
}

function parseNumberValue(value: string): number | null {
    return value ? Number(value) : null;
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
                <div class="org-form__field">
                    <span class="org-form__label">
                        Группа <span class="org-form__required">*</span>
                    </span>

                    <BaseSelect
                        :model-value="modelValue.groupId ? String(modelValue.groupId) : ''"
                        :options="groupSelectOptions"
                        :disabled="isSubmitting"
                        placeholder="Выберите группу"
                        aria-label="Выбрать группу"
                        @update:model-value="updateField('groupId', parseNumberValue($event))"
                    />

                    <span
                        v-if="errors.groupId"
                        class="org-form__error"
                    >
                        {{ errors.groupId }}
                    </span>
                </div>

                <div class="org-form__field">
                    <span class="org-form__label">
                        Преподаватель <span class="org-form__required">*</span>
                    </span>

                    <BaseSelect
                        :model-value="modelValue.teacherId ? String(modelValue.teacherId) : ''"
                        :options="teacherSelectOptions"
                        :disabled="isSubmitting"
                        placeholder="Выберите преподавателя"
                        aria-label="Выбрать преподавателя"
                        @update:model-value="updateField('teacherId', parseNumberValue($event))"
                    />

                    <span
                        v-if="errors.teacherId"
                        class="org-form__error"
                    >
                        {{ errors.teacherId }}
                    </span>
                </div>

                <label class="org-form__field">
                    <span class="org-form__label">Дата начала</span>

                    <input
                        class="org-form__control"
                        type="date"
                        :value="modelValue.startsAt || ''"
                        :disabled="isSubmitting"
                        @input="updateField('startsAt', getInputValue($event) || null)"
                    />

                    <span
                        v-if="errors.startsAt"
                        class="org-form__error"
                    >
                        {{ errors.startsAt }}
                    </span>
                </label>

                <label class="org-form__field">
                    <span class="org-form__label">Дата окончания</span>

                    <input
                        class="org-form__control"
                        type="date"
                        :value="modelValue.endsAt || ''"
                        :disabled="isSubmitting"
                        @input="updateField('endsAt', getInputValue($event) || null)"
                    />

                    <span
                        v-if="errors.endsAt"
                        class="org-form__error"
                    >
                        {{ errors.endsAt }}
                    </span>
                </label>

                <label class="org-form__field org-form__field--wide">
                    <span class="org-form__label">Заметки</span>

                    <textarea
                        class="org-form__control org-form__textarea"
                        :value="modelValue.notes"
                        :disabled="isSubmitting"
                        placeholder="Например: основной куратор группы на 2025/2026 учебный год"
                        @input="updateField('notes', getTextareaValue($event))"
                    />

                    <span
                        v-if="errors.notes"
                        class="org-form__error"
                    >
                        {{ errors.notes }}
                    </span>
                </label>

                <div class="org-form__field org-form__field--wide">
                    <label class="org-form__switch">
                        <input
                            class="org-form__switch-input"
                            type="checkbox"
                            :checked="modelValue.isPrimary"
                            :disabled="isSubmitting"
                            @change="updateField('isPrimary', getCheckboxValue($event))"
                        />

                        <span class="org-form__switch-track" />
                        <span class="org-form__switch-text">
                            <span class="org-form__switch-label">Основной куратор</span>
                            <span class="org-form__switch-hint">
                                Основной куратор принимает заявки учащихся в группу.
                            </span>
                        </span>
                    </label>

                    <label class="org-form__switch">
                        <input
                            class="org-form__switch-input"
                            type="checkbox"
                            :checked="modelValue.isActive"
                            :disabled="isSubmitting"
                            @change="updateField('isActive', getCheckboxValue($event))"
                        />

                        <span class="org-form__switch-track" />
                        <span class="org-form__switch-text">
                            <span class="org-form__switch-label">Активное назначение</span>
                            <span class="org-form__switch-hint">
                                Неактивный куратор не участвует в рассмотрении заявок.
                            </span>
                        </span>
                    </label>
                </div>
            </div>
        </section>

        <footer class="org-form__footer">
            <p class="org-form__footer-text">
                У группы может быть несколько кураторов, но основной должен быть один.
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
