<script setup lang="ts">
import ProfileCitySelect from "@/modules/profile/components/ProfileCitySelect.vue";
import { formatRussianPhone } from "@/modules/auth/composables/usePhoneMask";
import type { ProfileCitySuggestion } from "@/modules/profile/types/profile-edit.types";

import type { OrganizationFormModel } from "../../types";

interface Props {
    modelValue: OrganizationFormModel;
    errors?: Partial<Record<keyof OrganizationFormModel | "detail", string>>;
    title: string;
    text?: string;
    submitLabel: string;
    cancelLabel: string;
    isSubmitting?: boolean;
    citySuggestions?: ProfileCitySuggestion[];
    isCitySuggestionsLoading?: boolean;
}

interface Emits {
    (event: "update:modelValue", value: OrganizationFormModel): void;
    (event: "submit"): void;
    (event: "cancel"): void;
    (event: "searchCity", value: string): void;
    (event: "selectCity", suggestion: ProfileCitySuggestion): void;
}

const props = withDefaults(defineProps<Props>(), {
    errors: () => ({}),
    text: "",
    isSubmitting: false,
    citySuggestions: () => [],
    isCitySuggestionsLoading: false,
});

const emit = defineEmits<Emits>();

function updateField<K extends keyof OrganizationFormModel>(
    field: K,
    value: OrganizationFormModel[K],
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

function handlePhoneInput(event: Event): void {
    updateField("phone", formatRussianPhone(getInputValue(event)));
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
                        placeholder="Например: Владимирский колледж"
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
                    <span class="org-form__label">Краткое название</span>

                    <input
                        class="org-form__control"
                        type="text"
                        :value="modelValue.shortName"
                        :disabled="isSubmitting"
                        placeholder="Например: ВлГК"
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
                        placeholder="Например: vlgk"
                        @input="updateField('code', getInputValue($event))"
                    />

                    <span
                        v-if="errors.code"
                        class="org-form__error"
                    >
                        {{ errors.code }}
                    </span>
                </label>

                <label class="org-form__field">
                    <span class="org-form__label">Slug</span>

                    <input
                        class="org-form__control"
                        type="text"
                        :value="modelValue.slug"
                        :disabled="isSubmitting"
                        placeholder="vlgk"
                        @input="updateField('slug', getInputValue($event))"
                    />

                    <span
                        v-if="errors.slug"
                        class="org-form__error"
                    >
                        {{ errors.slug }}
                    </span>
                </label>

                <div class="org-form__field">
                    <span class="org-form__label">Город</span>

                    <ProfileCitySelect
                        :model-value="modelValue.city"
                        :suggestions="citySuggestions"
                        :is-loading="isCitySuggestionsLoading"
                        @update:model-value="updateField('city', $event)"
                        @search="$emit('searchCity', $event)"
                        @select="$emit('selectCity', $event)"
                    />

                    <span
                        v-if="errors.city"
                        class="org-form__error"
                    >
                        {{ errors.city }}
                    </span>
                </div>

                <label class="org-form__field org-form__field--wide">
                    <span class="org-form__label">Адрес</span>

                    <input
                        class="org-form__control"
                        type="text"
                        :value="modelValue.address"
                        :disabled="isSubmitting"
                        placeholder="Адрес образовательной организации"
                        @input="updateField('address', getInputValue($event))"
                    />

                    <span
                        v-if="errors.address"
                        class="org-form__error"
                    >
                        {{ errors.address }}
                    </span>
                </label>

                <label class="org-form__field">
                    <span class="org-form__label">Телефон</span>

                    <input
                        class="org-form__control"
                        type="tel"
                        inputmode="tel"
                        :value="modelValue.phone"
                        :disabled="isSubmitting"
                        placeholder="+7 999 123-45-67"
                        @input="handlePhoneInput"
                    />

                    <span
                        v-if="errors.phone"
                        class="org-form__error"
                    >
                        {{ errors.phone }}
                    </span>
                </label>

                <label class="org-form__field">
                    <span class="org-form__label">Email</span>

                    <input
                        class="org-form__control"
                        type="email"
                        :value="modelValue.email"
                        :disabled="isSubmitting"
                        placeholder="mail@example.ru"
                        @input="updateField('email', getInputValue($event))"
                    />

                    <span
                        v-if="errors.email"
                        class="org-form__error"
                    >
                        {{ errors.email }}
                    </span>
                </label>

                <label class="org-form__field org-form__field--wide">
                    <span class="org-form__label">Сайт</span>

                    <input
                        class="org-form__control"
                        type="url"
                        :value="modelValue.website"
                        :disabled="isSubmitting"
                        placeholder="https://example.ru"
                        @input="updateField('website', getInputValue($event))"
                    />

                    <span
                        v-if="errors.website"
                        class="org-form__error"
                    >
                        {{ errors.website }}
                    </span>
                </label>

                <label class="org-form__field org-form__field--wide">
                    <span class="org-form__label">Описание</span>

                    <textarea
                        class="org-form__control org-form__textarea"
                        :value="modelValue.description"
                        :disabled="isSubmitting"
                        placeholder="Краткое описание организации"
                        @input="updateField('description', getTextareaValue($event))"
                    />

                    <span
                        v-if="errors.description"
                        class="org-form__error"
                    >
                        {{ errors.description }}
                    </span>
                </label>

                <div class="org-form__field org-form__field--wide">
                    <label class="org-form__switch">
                        <input
                            class="org-form__switch-input"
                            type="checkbox"
                            :checked="modelValue.isPublic"
                            :disabled="isSubmitting"
                            @change="updateField('isPublic', getCheckboxValue($event))"
                        />

                        <span class="org-form__switch-track" />

                        <span class="org-form__switch-text">
                            <span class="org-form__switch-label">Показывать публично</span>
                            <span class="org-form__switch-hint">
                                Организация будет доступна в публичной зоне.
                            </span>
                        </span>
                    </label>

                    <label class="org-form__switch">
                        <input
                            class="org-form__switch-input"
                            type="checkbox"
                            :checked="modelValue.isDefaultPublic"
                            :disabled="isSubmitting"
                            @change="updateField('isDefaultPublic', getCheckboxValue($event))"
                        />

                        <span class="org-form__switch-track" />

                        <span class="org-form__switch-text">
                            <span class="org-form__switch-label">Организация по умолчанию</span>
                            <span class="org-form__switch-hint">
                                Используется для публичного каталога преподавателей.
                            </span>
                        </span>
                    </label>
                </div>
            </div>
        </section>

        <footer class="org-form__footer">
            <p class="org-form__footer-text">
                Поля со звёздочкой обязательны для заполнения.
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
