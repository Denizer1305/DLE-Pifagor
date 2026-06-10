<script setup lang="ts">
import { computed } from "vue";

import BaseSelect from "@/components/base/BaseSelect.vue";

import type {
    TeacherEmploymentTypeApi,
    TeacherOrganizationFormModel,
} from "../../types";

interface SelectOption<TValue extends string | number = string | number> {
    label: string;
    value: TValue;
    hint?: string;
}

interface Props {
    modelValue: TeacherOrganizationFormModel;
    teacherOptions: SelectOption<number>[];
    organizationOptions: SelectOption<number>[];
    employmentTypeOptions: SelectOption<TeacherEmploymentTypeApi>[];
    errors?: Partial<Record<keyof TeacherOrganizationFormModel | "detail", string>>;
    title: string;
    text?: string;
    submitLabel: string;
    cancelLabel: string;
    isSubmitting?: boolean;
}

interface Emits {
    (event: "update:modelValue", value: TeacherOrganizationFormModel): void;
    (event: "submit"): void;
    (event: "cancel"): void;
}

const props = withDefaults(defineProps<Props>(), {
    errors: () => ({}),
    text: "",
    isSubmitting: false,
});

const emit = defineEmits<Emits>();

const teacherSelectOptions = computed(() => createNumberOptions(
    props.teacherOptions,
    "Выберите преподавателя",
));
const organizationSelectOptions = computed(() => createNumberOptions(
    props.organizationOptions,
    "Выберите организацию",
));
const employmentTypeSelectOptions = computed(() => {
    return props.employmentTypeOptions.map((option) => ({
        label: option.label,
        value: option.value,
    }));
});

function createNumberOptions(
    options: SelectOption<number>[],
    placeholder: string,
) {
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

function updateField<K extends keyof TeacherOrganizationFormModel>(
    field: K,
    value: TeacherOrganizationFormModel[K],
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

                <div class="org-form__field">
                    <span class="org-form__label">
                        Организация <span class="org-form__required">*</span>
                    </span>

                    <BaseSelect
                        :model-value="modelValue.organizationId ? String(modelValue.organizationId) : ''"
                        :options="organizationSelectOptions"
                        :disabled="isSubmitting"
                        placeholder="Выберите организацию"
                        aria-label="Выбрать организацию"
                        @update:model-value="updateField('organizationId', parseNumberValue($event))"
                    />

                    <span
                        v-if="errors.organizationId"
                        class="org-form__error"
                    >
                        {{ errors.organizationId }}
                    </span>
                </div>

                <label class="org-form__field">
                    <span class="org-form__label">Должность</span>

                    <input
                        class="org-form__control"
                        type="text"
                        :value="modelValue.position"
                        :disabled="isSubmitting"
                        placeholder="Например: преподаватель математики"
                        @input="updateField('position', getInputValue($event))"
                    />

                    <span
                        v-if="errors.position"
                        class="org-form__error"
                    >
                        {{ errors.position }}
                    </span>
                </label>

                <div class="org-form__field">
                    <span class="org-form__label">Тип занятости</span>

                    <BaseSelect
                        :model-value="modelValue.employmentType"
                        :options="employmentTypeSelectOptions"
                        :disabled="isSubmitting"
                        aria-label="Выбрать тип занятости"
                        @update:model-value="updateField('employmentType', $event as TeacherEmploymentTypeApi)"
                    />

                    <span
                        v-if="errors.employmentType"
                        class="org-form__error"
                    >
                        {{ errors.employmentType }}
                    </span>
                </div>

                <label class="org-form__field">
                    <span class="org-form__label">Начало работы</span>

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
                    <span class="org-form__label">Окончание работы</span>

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
                        placeholder="Служебная информация по связи преподавателя с организацией"
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
                            <span class="org-form__switch-label">Основная организация</span>
                            <span class="org-form__switch-hint">
                                Используется как основная привязка преподавателя.
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
                            <span class="org-form__switch-label">Активная связь</span>
                            <span class="org-form__switch-hint">
                                Неактивные связи скрываются из рабочих списков.
                            </span>
                        </span>
                    </label>
                </div>
            </div>
        </section>

        <footer class="org-form__footer">
            <p class="org-form__footer-text">
                Преподаватель может быть связан с несколькими организациями.
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
