<script setup lang="ts">
import { computed } from "vue";

import BaseSelect from "@/components/base/BaseSelect.vue";

import type {
    StudyFormApi,
    StudyGroupFormModel,
    StudyGroupStatusApi,
} from "../../types";

interface SelectOption<TValue extends string | number = string | number> {
    label: string;
    value: TValue;
    hint?: string;
}

interface Props {
    modelValue: StudyGroupFormModel;
    organizationOptions: SelectOption<number>[];
    departmentOptions: SelectOption<number>[];
    statusOptions: SelectOption<StudyGroupStatusApi>[];
    studyFormOptions: SelectOption<StudyFormApi>[];
    errors?: Partial<Record<keyof StudyGroupFormModel | "detail", string>>;
    title: string;
    text?: string;
    submitLabel: string;
    cancelLabel: string;
    isSubmitting?: boolean;
}

interface Emits {
    (event: "update:modelValue", value: StudyGroupFormModel): void;
    (event: "submit"): void;
    (event: "cancel"): void;
}

const props = withDefaults(defineProps<Props>(), {
    errors: () => ({}),
    text: "",
    isSubmitting: false,
});

const emit = defineEmits<Emits>();

const organizationSelectOptions = computed(() => createNumberOptions(
    props.organizationOptions,
    "Выберите организацию",
));
const departmentSelectOptions = computed(() => createNumberOptions(
    props.departmentOptions,
    "Без отделения",
));
const statusSelectOptions = computed(() => createStringOptions(props.statusOptions));
const studyFormSelectOptions = computed(() => createStringOptions(props.studyFormOptions));

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

function createStringOptions<TValue extends string>(
    options: SelectOption<TValue>[],
) {
    return options.map((option) => ({
        label: option.label,
        value: option.value,
    }));
}

function updateField<K extends keyof StudyGroupFormModel>(
    field: K,
    value: StudyGroupFormModel[K],
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

function getNumberValue(event: Event): number | null {
    const value = (event.target as HTMLInputElement).value;

    return value ? Number(value) : null;
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

                <div class="org-form__field">
                    <span class="org-form__label">Отделение</span>

                    <BaseSelect
                        :model-value="modelValue.departmentId ? String(modelValue.departmentId) : ''"
                        :options="departmentSelectOptions"
                        :disabled="isSubmitting"
                        placeholder="Без отделения"
                        aria-label="Выбрать отделение"
                        @update:model-value="updateField('departmentId', parseNumberValue($event))"
                    />

                    <span
                        v-if="errors.departmentId"
                        class="org-form__error"
                    >
                        {{ errors.departmentId }}
                    </span>
                </div>

                <label class="org-form__field org-form__field--wide">
                    <span class="org-form__label">
                        Название <span class="org-form__required">*</span>
                    </span>

                    <input
                        class="org-form__control"
                        type="text"
                        :value="modelValue.name"
                        :disabled="isSubmitting"
                        placeholder="Например: ИС-21"
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
                    <span class="org-form__label">Код группы</span>

                    <input
                        class="org-form__control"
                        type="text"
                        :value="modelValue.code"
                        :disabled="isSubmitting"
                        placeholder="is-21"
                        @input="updateField('code', getInputValue($event))"
                    />

                    <span
                        v-if="errors.code"
                        class="org-form__error"
                    >
                        {{ errors.code }}
                    </span>
                </label>

                <div class="org-form__field">
                    <span class="org-form__label">Статус</span>

                    <BaseSelect
                        :model-value="modelValue.status"
                        :options="statusSelectOptions"
                        :disabled="isSubmitting"
                        aria-label="Выбрать статус группы"
                        @update:model-value="updateField('status', $event as StudyGroupStatusApi)"
                    />

                    <span
                        v-if="errors.status"
                        class="org-form__error"
                    >
                        {{ errors.status }}
                    </span>
                </div>

                <label class="org-form__field">
                    <span class="org-form__label">Год поступления</span>

                    <input
                        class="org-form__control"
                        type="number"
                        min="1900"
                        max="2100"
                        :value="modelValue.admissionYear ?? ''"
                        :disabled="isSubmitting"
                        @input="updateField('admissionYear', getNumberValue($event))"
                    />

                    <span
                        v-if="errors.admissionYear"
                        class="org-form__error"
                    >
                        {{ errors.admissionYear }}
                    </span>
                </label>

                <label class="org-form__field">
                    <span class="org-form__label">Год выпуска</span>

                    <input
                        class="org-form__control"
                        type="number"
                        min="1900"
                        max="2100"
                        :value="modelValue.graduationYear ?? ''"
                        :disabled="isSubmitting"
                        @input="updateField('graduationYear', getNumberValue($event))"
                    />

                    <span
                        v-if="errors.graduationYear"
                        class="org-form__error"
                    >
                        {{ errors.graduationYear }}
                    </span>
                </label>

                <label class="org-form__field">
                    <span class="org-form__label">Курс</span>

                    <input
                        class="org-form__control"
                        type="number"
                        min="1"
                        max="6"
                        :value="modelValue.courseNumber ?? ''"
                        :disabled="isSubmitting"
                        @input="updateField('courseNumber', getNumberValue($event))"
                    />

                    <span
                        v-if="errors.courseNumber"
                        class="org-form__error"
                    >
                        {{ errors.courseNumber }}
                    </span>
                </label>

                <div class="org-form__field">
                    <span class="org-form__label">Форма обучения</span>

                    <BaseSelect
                        :model-value="modelValue.studyForm"
                        :options="studyFormSelectOptions"
                        :disabled="isSubmitting"
                        aria-label="Выбрать форму обучения"
                        @update:model-value="updateField('studyForm', $event as StudyFormApi)"
                    />

                    <span
                        v-if="errors.studyForm"
                        class="org-form__error"
                    >
                        {{ errors.studyForm }}
                    </span>
                </div>

                <label class="org-form__field org-form__field--wide">
                    <span class="org-form__label">Описание</span>

                    <textarea
                        class="org-form__control org-form__textarea"
                        :value="modelValue.description"
                        :disabled="isSubmitting"
                        placeholder="Краткое описание группы"
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
                Группа используется для заявок учащихся, кураторов и учебной структуры.
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
